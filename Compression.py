import umap.umap_ as u

def CompressingData(data, n = 5):
    embedding = u.UMAP(n_neighbors=30, min_dist=0.1, ).fit_transform(data)
    return embedding
