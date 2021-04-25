import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import os

# to_array_2 = lambda data : np.array(np.squeeze(data))[0]
# Set color board
colorboard = ["red", "peru", "orange", "lawngreen", "green", "violet",
                "slategray", "teal", "dodgerblue", "blue"]

def kmeans_building_from_sklearn(data, types_num, types_init = "k-means++"):
    '''
    K-means++
    :param data: Numpy array data with one-dimensional or multi-dimensional
    :param types_num: The number of cluster centers
    :return: (Classified new data, Classified center point, Classified slice label)
    '''
    kmeans_model = KMeans(n_clusters=types_num, init=types_init).fit(data)
    newdata = np.c_[kmeans_model.labels_, np.array(data)]
    slice_ = [np.squeeze((newdata==i)[:,0:1]) for i in range(types_num)]
    return [newdata[i] for i in slice_], kmeans_model.cluster_centers_, slice_

if __name__ == "__main__":
    cluster_num = 6
    # You can change the following two variables to custom paths
    graphvec_path = "./emb/graphvec.txt"
    cluster_path = "./cluster/group.txt"

    Vec = list()
    tab = list()
    cluster_list = list()
    
    # Load the embedding vector of each command graph and set the tab
    with open(graphvec_path, "r") as f:
        for index, line in enumerate(f):
            l = line[:-1].split(" ")
            if len(l) == 0:
                continue
            Vec.append([float(i) for i in l])
            tab.append(index + 1)
    
    color = ["" for i in range(tab[-1])]

    # Get clustering results
    data = np.mat(Vec)
    result = kmeans_building_from_sklearn(data, cluster_num)
    for index, item in enumerate(result[2]):
        tmp = list()
        for index_, judge in enumerate(item):
            if judge == True:
                color[index_] = colorboard[index]
                tmp.append(index_ + 1)
        cluster_list.append(tmp)
    
    # Save the clustering results (Each row represents the elements in a cluster)
    with open(cluster_path, "w") as f:
        for items in cluster_list:
            for i in range(len(items) - 1):
                f.write(str(items[i]))
                f.write(" ")
            f.write(str(items[len(items) - 1]))
            f.write("\n")
    
    # The clustering center is added to "Vec" for visualization
    for center in result[1]:
        Vec.append(center)

    # Dimension reduction and visualization using t-SNE
    model = TSNE(perplexity=30)
    Y = model.fit_transform(Vec)
    for i in range(cluster_num):
        color.append("black")
        tab.append("x")

    plt.figure(figsize = (4, 4), dpi = 200)
    for index, sc in enumerate(Y):
        if color[index] == "black":
            plt.scatter(sc[0], sc[1], 50, color=color[index], marker="x")
        else:
            plt.scatter(sc[0], sc[1], 30, c=color[index])
    for i in range(len(tab)):
        plt.text(Y[i][0], Y[i][1], tab[i], fontsize=2)
    plt.savefig("./cluster/tranSH.png")
    plt.show()
