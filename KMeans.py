import cv2
import numpy as np
from sklearn.cluster import KMeans
import glob

def calculate_perc(clusters):
    width = 300
    palette = np.zeros((50, width, 3), np.uint8)
    steps = width / clusters.cluster_centers_.shape[0]
    for idx, centers in enumerate(clusters.cluster_centers_):
        palette[:, int(idx * steps):(int((idx + 1) * steps)), :] = centers
    return palette

#K值聚类，获取30个颜色
clt = KMeans(n_clusters=30)


img = cv2.imread("D:\\project_paper\\process\\0407001\\A010.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
clt_1 = clt.fit(img.reshape(-1, 3))
image = calculate_perc(clt_1)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.imwrite("D:\\project_paper\\process\\colors\\A010.png", image, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
