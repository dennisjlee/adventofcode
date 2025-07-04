use itertools::Itertools;
use std::io::Read;

const WIDTH: i32 = 25;
const HEIGHT: i32 = 6;

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let mut layers: Vec<Vec<i32>> = Vec::new();
    let layer_size = (WIDTH * HEIGHT) as usize;
    for chunk in &contents.trim().chars().chunks(layer_size) {
        let layer: Vec<i32> = chunk
            .into_iter()
            .map(|c| c.to_digit(10).unwrap() as i32)
            .collect();
        layers.push(layer);
    }

    // part 1
    let min0_layer = layers
        .iter()
        .min_by_key(|layer| layer.iter().filter(|x| **x == 0).count()).unwrap();
    let count1 = min0_layer.iter().filter(|x| **x == 1).count();
    let count2 = min0_layer.iter().filter(|x| **x == 2).count();
    println!("{}", count1 * count2);
    
    // part 2
    let mut image: Vec<i32> = vec![2; layer_size];
    for i in 0..layer_size {
        for layer in &layers {
            if layer[i] != 2 {
                image[i] = layer[i];
                break;
            }
        }
    }
    for y in 0..HEIGHT {
        for x in 0..WIDTH {
            let pixel = image[(y * WIDTH + x) as usize];
            if pixel == 1 {
                print!("@");
            } else {
                print!(" ");
            }
        }
        println!();
    }

    Ok(())
}
