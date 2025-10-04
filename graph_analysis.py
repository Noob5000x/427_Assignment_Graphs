# Import modules and appropriate functions
import argparse
import networkx as nx
import os

from detect_community import partition_graph
from metrics import metrics_computation, verify_homophily, verify_balanced_graph
from simulation import failure_sim, robustness_check
from visualization import plot_graph, temporal_sim

def main():
    '''
    Main driver that handles command-line inputs and runs analysis process.
    '''

    # Reading the .gml file
    parser = argparse.ArgumentParser(description='Analyze structural properties, explore patterns, and simulate manipulations.')
    parser.add_argument('graph_file', type=str, help='Paths to one .gml graph file')

    # Community Identifier and Robustness
    parser.add_argument('--components', type=int, help='Partition graph into n components using Girvan-Newman')
    parser.add_argument('--robustness_check', type=int, nargs='?', const=5, help='Perform robustness check with a specified number of random edge failures')
    parser.add_argument('--split_output_dir', type=str, help='Directory to separate the components in their own separate .gml file')

    # Visualization
    parser.add_argument('--plot', choices=['C', 'N', 'P', 'T'], help='Controls output visualization')

    # Verification
    parser.add_argument('--verify_homophily', action='store_true', help='Perform statistical t-test for homophily check')
    parser.add_argument('--verify_balanced_graph', action='store_true', help='Check if graph is balanced')

    # Simulations
    parser.add_argument('--simulate_failures', type=int, help='Randomly remove k edges and analyze how it affects the network')

    # Temporal Analysis
    parser.add_argument('--temporal_simulation', type=str, help='Load a time series of edge changes and animate graph evolution')

    # Outputs
    parser.add_argument('--output', type=str, help='Save graph with all new updates')

    args = parser.parse_args()

    # Load the graph file
    print(f"\n======================================")
    print(f"Starting analysis for: {args.graph_file}")
    print(f"======================================")

    try:
        graph_path = args.graph_file
        if isinstance(args.graph_file, list):
            graph_path = args.graph_file[0]
    
        print(f"Attempting to load: {graph_path}")
    
        # Check if file exists
        if not os.path.exists(graph_path):
            print(f"Error: File '{graph_path}' does not exist")
            return
    
        # Load the graph
        g = nx.read_gml(graph_path)
    
        # Convert string signs to integers
        for u, v, data in g.edges(data=True):
            if 'sign' in data:
                if data['sign'] == '+':
                    data['sign'] = 1
                elif data['sign'] == '-':
                    data['sign'] = -1
                elif isinstance(data['sign'], str):
                    # Handle other string representations
                    try:
                        data['sign'] = int(data['sign'])
                    except ValueError:
                        print(f"Warning: Could not convert sign value '{data['sign']}' to integer")
                        data['sign'] = 1  # Default to positive
    
        print(f"Graph loaded successfully: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")
    
    except FileNotFoundError:
        print(f"Error: File '{graph_path}' could not be found")
        return
    except Exception as e:
        print(f"Error: Could not load file - {str(e)}")
        return
    
    # Analysis
    if args.simulate_failures:
        failure_sim(g, args.simulate_failures)
    
    if args.robustness_check is not None and args.components:
        robustness_check(g, args.robustness_check, args.components)
    
    if args.components:
        partition_graph(g, args.components, args.split_output_dir)
    
    if args.verify_homophily:
        verify_homophily(g)

    if args.verify_balanced_graph:
        verify_balanced_graph(g)
    
    if args.plot in ['C', 'N']:
        metrics_computation(g)
    
    if args.plot == 'T' and args.temporal_simulation:
        temporal_sim(g, args.temporal_simulation)
    elif args.plot:
        plot_graph(g, args.plot)

    if args.output:
        name = os.path.basename(args.graph_file).replace('.gml','')
        path_output = args.output.replace('.gml', f'_{name}.gml')
        nx.write_gml(g, path_output)
        print(f"Final graph saved to {path_output}")

if __name__ == '__main__':
    main()