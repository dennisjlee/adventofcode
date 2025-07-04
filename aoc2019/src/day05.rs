use crate::intcode::{IntCode, LoggingIOModule};
use std::io::Read;

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let memory = IntCode::parse_memory(&contents);

    // part 1
    let mut part1_io = LoggingIOModule::new(1);

    let mut intcode = IntCode::new(memory, String::from("day5"), 0);
    intcode.run(Some(&mut part1_io));

    println!("{}", part1_io.outputs().last().unwrap());

    // part 2
    let memory = IntCode::parse_memory(&contents);

    let mut part2_io = LoggingIOModule::new(5);
    intcode = IntCode::new(memory, String::from("day5"), 0);
    intcode.run(Some(&mut part2_io));

    println!("{}", part2_io.outputs().last().unwrap());

    Ok(())
}
