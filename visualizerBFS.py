import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import numpy as np

def plotBFStree(graph, bfs_start_nodes):
    '''
    Creates BFS tree from first node

    Arguments:
        graph (nx.Graph): the input graph
    '''

    start_node = list(graph.nodes())[0]

    tree = nx.Graph()
    queue = deque([start_node])
    depths = {start_node: 0}

    while queue:
        current= queue.popleft()
        for neighbor in graph.neighbors(current):
            if neighbor not in depths:
                depths[neighbor] = depths[current] + 1
                queue.append(neighbor)
                tree.add_edge(current, neighbor)

    # Calculate optimal spacing for large graphs
    max_depth = max(depths.values()) if depths else 0
    max_nodes_at_depth = 0
    for depth in range(max_depth + 1):
        nodes_at_depth = sum(1 for d in depths.values() if d == depth)
        max_nodes_at_depth = max(max_nodes_at_depth, nodes_at_depth)

    y_spacing = max(2, max_nodes_at_depth * 0.5)

    pos = {}
    for node, depth in depths.items():
        same_depth = [n for n in depths if depths[n] == depth]
        same_depth_sorted = sorted(same_depth)
        index = same_depth_sorted.index(node)
        x = depth * 2
        y = (index - len(same_depth)/2) * y_spacing
        pos[node] = (x, y)

    plt.figure(figsize=(max_depth * 3 + 6, max_nodes_at_depth * y_spacing / 1.5 + 6))

    nx.draw(tree, pos, with_labels=True, node_color='lightblue',
            node_size=300, font_size=8, width=1, alpha=.7)
    
    nx.draw_networkx_nodes(tree, pos, nodelist=[start_node],
                           node_color='red', node_size=400)
    
    colors = plt.cm.Set2(np.linspace(0, 1, len(bfs_start_nodes)))
    
    for i, highlight_node in enumerate(bfs_start_nodes[1:], 1):
        if highlight_node not in graph.nodes():
            print(f"Node {highlight_node} not found in graph.")
            continue
            
        if highlight_node == start_node:
            continue
        bfs_depths = {highlight_node: 0}
        bfs_queue = deque([highlight_node])
        bfs_edges = []

        while bfs_queue:
            current = bfs_queue.popleft()
            for neighbor in graph.neighbors(current):
                if neighbor not in bfs_depths:
                    bfs_depths[neighbor] = bfs_depths[current] + 1
                    bfs_queue.append(neighbor)
                    bfs_edges.append((current, neighbor))
        
        color = colors[i]
        nx.draw_networkx_edges(tree, pos, edgelist=bfs_edges,
                               edge_color = [color] * len(bfs_edges),
                               width=2, alpha=.8)
        nx.draw_networkx_nodes(tree, pos, nodelist=[highlight_node],
                               node_color=[color], node_size=350)
    
    plt.title(f"BFS Tree")
    plt.tight_layout()
    plt.axis('off')
    plt.show()
