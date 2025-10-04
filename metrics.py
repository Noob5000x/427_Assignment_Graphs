import networkx as nx
import numpy as np

def metrics_computation(g):
    '''
    Computes and adds clustering coefficient and neighborhood overlap as node/edge attributes.
    '''

    if g.number_of_nodes() == 0:
        print("Graph empty: No metrics computed")
        return
    
    # Clustering Coefficient
    cluster_coef = nx.clustering(g)
    nx.set_node_attributes(g, cluster_coef, 'clustering_coefficient')
    print("Clustering coefficients successfully computed.")

    # Neighborhood Overlap
    for u, v in g.edges():
        u_neighbors = set(g.neighbors(u))
        v_neighbors = set(g.neighbors(v))
        common = len(u_neighbors.intersection(v_neighbors))
        all = len(u_neighbors.union(v_neighbors))
    
        overlap = common / all if all > 0 else 0.0
        g.edges[u,v]['neighborhood_overlap'] = overlap
    print("Neighborhood overlap computed")

def verify_homophily(g, attribute_key='color'):
    '''
    Perform homophily check based on the mean attribute differences
    '''
    node_attrs = nx.get_node_attributes(g, attribute_key)
    if not node_attrs:
        print(f"Nodes lack the '{attribute_key}' attribute. Homophily check failed.")
        return
    
    sample_value = list(node_attrs.values())[0]
    
    if isinstance(sample_value, (int, float)):
        connected_diffs = []
        for u, v in g.edges():
            if attribute_key in g.nodes[u] and attribute_key in g.nodes[v]:
                try:
                    diff = abs(float(g.nodes[u][attribute_key]) - float(g.nodes[v][attribute_key]))
                    connected_diffs.append(diff)
                except ValueError:
                    print(f"Skipping homophily check. Attribute '{attribute_key}' is not consistently numeric.")
                    return
    
        disconnected = list(nx.non_edges(g))
        samplesize = min(len(disconnected), len(connected_diffs))

        disconnected_diffs = []
        if samplesize > 0:
            indices = np.random.choice(len(disconnected), size=samplesize, replace=False)
            disconnected_samp = [disconnected[i] for i in indices]

            for u, v in disconnected_samp:
                if attribute_key in g.nodes[u] and attribute_key in g.nodes[v]:
                    diff = abs(float(g.nodes[u][attribute_key]) - float(g.nodes[v][attribute_key]))
                    disconnected_diffs.append(diff)
    
        if len(connected_diffs) == 0 or len(disconnected_diffs) == 0:
            print("Not enough data points for homophily check")
            return
        
        conn_diff_mean = np.mean(connected_diffs)
        unconn_diff_mean = np.mean(disconnected_diffs)

        print("\n===== Homophily Check Results =====")
        print(f"Attribute Key: {attribute_key}")
        print(f"Connected Node Mean Difference: {conn_diff_mean:.4f}")
        print(f"Unconnected Node Mean Difference: {unconn_diff_mean:.4f}")

        if conn_diff_mean > unconn_diff_mean:
            print("Graph shows evidence of homophily")
        else:
            print("Graph does not show evidence of homophily")
    else:
        # Categorical attributes - check for same attribute values
        same_attr_count = 0
        total_edges = g.number_of_edges()
        
        for u, v in g.edges():
            if (attribute_key in g.nodes[u] and attribute_key in g.nodes[v] and 
                g.nodes[u][attribute_key] == g.nodes[v][attribute_key]):
                same_attr_count += 1
        
        homophily_ratio = same_attr_count / total_edges if total_edges > 0 else 0
        
        print("\n===== Homophily Check Results =====")
        print(f"Attribute Key: {attribute_key} (categorical)")
        print(f"Edges with same attribute: {same_attr_count}/{total_edges}")
        print(f"Homophily ratio: {homophily_ratio:.4f}")
        
        if homophily_ratio > 0.5:  # More than half of edges connect similar nodes
            print("Graph shows evidence of homophily")
        else:
            print("Graph does not show evidence of homophily")

def verify_balanced_graph(g, sign_attribute='sign'):
    '''
    Checks if a signed graph is balanced
    '''
    print(f"\n=== Structural Balance Check with attribute '{sign_attribute}' ===")
    try:
        g_target = g.subgraph(max(nx.connected_components(g), key=len)).copy() if not nx.is_connected(g) else g
        is_balanced = _is_balanced(g_target)
        if is_balanced:
            print("The graph is structurally balanced.")
        else:
            print("The graph is not structurally balanced.")
    except nx.NetworkXException:
        print(f"Error: Edges must have the '{sign_attribute}' attribute.")
    except Exception as e:
        print(f"An expected error occured: {e}")

def _is_balanced(graph):
    try:
        # Check if all cycles have even number of negative edges
        for cycle in nx.cycle_basis(graph):
            if len(cycle) > 2:  # Only consider cycles of length 3+
                negative_count = 0
                for i in range(len(cycle)):
                    u, v = cycle[i], cycle[(i + 1) % len(cycle)]
                    if graph[u][v].get('sign', 1) == -1:
                        negative_count += 1
                if negative_count % 2 != 0:
                    return False
        return True
    except:
        return False