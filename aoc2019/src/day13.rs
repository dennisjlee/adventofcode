use crate::intcode::{IOModule, IntCode};
use crossterm::{
    ExecutableCommand, QueueableCommand, cursor,
    event::{Event, KeyCode, poll, read},
    style, terminal,
};
use std::collections::HashMap;
use std::io::{self, Read, Stdout, Write};
use std::time;

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

struct ArcadeIOModule<'a> {
    output_buffer: [i64; 3],
    output_index: usize,
    score: u32,
    score_history: Vec<(u32, usize)>,
    joystick_state: JoystickState,
    screen: HashMap<Point, u8>,
    verbose: bool,
    first_input_requested: bool,
    stdout: Option<&'a mut Stdout>,
}

impl<'a> ArcadeIOModule<'a> {
    pub fn new(verbose: bool, stdout: Option<&'a mut Stdout>) -> Self {
        let mut arcade_module = ArcadeIOModule {
            output_buffer: [0; 3],
            output_index: 0,
            score: 0,
            score_history: Vec::new(),
            joystick_state: JoystickState::Neutral,
            screen: HashMap::new(),
            first_input_requested: false,
            verbose,
            stdout,
        };

        arcade_module.initialize().unwrap();
        arcade_module
    }

    pub fn count_tiles(&self, tile_id: u8) -> usize {
        self.screen.values().filter(|&&id| id == tile_id).count()
    }

    pub fn score_history(&self) -> &[(u32, usize)] {
        &self.score_history
    }

    fn initialize(&mut self) -> io::Result<()> {
        if let Some(output) = self.stdout.as_mut() {
            terminal::enable_raw_mode()?;
            output.execute(terminal::Clear(terminal::ClearType::All))?;
            output.execute(cursor::Hide)?;
        }
        Ok(())
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
                print!("{}", Self::tile_id_to_char(tile_id));
            }
            println!();
        }
    }

    fn tile_id_to_char(tile_id: u8) -> char {
        match tile_id {
            0 => ' ', // Empty
            1 => '#', // Wall
            2 => '▒', // Block
            3 => '─', // Paddle
            4 => 'o', // Ball
            _ => '?', // Unknown tile
        }
    }
}

impl IOModule for ArcadeIOModule<'_> {
    fn next_input(&mut self) -> Option<i64> {
        self.first_input_requested = true;
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
                self.score_history.push((self.score, self.count_tiles(2)));
                if self.verbose {
                    println!(
                        "Updated score: {}, {} tiles left",
                        self.score,
                        self.count_tiles(2)
                    );
                } else if let Some(stdout) = self.stdout.as_mut() {
                    stdout.queue(cursor::MoveTo(0, 30)).unwrap();
                    stdout
                        .queue(style::Print(format!("Score: {}", self.score)))
                        .unwrap();
                }
            } else {
                let tile_id = self.output_buffer[2] as u8;
                self.screen.insert(Point { x, y }, tile_id);
                if self.verbose && tile_id == 4 {
                    println!("Ball at ({}, {})", x, y);
                } else if let Some(stdout) = self.stdout.as_mut()
                    && x >= 0
                    && y >= 0
                {
                    stdout.queue(cursor::MoveTo(x as u16, y as u16)).unwrap();
                    stdout
                        .queue(style::Print(Self::tile_id_to_char(tile_id)))
                        .unwrap();

                    if (self.first_input_requested) {
                        stdout.flush().unwrap();
                        if poll(time::Duration::from_millis(1000 / 10)).unwrap() {
                            // It's guaranteed that the `read()` won't block when the `poll()`
                            // function returns `true`
                            self.joystick_state = match read().unwrap() {
                                Event::Key(event) => match event.code {
                                    KeyCode::Left => JoystickState::Left,
                                    KeyCode::Right => JoystickState::Right,
                                    // Keep the current joystick state if an unexpected key
                                    _ => self.joystick_state,
                                },
                                // Keep the current joystick state if a different event
                                _ => self.joystick_state
                            }
                        } else {
                            // If no input was given, switch back to neutral
                            self.joystick_state = JoystickState::Neutral;
                        }
                    }
                }
            }
            self.output_index = 0;
        }
    }
}

pub fn run(input_filename: &str) -> io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    // part 1
    let memory = IntCode::parse_memory(&contents);
    let mut arcade_io = ArcadeIOModule::new(false, None);

    let mut intcode = IntCode::new(memory, String::from("day13"), 0);
    intcode.run(Some(&mut arcade_io));

    println!("{}", arcade_io.count_tiles(2));
    arcade_io.render_screen();

    // part 2
    let mut memory = IntCode::parse_memory(&contents);
    memory[0] = 2;
    let mut stdout = io::stdout();

    let mut arcade_io = ArcadeIOModule::new(false, Some(&mut stdout));

    let mut intcode = IntCode::new(memory, String::from("day13"), 0);
    intcode.run(Some(&mut arcade_io));
    terminal::disable_raw_mode()?;

    println!("{:?}", arcade_io.score_history());

    Ok(())
}
