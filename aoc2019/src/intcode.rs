pub trait IOModule {
    fn next_input(&mut self) -> Option<i32>;
    fn output(&mut self, value: i32);
}

pub struct NoOpIOModule;

impl IOModule for NoOpIOModule {
    fn next_input(&mut self) -> Option<i32> {
        None
    }
    fn output(&mut self, _value: i32) {
        // No-op, does nothing with the output
    }
}

pub enum RunState {
    Running,
    Suspended,
    Stopped,
}

pub struct IntCode {
    memory: Vec<i32>,
    ip: usize,
    state: RunState,
    verbose: bool,
}

impl IntCode {
    pub fn new(memory: Vec<i32>, verbose: bool) -> Self {
        IntCode {
            memory,
            ip: 0,
            state: RunState::Stopped,
            verbose,
        }
    }

    pub fn parse_memory(input: &str) -> Vec<i32> {
        input
            .trim()
            .split(',')
            .filter_map(|s| s.parse().ok())
            .collect()
    }

    pub fn run(&mut self, io_module: Option<&mut dyn IOModule>) {
        self.state = RunState::Running;
        let io = match io_module {
            Some(module) => module,
            None => &mut NoOpIOModule {},
        };
        loop {
            let instruction = self.memory[self.ip];
            let opcode = instruction % 100;
            let ip = self.ip;
            match opcode {
                1 => {
                    // Add
                    let a = self.interpret_parameter(1);
                    let b = self.interpret_parameter(2);
                    let dest = self.memory[ip + 3] as usize;
                    self.memory[dest] = a + b;
                    if self.verbose {
                        println!("IP: {ip}; {a} + {b} -> loc {dest} ({})", self.memory[dest]);
                    }
                    self.ip += 4;
                }
                2 => {
                    // Multiply
                    let a = self.interpret_parameter(1);
                    let b = self.interpret_parameter(2);
                    let dest = self.memory[ip + 3] as usize;
                    self.memory[dest] = a * b;
                    if self.verbose {
                        println!("IP: {ip}; {a} * {b} -> loc {dest} ({})", self.memory[dest]);
                    }
                    self.ip += 4;
                }
                3 => {
                    // Input
                    let dest = self.memory[ip + 1] as usize;
                    match io.next_input() {
                        Some(input_value) => {
                            self.memory[dest] = input_value;
                            if self.verbose {
                                println!("IP: {ip}; Input ({input_value}) -> loc {dest}");
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
                    let output_value = self.interpret_parameter(1);
                    io.output(output_value);
                    if self.verbose {
                        println!("IP: {ip}; Output ({output_value})");
                    }
                    self.ip += 2;
                }
                5 => {
                    // Jump-if-true
                    let a = self.interpret_parameter(1);
                    if a != 0 {
                        let new_ip = self.interpret_parameter(2) as usize;
                        if self.verbose {
                            println!("IP: {ip}; Jumping to {new_ip} (a == 0)");
                        }
                        self.ip = new_ip;
                    } else {
                        if self.verbose {
                            println!("IP: {ip}; Not jumping (a == {a})");
                        }
                        self.ip += 3;
                    }
                }
                6 => {
                    // Jump-if-false
                    let a = self.interpret_parameter(1);
                    if a == 0 {
                        let new_ip = self.interpret_parameter(2) as usize;
                        if self.verbose {
                            println!("IP: {ip}; Jumping to {new_ip} (a == 0)");
                        }
                        self.ip = new_ip;
                    } else {
                        if self.verbose {
                            println!("IP: {ip}; Not jumping (a == {a})");
                        }
                        self.ip += 3;
                    }
                }
                7 => {
                    // Less than
                    let a = self.interpret_parameter(1);
                    let b = self.interpret_parameter(2);
                    let dest = self.memory[ip + 3] as usize;
                    self.memory[dest] = if a < b { 1 } else { 0 };
                    if self.verbose {
                        println!("IP: {ip}; {a} < {b} -> loc {dest} ({})", self.memory[dest]);
                    }
                    self.ip += 4;
                }
                8 => {
                    // Equal
                    let a = self.interpret_parameter(1);
                    let b = self.interpret_parameter(2);
                    let dest = self.memory[ip + 3] as usize;
                    self.memory[dest] = if a == b { 1 } else { 0 };
                    if self.verbose {
                        println!("IP: {ip}; {a} == {b} -> loc {dest} ({})", self.memory[dest]);
                    }
                    self.ip += 4;
                }
                99 => {
                    self.state = RunState::Stopped;
                    break;
                } // Halt
                _ => panic!("Unknown opcode: {}", opcode),
            }
        }
    }

    pub fn memory(&self) -> &[i32] {
        &self.memory
    }

    pub fn state(&self) -> &RunState {
        &self.state
    }

    fn interpret_parameter(&self, parameter_number: usize) -> i32 {
        let instruction = self.memory[self.ip];
        let value = self.memory[self.ip + parameter_number];

        let mode = (instruction / 10_i32.pow((parameter_number + 1) as u32)) % 10;
        match mode {
            0 => self.memory[value as usize],
            1 => value,
            _ => panic!("Unknown parameter mode: {}", mode),
        }
    }
}
