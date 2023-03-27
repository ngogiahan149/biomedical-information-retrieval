import pandas as pd
import json
import csv
import networkx as nx
import community as community_louvain
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
node_content = pd.read_csv('./paragraphs.csv')
node_weight = pd.read_csv('./nodeWeight.csv')
def createRepresentative():
    with open('paragraphCommunity.json', encoding='utf-8') as f:
        data = json.load(f)
        with open('clusterRep.csv', 'w', encoding= 'utf-8', newline='') as csvfile:
            fieldnames = ["clusterid", "paraid", "content"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in data:
                max_weight = 0
                max_id = 0
                max_content = ''
                for value in data[item]:
                    weight = node_weight.loc[node_weight['paraid'] == value, "weight"].values[0]
                    if weight >=max_weight:
                        max_weight=weight
                        max_id = value
                        max_content = node_content.loc[node_content['id'] == value, "column"].values[0]
                print(item, max_id, max_content)
                writer.writerow({
                    "clusterid": item,
                    "paraid": max_id,
                    "content": max_content,
                })
def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

def create_community():
    G = nx.Graph()

    # Load data
    network = pd.read_csv('./citationNetworkUnique.csv')
    node_content = pd.read_csv('./paragraphs.csv')
    node_keyphrase = pd.read_csv('./paragraphs_new.csv')
    node_weight = pd.read_csv('./nodeWeight.csv')
    # Add edge from network
    for i in range(len(network.index)):
        # G.add_node(network['paraid'][i], content = network['citedsentence'][i])
        # G.add_node(network['citedparaid'][i])
        para_id = network['paraid'][i]
        cite_id = network['citedparaid'][i]

        # Add nodes
        if para_id not in set(node_content['id']) and cite_id not in set(node_content['id']):
            
            G.add_node(para_id, weight = node_weight.loc[node_weight['paraid'] == para_id, 'weight'].values[0],
                    attribute = '', keyphrase = node_keyphrase.loc[node_keyphrase['id'] == para_id, 'keyword'].values[0])
            G.add_node(cite_id, weight = node_weight.loc[node_weight['paraid'] == cite_id, 'weight'].values[0],
                attribute = '', keyphrase = node_keyphrase.loc[node_keyphrase['id'] == cite_id, 'keyword'].values[0])
        elif para_id not in set(node_content['id']) and cite_id in set(node_content['id']):
           
            G.add_node(cite_id, weight = node_weight.loc[node_weight['paraid'] == cite_id, 'weight'].values[0],
                attribute = node_content.loc[node_content['id'] == cite_id, 'column'].values[0],
                keyphrase = node_keyphrase.loc[node_keyphrase['id'] == para_id, 'keyword'].values[0])
            G.add_node(para_id, weight = node_weight.loc[node_weight['paraid'] == cite_id, 'weight'].values[0],
                    attribute = '', keyphrase = node_keyphrase.loc[node_keyphrase['id'] == cite_id, 'keyword'].values[0])
        elif para_id in set(node_content['id']) and cite_id not in set(node_content['id']):
            G.add_node(para_id, weight = node_weight.loc[node_weight['paraid'] == cite_id, 'weight'].values[0],
                attribute = node_content.loc[node_content['id'] == para_id, 'column'].values[0],
                keyphrase = node_keyphrase.loc[node_keyphrase['id'] == para_id, 'keyword'].values[0])
            G.add_node(cite_id, weight = node_weight.loc[node_weight['paraid'] == cite_id, 'weight'].values[0],
                    attribute = '', keyphrase = node_keyphrase.loc[node_keyphrase['id'] == cite_id, 'keyword'].values[0])
        else:
            G.add_node(para_id, weight = node_weight.loc[node_weight['paraid'] == cite_id, 'weight'].values[0],
                attribute = node_content.loc[node_content['id'] == para_id, 'column'].values[0],
                keyphrase = node_keyphrase.loc[node_keyphrase['id'] == para_id, 'keyword'].values[0])
            G.add_node(cite_id, weight = node_weight.loc[node_weight['paraid'] == cite_id, 'weight'].values[0],
                    attribute = node_content.loc[node_content['id'] == cite_id, 'column'].values[0],
                    keyphrase = node_keyphrase.loc[node_keyphrase['id'] == cite_id, 'keyword'].values[0])
        G.add_edge(network['paraid'][i], network['citedparaid'][i], weight = network['finalscore'][i])

    coms = community_louvain.best_partition(G)
    print(coms)
    
    # # Save community file 
    # d = {n:[k for k in coms.keys() if coms[k] == n] for n in set(coms.values())}
    # # Serialize data into file:
    # json.dump( d, open("paragraphCommunity2.json", 'w'), default = np_encoder )

    pos = nx.spring_layout(G)
    cmap = cm.get_cmap('viridis', max(coms.values()) + 1)
    nx.draw_networkx_nodes(G, pos, coms.keys(), node_size=10,
                        cmap=cmap, node_color=list(coms.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()
# node labels
# nx.draw_networkx_labels(G, pos, font_size=3, font_family="sans-serif")

# edge weight labels
# edge_labels = nx.get_edge_attributes(G, "weight")
# nx.draw_networkx_edge_labels(G, pos, edge_labels)
    # nx.write_gexf(G, "community_graph.gexf",  encoding='utf-8')
create_community()