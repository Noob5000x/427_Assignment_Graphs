import networkx as nx
import math

# Import modular component files
import graph_io
import graph_algorithms
import graph_analysis
import argument_parser
import visualizerBFS

args = argument_parser.get_args()

# Generate Graph
if args.create_random_graph:
    n, c = args.create_random_graph
    n = int(n)
    p = c * math.log(n) / n if n > 1 else 0
    graph = nx.erdos_renyi_graph(n, p)
    mapping = {i: str(i) for i in range(n)}
    graph = nx.relabel_nodes(graph, mapping)
    print(f'Generated a random graph with {n} nodes and p={p:.4f}.')
elif args.input:
    try:
        graph = graph_io.readGraph(args.input)
        print(f"Successfully read graph from {args.input}.")

    except FileNotFoundError:
        print(f"Error: The file '{args.input}' was not found.")
        exit(1)
else:
    print("Missing arguments (\"--input graph_file.gml\" or \"--create_random_graph n c\")\n")
    exit(1)

if args.multi_BFS:
    bfs_nodes = [str(node) for node in args.multi_BFS]
    graph_algorithms.multi_BFS(graph, bfs_nodes)

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
    isolated_nodes_list = graph_algorithms.isolated_nodes(graph)
    print(f"The graph contains the following isolated nodes: {isolated_nodes_list}.")

    # Prints the density of the graph
    density = graph_analysis.graph_density(graph)
    print(f"Graph Density: {density:.4f}")
    
    # Prints the average shortest path length
    avg_path_length = graph_analysis.avgShortestPath(graph)
    print(f"Average Shortest Path Length: {avg_path_length}")

# Plots graph
if args.plot:
    print("\n--- Plotting Graph ---")
    visualizerBFS.plotBFStree(graph, args.multi_BFS)
    
# Saves output into a file
if args.output:
    graph_io.writeGraph(graph, str(args.output))