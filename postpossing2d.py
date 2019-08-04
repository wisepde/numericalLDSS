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
		u = pd.read_csv(filename + '_sol' + str(self.h)+'.csv')
		# t = pd.read_csv('a_t0.01.csv')
		x = pd.read_csv(filename + '_x' + str(self.h) +'.csv')
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

import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--e',nargs='?',default=0.001,type=float,help = 'e')
	parser.add_argument('--m',nargs='?',default=1,type=int,help='m')
	parser.add_argument('--h',nargs='?',default=1e-1,type=float,help='h')
	parser.add_argument('--k',nargs='?',default=1e-9,type=float,help='k')
	args = parser.parse_args()
	t = [0.0,8e-6,3.2e-5, 1e-4, 7.2e-4]
	a = postposs(t,args.h,"result/e2d%.0Em%d" %(args.e,args.m))
	a.plot()