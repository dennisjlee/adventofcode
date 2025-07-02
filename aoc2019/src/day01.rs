use std::fs::File;
use std::io::prelude::Read;

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let mut total_fuel = 0u64;
    let mut total_fuel_iterative = 0u64;
    for line in contents.lines() {
        if let Ok(mass) = line.parse::<u64>() {
            total_fuel += fuel_mass(mass);
            total_fuel_iterative += fuel_mass_iterative(mass);
        } else {
            eprintln!("Invalid mass value: {}", line);
        }
    }
    println!("{}", total_fuel);
    println!("{}", total_fuel_iterative);
    
    Ok(())
}

fn fuel_mass(mass: u64) -> u64 {
    let fuel = mass / 3;
    if fuel < 2 {
        0
    } else {
        fuel - 2
    }
}

fn fuel_mass_iterative(mass: u64) -> u64 {
    let mut total_fuel = 0;
    let mut current_mass = mass;
    while current_mass > 0 {
        current_mass = fuel_mass(current_mass);
        total_fuel += current_mass;
    }
    total_fuel
}