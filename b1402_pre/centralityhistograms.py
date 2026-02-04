# this code reads the twitter dataset, creates a graph based on the data, and generates 3 histograms of the graph's centrality scores
import networkx as nx
import matplotlib.pyplot as plt
import random
import os

G = nx.DiGraph() # creates directed graph G

# reads each line in twitter_combined.txt and splits the two numbers into source and target nodes to create edges in graph G
with open("twitter_combined.txt", "r") as file:
    for line in file:
        source, target = map(int, line.split())
        G.add_edge(source, target)

G = G.to_undirected() # turns the directed graph into an undirected graph

# file checking allows program to skip certain histograms if the files already exist (mostly helpful for testing)
if not os.path.isfile("degree_c.png"):
    # creates a basic histogram using degree centrality values
    degree_c = nx.degree_centrality(G)
    plt.title("Degree Centrality Plot")
    plt.xlabel("Degree Centrality (normalized)")
    plt.ylabel("Frequency (log scale)")
    plt.hist(degree_c.values(), bins=30, log=True)
    plt.savefig("degree_c.png")
    plt.clf()
    print("Degree centrality plot made!")
else:
    print("Degree centrality plot already exists!")

if not os.path.isfile("closeness_c.png"):
    # creates a basic histogram using closeness centrality values (using a random sample of 1000)
    closeness_sample = random.sample(list(G.nodes),k=1000)
    closeness_c = {node: nx.closeness_centrality(G, node) for node in closeness_sample}
    plt.title("Closeness Centrality Plot")
    plt.xlabel("Closeness Centrality (normalized)")
    plt.ylabel("Frequency (log scale)")
    plt.hist(closeness_c.values(), bins=30, log=True)
    plt.savefig("closeness_c.png")
    plt.clf()
    print("Closeness centrality plot made!")
else:
    print("Closeness centrality plot already exists!")

if not os.path.isfile("betweenness_c.png"):
    # creates a basic histogram using betweenness centrality values (using a random sample of 1000)
    betweenness_c = nx.betweenness_centrality(G, k=1000, seed=42)
    plt.title("Betweenness Centrality Plot")
    plt.hist(list(betweenness_c.values()), bins=30, log=True)
    plt.xlabel("Betweenness Centrality (normalized)")
    plt.ylabel("Frequency (log scale)")
    plt.savefig("betweenness_c.png")
    plt.clf()
    print("Betweenness centrality plot made!")
else:
    print("Betweenness centrality plot already exists!")

print("Finished!")