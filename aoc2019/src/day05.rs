use crate::intcode::{IOModule, IntCode};
use std::io::Read;

pub struct LoggingIOModule {
    fixed_input: i32,
    outputs: Vec<i32>
}

impl LoggingIOModule {
    pub fn new(fixed_input: i32) -> Self {
        LoggingIOModule {
            fixed_input,
            outputs: Vec::new(),
        }
    }
}

impl IOModule for LoggingIOModule {
    fn input(&mut self) -> i32 { self.fixed_input }

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

    // part 1
    let mut part1_io = LoggingIOModule::new(1);

    let mut intcode = IntCode::new(
        memory,
        false,
    );
    intcode.run(Some(&mut part1_io));

    println!("{}", part1_io.outputs.last().unwrap());
    
    // part 2
    let memory = IntCode::parse_memory(&contents);

    let mut part2_io = LoggingIOModule::new(5);
    let mut intcode = IntCode::new(
        memory,
        false,
    );
    intcode.run(Some(&mut part2_io));

    println!("{}", part2_io.outputs.last().unwrap());

    Ok(())
}
