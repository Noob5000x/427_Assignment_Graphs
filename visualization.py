import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np
import csv

def plot_graph(g, plot_type):
    '''
    Plots graph based on visualization type.
    '''
    plt.figure(figsize=(12, 9))
    pos = nx.spring_layout(g)

    if plot_type == 'C':
        cc_attr = nx.get_node_attributes(g, 'clustering_coefficient')
        degrees = dict(g.degree())

        
        node_sizes = [cc_attr.get(node, 0) * 1000 + 50 for node in g.nodes()]
        node_colors = [degrees.get(node, 0) for node in g.nodes]
        
        nodes = nx.draw_networkx_nodes(g, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.viridis)
        nx.draw_networkx_edges(g, pos, alpha=0.5)

        if nodes:
            plt.colorbar(nodes, label='Node Degree')
        plt.title('Visualization C: Node Size = Clustering Coefficient, Color = Degree')

    elif plot_type == 'N':
        for u, v, d in g.edges(data=True):
            edge_widths = [d.get('neighborhood_overlap', 0) * 8 + 0.5]
        for u, v in g.edges():
            edge_colors = g.degree(u) + g.degree(v)
        nx.draw_networkx_nodes(g, pos, node_color='lightgray', node_size=300)
        edges = nx.draw_networkx_edges(g, pos, width=edge_widths, edge_color=edge_colors, edge_cmap=plt.cm.cividis, alpha=0.8)

        if edges:
            plt.colorbar(edges, label='Sum of Degrees (Edge Color)')
        plt.title("Visualization N: Edge Thickness = Neighborhood Overlap, Color = Sum of Degrees")

    elif plot_type == 'P':
        node_colors = ['gray'] * g.number_of_nodes()
        node_labels = nx.get_node_attributes(g, 'community_id')

        if node_labels:
            node_colors = [d.get('community_id', 0) for n, d in g.nodes(data=True)]
            print("Plotting nodes colored by 'community_id'.")
        edge_colors = ['gray'] * g.number_of_edges()
        if any('sign' in d for u, v, d in g.edges(data=True)):
            edge_colors = ['red' if d.get('sign', 1) == -1 else 'blue' for u, v, d in g.edges(data=True)]
            print("Plotting edges colored by 'sign' attribute.")
            print("Key: Blue = Positive, Red = Negative")

        nx.draw_networkx_nodes(g, pos, node_color=node_colors, cmap=plt.cm.get_cmap('Set1'), node_size=400)
        nx.draw_networkx_edges(g, pos, edge_color=edge_colors, alpha=0.7)
        plt.title('Visualization P: Plotting Graph Attributes (Community ID/Edge Sign)')

    plt.axis('off')
    plt.show()

def temporal_sim(g_base, csv_file):
    '''
    Loads a time series of edge changes and animates graph evolution.
    '''
    print(f"\n===== Starting Temporal Simulation from {csv_file} =====")

    events = []

    try:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                events.append({
                    'timestamp': row['timestamp'],
                    'source': row['source'],
                    'target': row['target'],
                    'action': row['action'].lower()
                })
    except FileNotFoundError:
        print(f"Error: {csv_file} could not be found")
        return
    except KeyError:
        print("Error: CSV must contain 'timestamp', 'source', 'target', and 'action' columns")
        return
    
    events.sort(key=lambda x: x['timestamp'])

    g = g_base.copy()

    plt.figure(figsize=(10,8))

    all_nodes = set(g.nodes())
    for event in events:
        all_nodes.add(event['source'])
        all_nodes.add(event['target'])
    
    temp_g = nx.Graph()
    temp_g.add_nodes_from(all_nodes)
    pos = nx.spring_layout(temp_g)
    
    for row in events:
        source, target, action = row['source'], row['target'], row['action']

        if action == 'add':
            g.add_edge(source, target)
        elif action == 'remove':
            if g.has_edge(source, target):
                g.remove_edge(source, target)
        
        plt.clf
        current_nodes = list(g.nodes())
        current_pos = {n: pos[n] for n in current_nodes}

        nx.draw_networkx_nodes(g, current_pos, node_color='skyblue', node_size=400)
        nx.draw_networkx_edges(g, current_pos, edge_color='black')
        nx.draw_networkx_labels(g, current_pos)
        plt.title(f"Time: {row['timestamp']} | Action: {action.upper()} ({source}-{target})")
        plt.axis('off')
        plt.draw()
        plt.pause(0.5)
    plt.close()
    print("Temporal simulation finished.")

