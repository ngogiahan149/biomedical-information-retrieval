import matplotlib.pyplot as plt
import networkx as nx
import community as community_louvain
import matplotlib.cm as cm
import streamlit as st
import plotly.express as px
import json

st.set_option('deprecation.showPyplotGlobalUse', False)
G = nx.Graph()
G.add_node('a', weight = 0.11, attribute = 'hello world')
G.add_node('b', weight = 0.6)
G.add_node('c', weight = 1.7)
G.add_node('d', weight = 0.4)
G.add_node('e', weight = 0.7)
G.add_node('f', weight = 0.9)

G.add_edge("a", "b", weight=0.6)
G.add_edge("a", "c", weight=0.2)
G.add_edge("c", "d", weight=0.1)
G.add_edge("c", "e", weight=0.7)
G.add_edge("c", "f", weight=0.9)
G.add_edge("a", "d", weight=0.3)

coms = community_louvain.best_partition(G)
print(coms)
d = {n:[k for k in coms.keys() if coms[k] == n] for n in set(coms.values())}


# # Serialize data into file:
# json.dump( d, open( "file_name.json", 'w' ) )

# Read data from file:
data = json.load( open( "file_name.json" ) )
for key, value in data.items():
    print(value)
pos = nx.spring_layout(G)
cmap = cm.get_cmap('viridis', max(coms.values()) + 1)
nx.draw_networkx_nodes(G, pos, coms.keys(), node_size=20,
                       cmap=cmap, node_color=list(coms.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
# node labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

# edge weight labels
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels)
nx.write_gexf(G, "cluster2.gexf")
plt.show()