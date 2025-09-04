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

if args.create_random_graph:
    n, c = args.create_random_graph
    p = c * math.log(n) / n if n > 1 else 0
    ## graph = nx.erdos_renyi_graph(n, p)
    ## mapping = {i: str(i) for i in range(n)}
    ## graph = nx.relabel_nodes(graph, mapping)
elif args.input:
    graph = nx.read_gml(args.input)
    print("Nodes: ", graph.nodes())
    print("Edges: ", graph.edges())
    pass # reads given graph, is overriden by create_random_graph
else:
    print("Missing arguments (--input graph_file.gml or --create_random_graph n c)\n")
    exit(1)
    

