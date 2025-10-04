import networkx as nx
import os

def partition_graph(g, num_components, output_dir=None):
    '''
    Partitions graph (using Girvan-Newman Method) into n components.
    '''

    print(f"\n===== Community Partitioning (Girvan-Newman) =====")
    print(f"Target Components: {num_components}")

    if g.number_of_nodes() < num_components:
        print(f"Error: cannot find {num_components} components in a graph with only {g.number_of_nodes()} nodes.")
        return
    
    component_iter = nx.community.girvan_newman(g)

    curr_comps = []
    while len(curr_comps) < num_components:
        try:
            curr_comps = next(component_iter)
        except StopIteration:
            print("Warning: Completed algorithm before reaching desired number of components")
            break

    actual = len(curr_comps)
    print(f"Partitioning successful. Found {actual} communities.")

    for i, component in enumerate(curr_comps):
        for node in component:
            g.nodes[node]['community_id'] = i
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Exporting to {output_dir}")
        for i, component in enumerate(curr_comps):
            sub = g.subgraph(component).copy()
            filename = os.path.join(output_dir, f'component_{i}.gml')
            nx.write_gml(sub, filename)
            print(f" -> Component {i} has been exported")
            print(f"Nodes: {sub.number_nodes()}")