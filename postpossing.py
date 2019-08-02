import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import OrderedDict
from numericLDSS1d import *
# filename = 'e-3m8'
class postposs():
	def __init__(self,t,h=0.01,filename = "a", dpi = 300):
		self.filename = filename
		self.t = t
		self.h = h
		self.dpi = dpi 
	def plot(self):
		filename = self.filename
		u = pd.read_csv(filename + '_sol0.01.csv')
		# t = pd.read_csv('a_t0.01.csv')
		x = pd.read_csv(filename + '_x0.01.csv')
		xx = x['0']
		# print u.shape[0]

		linestyles = OrderedDict(
		[('solid',               (0, ())),
		 ('dashed',              (0, (5, 5))),
		 ('dotted',              (0, (1, 5))),
		 ('dashdotted',          (0, (3, 5, 1, 5))),
		 ('densely dashed',      (0, (5, 1)))])
		lstyle= [ style for i,(name, style) in enumerate(linestyles.items())]

		mass = []
		fisher = []
		umin  = []
		for i in range(u.shape[0]):
			yy = u.iloc[i]
			mass.append(np.sum(yy))
			umin.append(np.min(yy))
			fisher.append(self.h**2*np.sum(Df(yy,1)**2/yy))
			plt.semilogy(xx,yy,linestyle = lstyle[i])
		plt.xlim([0,1])	
		plt.ylim([0.0001,2])
		plt.xticks([0,0.25,0.5,0.75,1.0])	
		plt.savefig(filename + 'u.png',dpi=self.dpi)

		# plot mass
		plt.figure()
		plt.plot(mass-mass[0],'.-')
		t11 = [str(i) for i in self.t]
		plt.xticks(range(len(t11)), t11, size='small')
		plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		plt.ylim([-1e-10,1e-10])
		plt.savefig(filename + 'mass.png',dpi=self.dpi)

		#plot energy
		plt.figure()
		plt.plot(fisher,'.-')
		t11 = [str(i) for i in self.t]
		plt.xticks(range(len(t11)), t11, size='small')
		plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		plt.savefig(filename + 'energy.png',dpi=self.dpi)

		#plot min value
		plt.figure()
		plt.semilogy(umin,'.-')
		t11 = [str(i) for i in self.t]
		plt.xticks(range(len(t11)), t11, size='small')
		# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		plt.savefig(filename + 'min.png',dpi=self.dpi)

if __name__ == "__main__":
	t = [0.0,8e-6,3.2e-5, 1e-4, 7.2e-4]
	a = postposs(t,0.01,'e-3m1')
	a.plot()