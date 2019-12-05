import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA
def plot_clusters(model, X, y, title="Cluster_Visualization", dir=""):
    pca = PCA(n_components=2).fit(X)
    pca_2d = pca.transform(X)
    plt.scatter(pca_2d[:, 0], pca_2d[:, 1], c=y, s=10, cmap='viridis')
    centers = model.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=0.5)
    # plt.axis([-20,0,-3,7.5])
    plt.title(title)
    plt.savefig(os.path.join(dir, "{}.png".format(title)))
