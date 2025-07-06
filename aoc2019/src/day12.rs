use num::integer::lcm;
use regex::Regex;
use std::collections::HashMap;
use std::io::Read;

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct Point3D {
    x: i32,
    y: i32,
    z: i32,
}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct Velocity3D {
    dx: i32,
    dy: i32,
    dz: i32,
}

#[derive(Debug)]
struct Moon {
    position: Point3D,
    velocity: Velocity3D,
}

impl Moon {
    fn potential_energy(&self) -> i32 {
        self.position.x.abs() + self.position.y.abs() + self.position.z.abs()
    }

    fn kinetic_energy(&self) -> i32 {
        self.velocity.dx.abs() + self.velocity.dy.abs() + self.velocity.dz.abs()
    }

    fn total_energy(&self) -> i32 {
        self.potential_energy() * self.kinetic_energy()
    }

    fn apply_gravity(&mut self, other: &mut Moon) {
        if self.position.x < other.position.x {
            self.velocity.dx += 1;
            other.velocity.dx -= 1;
        } else if self.position.x > other.position.x {
            self.velocity.dx -= 1;
            other.velocity.dx += 1;
        }
        if self.position.y < other.position.y {
            self.velocity.dy += 1;
            other.velocity.dy -= 1;
        } else if self.position.y > other.position.y {
            self.velocity.dy -= 1;
            other.velocity.dy += 1;
        }
        if self.position.z < other.position.z {
            self.velocity.dz += 1;
            other.velocity.dz -= 1;
        } else if self.position.z > other.position.z {
            self.velocity.dz -= 1;
            other.velocity.dz += 1;
        }
    }

    fn apply_velocity(&mut self) {
        self.position.x += self.velocity.dx;
        self.position.y += self.velocity.dy;
        self.position.z += self.velocity.dz;
    }
}

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let re = Regex::new(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>").unwrap();
    
    let mut moons = Vec::new();
    for (_, [x, y, z]) in re.captures_iter(&contents).map(|c| c.extract()) {
        moons.push(Moon {
            position: Point3D {
                x: x.parse().unwrap(),
                y: y.parse().unwrap(),
                z: z.parse().unwrap(),
            },
            velocity: Velocity3D {
                dx: 0,
                dy: 0,
                dz: 0,
            },
        });
    }

    let mut previous_x_states: HashMap<Vec<i32>, i32> = HashMap::new();
    let mut previous_y_states: HashMap<Vec<i32>, i32> = HashMap::new();
    let mut previous_z_states: HashMap<Vec<i32>, i32> = HashMap::new();
    for step in 0..300_000 {
        for i in 0..moons.len() - 1 {
            let (split1, split2) = moons.split_at_mut(i + 1);
            for j in 0..split2.len() {
                split1[i].apply_gravity(&mut split2[j]);
            }
        }
        for moon in &mut moons {
            moon.apply_velocity();
        }

        if step == 999 {
            // Part 1: Calculate total energy after 1000 steps
            println!("{}", moons.iter().map(Moon::total_energy).sum::<i32>());
        }

        let x_state: Vec<i32> = moons
            .iter()
            .flat_map(|m| vec![m.position.x, m.velocity.dx])
            .collect();
        let y_state: Vec<i32> = moons
            .iter()
            .flat_map(|m| vec![m.position.y, m.velocity.dy])
            .collect();
        let z_state: Vec<i32> = moons
            .iter()
            .flat_map(|m| vec![m.position.z, m.velocity.dz])
            .collect();
        let previous_x_step = previous_x_states.insert(x_state, step);
        let previous_y_step = previous_y_states.insert(y_state, step);
        let previous_z_step = previous_z_states.insert(z_state, step);
        if previous_x_step.is_some() && previous_y_step.is_some() && previous_z_step.is_some() {
            println!(
                "Part 2: Found repeat in all axes at step {step}, previously at x={}, y={}, z={}",
                previous_x_step.unwrap(),
                previous_y_step.unwrap(),
                previous_z_step.unwrap()
            );

            // Calculate the least common multiple of the steps for each axis
            let x_cycle_size = (step - previous_x_step.unwrap()) as i64;
            let y_cycle_size = (step - previous_y_step.unwrap()) as i64;
            let z_cycle_size = (step - previous_z_step.unwrap()) as i64;
            println!("{}", lcm(lcm(x_cycle_size, y_cycle_size), z_cycle_size));
            break;
        }
    }

    Ok(())
}
