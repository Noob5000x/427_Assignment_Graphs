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
        if startNode not in graph:
            print(f"Node '{startNode}' could not be found. Skipping node.")
            continue

        # Dictionaries to store distances and parents for BFS
        distances = {node: float('inf') for node in graph.nodes()}
        parents = {node: None for node in graph.nodes()} 

        distances[startNode] = 0
        queue = [(startNode), 0]

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