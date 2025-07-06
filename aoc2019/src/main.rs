use std::env;
mod day01;
mod day02;
mod intcode;
mod day03;
mod day04;
mod day05;
mod day06;
mod day07;
mod day08;
mod day09;
mod day10;
mod day11;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 || args.len() > 3 {
        eprintln!("Usage: {} <day_number> [<input_file>]", args[0]);
        return;
    }

    let day_number: u32 = match args[1].parse() {
        Ok(num) => num,
        Err(_) => {
            eprintln!("Invalid day number: {}", args[1]);
            return;
        }
    };
    let input_file = if args.len() == 3 {
        &args[2]
    } else {
        &format!("inputs/day{day_number:0>2}.txt")
    };

    match day_number {
        1 => day01::run(input_file).unwrap(),
        2 => day02::run(input_file).unwrap(),
        3 => day03::run(input_file).unwrap(),
        4 => day04::run(input_file).unwrap(),
        5 => day05::run(input_file).unwrap(),
        6 => day06::run(input_file).unwrap(),
        7 => day07::run(input_file).unwrap(),
        8 => day08::run(input_file).unwrap(),
        9 => day09::run(input_file).unwrap(),
        10 => day10::run(input_file).unwrap(),
        11 => day11::run(input_file).unwrap(),
        // Add more days here as needed
        _ => eprintln!("Day {} is not implemented yet.", day_number),
    }
}
