import networkx as nx
import graph_io
import graph_algorithms
import graph_analysis  # Import the graph_analysis module
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

def test_metrics():
    """This function tests the graph analysis metrics, including density."""
    print("\n--- Testing Graph Analysis Metrics ---")

    # Test Case 1: A complete graph (density should be 1.0)
    print("\nTesting a complete graph...")
    g_complete = nx.complete_graph(5)
    density_complete = graph_analysis.get_graph_density(g_complete)
    assert density_complete == 1.0, f"Density of complete graph is incorrect. Expected 1.0, got {density_complete}"
    print("Density test for complete graph passed.")

    # Test Case 2: A disconnected graph (density should be 0.0)
    print("\nTesting a disconnected graph...")
    g_disconnected = nx.Graph()
    g_disconnected.add_nodes_from(['A', 'B', 'C'])
    density_disconnected = graph_analysis.get_graph_density(g_disconnected)
    assert density_disconnected == 0.0, f"Density of disconnected graph is incorrect. Expected 0.0, got {density_disconnected}"
    print("Density test for disconnected graph passed.")

    # Test Case 3: A path graph (connected, avg shortest path is predictable)
    print("\nTesting a path graph for average shortest path length...")
    g_path = nx.path_graph(5)
    avg_path_path = graph_analysis.get_average_shortest_path_length(g_path)
    assert abs(avg_path_path - 2.0) < 1e-9, f"Avg path length for path graph is incorrect. Expected 2.0, got {avg_path_path}"
    print("Average shortest path test for path graph passed.")

    # Test Case 4: A disconnected graph (avg shortest path should be 'N/A')
    print("\nTesting a disconnected graph for average shortest path...")
    g_disconnected_path = nx.Graph()
    g_disconnected_path.add_nodes_from(['A', 'B'])
    g_disconnected_path.add_nodes_from(['C', 'D'])
    g_disconnected_path.add_edge('A', 'B')
    avg_path_disconnected = graph_analysis.get_average_shortest_path_length(g_disconnected_path)
    assert avg_path_disconnected == "N/A (graph is not connected)", f"Avg path length for disconnected graph is incorrect. Expected 'N/A', got {avg_path_disconnected}"
    print("Average shortest path test for disconnected graph passed.")

def guide_visualization_test():
    """
    Provides instructions for manually testing graph visualization.
    """
    print("\n--- Testing Graph Visualization (Manual) ---")
    print("Visualization requires a visual check and cannot be automated with assertions.")
    print("To test plotting, run your main program (`graph.py`) with the --plot flag.")
    print("\nExamples:")
    print("1. To see a random graph with highlighted BFS paths:")