import networkx as nx
import random as rand
import argparse as ap

parser = ap.ArgumentParser()

parser.add_argument("--input")
parser.add_argument("--create_random_graph", nargs=2, type=int)

parser.add_argument("--multi_BFS", nargs="+")
parser.add_argument("--analyze", action="store_true")
parser.add_argument("--plot", action="store_true")
parser.add_argument("--output")

args = parser.parse_args()

def main():

    if args.count < 1:
        print("Missing argsuments\n")
        exit(1)
    if args.create_random_graph:
        n, c = args.create_random_graph
        pass # creates erdos-renyi graph, overrides --input
    elif args.input:
        pass # reads given graph, is overriden by create_random_graph
    else:
        print("Missing arguments (--input graph_file.gml or --create_random_graph n c)\n")
        exit(1)
    
    
    
    graph = nx.read_gml('balanced_graph.gml')
    print("Nodes: ", graph.nodes())
    print("Edges: ", graph.edges())