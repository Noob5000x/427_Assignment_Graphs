import networkx as nx
import random as rand
import argparse as ap
import math

# Import modular component files
import graph_io
import graph_algorithms
import graph_analysis
import visualizer

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

if args.multi_BFS:
    graph_algorithms.multi_BFS(graph, args.multi_BFS)

if args.analyze:
    print("\n---Graph Analysis---")

    # Prints the number of connected components
    num_components = graph_algorithms.connectedComp(graph)
    print(f"Number of Connected Components: {num_components}")

    # Prints whether or not the graph contains cycles
    cycles = graph_algorithms.findCycles(graph, num_components)
    if cycles:
        print (f"The inputted graph contains cycles.")
    else:
        print (f"The inputted graph does not contain cycles.")
    
    # Identifies nodes that are not connected to any other nodes
    isolated_nodes = graph_algorithms.isolatedNodes(graph)
    print(f"The graph contains the following isolated nodes: {isolated_nodes}.")

    # Prints the density of the graph - needs to be implemented in graph_analysis
    
    
    # Prints the average shortest path length - needs to be implemented in graph_analysis

# Plots graph - needs to be implemented in visualizer.py
if args.plot:
    print("\--- Plotting Graph ---")
    visualizer.plot_graph(graph, args.multi_BFS) 

# Saves output into a file - needs to be implemented
if args.output:
    graph_io.writeGraph(graph, args.output)
    print(f"\nGraph with attributes saved to {args.output}")