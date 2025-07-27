pub trait IOModule {
    fn next_input(&mut self) -> Option<i64>;
    fn output(&mut self, value: i64);
}

pub struct NoOpIOModule;

impl IOModule for NoOpIOModule {
    fn next_input(&mut self) -> Option<i64> {
        None
    }
    fn output(&mut self, _value: i64) {
        // No-op, does nothing with the output
    }
}

pub struct LoggingIOModule {
    fixed_input: i64,
    outputs: Vec<i64>,
}

impl LoggingIOModule {
    pub fn new(fixed_input: i64) -> Self {
        LoggingIOModule {
            fixed_input,
            outputs: Vec::new(),
        }
    }

    pub fn outputs(&self) -> &[i64] {
        &self.outputs
    }
}

impl IOModule for LoggingIOModule {
    fn next_input(&mut self) -> Option<i64> {
        Some(self.fixed_input)
    }
    fn output(&mut self, value: i64) {
        self.outputs.push(value)
    }
}

#[derive(PartialEq, Debug, Clone)]
pub enum RunState {
    Init,
    Running,
    Suspended,
    Halted,
}

#[derive(Clone)]
pub struct IntCode {
    memory: Vec<i64>,
    name: String,
    verbosity: u8,
    ip: usize,
    state: RunState,
    relative_base: i64,
}

impl IntCode {
    pub fn new(memory: Vec<i64>, name: String, verbosity: u8) -> Self {
        IntCode {
            memory,
            name,
            verbosity,
            ip: 0,
            state: RunState::Init,
            relative_base: 0,
        }
    }

    pub fn parse_memory(input: &str) -> Vec<i64> {
        input
            .trim()
            .split(',')
            .filter_map(|s| s.parse().ok())
            .collect()
    }

    pub fn run(&mut self, io_module: Option<&mut dyn IOModule>) {
        let name = &self.name;

        match self.state {
            RunState::Init | RunState::Suspended => {
                self.state = RunState::Running;
            }
            RunState::Running => {
                panic!("{name}: run requested while already running!")
            }
            RunState::Halted => {
                return;
            }
        }
        let io = match io_module {
            Some(module) => module,
            None => &mut NoOpIOModule {},
        };
        loop {
            let ip = self.ip;
            let rb = self.relative_base;
            let instruction = read_memory(&mut self.memory, ip);
            let opcode = instruction % 100;
            match opcode {
                1 => {
                    // Add
                    let a = IntCode::interpret_parameter(&mut self.memory, 1, ip, rb);
                    let b = IntCode::interpret_parameter(&mut self.memory, 2, ip, rb);
                    let dest = IntCode::interpret_out_parameter(&mut self.memory, 3, ip, rb);
                    write_memory(&mut self.memory, dest, a + b);
                    if self.verbosity >= 3 {
                        println!(
                            "{name} IP: {ip}; {a} + {b} -> loc {dest} ({})",
                            self.memory[dest]
                        );
                    }
                    self.ip += 4;
                }
                2 => {
                    // Multiply
                    let a = IntCode::interpret_parameter(&mut self.memory, 1, ip, rb);
                    let b = IntCode::interpret_parameter(&mut self.memory, 2, ip, rb);
                    let dest = IntCode::interpret_out_parameter(&mut self.memory, 3, ip, rb);
                    write_memory(&mut self.memory, dest, a * b);
                    if self.verbosity >= 3 {
                        println!(
                            "{name} IP: {ip}; {a} * {b} -> loc {dest} ({})",
                            self.memory[dest]
                        );
                    }
                    self.ip += 4;
                }
                3 => {
                    // Input
                    match io.next_input() {
                        Some(input_value) => {
                            let dest = IntCode::interpret_out_parameter(&mut self.memory, 1, ip, rb);
                            write_memory(&mut self.memory, dest, input_value);
                            if self.verbosity >= 1 {
                                println!("{name} IP: {ip}; Input ({input_value}) -> loc {dest}");
                            }
                            self.ip += 2;
                        }
                        None => {
                            self.state = RunState::Suspended;
                            break;
                        }
                    }
                }
                4 => {
                    // Output
                    let output_value = IntCode::interpret_parameter(&mut self.memory, 1, ip, rb);
                    io.output(output_value);
                    if self.verbosity >= 1 {
                        println!("{name} IP: {ip}; Output ({output_value})");
                    }
                    self.ip += 2;
                }
                5 => {
                    // Jump-if-true
                    let a = IntCode::interpret_parameter(&mut self.memory, 1, ip, rb);
                    if a != 0 {
                        let new_ip =
                            IntCode::interpret_parameter(&mut self.memory, 2, ip, rb) as usize;
                        if self.verbosity >= 3 {
                            println!("{name} IP: {ip}; Jumping to {new_ip} (a == {a})");
                        }
                        self.ip = new_ip;
                    } else {
                        if self.verbosity >= 3 {
                            println!("{name} IP: {ip}; Not jumping (a == 0)");
                        }
                        self.ip += 3;
                    }
                }
                6 => {
                    // Jump-if-false
                    let a = IntCode::interpret_parameter(&mut self.memory, 1, ip, rb);
                    if a == 0 {
                        let new_ip =
                            IntCode::interpret_parameter(&mut self.memory, 2, ip, rb) as usize;
                        if self.verbosity >= 3 {
                            println!("{name} IP: {ip}; Jumping to {new_ip} (a == 0)");
                        }
                        self.ip = new_ip;
                    } else {
                        if self.verbosity >= 3 {
                            println!("{name} IP: {ip}; Not jumping (a == {a})");
                        }
                        self.ip += 3;
                    }
                }
                7 => {
                    // Less than
                    let a = IntCode::interpret_parameter(&mut self.memory, 1, ip, rb);
                    let b = IntCode::interpret_parameter(&mut self.memory, 2, ip, rb);
                    let dest = IntCode::interpret_out_parameter(&mut self.memory, 3, ip, rb);
                    write_memory(&mut self.memory, dest, if a < b { 1 } else { 0 });
                    if self.verbosity >= 3 {
                        println!(
                            "{name} IP: {ip}; {a} < {b} -> loc {dest} ({})",
                            self.memory[dest]
                        );
                    }
                    self.ip += 4;
                }
                8 => {
                    // Equal
                    let a = IntCode::interpret_parameter(&mut self.memory, 1, ip, rb);
                    let b = IntCode::interpret_parameter(&mut self.memory, 2, ip, rb);
                    let dest = IntCode::interpret_out_parameter(&mut self.memory, 3, ip, rb);
                    write_memory(&mut self.memory, dest, if a == b { 1 } else { 0 });
                    if self.verbosity >= 3 {
                        println!(
                            "{name} IP: {ip}; {a} == {b} -> loc {dest} ({})",
                            self.memory[dest]
                        );
                    }
                    self.ip += 4;
                }
                9 => {
                    // Adjust relative base
                    let adjustment = IntCode::interpret_parameter(&mut self.memory, 1, ip, rb);
                    self.relative_base += adjustment;
                    if self.verbosity >= 3 {
                        println!(
                            "{name} IP: {ip}; Adjusting relative base by {adjustment} to {}",
                            self.relative_base
                        );
                    }
                    self.ip += 2;
                }
                99 => {
                    self.state = RunState::Halted;
                    break;
                } // Halt
                _ => panic!("Unknown opcode: {}", opcode),
            }
        }
    }

