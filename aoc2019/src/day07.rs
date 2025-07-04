use crate::intcode::{IOModule, IntCode, RunState};
use itertools::*;
use std::cell::RefCell;
use std::io::Read;
use std::ops::DerefMut;
use std::rc::Rc;

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

impl IOModule for SequentialAmplifierIOModule {
    fn next_input(&mut self) -> Option<i32> {
        if self.input_index < 2 {
            let next_input = self.inputs[self.input_index];
            self.input_index += 1;
            Some(next_input)
        } else {
            None
        }
    }

    fn output(&mut self, value: i32) {
        self.output = value
    }
}

pub struct FeedbackLoopAmplifierIOModule {
    next_input: Option<i32>,
    output: Option<i32>,
    downstream: Option<Rc<RefCell<FeedbackLoopAmplifierIOModule>>>,
}

impl FeedbackLoopAmplifierIOModule {
    pub fn new(phase: i32) -> Self {
        FeedbackLoopAmplifierIOModule {
            next_input: Some(phase),
            output: None,
            downstream: None,
        }
    }

    pub fn set_downstream(
        &mut self,
        downstream: Option<Rc<RefCell<FeedbackLoopAmplifierIOModule>>>,
    ) {
        self.downstream = downstream;
    }

    pub fn set_next_input(&mut self, value: i32) {
        self.next_input = Some(value);
    }
}

impl IOModule for FeedbackLoopAmplifierIOModule {
    fn next_input(&mut self) -> Option<i32> {
        let val = self.next_input;
        self.next_input = None;
        val
    }

    fn output(&mut self, value: i32) {
        self.output = Some(value);
        if let Some(downstream) = self.downstream.as_mut() {
            downstream.borrow_mut().set_next_input(value);
        }
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

    // part 2
    let mut best_output = -1;
    for phases in (5..10).permutations(5) {
        let output = run_amplifiers_in_loop(&phases, &memory);
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
        let mut intcode = IntCode::new(memory.clone(), format!("day7_seq_{i}"), 0);
        intcode.run(Some(&mut io));
        last_output = io.output;
    }
    last_output
}

fn run_amplifiers_in_loop(phases: &Vec<i32>, memory: &Vec<i32>) -> i32 {
    const LEN: usize = 5;
    assert_eq!(phases.len(), LEN, "Expected exactly 5 phases");

    let io_modules = phases
        .iter()
        .map(|&phase| Rc::new(RefCell::new(FeedbackLoopAmplifierIOModule::new(phase))))
        .collect::<Vec<_>>();

    for i in 0..LEN {
        let next_index = (i + 1) % LEN;
        io_modules[i]
            .borrow_mut()
            .set_downstream(Some(Rc::clone(&io_modules[next_index])));
    }

    let mut programs = phases
        .iter()
        .enumerate()
        .map(|(i, _)| IntCode::new(memory.clone(), format!("day7_loop_{i}"), 0))
        .collect::<Vec<_>>();

    let mut first_input_sent = false;

    while !programs.iter().all(|p| *p.state() == RunState::Halted) {
        for i in 0..LEN {
            programs[i].run(Some(io_modules[i].borrow_mut().deref_mut()))
        }
        if !first_input_sent {
            io_modules[0].borrow_mut().set_next_input(0);
            first_input_sent = true;
        }
    }

    io_modules[LEN - 1].borrow().output.unwrap()
}
