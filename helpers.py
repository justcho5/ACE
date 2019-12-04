import matplotlib.pyplot as plt
import os
def plot_clusters(model, X, y, title="Cluster_Visualization", dir=""):
    plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='viridis')
    centers = model.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    plt.title(title)
    plt.savefig(os.path.join(dir, "{}.png".format(title)))
