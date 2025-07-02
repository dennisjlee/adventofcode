use crate::intcode::{IOModule, IntCode};
use std::io::Read;

pub struct Day5IOModule {
    outputs: Vec<i32>
}

impl IOModule for Day5IOModule {
    fn input(&mut self) -> i32 { 1 }

    fn output(&mut self, value: i32) {
        self.outputs.push(value)
    }
}

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let memory = IntCode::parse_memory(&contents);

    let mut io_module = Day5IOModule { outputs: Vec::new() };

    let mut intcode = IntCode::new(
        memory,
        false,
    );
    intcode.run(Some(&mut io_module));

    println!("{}", io_module.outputs.last().unwrap());

    Ok(())
}
