import numpy as np
import umap as u

def CompressingData(data, n = 5):
    embedding = u.UMAP(n_neighbors=5).fit_transform(data)
    return embedding
