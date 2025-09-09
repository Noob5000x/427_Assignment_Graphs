import networkx as nx

def multi_BFS(graph, startNodes):
    '''
    Performs BFS after accepting one or more starting nodes.
    Computes BFS trees from each and stores all shortest paths.

    Arguments:
        graph (nx.Graph): the graph being inputted to traverse
        startNodes (list): a list of starting nodes for BFS
    '''

    for i, startNode in enumerate(startNodes):

        startNode_str = str(startNode)

        if startNode_str not in graph:
            print(f"Node '{startNode_str}' could not be found. Skipping node.")
            continue

        # Dictionaries to store distances and parents for BFS
        distances = {node: float('inf') for node in graph.nodes()}
        parents = {node: None for node in graph.nodes()} 

        distances[startNode_str] = 0
        queue = [(startNode_str, 0)]

        while queue:
            currentNode, currentDistance = queue.pop(0)
            for neighbor in graph.neighbors(currentNode):
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = currentDistance + 1
                    parents[neighbor] = currentNode
                    queue.append((neighbor, currentDistance + 1))
        
        # Stores nodes
        suffix = f"_{i}"
        for node in graph.nodes():
            graph.nodes[node][f"distance{suffix}"] = distances[node]
            graph.nodes[node][f"parent{suffix}"] = parents[node]
        
        print(f"BFS from node '{startNode}' was successful. Path attributes were stored with suffix '{suffix}'.")

def connectedComp(graph):
    '''
    Identifies and labels connected components in the graph.

    Arguments:
        graph (nx.Graph): graph to analyze

    Returns:
        int: # of connected components
    '''

    components = list(nx.connected_components(graph))
    for i, component in enumerate(components):
        for node in component:
            graph.nodes[node]['component_id'] = i
    return len(components)

def findCycles(graph, num_components):
    '''
    Looks for any cycles in the graph

    Arguments:
        graph (nx.Graph): graph to analyze
        num_components (int): # of connected components

    Returns:
        bool: True if cycles exist, False otherwise.
    '''
    return not nx.is_forest(graph)

def isolated_nodes(graph):
    '''
    Identifies and returns a list of isolated nodes.

    Arguments:
        graph (nx.Graph): graph to analyze
    
    Returns:
        list: list of isolated node IDs
    '''
    return list(nx.isolates(graph))