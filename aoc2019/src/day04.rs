use std::io::Read;
use std::ops::RangeInclusive;

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let split: Vec<i32> = contents
        .split("-")
        .filter_map(|s| s.parse::<i32>().ok())
        .collect();
    let bounds = split[0]..=split[1];

    println!("{:?}", split);

    let (count_part1, count_part2) = count_valid_passwords(&bounds, &mut [0; 6], 0);

    println!("{}", count_part1);
    println!("{}", count_part2);

    Ok(())
}

fn count_valid_passwords(
    bounds: &RangeInclusive<i32>,
    candidate_digits: &mut [i32; 6],
    index: usize,
) -> (i32, i32) {
    let mut count_part1 = 0;
    let mut count_part2 = 0;

    let valid_next_digits = if index == 0 {
        bounds.start() / 100_000..=bounds.end() / 100_000
    } else {
        candidate_digits[index - 1]..=9
    };

    if index == 5 {
        for digit in valid_next_digits {
            candidate_digits[index] = digit;

            // Convert the candidate digits to a number
            let candidate_number = convert_to_number(&candidate_digits);
            if bounds.contains(&candidate_number) {
                if has_adjacent_duplicate_digits(&candidate_digits) {
                    count_part1 += 1;
                }
                if has_adjacent_duplicate_digits_pair_only(&candidate_digits) {
                    count_part2 += 1;
                }
            }
        }
    } else {
        for digit in valid_next_digits {
            candidate_digits[index] = digit;

            // Recursively count valid passwords for the next index
            let (new_part1, new_part2) = count_valid_passwords(bounds, candidate_digits, index + 1);
            count_part1 += new_part1;
            count_part2 += new_part2;
        }
    }

    (count_part1, count_part2)
}

fn convert_to_number(digits: &[i32; 6]) -> i32 {
    digits.iter().fold(0, |acc, &d| acc * 10 + d)
}

fn has_adjacent_duplicate_digits(digits: &[i32; 6]) -> bool {
    for i in 0..5 {
        if digits[i] == digits[i + 1] {
            return true;
        }
    }
    false
}

fn has_adjacent_duplicate_digits_pair_only(digits: &[i32; 6]) -> bool {
    for i in 0..5 {
        if digits[i] == digits[i + 1] && (i == 4 || digits[i] != digits[i + 2]) && (i == 0 || digits[i] != digits[i - 1]) {
            return true;
        }
    }
    false
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_has_adjacent_duplicate_digits() {
        assert!(has_adjacent_duplicate_digits(&[1, 1, 2, 3, 4, 5]));
        assert!(!has_adjacent_duplicate_digits(&[1, 2, 3, 4, 5, 6]));
    }

    #[test]
    fn test_has_adjacent_duplicate_digits_pair_only() {
        assert!(has_adjacent_duplicate_digits_pair_only(&[1, 1, 2, 3, 4, 5]));
        assert!(!has_adjacent_duplicate_digits_pair_only(&[1, 1, 1, 3, 4, 5]));
        assert!(has_adjacent_duplicate_digits_pair_only(&[1, 1, 1, 1, 2, 2]));
    }
}