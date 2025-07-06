use regex::Regex;
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

    for _step in 0..1000 {
        for i in 0..moons.len() - 1 {
            let (split1, split2) = moons.split_at_mut(i + 1);
            for j in 0..split2.len() {
                split1[i].apply_gravity(&mut split2[j]);
            }
        }
        for moon in &mut moons {
            moon.apply_velocity();
        }
    }
    println!("{}", moons.iter().map(Moon::total_energy).sum::<i32>());

    Ok(())
}
