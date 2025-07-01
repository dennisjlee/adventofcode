use std::fs::File;
use std::io::prelude::Read;

pub fn run(input_filename: &str) -> () {
    let mut file = File::open(input_filename).unwrap();

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();

    let mut total_fuel = 0u64;
    let mut total_fuel_recursive = 0u64;
    for line in contents.lines() {
        if let Ok(mass) = line.parse::<u64>() {
            total_fuel += fuel_mass(mass);
            total_fuel_recursive += fuel_mass_recursive(mass);
        } else {
            eprintln!("Invalid mass value: {}", line);
        }
    }
    println!("{}", total_fuel);
    println!("{}", total_fuel_recursive);
}

fn fuel_mass(mass: u64) -> u64 {
    let fuel = mass / 3;
    if fuel < 2 {
        0
    } else {
        fuel - 2
    }
}

fn fuel_mass_recursive(mass: u64) -> u64 {
    let fuel = fuel_mass(mass);
    if fuel == 0 {
        0
    } else {
        fuel + fuel_mass_recursive(fuel)
    }
}