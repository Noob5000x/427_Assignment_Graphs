# 427 Assignment Graphs

### Objective

The goal of this team-based assignment is to advance your skills in graph theory, algorithmic analysis, and professional software development by collaboratively designing and implementing a comprehensive Python application that handles Erdős–Rényi random graph generation, analysis, transformation, and visualization.

You will work in pairs to design, implement, and analyze a modular program capable of:

- Generating and exporting Erdős–Rényi graphs;

- Importing and analyzing graphs from .gml files;

- Performing multi-source BFS with path tracking;

- Identifying connected components;

- Detecting cycles and isolated nodes;

- Visualizing graphs with annotated paths and substructures;

- Exporting computed metadata alongside the graph.

This assignment emphasizes both theoretical understanding and practical implementation. The quality of your design decisions, documentation, and analysis is just as important as functional correctness.

### Functional Requirements

You must implement a Python script graph.py that accepts the following command-line parameters and performs operations accordingly. Your solution must be well-structured and modular, with meaningful separation between graph generation, file I/O, algorithms, and visualization.

#### Command-Line Structure
python ./graph.py [--input graph_file.gml] [--create_random_graph n c] [--multi_BFS a1 a2 ...] [--analyze] [--plot] [--output out_graph_file.gml]
#### Descriptions of Parameters
- --input graph_file.gml
Reads a graph from the given .gml file and uses it for all subsequent operations.

- --create_random_graph n c
Generates a new Erdős–Rényi graph with n nodes and edge probability 
p=nc⋅lnn​. Overrides --input. Nodes must be labeled with strings ("0", "1", ..., "n-1").

- --multi_BFS a1 a2 ...
Accepts one or more starting nodes and computes BFS trees from each, storing all shortest paths. Each BFS tree must be independently visualized and compared.

- --analyze
Performs additional structural analyses on the graph, including:

1. Connected Components
Counts how many distinct connected subgraphs exist.

2. Cycle Detection
Determines whether the graph contains any cycles.
A cycle is a path that starts and ends at the same node, without repeating any edges or nodes (except the start/end).

3. Isolated Nodes
Identifies nodes that are not connected to any other node.

4. Graph Density
Computes how dense the graph is.
Graph density measures how many edges exist in the graph compared to the maximum possible. It is a number between 0 (very sparse) and 1 (fully connected).

5. Average Shortest Path Length
If the graph is connected, computes the average number of steps along the shortest paths for all pairs of nodes.

- --plot
Visualizes the graph with:

1. Highlighted shortest paths from each BFS root node;

2. Distinct styling for isolated nodes;

3. Optional visualization of individual connected components.

- --output out_graph_file.gml
Saves the final graph, with all computed attributes (e.g., distances, parent nodes, component IDs), to the specified .gml file.

### Examples
python ./graph.py --create_random_graph 200 1.5 --multi_BFS 0 5 20 --analyze --plot --output final_graph.gml
Creates a 200-node graph, computes BFS trees from nodes 0, 5, and 20, performs full structural analysis, plots all findings, and saves the graph to final_graph.gml.

python ./graph.py --input data.gml --analyze --plot
Reads a pre-defined graph, analyzes its structure, and displays a visualization.

### Expected Output
#### Your program must:

- Provide terminal output summarizing all analyses in a clear, professional format;

- Include visual plots with meaningful legends, titles, and annotations;

- Export enriched .gml files with custom attributes for nodes and edges.

### Design Expectations
#### Use a modular code structure, with separate components for:

- Graph generation;

- File I/O;

- Graph algorithms (BFS, component detection, cycle detection);

- Visualization;

- Argument parsing and orchestration.

#### Implement robust error handling, including:

- File not found;

- Malformed input graphs;

- Invalid node IDs;

- Insufficient parameters.

#### Document your code thoroughly with function docstrings and comments.

 

Programs that fail to follow the instructions or do not produce working results will not receive points. Ensure that your solution is complete and meets all outlined requirements.
