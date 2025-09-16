import networkx as nx

def graph_density(graph):
    '''
    Computes how dense the graph is.

    Arguments:
        graph (nx.Graph): the graph to analyze
    
    Returns:
        float: the graph density (between 0.0 and 1.0)
    '''
    # Identifies the number of nodes
    num_nodes = graph.number_of_nodes()
    if num_nodes <= 1:
        return 0.0
    num_edges = graph.number_of_edges()
    return (2 * num_edges) / (num_nodes *(num_nodes - 1)) # Calculates graph density

def avgShortestPath(graph):
    '''
    Computes the average shortest path of the graph given that the graph is connected.

    Arguments:
        graph (nx.Graph): the graph to analyze

    Returns:
        float or str: Average shortest path length or 'The graph is not connected.'
    '''
    # Identifies and returns the average shortest path length for the graph
    if nx.is_connected(graph):
        return nx.average_shortest_path_length(graph)
    return "The graph is not connected (N/A)."