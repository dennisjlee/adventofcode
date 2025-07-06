use crate::intcode::{IOModule, IntCode};
use num::Complex;
use std::collections::HashMap;
use std::io::Read;
// We are using Complex<i32> to represent the position on a 2D grid.
// The real part (re) is the x-coordinate and the imaginary part (im) is the y-coordinate.
// Positive x is to the right, positive y is up.

struct PaintIOModule {
    // Maps positions to whether they have been painted black (false) or white (false).
    // Any panel that is not in this map is considered unpainted (black).
    painted_panels: HashMap<Complex<i32>, bool>,
    current_position: Complex<i32>,

    // 1 = right, i = up, -1 = left, -i = down
    current_direction: Complex<i32>,

    paint_on_next_output: bool,
}

impl PaintIOModule {
    pub fn new() -> Self {
        PaintIOModule {
            painted_panels: HashMap::new(),
            current_position: Complex::ZERO,
            current_direction: Complex::I, // start facing up
            paint_on_next_output: true,
        }
    }

    pub fn paint_panel(&mut self, color: bool) {
        self.painted_panels.insert(self.current_position, color);
    }

    pub fn turn_and_move(&mut self, turn_right: bool) {
        if turn_right {
            self.current_direction *= -Complex::I; // Multiply by -i to rotate 90 degrees clockwise
        } else {
            self.current_direction *= Complex::I; // Multiply by i to rotate 90 degrees counter-clockwise
        }
        self.current_position += self.current_direction;
    }

    pub fn painted_panels_count(&self) -> usize {
        self.painted_panels.len()
    }

    pub fn render_painted_panels(&self) {
        let mut min_x = i32::MAX;
        let mut max_x = i32::MIN;
        let mut min_y = i32::MAX;
        let mut max_y = i32::MIN;

        for (&point, &value) in self.painted_panels.iter() {
            if value {
                if point.re < min_x {
                    min_x = point.re;
                }
                if point.re > max_x {
                    max_x = point.re;
                }
                if point.im < min_y {
                    min_y = point.im;
                }
                if point.im > max_y {
                    max_y = point.im;
                }
            }
        }

        for y in (min_y..=max_y).rev() {
            let mut line = String::new();
            for x in min_x..=max_x {
                let pos = Complex::new(x, y);
                line.push(match self.painted_panels.get(&pos) {
                    Some(&true) => '@',
                    Some(&false) | None => '.',
                });
            }
            println!("{}", line)
        }
    }
}

impl IOModule for PaintIOModule {
    fn next_input(&mut self) -> Option<i64> {
        match self.painted_panels.get(&self.current_position) {
            Some(&true) => Some(1),  // White panel
            Some(&false) => Some(0), // Black panel
            None => Some(0),         // Unpainted panel is considered black
        }
    }

    fn output(&mut self, value: i64) {
        if self.paint_on_next_output {
            self.paint_panel(value == 1);
        } else {
            self.turn_and_move(value == 1);
        }
        self.paint_on_next_output = !self.paint_on_next_output;
    }
}

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    // Part 1
    let memory = IntCode::parse_memory(&contents);
    let mut intcode = IntCode::new(memory, String::from("day11"), 0);
    let mut paint_io = PaintIOModule::new();
    intcode.run(Some(&mut paint_io));
    println!("{}", paint_io.painted_panels_count());

    // Part 2
    let memory = IntCode::parse_memory(&contents);
    let mut intcode = IntCode::new(memory, String::from("day11"), 0);
    let mut paint_io = PaintIOModule::new();
    paint_io.paint_panel(true); // Start with the starting panel painted white
    intcode.run(Some(&mut paint_io));
    paint_io.render_painted_panels();

    Ok(())
}
