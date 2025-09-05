import networkx as nx
import random as rand
import argparse as ap
import math

parser = ap.ArgumentParser()

parser.add_argument("--input")
parser.add_argument("--create_random_graph", nargs=2, type=int)

parser.add_argument("--multi_BFS", nargs="+")
parser.add_argument("--analyze", action="store_true")
parser.add_argument("--plot", action="store_true")
parser.add_argument("--output")

args = parser.parse_args()

# Generate Graph
if args.create_random_graph:
    n, c = args.create_random_graph
    p = c * math.log(n) / n if n > 1 else 0
    graph = nx.erdos_renyi_graph(n, p)
    mapping = {i: str(i) for i in range(n)}
    graph = nx.relabel_nodes(graph, mapping)
    print(f'Generated a random graph with {n} nodes and p={p:.4f}.')
elif args.input:
    try:
        graph = nx.read_gml(args.input)
        print("Successfully read graph from {args.input}.")
        print("Nodes: ", graph.nodes())
        print("Edges: ", graph.edges())
    # pass # reads given graph, is overridden by create_random_graph
    except FileNotFoundError:
        print(f"Error: The file '{args.input}' was not found.")
        exit(1)
else:
    print("Missing arguments (--input graph_file.gml or --create_random_graph n c)\n")
    exit(1)

# Multi-source BFS w/ Path Tracking
if args.multi_BFS:
    for i, startingNode in enumerate(args.multi_BFS):
        if startingNode not in graph:
            print(f"Node '{startingNode}' was not found in the graph.")
            continue

        suffix = f"_{i}"
        # Vertices are not visited
        for node in graph.nodes():
            graph.nodes[node][f"distance{suffix}"] = float ('inf')
            graph.nodes[node][f"parent{suffix}"] = None
        
        graph.nodes[startingNode][f"distance{suffix}"] = 0

        queue = [(startingNode, 0)]

        while queue:
            currentNode, currentDist = queue.pop(0)
            for neighbor in graph.neighbors(currentNode):
                if graph.nodes[neighbor][f"distance{suffix}"] == float('inf'):
                    graph.nodes[neighbor][f"distance{suffix}"] = currentDist + 1
                    graph.nodes[neighbor][f"parent{suffix}"] = currentNode
                    queue.append((neighbor, currentDist + 1))
        print(f"BFS from node '{startingNode}' was completed. Path attributes stored with suffix '{suffix}'.")




