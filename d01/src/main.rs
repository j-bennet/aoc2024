use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashMap;

fn read_data<P>(filename: P) -> io::Result<Vec<String>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    let buf_reader = io::BufReader::new(file);
    buf_reader.lines().collect()
}

fn parse_numbers(lines: Vec<String>) -> Result<(Vec<i32>, Vec<i32>, HashMap<i32, i32>), io::Error> {
    let mut vl = Vec::new();
    let mut vr = Vec::new();
    let mut counter = HashMap::new();
    for line in lines {
        let numbers: Result<Vec<i32>, _> = line.split_whitespace()
                                               .map(|s| s.parse::<i32>())
                                               .collect();
        match numbers {
            Ok(nums) => {
                vl.push(nums[0]);
                vr.push(nums[1]);
                *counter.entry(nums[1]).or_insert(0) += 1;
            },
            Err(_) => return Err(io::Error::new(io::ErrorKind::InvalidData, "Failed to parse numbers")),
        }
    }
    vl.sort();
    vr.sort();
    Ok((vl, vr, counter))
}

fn part1<P>(filename: P)
where
    P: AsRef<Path>,
{
    match read_data(filename) {
        Ok(lines) => {
            match parse_numbers(lines) {
                Ok((vl, vr, _)) => {
                    let zipped: Vec<_> = vl.iter().zip(vr.iter()).collect();
                    let mut distance = 0;
                    for (l, r) in zipped {
                        distance += (l - r).abs();
                    }
                    println!("{:?}", distance);
                }
                Err(e) => println!("Error parsing numbers: {}", e),
            }
        }
        Err(e) => println!("Error opening file: {}", e),
    }
}


fn part2<P>(filename: P)
where
    P: AsRef<Path>,
{
    match read_data(filename) {
        Ok(lines) => {
            match parse_numbers(lines) {
                Ok((vl, _, counter)) => {
                    let mut distance = 0;
                    for l in vl {
                        if counter.contains_key(&l) {
                            distance += l * counter[&l];
                        }
                        }
                    println!("{:?}", distance);
                }
                Err(e) => println!("Error parsing numbers: {}", e),
            }
        }
        Err(e) => println!("Error opening file: {}", e),
    }
}

fn main() {
    part1("example.txt");
    part2("example.txt");
}
