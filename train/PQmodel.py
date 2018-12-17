import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import joblib
import json

class ProductQuantization(object):
	""" pq乘积量化 """

	def __init__(self, n, dim, k):
		"""
		args:
			n 子空间数量
			dim 子空间纬度
			k 子空间聚类个数
			estimatorlist 模型列表
			querydict 索引字典
			clucenterlist 聚类中心列表
		"""
		self.n = n
		self.dim = dim
		self.k = k
		self.estimatorlist = None
		self.querydict = None
		self.clucenterlist = None

	def trainModel(self, data):
		""" 训练模型 
		args:
			data: numpy
		return:
			聚类标签code
		"""
		h, w = data.shape

		if w/self.dim != self.n:
			raise Exception('data dim need ({}), not {}!'.format(self.dim*self.n, w))

		datalist = [data[:,i*self.dim:(i+1)*self.dim] for i in range(self.n)]
		clusterlist = [self._trainKmeans(idata) for idata in datalist]

		self.estimatorlist = [cluster[0] for cluster in clusterlist]
		self.clucenterlist = [cluster[2] for cluster in clusterlist]
		self.querydict = {'km_' + str(i): self._geneIndexDict(cluster[2]) for i, cluster in zip(range(self.n), clusterlist)}

		return self._clusterDecode([cluster[1] for cluster in clusterlist])

	def _trainKmeans(self, data):
		""" 对子空间进行聚类 """

		estimator = KMeans(n_clusters=self.k, init='k-means++')
		estimator.fit(data)
		label_pred = estimator.labels_
		centroids = estimator.cluster_centers_

		return (estimator, label_pred, centroids)

	def _geneIndexDict(self, cluste_centroids):
		""" 产生索引字典 """

		indexdict = {}
		for i in range(self.k):
			dislist = [sum((cluste_centroids[i,:] - cluste_centroids[j,:])**2)**(1/2) for j in range(self.k)]
			indexdict[str(i)] = dislist

		return indexdict

	def _clusterDecode(self, cluste_label):
		""" 类别编码 """

		cluste_label = [pd.Series(label).map(str) for label in cluste_label]
		cluste_code = cluste_label[0]
		for label in cluste_label[1:]:
			cluste_code = cluste_code + label

		return list(cluste_code)

	def saveModel(self, path='./model/'):
		""" 保存模型结果 """

		for i, estimator in zip(range(self.n), self.estimatorlist):
			joblib.dump(estimator , path + 'km_{}.pkl'.format(i))

		json.dump(self.querydict, open(path + 'indexdict.json','w'))

		for i, centroids in zip(range(self.n), self.clucenterlist):
			np.savetxt(path + 'km_centroids_{}.txt'.format(i), centroids, fmt='%f', delimiter=',')

	def loadModel(self, path='./model/'):
		""" 加载模型
			args:
				path 模型保存路径
		"""

		self.estimatorlist = [joblib.load(path + 'km_{}.pkl'.format(i)) for i in range(self.n)]
		self.querydict = json.load(open(path+'indexdict.json','r'))
		self.clucenterlist = [np.loadtxt(path + 'km_centroids_{}.txt'.format(i), delimiter=",") for i in range(self.n)]

	def fit(self, array):
		""" 预分类 """

		if len(array)/self.dim != self.n:
			raise Exception('data dim need ({}), not {}!'.format(self.dim*self.n, len(array)))

		arrylist = [array[i*self.dim:(i+1)*self.dim] for i in range(self.n)]
		dislist = [self.estimatorlist[i].predict(arrylist[i].reshape(1, -1))[0] for i in range(self.n)]

		return ''.join([str(x) for x in dislist])

	def query(self, arry, func='sdc', topC=5):
		""" 查找相似数据
			args:
				arry 查询向量
				func 查询方法
				topC 返回c个相似类型
		"""
		if len(arry)/self.dim != self.n:
			raise Exception('data dim need ({}), not {}!'.format(self.dim*self.n, len(arry)))

		arrylist = [arry[i*self.dim:(i+1)*self.dim] for i in range(self.n)]
		if func == 'sdc':
			dislist = self._query_sdc(arrylist, topC)
		elif func == 'adc':
			dislist = self._query_adc(arrylist, topC)
		else:
			dislist = []

		dislist.reverse()
		allpath = self._allpath(dislist, [])
		allpath = sorted(allpath, key=lambda path : path[1])

		return allpath[:topC]

	def _query_sdc(self, arrylist, topC):
		""" sdc """

		dislist = []
		for i in range(self.n):
			cluter_type = self.estimatorlist[i].predict(arrylist[i].reshape(1, -1))[0]
			dislist.append(self.querydict['km_'+str(i)][str(cluter_type)])

		return dislist

	def _query_adc(self, arrylist, topC):
		""" adc """

		dislist = []
		for i in range(self.n):
			centermatrix = self.clucenterlist[i]
			dislist.append([sum((arrylist[i] - centermatrix[j,:])**2)**(1/2) for j in range(centermatrix.shape[0])])

		return dislist

	def _allpath(self, dislist, pathrecord):
		""" 最短路径 """
		if dislist == []:
			return pathrecord
		else:
			pathlist = []
			nowdis = dislist.pop()
			if pathrecord == []:
				for i, dis in zip(range(len(nowdis)), nowdis):
					pathlist.append((str(i), dis))
			else:
				for pathr, pathdis in pathrecord:
					for i, dis in zip(range(len(nowdis)), nowdis):
						pathlist.append((pathr+str(i), pathdis+dis))
			return self._allpath(dislist, pathlist)