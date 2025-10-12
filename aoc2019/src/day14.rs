use itertools::Itertools;
use regex::Regex;
use std::collections::HashMap;
use std::io::Read;
use std::rc::Rc;

#[derive(Debug)]
struct Reaction {
    output_amount: usize,
    inputs: Vec<(usize, String)>,
}

#[derive(Debug)]
struct Chemical {
    reaction: Option<Reaction>
}

const ORE_NAME: &str = "ORE";
const FUEL_NAME: &str = "FUEL";

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let mut chemicals_by_name: HashMap<String, Rc<Chemical>> = HashMap::new();
    chemicals_by_name.insert(String::from(ORE_NAME), Rc::new(Chemical {
        reaction: None,
    }));

    let re = Regex::new(r"(\d+) ([^, ]+)").unwrap();

    for line in contents.lines() {
        let parts: Vec<&str> = line.split(" => ").collect();
        match parts[..] {
            [left, right] => {
                let (_, [count, name]) = re.captures(right).unwrap().extract();
                let output_amount: usize = count.parse().unwrap();

                let inputs = re.captures_iter(left).map(|c| c.extract())
                    .map(|(_, [input_amount, input_name])| {
                        (input_amount.parse().unwrap(), input_name.to_string())
                    }).collect_vec();
                let chemical = Chemical {
                    reaction: Some(Reaction {
                        output_amount,
                        inputs,
                    }),
                };
                chemicals_by_name.insert(name.to_string(), Rc::new(chemical));
            }
            _ => {
                panic!("Malformed line: {}", line);
            }
        }
    }

    // Part 1: calculate minimum amount of ore needed to make one fuel
    let ore_for_one_fuel = ore_needed_for_fuel(&chemicals_by_name, 1);
    println!("{}", ore_for_one_fuel);

    // Part 2: calculate maximum amount of fuel that can be made with 1 trillion ore
    let trillion: i64 = 1_000_000_000_000;
    let mut low = 1_i64;
    let mut high = 2 * (trillion as f64 / ore_for_one_fuel as f64).ceil() as i64;
    while low < high {
        let mid = (low + high + 1) / 2;
        let ore_needed = ore_needed_for_fuel(&chemicals_by_name, mid) as i64;
        if ore_needed > trillion {
            high = mid - 1;
        } else {
            low = mid;
        }
    }
    println!("{} ORE => {} FUEL", ore_needed_for_fuel(&chemicals_by_name, low), low);

    Ok(())
}

fn ore_needed_for_fuel(chemicals_by_name: &HashMap<String, Rc<Chemical>>, fuel_needed: i64) -> i64 {
    let mut needs: HashMap<String, i64> = HashMap::new();
    let mut ore_needed: i64 = 0;
    let mut surplus: HashMap<String, i64> = HashMap::new();
    needs.insert(String::from(FUEL_NAME), fuel_needed);

    while !needs.is_empty() {
        let chemical_name = needs.keys().next().unwrap().clone();
        let amount_needed = needs.remove(&chemical_name).unwrap();
        needs.remove(&chemical_name);

        let chemical = chemicals_by_name.get(&chemical_name).unwrap();
        let reaction = chemical.reaction.as_ref().unwrap();

        let surplus_amount = surplus.get(&chemical_name).cloned().unwrap_or(0);
        let net_needed = amount_needed - surplus_amount;
        if net_needed <= 0 {
            // We have enough surplus to satisfy the need
            surplus.insert(chemical_name.clone(), -net_needed);
            continue;
        }

        let times_to_run = (net_needed as f64 / reaction.output_amount as f64).ceil() as i64;
        let total_produced = times_to_run * reaction.output_amount as i64;
        let new_surplus = total_produced - net_needed;
        surplus.insert(chemical_name.clone(), new_surplus);

        for (input_amount, input_name) in &reaction.inputs {
            if input_name == ORE_NAME {
                // Directly add to ore needed
                ore_needed += times_to_run * (*input_amount as i64);
            } else {
                let entry = needs.entry(input_name.clone()).or_insert(0);
                *entry += times_to_run * (*input_amount as i64);
            }
        }
    }

    ore_needed
}