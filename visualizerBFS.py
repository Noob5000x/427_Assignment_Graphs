import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def plotBFStreeDetailed(graph, bfs_start_nodes):
    """Visualization for small graphs with highlighted BFS paths"""
    start_node = list(graph.nodes())[0]
    
    # Build BFS tree and record depths
    tree = nx.Graph()
    depths = {start_node: 0}
    queue = deque([start_node])
    
    while queue:
        current = queue.popleft()
        for neighbor in graph.neighbors(current):
            if neighbor not in depths:
                depths[neighbor] = depths[current] + 1
                queue.append(neighbor)
                tree.add_edge(current, neighbor)
    
    # Create depth-based layout
    pos = {}
    for node, depth in depths.items():
        nodes_at_depth = [n for n, d in depths.items() if d == depth]
        index = nodes_at_depth.index(node)
        x = depth * 1.5
        y = index - len(nodes_at_depth)/2
        pos[node] = (x, y)
    
    plt.figure(figsize=(12, 8))
    
    # Draw the base tree
    nx.draw_networkx_edges(tree, pos, alpha=0.2, width=1.0, edge_color='gray')
    nx.draw_networkx_nodes(tree, pos, node_size=500, node_color='lightblue', alpha=0.6)
    nx.draw_networkx_labels(tree, pos, font_size=9)
    
    # Generate distinct colors for each BFS path
    colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'cyan']
    
    # Highlight each BFS path
    for i, bfs_start in enumerate(bfs_start_nodes):
        if bfs_start not in graph.nodes():
            print(f"Node {bfs_start} not found, skipping...")
            continue
            
        # Perform BFS from this start node
        bfs_depths = {bfs_start: 0}
        bfs_queue = deque([bfs_start])
        bfs_edges = []
        bfs_nodes = [bfs_start]
        
        while bfs_queue:
            current = bfs_queue.popleft()
            for neighbor in graph.neighbors(current):
                if neighbor not in bfs_depths:
                    bfs_depths[neighbor] = bfs_depths[current] + 1
                    bfs_queue.append(neighbor)
                    bfs_edges.append((current, neighbor))
                    bfs_nodes.append(neighbor)
        
        color = colors[i % len(colors)]
        
        # Highlight path edges and nodes
        nx.draw_networkx_edges(tree, pos, edgelist=bfs_edges,
                              edge_color=color, width=2.5, alpha=0.8)
        nx.draw_networkx_nodes(tree, pos, nodelist=bfs_nodes,
                              node_size=400, node_color=color, alpha=0.7)
        
        # Highlight start node
        nx.draw_networkx_nodes(tree, pos, nodelist=[bfs_start],
                              node_size=600, node_color=color, alpha=1.0)
        
        # Simple start node label
        plt.text(pos[bfs_start][0], pos[bfs_start][1] + 0.2, f'Start {bfs_start}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=color)
    
    # Add depth indicators
    max_depth = max(depths.values()) if depths else 0
    for depth in range(max_depth + 1):
        plt.axvspan(depth * 1.5 - 0.5, depth * 1.5 + 0.5, color='gray', alpha=0.1)
        plt.text(depth * 1.5, min([pos[n][1] for n in tree.nodes()]) - 1, f'Depth {depth}', 
                ha='center', fontsize=10, backgroundcolor='white')
    
    plt.title(f"BFS Paths from Different Start Nodes\n(Base tree from {start_node})", fontsize=12)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def plotBFStreeMinimalist(graph, bfs_start_nodes):
    """Visualization with depth layers and node highlighting"""
    start_node = list(graph.nodes())[0]
    
    # Build BFS tree from main start node
    tree = nx.Graph()
    depths = {start_node: 0}
    queue = deque([start_node])
    
    while queue:
        current = queue.popleft()
        for neighbor in graph.neighbors(current):
            if neighbor not in depths:
                depths[neighbor] = depths[current] + 1
                queue.append(neighbor)
                tree.add_edge(current, neighbor)
    
    pos = {}
    for node, depth in depths.items():
        nodes_at_depth = [n for n, d in depths.items() if d == depth]
        y_pos = nodes_at_depth.index(node) - len(nodes_at_depth)/2
        pos[node] = (depth, y_pos)
    
    plt.figure(figsize=(12, 6))
    
    # Draw the tree
    nx.draw(tree, pos, with_labels=False, node_size=30, node_color='lightblue', 
            alpha=0.7, edge_color='gray', width=0.5)
    
    # Highlight the important nodes
    important_nodes = set(bfs_start_nodes)
    important_nodes.add(start_node)
    
    nx.draw_networkx_nodes(tree, pos, nodelist=list(important_nodes), 
                          node_size=100, node_color='red')
    
    # Label the important nodes
    labels = {node: str(node) for node in important_nodes}
    nx.draw_networkx_labels(tree, pos, labels, font_size=8)
    
    # Add depth indicators
    max_depth = max(depths.values(), default=0)
    for depth in range(max_depth + 1):
        plt.axvline(x=depth, color='gray', linestyle='--', alpha=0.3)
        plt.text(depth, -max_depth/2 - 0.5, f'Depth {depth}', 
                ha='center', fontsize=9, backgroundcolor='white')
    
    plt.title(f"BFS Tree Structure (Main start: {start_node})")
    plt.xlabel("Depth")
    plt.grid(True, alpha=0.1)
    plt.show()

def plotBFStree(graph, bfs_start_nodes):
    # Creates a graph for nodes less than 20 & labels nodes
    if len(graph.nodes()) < 20:
        plotBFStreeDetailed(graph, bfs_start_nodes)
    else:
        plotBFStreeMinimalist(graph, bfs_start_nodes)
