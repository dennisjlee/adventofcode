use crate::intcode::{IOModule, IntCode};
use std::collections::HashMap;
use std::io::Read;

#[derive(PartialEq, Eq, Hash, Clone, Debug, Copy)]
struct Point {
    x: i32,
    y: i32,
}


#[derive(PartialEq, Eq, Clone, Debug, Copy)]
enum JoystickState {
    Left = -1,
    Neutral = 0,
    Right = 1,
}


struct ArcadeIOModule {
    output_buffer: [i64; 3],
    output_index: usize,
    score: u32,
    joystick_state: JoystickState,
    screen: HashMap<Point, u8>,
    verbose: bool,
}

impl ArcadeIOModule {
    pub fn new(verbose: bool) -> Self {
        ArcadeIOModule {
            output_buffer: [0; 3],
            output_index: 0,
            score: 0,
            joystick_state: JoystickState::Neutral,
            screen: HashMap::new(),
            verbose
        }
    }

    pub fn count_tiles(&self, tile_id: u8) -> usize {
        self.screen.values().filter(|&&id| id == tile_id).count()
    }

    pub fn render_screen(&self) {
        let mut min_x = i32::MAX;
        let mut max_x = i32::MIN;
        let mut min_y = i32::MAX;
        let mut max_y = i32::MIN;

        for &point in self.screen.keys() {
            if point.x < min_x {
                min_x = point.x;
            }
            if point.x > max_x {
                max_x = point.x;
            }
            if point.y < min_y {
                min_y = point.y;
            }
            if point.y > max_y {
                max_y = point.y;
            }
        }

        for y in min_y..=max_y {
            for x in min_x..=max_x {
                let tile_id = *self.screen.get(&Point { x, y }).unwrap_or(&0);
                print!("{}", match tile_id {
                    0 => ' ', // Empty
                    1 => '#', // Wall
                    2 => '▒', // Block
                    3 => '─', // Paddle
                    4 => 'o', // Ball
                    _ => '?', // Unknown tile
                });
            }
            println!();
        }
    }
}

impl IOModule for ArcadeIOModule {
    fn next_input(&mut self) -> Option<i64> {
        Some(self.joystick_state as i64)
    }

    fn output(&mut self, value: i64) {
        self.output_buffer[self.output_index] = value;
        self.output_index += 1;

        if self.output_index == 3 {
            // We have a complete output triplet (x, y, tile_id)
            let x = self.output_buffer[0] as i32;
            let y = self.output_buffer[1] as i32;
            if x == -1 && y == 0 {
                // Special case for the score output
                self.score = self.output_buffer[2] as u32;
                if self.verbose {
                    println!("Updated score: {}, {} tiles left", self.score, self.count_tiles(2));
                }
            } else {
                let tile_id = self.output_buffer[2] as u8;
                self.screen.insert(Point { x, y }, tile_id);
                if self.verbose && tile_id == 4 {
                    println!("Ball at ({}, {})", x, y);
                }

            }
            self.output_index = 0;
        }
    }
}

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    // part 1
    let memory = IntCode::parse_memory(&contents);
    let mut arcade_io = ArcadeIOModule::new(false);

    let mut intcode = IntCode::new(memory, String::from("day13"), 0);
    intcode.run(Some(&mut arcade_io));

    println!("{}", arcade_io.count_tiles(2));
    arcade_io.render_screen();

    // part 2
    let mut memory = IntCode::parse_memory(&contents);
    memory[0] = 2;
    let mut arcade_io = ArcadeIOModule::new(true);

    let mut intcode = IntCode::new(memory, String::from("day13"), 0);
    intcode.run(Some(&mut arcade_io));
    println!("{:?}", intcode.state());

    Ok(())
}
