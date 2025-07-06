use std::collections::{BTreeMap, HashMap, HashSet};
use std::f64::consts::PI;
use std::io::Read;

#[derive(PartialEq, Eq, Hash, Clone, Debug, Copy)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Self {
        Point { x, y }
    }

    fn count_detectable_points(&self, points: &HashSet<Point>) -> usize {
        let mut points_by_angle: HashMap<String, Vec<&Point>> = HashMap::new();
        for point in points {
            if point == self {
                continue;
            }
            let dx = point.x - self.x;
            let dy = point.y - self.y;
            let angle = (dy as f64).atan2(dx as f64);
            let angle_key = format!("{:.12}", angle);
            points_by_angle.entry(angle_key).or_default().push(point);
        }
        points_by_angle.len()
    }

    fn vaporization_order(
        &self,
        points: &HashSet<Point>,
    ) -> Vec<Point> {
        let mut vaporization_order: Vec<Point> = Vec::new();
        let mut points_by_angle: BTreeMap<String, BTreeMap<u8, &Point>> = BTreeMap::new();

        for point in points {
            if point == self {
                continue;
            }
            let dx = point.x - self.x;
            let dy = self.y - point.y; // invert y, we want "up" to be positive
            let angle = (dy as f64).atan2(dx as f64); // counter-clockwise from the positive x-axis
            let mut angle_prime = PI / 2.0 - angle; // clockwise from the positive y-axis
            if angle_prime < 0.0 {
                angle_prime += 2.0 * PI; // normalize to [0, 2π)
            }
            let angle_key = format!("{:.12}", angle_prime);
            let manhattan_distance = (dx.abs() + dy.abs()) as u8;
            points_by_angle.entry(angle_key).or_default().insert(manhattan_distance, point);
        }

        while !points_by_angle.values().all(BTreeMap::is_empty) {
            for points in points_by_angle.values_mut() {
                if let Some((_distance, point)) = points.pop_first() {
                    vaporization_order.push(*point);
                }
            }
        }

        vaporization_order
    }
}

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let mut asteroids: HashSet<Point> = HashSet::new();
    for (y, line) in contents.lines().enumerate() {
        for (x, char) in line.chars().enumerate() {
            if char == '#' {
                asteroids.insert(Point::new(x as i32, y as i32));
            }
        }
    }

    let (max_detectable_count, best_location) = asteroids
        .iter()
        .map(|asteroid| (asteroid.count_detectable_points(&asteroids), asteroid))
        .max_by_key(|a| a.0)
        .unwrap();
    println!("{}", max_detectable_count);

    let vaporization_order = best_location.vaporization_order(&asteroids);
    let asteroid_200 = &vaporization_order[199];
    println!("{}", asteroid_200.x * 100 + asteroid_200.y);

    Ok(())
}
