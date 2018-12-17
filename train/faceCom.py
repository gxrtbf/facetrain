import pandas as pd
import numpy as np
from sklearn.externals import joblib

class SamePerson():
	""" 人脸匹配 """

	def __init__(self, dis=[0.35, 0.55], cor=[0.93, 0.98]):
		""" 
			dis 欧式距离的判断范围
			cor 相关系数的判断范围
		"""

		self.dis = dis
		self.cor = cor
		self.model = joblib.load('train/model/lrcv.pkl')
		self.threshold = 0.5

	def _o_dis(self, array1, array2):
		""" 欧式距离 """

		return sum((array1 - array2)**2)**(1/2)

	def _c_cor(self, array1, array2):
		""" 相关系数 """

		return pd.Series(array1).corr(pd.Series(array2))

	def _pass_o_dis(self, distance):
		""" 根据距离进行拒绝和通过 """

		if distance < self.dis[0]:
			return 'pass'
		elif distance > self.dis[1]:
			return 'reject'
		else:
			return 'no_result'

	def _pass_c_cor(self, corralation):
		""" 根据相关系数进行拒绝和通过 """

		if corralation > 0.98:
			return 'pass'
		elif corralation < 0.93:
			return 'reject'
		else:
			return 'no_result'

	def _pass_model(self, distance, corralation):
		""" 模型判断是否是人脸 """

		proba = self.model.predict_proba(np.array([distance, corralation]).reshape(1,-1))

		if proba[0][0] < self.threshold:
			return True
		else:
			return False

	def _pass(self, distance, corralation):
		""" 是否通过 """

		if self._pass_o_dis(distance) == 'reject' or self._pass_c_cor(corralation) == 'reject':
			return False
		elif self._pass_o_dis(distance) == 'pass' and self._pass_c_cor(corralation) == 'pass':
			return True
		else:
			return self._pass_model(distance, corralation)

	def isWho(self, t_array, wholist):
		""" 是谁啊 """
		
		wholist = [(name, self._o_dis(t_array, array), self._c_cor(t_array, array)) for name, array in wholist]
		wholist = sorted(wholist, key = lambda x: x[1]+(1-x[2]))
		tar_who = wholist[0]

		if self._pass(tar_who[1], tar_who[2]):
			return tar_who[0]
		else:
			return None