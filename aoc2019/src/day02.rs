use std::io::Read;
use crate::intcode::IntCode;

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let memory = IntCode::parse_memory(&contents);

    // part 1
    println!("{}", execute_program(&memory, 12, 2, 0));

    // part 2 - find inputs that produce output 19690720 - did it manually (guess and check lol)
    for noun in 0..100 {
        for verb in 0..100 {
            if execute_program(&memory, noun, verb, 0) == 19690720 {
                println!("{}", 100 * noun + verb);
                return Ok(());
            }
        }
    }

    Ok(())
}

fn execute_program(memory: &Vec<i32>, noun: i32, verb: i32, verbosity: u8) -> i32 {
    let mut program = memory.clone();
    program[1] = noun;
    program[2] = verb;

    let mut intcode = IntCode::new(program, String::from("day2"), verbosity);
    intcode.run(None);
    intcode.memory()[0]
}