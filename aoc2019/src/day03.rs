use std::cmp::{PartialEq, max, min};
use std::io::Read;
use std::ops::RangeInclusive;

struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn manhattan_distance(&self, other: &Point) -> i32 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }
}

const ORIGIN: Point = Point { x: 0, y: 0 };

enum Direction {
    Up,
    Down,
    Left,
    Right,
}

struct Move {
    direction: Direction,
    distance: i32,
}

impl Move {
    fn from_str(s: &str) -> Option<Self> {
        let (dir, dist) = s.split_at(1);
        let distance = dist.parse().ok()?;
        let direction = match dir {
            "U" => Direction::Up,
            "D" => Direction::Down,
            "L" => Direction::Left,
            "R" => Direction::Right,
            _ => return None,
        };
        Some(Move {
            direction,
            distance,
        })
    }
}

#[derive(PartialEq)]
enum Axis {
    X,
    Y,
}

struct LineSegment {
    axis: Axis,
    value: i32,
    start: i32,
    end: i32,
    bounds: RangeInclusive<i32>,
}

impl LineSegment {
    fn new(axis: Axis, value: i32, start: i32, end: i32) -> Self {
        let bounds = min(start, end)..=max(start, end);
        LineSegment {
            axis,
            value,
            start,
            end,
            bounds,
        }
    }

    fn intersects(&self, other: &LineSegment) -> Option<Point> {
        if self.axis == other.axis {
            return None; // Parallel segments do not intersect (we don't count overlaps)
        }

        let (horizontal, vertical) = if self.axis == Axis::X {
            (self, other)
        } else {
            (other, self)
        };

        if vertical.bounds.contains(&horizontal.value)
            && horizontal.bounds.contains(&vertical.value)
        {
            Some(Point {
                x: vertical.value,
                y: horizontal.value,
            })
        } else {
            None
        }
    }

    fn len(&self) -> i32 {
        (self.start - self.end).abs()
    }

    fn distance(&self, point: &Point) -> i32 {
        match self.axis {
            Axis::X => (self.start - point.x).abs(),
            Axis::Y => (self.start - point.y).abs(),
        }
    }
}

struct Wire {
    segments: Vec<LineSegment>,
}

impl Wire {
    fn from_str(s: &str) -> Self {
        let moves: Vec<Move> = s.split(',').filter_map(Move::from_str).collect();
        let mut segments = Vec::new();
        let mut current_point = Point { x: 0, y: 0 };
        for m in moves {
            let (value, bound_start, axis) = match m.direction {
                Direction::Up | Direction::Down => (current_point.x, current_point.y, Axis::Y),
                Direction::Left | Direction::Right => (current_point.y, current_point.x, Axis::X),
            };
            let bound_end = match m.direction {
                Direction::Up | Direction::Left => bound_start - m.distance,
                Direction::Down | Direction::Right => bound_start + m.distance,
            };
            match axis {
                Axis::X => {
                    current_point.x = bound_end;
                }
                Axis::Y => {
                    current_point.y = bound_end;
                }
            }
            segments.push(LineSegment::new(axis, value, bound_start, bound_end));
        }

        Wire { segments }
    }

    fn closest_intersection_distance(&self, other: &Wire) -> i32 {
        let mut min_distance = i32::MAX;

        for segment1 in &self.segments {
            for segment2 in &other.segments {
                if let Some(intersection) = segment1.intersects(segment2) {
                    let distance = intersection.manhattan_distance(&ORIGIN);
                    if distance > 0 && distance < min_distance {
                        min_distance = distance;
                    }
                }
            }
        }

        min_distance
    }

    fn shortest_delay_intersection(&self, other: &Wire) -> i32 {
        let mut min_delay = i32::MAX;
        let mut delay_self = 0;
        for segment1 in &self.segments {
            let mut delay_other = 0;
            for segment2 in &other.segments {
                if let Some(intersection) = segment1.intersects(segment2) {
                    let delay = delay_self
                        + delay_other
                        + segment1.distance(&intersection)
                        + segment2.distance(&intersection);
                    if delay < min_delay {
                        min_delay = delay;
                    }
                }
                delay_other += segment2.len();
            }
            delay_self += segment1.len();
        }
        min_delay
    }
}

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let mut lines = contents.lines();
    let wire1 = Wire::from_str(lines.next().unwrap());
    let wire2 = Wire::from_str(lines.next().unwrap());

    println!("{}", wire1.closest_intersection_distance(&wire2));
    println!("{}", wire1.shortest_delay_intersection(&wire2));

    Ok(())
}
