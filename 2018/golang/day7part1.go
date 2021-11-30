package main

import (
	"fmt"
	"github.com/dennisjlee/advent-of-code-2018/day7graphs"
	"os"
	"sort"
	"strings"
)

func insertNodeSortedByName(nodes []*day7graphs.Node, node *day7graphs.Node) []*day7graphs.Node {
	i := sort.Search(len(nodes), func(i int) bool { return nodes[i].Name >= node.Name })
	nodes = append(nodes, nil)
	copy(nodes[i+1:], nodes[i:])
	nodes[i] = node
	return nodes
}

func main() {
	graph := day7graphs.ParseGraph(os.Args[1])

	var readyNodes = make([]*day7graphs.Node, 0)
	for _, node := range graph {
		if len(node.EdgesIn) == 0 {
			readyNodes = append(readyNodes, node)
		}
	}
	sort.Slice(readyNodes, func(i, j int) bool { return readyNodes[i].Name < readyNodes[j].Name })
	processedNames := make([]string, len(graph))
	for len(readyNodes) > 0 {
		next := readyNodes[0]
		readyNodes = readyNodes[1:]
		processedNames = append(processedNames, next.Name)
		for neighbor := range next.EdgesOut {
			delete(neighbor.EdgesIn, next)
			if len(neighbor.EdgesIn) == 0 {
				readyNodes = insertNodeSortedByName(readyNodes, neighbor)
			}
		}
	}

	fmt.Println(strings.Join(processedNames, ""))
}
