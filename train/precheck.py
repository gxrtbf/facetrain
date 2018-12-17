######### 预检查，用于注册时使用 #########

import numpy as np
import pandas as pd
from PIL import Image
from train import config

class PreImage(object):
	""" 图像检查处理类 """

	def __init__(self, detector=None, align=None):
		"""
		args:
			detector 检测器
			align 标电器
			net 向量器
		"""
		self.detector = config.detector
		self.align = config.shape_predictor
		self.net = config.face_net_model

	def _convert_type(self, img):
		""" 转换成图片矩阵 """

		if type(img) != np.ndarray:
			img = Image.open(img)
			img = np.array(img)
			img = img[:,:,:3]

		return img

	def _oneface(self, img):
		""" 是否存在一个face """

		dets = self.detector(img, 1)
		if len(dets) == 1:
			return dets[0], True
		else:
			return dets, False


	def _dist(self, arraysource, arraytarget):
		""" 向量相似度 """
		return pd.Series(arraysource).corr(pd.Series(arraytarget))

	def faceCheck(self, img):
		""" face检查 """

		img = self._convert_type(img)
		det, hasface = self._oneface(img)
		if hasface:
			shape = self.align(img, det)
		else:
			shape = None

		return img, shape, hasface

	def faceVec(self, img, shape):
		""" 向量化 """
		
		face_descriptor = self.net.compute_face_descriptor(img, shape)

		return np.array(face_descriptor)

	def closeCheck(self, arraylist):
		""" 相似度比较 """

		allnum = len(arraylist)
		arraylist = [(i, array) for i, array in enumerate(arraylist)]

		oneset = []
		while arraylist:
			temparray = arraylist.pop(0)
			if oneset == []:
				oneset.append(temparray)
			else:
				for comparray in oneset:
					corr = self._dist(temparray[1], comparray[1])
					if corr > 0.98:
						oneset.append(temparray)
						break		

		if len(oneset) == allnum:
			return True, []
		else:
			return False, list(set(range(allnum)) - set([i for i, array in oneset]))

		
