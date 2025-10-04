import networkx as nx
import random
import numpy as np

def _calculate_metrics(g):
    '''
    Calculates key metrics for comparison
    '''
    if g.number_of_nodes() == 0:
        return 'N/A', 0, {}
    
    conn = nx.is_connected(g)
    avg_path = nx.average_shortest_path_length(g) if conn else 'Disconnected'
    comps = nx.number_connected_components(g)
    betweenness = nx.betweenness_centrality(g)
    return avg_path, comps, betweenness

def failure_sim(g, k):
    '''
    Randomly removes k edges and analyzes the impact on network.
    '''
    original_avg, original_comps, original_betweenness = _calculate_metrics(g)

    g_copy = g.copy()
    remove_edges = random.sample(list(g_copy.edges()), k)
    g_copy.remove_edges_from(remove_edges)

    new_avg, new_comps, new_betweenness = _calculate_metrics(g_copy)

    print(f"Original Connected Components: {original_comps}")
    print(f"New Connected Components: {new_comps}")

    if original_avg != 'Disconnected' and new_avg != 'Disconnected':
        path_change = (new_avg - original_avg) / original_avg * 100
        print(f"Average Shortest Path Change: {path_change:.2f}%")
    else:
        print("Average Shortest Path: N/A (disconnected graph).")

    bc_diffs = {node: original_betweenness.get(node, 0) - new_betweenness.get(node, 0) for node in g.nodes()}
    max_nodes_drop = max(bc_diffs, key=bc_diffs.get) if bc_diffs else 'N/A'
    print(f"Node with Max Betweenness Centrality Drop: {max_nodes_drop}")
    print(f"Drop: {bc_diffs.get(max_nodes_drop, 0):.4f}")

def robustness_check(g, num_fails, num_comps, num_sims=10):
    '''
    Performs multiple simulations of k random edge failures and reports robustness
    '''
    print(f"\n===== Running Robustness Check ({num_fails} Failures, {num_sims} Runs) =====")
    comp_counts = []
    max_comp_sizes = []

    if g.number_of_edges() < num_fails:
        print("Not enough edges to run simulation")
        return
    
    for _ in range(num_sims):
        g_temp = g.copy()
        edges_remove = random.sample(list(g_temp.edges()), num_fails)
        g_temp.remove_edges_from(edges_remove)

        comps = list(nx.connected_components(g_temp))
        comp_counts.append(len(comps))

        comp_size = [len(c) for c in comps]
        max_comp_sizes.append(max(comp_size) if comp_size else 0)

    print(f"Average number of connected components: {np.mean(comp_counts):.2f}")
    print(f"Max component size over all runs: {max(max_comp_sizes)}")
    print(f"Min components size over all runs: {min(max_comp_sizes)}")

    if num_comps and max(comp_counts) > 1:
        print(f"Note: The high component count suggests that the network's structure is vulnerable to {num_fails} failures.")