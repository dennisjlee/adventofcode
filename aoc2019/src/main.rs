use std::env;
mod day01;
mod day02;
mod intcode;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: {} <day_number> <input_file>", args[0]);
        return;
    }

    let day_number: u32 = match args[1].parse() {
        Ok(num) => num,
        Err(_) => {
            eprintln!("Invalid day number: {}", args[1]);
            return;
        }
    };
    let input_file = &args[2];

    match day_number {
        1 => day01::run(input_file).unwrap(),
        2 => day02::run(input_file).unwrap(),
        // Add more days here as needed
        _ => eprintln!("Day {} is not implemented yet.", day_number),
    }
}
