import pandas as pd
import numpy as np
import matplotlib
from mpl_toolkits import mplot3d
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import OrderedDict
from numericLDSS1d import *
# filename = 'e-3m8'
class postposs():
	def __init__(self,t,h,filename, dpi = 300):
		self.filename = filename
		self.t = t
		self.h = h
		self.dpi = dpi 
	def plot(self):
		filename = self.filename
		u = pd.read_csv(filename + '_sol0.1.csv')
		# t = pd.read_csv('a_t0.01.csv')
		x = pd.read_csv(filename + '_x0.1.csv')
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
		[xx,yy] = np.meshgrid(xx,xx)
		for i in range(u.shape[0]):
			uu = u.iloc[i]
			uu=uu.reshape([len(xx),len(xx)])
			# mass.append(np.sum(yy))
			umin.append(np.min(uu))
			# fisher.append(self.h**2*np.sum(Df(yy,1)**2/yy))
			# plt.semilogy(xx,yy,linestyle = lstyle[i])
			fig = plt.figure()
			ax = fig.gca(projection='3d')
			surf = ax.plot_surface(xx,yy,uu, lw=0.5, rstride=1, cstride=1)
			ax.set_zscale('log')
			# plt.contoursurf(xx,yy,uu)
			plt.savefig(filename + "_" + str(i)+ 'u.png',dpi=self.dpi)

		# plt.xlim([0,1])	
		# plt.ylim([0.0001,2])
		# plt.xticks([0,0.25,0.5,0.75,1.0])	
		# plt.savefig(filename + 'u.png',dpi=self.dpi)

		# # plot mass
		# plt.figure()
		# plt.plot(mass-mass[0],'.-')
		# t11 = [str(i) for i in self.t]
		# plt.xticks(range(len(t11)), t11, size='small')
		# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		# plt.ylim([-1e-10,1e-10])
		# plt.savefig(filename + 'mass.png',dpi=self.dpi)

		# #plot energy
		# plt.figure()
		# plt.plot(fisher,'.-')
		# t11 = [str(i) for i in self.t]
		# plt.xticks(range(len(t11)), t11, size='small')
		# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		# plt.savefig(filename + 'energy.png',dpi=self.dpi)

		#plot min value
		# plt.figure()
		# plt.plot(umin,'.-')
		# t11 = [str(i) for i in self.t]
		# plt.xticks(range(len(t11)), t11, size='small')
		# # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		# plt.savefig(filename + 'min.png',dpi=self.dpi)

if __name__ == "__main__":
	# t = [0.0,8e-6,3.2e-5, 1e-4, 7.2e-4]
	t = [0.0, 1e-4]
	a = postposs(t,0.1,'e2d-3m2')
	a.plot()