    pub fn memory(&self) -> &[i64] {
        &self.memory
    }

    pub fn state(&self) -> &RunState {
        &self.state
    }

    fn interpret_parameter(
        memory: &mut Vec<i64>,
        parameter_number: usize,
        ip: usize,
        relative_base: i64,
    ) -> i64 {
        let instruction = read_memory(memory, ip);
        let value = read_memory(memory, ip + parameter_number);

        let mode = (instruction / 10_i64.pow((parameter_number + 1) as u32)) % 10;
        match mode {
            0 => read_memory(memory, value as usize),
            1 => value,
            2 => read_memory(memory, (value + relative_base) as usize),
            _ => panic!("Unknown parameter mode: {}", mode),
        }
    }

    fn interpret_out_parameter(
        memory: &mut Vec<i64>,
        parameter_number: usize,
        ip: usize,
        relative_base: i64,
    ) -> usize {
        let instruction = read_memory(memory, ip);
        let value = read_memory(memory, ip + parameter_number);

        let mode = (instruction / 10_i64.pow((parameter_number + 1) as u32)) % 10;
        match mode {
            0 => value as usize,
            2 => (value + relative_base) as usize,
            1 => panic!("Output parameter cannot be in immediate mode (1)"),
            _ => panic!("Unknown parameter mode: {}", mode),
        }
    }
}

fn ensure_memory_size(memory: &mut Vec<i64>, size: usize) {
    if memory.len() < size {
        memory.resize(size, 0);
    }
}

fn read_memory(memory: &mut Vec<i64>, address: usize) -> i64 {
    ensure_memory_size(memory, address + 1);
    memory[address]
}

fn write_memory(memory: &mut Vec<i64>, address: usize, value: i64) {
    ensure_memory_size(memory, address + 1);
    memory[address] = value;
}
