import networkx as nx

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

    try:
        return nx.read_gml(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: file '{file_path}' could not be found")
    
def writeGraph(graph, file_path):
    '''
    Saves the graph to a .gml file, which will indicate all nodes and edges

    Arguments:
        graph (nx.graph): saved graph
        file_path (str): The path to the .gml output file
    '''
    if file_path is None:
        print("Error: no valid file path.")
        return
    try:
        nx.write_gml(graph, file_path)
    except Exception as e:
        print(f"Error: could not save graph {e}.")
