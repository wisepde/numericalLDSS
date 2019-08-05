import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import OrderedDict
from numericLDSS1d import *
matplotlib.rcParams.update({'font.size': 20})

# filename = 'e-3m8'
class postposs():
	def __init__(self,t,h=0.01,filename = "a", dpi = 300):
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
		for i in range(u.shape[0]):
			yy = u.iloc[i]
			mass.append(np.sum(yy))
			umin.append(np.min(yy))
			fisher.append(self.h**2*np.sum(Df(yy,1)**2/yy))
			plt.semilogy(xx,yy,linestyle = lstyle[i])
		plt.xlim([0,1])	
		plt.ylim([0.0001,2])
		plt.xticks([0,0.25,0.5,0.75,1.0])	
		plt.savefig(filename + 'u.pdf',dpi=self.dpi)

		# plot mass
		plt.figure()
		plt.plot(mass-mass[0],'.-')
		t11 = [str(i) for i in self.t]
		plt.xticks(range(len(t11)), t11)
		plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		plt.ylim([-1e-10,1e-10])
		plt.savefig(filename + 'mass.pdf',dpi=self.dpi)

		#plot energy
		plt.figure()
		plt.plot(fisher,'.-')
		t11 = [str(i) for i in self.t]
		plt.xticks(range(len(t11)), t11)
		# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		plt.savefig(filename + 'energy.pdf',dpi=self.dpi)

		#plot min value
		plt.figure()
		plt.semilogy(umin,'.-')
		t11 = [str(i) for i in self.t]
		plt.xticks(range(len(t11)), t11)
		# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		plt.savefig(filename + 'min.pdf',dpi=self.dpi)

import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--e',nargs='?',default=0.001,type=float,help = 'e')
	parser.add_argument('--m',nargs='?',default=1,type=int,help='m')
	parser.add_argument('--h',nargs='?',default=1e-2,type=float,help='h')
	parser.add_argument('--k',nargs='?',default=1e-10,type=float,help='k')
	args = parser.parse_args()

	t = [0.0,8e-6,3.2e-5, 1e-4, 7.2e-4]
	a = postposs(t,args.h,"result/e%.0Em%d" %(args.e,args.m))
	a.plot()
