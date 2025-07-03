pub trait IOModule {
    fn input(&mut self) -> i32;
    fn output(&mut self, value: i32);
}

pub struct NoOpIOModule;

impl IOModule for NoOpIOModule {
    fn input(&mut self) -> i32 {
        0 // No-op, returns 0
    }

    fn output(&mut self, _value: i32) {
        // No-op, does nothing with the output
    }
}

pub struct IntCode {
    memory: Vec<i32>,
    verbose: bool,
}

impl IntCode {
    pub fn new(memory: Vec<i32>, verbose: bool) -> Self {
        IntCode { memory, verbose }
    }

    pub fn parse_memory(input: &str) -> Vec<i32> {
        input
            .trim()
            .split(',')
            .filter_map(|s| s.parse().ok())
            .collect()
    }

    pub fn run(&mut self, io_module: Option<&mut dyn IOModule>) {
        let mut ip = 0; // Instruction pointer
        let io = match io_module {
            Some(module) => module,
            None => &mut NoOpIOModule {},
        };
        loop {
            let instruction = self.memory[ip];
            let opcode = instruction % 100;
            match opcode {
                1 => {
                    // Add
                    let a = self.interpret_parameter(ip, 1);
                    let b = self.interpret_parameter(ip, 2);
                    let dest = self.memory[ip + 3] as usize;
                    self.memory[dest] = a + b;
                    if self.verbose {
                        println!("IP: {ip}; {a} + {b} -> loc {dest} ({})", self.memory[dest]);
                    }
                    ip += 4;
                }
                2 => {
                    // Multiply
                    let a = self.interpret_parameter(ip, 1);
                    let b = self.interpret_parameter(ip, 2);
                    let dest = self.memory[ip + 3] as usize;
                    self.memory[dest] = a * b;
                    if self.verbose {
                        println!("IP: {ip}; {a} * {b} -> loc {dest} ({})", self.memory[dest]);
                    }
                    ip += 4;
                }
                3 => {
                    // Input
                    let dest = self.memory[ip + 1] as usize;
                    let input_value = io.input();
                    self.memory[dest] = input_value;
                    if self.verbose {
                        println!("IP: {ip}; Input ({input_value}) -> loc {dest}");
                    }
                    ip += 2;
                }
                4 => {
                    // Output
                    let output_value = self.interpret_parameter(ip, 1);
                    io.output(output_value);
                    if self.verbose {
                        println!("IP: {ip}; Output ({output_value})");
                    }
                    ip += 2;
                }
                5 => {
                    // Jump-if-true
                    let a = self.interpret_parameter(ip, 1);
                    if a != 0 {
                        let new_ip = self.interpret_parameter(ip, 2) as usize;
                        if self.verbose {
                            println!("IP: {ip}; Jumping to {new_ip} (a == 0)");
                        }
                        ip = new_ip;
                    } else {
                        if self.verbose {
                            println!("IP: {ip}; Not jumping (a == {a})");
                        }
                        ip += 3;
                    }
                }
                6 => {
                    // Jump-if-false
                    let a = self.interpret_parameter(ip, 1);
                    if a == 0 {
                        let new_ip = self.interpret_parameter(ip, 2) as usize;
                        if self.verbose {
                            println!("IP: {ip}; Jumping to {new_ip} (a == 0)");
                        }
                        ip = new_ip;
                    } else {
                        if self.verbose {
                            println!("IP: {ip}; Not jumping (a == {a})");
                        }
                        ip += 3;
                    }
                }
                7 => {
                    // Less than
                    let a = self.interpret_parameter(ip, 1);
                    let b = self.interpret_parameter(ip, 2);
                    let dest = self.memory[ip + 3] as usize;
                    self.memory[dest] = if a < b { 1 } else { 0 };
                    if self.verbose {
                        println!("IP: {ip}; {a} < {b} -> loc {dest} ({})", self.memory[dest]);
                    }
                    ip += 4;
                }
                8 => {
                    // Equal
                    let a = self.interpret_parameter(ip, 1);
                    let b = self.interpret_parameter(ip, 2);
                    let dest = self.memory[ip + 3] as usize;
                    self.memory[dest] = if a == b { 1 } else { 0 };
                    if self.verbose {
                        println!("IP: {ip}; {a} == {b} -> loc {dest} ({})", self.memory[dest]);
                    }
                    ip += 4;
                }
                99 => break, // Halt
                _ => panic!("Unknown opcode: {}", opcode),
            }
        }
    }

    pub fn memory(&self) -> &[i32] {
        &self.memory
    }

    fn interpret_parameter(&self, ip: usize, parameter_number: usize) -> i32 {
        let instruction = self.memory[ip];
        let value = self.memory[ip + parameter_number];

        let mode = (instruction / 10_i32.pow((parameter_number + 1) as u32)) % 10;
        match mode {
            0 => self.memory[value as usize],
            1 => value,
            _ => panic!("Unknown parameter mode: {}", mode),
        }
    }
}
