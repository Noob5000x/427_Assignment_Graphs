import networkx as nx
import re

def readGraph(file_path):
    '''
    Reads a graph from a .gml file.

    Arguments:
        file_path(str): the path to the .gml file.

    Returns:
        nx.Graph: the graph object

    Raises:
        FileNotFoundError: if the file cannot be found/does not exist
    '''
    # Reads the graph file inputted and returns an error if the file cannot be found
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Rewrites 'inf' into 999999999
        content = re.sub(r'\binf\b', '999999999', content)
        return nx.parse_gml(content)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: file '{file_path}' could not be found")

def writeGraph(graph, file_path):
    '''
    Saves the graph to a .gml file
    '''
    try:
        # Creates the .gml file
        with open(file_path, 'w') as f:
            f.write('graph [\n')
            
            # Write nodes
            for node in graph.nodes():
                f.write(f'  node [\n')
                f.write(f'    id {node}\n')
                f.write(f'    label "{node}"\n')
                
                # Write all attributes
                for attr_name, attr_value in graph.nodes[node].items():
                    if attr_value is not None:
                        if attr_value == float('inf'):
                            attr_value = 999999999
                        f.write(f'    {attr_name} {attr_value}\n')
                
                f.write('  ]\n')
            
            # Write edges
            for edge in graph.edges():
                f.write('  edge [\n')
                f.write(f'    source {edge[0]}\n')
                f.write(f'    target {edge[1]}\n')
                f.write('  ]\n')
            
            f.write(']\n')
        # Prints if graph is saved successfully
        print(f"Graph successfully saved to {file_path}")
        return True
        
    except Exception as e:
        # Outputs that the graph could not be saved
        print(f"Could not save graph. Error: {e}")
        return False