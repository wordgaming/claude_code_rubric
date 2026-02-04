# takes a subgraph of the twitter dataset, then runs and prints analysis based on that subgraph's betweenness and closeness centrality scores
import networkx as nx
import numpy as np

G = nx.DiGraph() # creates graph G

# reads each line in twitter_combined.txt and splits the two numbers into source and target nodes to create edges
with open("twitter_combined.txt", "r") as file:
    for line in file:
        source, target = map(int, line.split())
        G.add_edge(source, target)

degree_c = nx.degree_centrality(G) # gets the degree centrality of the graph

degree_top = sorted(degree_c, key=degree_c.get, reverse=True)[:200] # stores the nodes with the top 200 degree centrality scores

H = G.subgraph(degree_top).copy() # creates a subgraph of G consisting of the nodes with the top 200 degree centrality scores

print("The following is an analysis of a subgraph of the twitter dataset which consists only of the top 200 nodes with the highest degree centrality.\n")

closeness_top = nx.closeness_centrality(H)
close_vals = list(closeness_top.values())
print("Closeness centrality analysis:")
print(f"Mean: {np.mean(close_vals):.5f}")
print(f"Median: {np.median(close_vals):.5f}")
print(f"Standard Deviation: {np.std(close_vals):.5f}")
print()

betweenness_top = nx.betweenness_centrality(H)
between_vals = list(betweenness_top.values())
print("Betweenness centrality analysis:")
print(f"Mean: {np.mean(between_vals):.5f}")
print(f"Median: {np.median(between_vals):.5f}")
print(f"Standard Deviation: {np.std(between_vals):.5f}")
print()

print("Finished!")