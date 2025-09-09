import networkx as nx
import matplotlib.pyplot as plt

def plotGraph(graph, bfs_start_nodes):
    '''
    Creates the visual for the graph with the paths and substructures.

    Arguments:
        graph (nx.Graph): the graph to plot
        bfs_start_nodes (list): a list of nodes used for BFS
    '''

    pos = nx.spring_layout(graph, k=0.3, seed=42)
    plt.figure(figsize = (50, 50))

    nx.draw_networkx_nodes(graph, pos, node_color = 'lightgray', node_size = 100)
    nx.draw_networkx_edges(graph, pos, edge_color = 'black', width=1)
    nx.draw_networkx_labels(graph, pos, font_size = 8)

    isolated_nodes = list(nx.isolates(graph))
    if isolated_nodes:
        nx.draw_networkx_nodes(graph, pos, nodelist = isolated_nodes, node_color = 'red', node_size=50, label='Isolated Nodes')
    
    if bfs_start_nodes:
        for i, startNode in enumerate(bfs_start_nodes):
            if startNode in graph:
                path_edges = []
                for node in graph.nodes():
                    parent_attr = f"parent_{i}"
                    if parent_attr in graph.nodes[node] and graph.nodes[node][parent_attr] is not None:
                        parent_node = graph.nodes[node][parent_attr]
                        path_edges.append((parent_node, node))
                path_color = plt.cm.get_cmap('rainbow', len(bfs_start_nodes))(i)
                nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color=[path_color] * len(path_edges), width=3, label=f'Path from {startNode}')
        plt.legend()
    plt.title("Graph Visualization with BFS Paths & Components")
    plt.axis('off')
    plt.show()