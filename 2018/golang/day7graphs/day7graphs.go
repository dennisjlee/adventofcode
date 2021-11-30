package day7graphs

import (
	"bufio"
	"log"
	"os"
	"regexp"
)

type Node struct {
	Name     string
	Cost     int
	EdgesOut map[*Node]struct{}
	EdgesIn  map[*Node]struct{}
}

func newNode(name string, cost int) *Node {
	return &Node{
		name,
		cost,
		make(map[*Node]struct{}),
		make(map[*Node]struct{})}
}

// Dummy zero-byte value to treat a map as a set
var keyExists = struct{}{}

func ParseGraph(fileName string) map[string]*Node {
	file, err := os.Open(fileName)

	if err != nil {
		log.Fatalf("failed opening file: %s", err)
	} else {
		defer file.Close()
	}

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)

	regex := regexp.MustCompile("Step ([A-Z]) must be finished before step ([A-Z]) can begin\\.")

	graph := make(map[string]*Node)
	for scanner.Scan() {
		matches := regex.FindStringSubmatch(scanner.Text())
		srcName := matches[1]
		destName := matches[2]
		//fmt.Println(srcName, "->", destName)
		src, ok := graph[srcName]
		if !ok {
			srcCost := 61 + int(srcName[0] - 'A')
			src = newNode(srcName, srcCost)
			graph[srcName] = src
		}

		dest, ok := graph[destName]
		if !ok {
			destCost := 61 + int(destName[0] - 'A')
			dest = newNode(destName, destCost)
			graph[destName] = dest
		}
		src.EdgesOut[dest] = keyExists
		dest.EdgesIn[src] = keyExists
	}
	return graph
}

