use std::cell::RefCell;
use std::cmp::min;
use std::collections::HashMap;
use std::io::Read;
use std::rc::Rc;

#[derive(Debug)]
struct Node {
    _name: String,
    parent_name: Option<String>,
    children: Vec<Rc<RefCell<Node>>>,
    depth: usize,
}

impl Node {
    fn new(name: &str) -> Self {
        Node {
            _name: name.to_string(),
            parent_name: None,
            depth: 0,
            children: Vec::new(),
        }
    }

    fn add_child(&mut self, child: Rc<RefCell<Node>>) {
        self.children.push(child);
    }

    fn set_parent_name(&mut self, parent_name: &str) {
        self.parent_name = Some(parent_name.to_string());
    }

    fn update_depth(&mut self, depth: usize) {
        self.depth = depth;
        for child in &self.children {
            child.borrow_mut().update_depth(depth + 1);
        }
    }
}

pub fn run(input_filename: &str) -> std::io::Result<()> {
    let mut file = std::fs::File::open(input_filename)?;

    // read file into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let mut nodes_by_name: HashMap<String, Rc<RefCell<Node>>> = HashMap::new();

    for line in contents.lines() {
        let parts: Vec<&str> = line.split(')').collect();
        match parts[..] {
            [parent_name, child_name] => {
                {
                    // Hacks to get around borrow checker behavior with HashMap - I need to
                    // mutate the parent node after removing it from the map, then put it back.
                    // I also need to wrap references to nodes in Rc<RefCell<Node>> to allow for
                    // shared ownership.
                    let parent = nodes_by_name.remove(parent_name).unwrap_or_else(
                        || Rc::new(RefCell::new(Node::new(parent_name))));

                    let child = nodes_by_name
                        .entry(child_name.to_string())
                        .or_insert_with(|| Rc::new(RefCell::new(Node::new(child_name))));
                    parent.borrow_mut().add_child(Rc::clone(child));
                    child.borrow_mut().set_parent_name(parent_name);

                    nodes_by_name.insert(parent_name.to_string(), parent);
                }
            }
            _ => {
                panic!("Malformed line: {}", line);
            }
        }
    }

    // Part 1: calculate depth of each node and add them all up
    let root = nodes_by_name.get("COM").expect("Missing root");
    root.borrow_mut().update_depth(0);
    let total_depth: usize = nodes_by_name.values()
        .map(|node| node.borrow().depth)
        .sum();
    println!("{}", total_depth);

    // Part 2: find the path from YOU to COM and SAN to COM, then find the first common node
    let you_path = find_path_to_root(&nodes_by_name, "YOU");
    let santa_path = find_path_to_root(&nodes_by_name, "SAN");
    let mut last_common_ancestor: &String = &"".to_string();
    for i in 1..=min(you_path.len(), santa_path.len()) {
        let you_ancestor = &you_path[you_path.len() - i];
        let santa_ancestor = &santa_path[santa_path.len() - i];
        if you_ancestor == santa_ancestor {
            last_common_ancestor = you_ancestor;
        } else {
            break;
        }
    }
    let you_node = nodes_by_name.get("YOU").unwrap().borrow();
    let santa_node = nodes_by_name.get("SAN").unwrap().borrow();
    let common_node = nodes_by_name.get(last_common_ancestor).unwrap().borrow();

    // We want the distance from the object YOU is orbiting to the object SAN is orbiting, so
    // we subtract 2.
    let distance = you_node.depth - common_node.depth + santa_node.depth - common_node.depth - 2;
    println!("{}", distance);

    Ok(())
}

fn find_path_to_root(
    nodes_by_name: &HashMap<String, Rc<RefCell<Node>>>,
    start_node_name: &str,
) -> Vec<String> {
    let mut path = Vec::new();
    let mut current = nodes_by_name.get(start_node_name).expect("Missing start node");

    while let Some(parent_name) = current.borrow().parent_name.clone() {
        path.push(parent_name.clone());
        current = nodes_by_name.get(&parent_name).expect("Missing parent");
    }

    path
}