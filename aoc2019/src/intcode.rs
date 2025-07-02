pub struct IntCode {
    memory: Vec<i32>,
    verbose: bool,
}

impl IntCode {
    pub fn new(memory: Vec<i32>, verbose: bool) -> Self {
        IntCode { memory, verbose }
    }
    pub fn run(&mut self) {
        let mut ip = 0; // Instruction pointer
        loop {
            let opcode = self.memory[ip];
            match opcode {
                1 => {
                    let (a, b, dest) = (self.memory[ip + 1] as usize, self.memory[ip + 2] as usize, self.memory[ip + 3] as usize);
                    self.memory[dest] = self.memory[a] + self.memory[b];
                    if self.verbose {
                        println!("IP: {ip}; loc {a} ({0}) + loc {b} ({1}) -> loc {dest} ({2})",
                                 self.memory[a], self.memory[b], self.memory[dest]);
                    }
                    ip += 4;
                }
                2 => {
                    let (a, b, dest) = (self.memory[ip + 1] as usize, self.memory[ip + 2] as usize, self.memory[ip + 3] as usize);
                    self.memory[dest] = self.memory[a] * self.memory[b];
                    if self.verbose {
                        println!("IP: {ip}; loc {a} ({0}) * loc {b} ({1}) -> loc {dest} ({2})",
                                 self.memory[a], self.memory[b], self.memory[dest]);
                    }
                    ip += 4;
                }
                99 => break,
                _ => panic!("Unknown opcode: {}", opcode),
            }
        }
    }

    pub fn memory(&self) -> &[i32] {
        &self.memory
    }
}