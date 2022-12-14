package main

import (
	"fmt"
	"github.com/dennisjlee/advent-of-code-2018/day7graphs"
	"os"
	"sort"
)

func insertNodeSortedByCost(nodes []*day7graphs.Node, node *day7graphs.Node) []*day7graphs.Node {
	i := sort.Search(len(nodes), func(i int) bool { return nodes[i].Cost >= node.Cost })
	nodes = append(nodes, nil)
	copy(nodes[i+1:], nodes[i:])
	nodes[i] = node
	return nodes
}

func min(a, b int) int {
	if a <= b {
		return a
	}
	return b
}

func main() {
	graph := day7graphs.ParseGraph(os.Args[1])

	var readyNodes = make([]*day7graphs.Node, 0, len(graph))
	for _, node := range graph {
		if len(node.EdgesIn) == 0 {
			readyNodes = append(readyNodes, node)
		}
	}
	sort.Slice(readyNodes, func(i, j int) bool { return readyNodes[i].Cost < readyNodes[j].Cost })
	secondsElapsed := 0
	const WorkerCount = 5
	for len(readyNodes) > 0 {
		nodesToWork := readyNodes[:min(len(readyNodes), WorkerCount)]
		firstNode := readyNodes[0]
		nextTimeChunk := firstNode.Cost
		for _, node := range nodesToWork {
			node.Cost -= nextTimeChunk
		}
		secondsElapsed += nextTimeChunk

		readyNodes = readyNodes[1:]
		for neighbor := range firstNode.EdgesOut {
			delete(neighbor.EdgesIn, firstNode)
			if len(neighbor.EdgesIn) == 0 {
				readyNodes = insertNodeSortedByCost(readyNodes, neighbor)
			}
		}
	}

	fmt.Println(secondsElapsed)
}
