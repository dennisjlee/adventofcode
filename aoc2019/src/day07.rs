use crate::intcode::{IOModule, IntCode};
use std::io::Read;
use itertools::*;

pub struct SequentialAmplifierIOModule {
    inputs: [i32; 2],
    output: i32,
    input_index: usize,
}

impl SequentialAmplifierIOModule {
    pub fn new(inputs: [i32; 2]) -> Self {
        SequentialAmplifierIOModule {
            inputs,
            output: -1,
            input_index: 0,
        }
    }
}

impl Iterator for SequentialAmplifierIOModule {
    type Item = i32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.input_index < 2 {
            let next_input = self.inputs[self.input_index];
            self.input_index += 1;
            Some(next_input)
        } else {
            None
        }
    }
}

impl IOModule for SequentialAmplifierIOModule {
    fn output(&mut self, value: i32) {
        self.output = value
    }
}

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let memory = IntCode::parse_memory(&contents);

    // part 1
    let mut best_output = -1;
    for phases in (0..5).permutations(5) {
        let output = run_amplifiers_in_sequence(&phases, &memory);
        if output > best_output {
            best_output = output;
        }
    }
    println!("{}", best_output);

    Ok(())
}

fn run_amplifiers_in_sequence(phases: &Vec<i32>, memory: &Vec<i32>) -> i32 {
    let mut last_output = 0;
    for i in 0..5 {
        let mut io = SequentialAmplifierIOModule::new([phases[i], last_output]);
        let mut intcode = IntCode::new(memory.clone(), false);
        intcode.run(Some(&mut io));
        last_output = io.output;
    }
    last_output
}