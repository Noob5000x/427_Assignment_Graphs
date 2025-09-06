import networkx as nx
import graph_io
import graph_algorithms
import pytest

def test_io():
    print("--- Testing graph_io.py ---")
    
    # Test writing a graph
    g = nx.Graph()
    g.add_nodes_from(['A', 'B', 'C'])
    g.add_edges_from([('A', 'B'), ('B', 'C')])
    graph_io.writeGraph(g, "test_io.gml")
    print("Graph written to test_io.gml.")
    
    # Test reading the same graph
    read_g = graph_io.readGraph("test_io.gml")
    print("Graph read from test_io.gml. Nodes:", read_g.nodes())
    assert set(g.nodes()) == set(read_g.nodes()), "IO test failed: nodes don't match."
    print("IO tests passed.")

def test_algorithms():
    print("\n--- Testing graph_algorithms.py ---")
    
    # Test BFS
    g_bfs = nx.Graph()
    nx.add_path(g_bfs, ['0', '1', '2', '3'])
    graph_algorithms.multi_BFS(g_bfs, ['0'])
    assert g_bfs.nodes['3']['distance_0'] == 3, "BFS distance test failed."
    print("BFS test passed.")

    # Test Connected Components
    g_comp = nx.Graph()
    g_comp.add_nodes_from(['A', 'B', 'C'])
    g_comp.add_edge('A', 'B')
    num_comp = graph_algorithms.connectedComp(g_comp)
    assert num_comp == 2, "Connected components test failed."
    print("Connected components test passed.")
    
    # Test Cycle Detection
    g_cycle = nx.cycle_graph(4)  # Creates a 4-node cycle
    num_comp_cycle = graph_algorithms.connectedComp(g_cycle)
    assert graph_algorithms.findCycles(g_cycle, num_comp_cycle), "Cycle detection test failed."
    print("Cycle detection test passed.")

def test_file_not_found():
    """Test that graph_io.read_graph raises an error for a non-existent file."""
    print("\n--- Testing File Not Found Error Handling ---")
    with pytest.raises(FileNotFoundError):
        graph_io.readGraph("non_existent_file.gml")
    print("File not found test passed.")

if __name__ == '__main__':
    test_io()
    test_algorithms()
    test_file_not_found()