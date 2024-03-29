from __future__ import division
import numpy as np
from scipy.optimize import root, fsolve, broyden1
from functools import partial
from collections import OrderedDict
import pandas as pd
# mplstyle.use(['ggplot'])

# defined for 1d use
def Df(u,h):
	return np.diff(np.append(u,u[0]))/h
def df(u,h):
	# return np.diff(np.append(u,u[0]))/h
	return np.diff(np.append(u[-1],u))/h	

class DLSSsolver1d():
	def __init__(self, k, h, scope, uinitial, steps = 1000, savesteps = 10):
		self.h = h
		self.k = k
		self.x = np.linspace(scope[0],scope[1],(scope[1]-scope[0])/h+1)
		self.u0 = uinitial(self.x)
		self.u = self.u0
		self.uold = self.u0
		self.steps = steps
		if type(savesteps) == int:
			self.savesteps = range(0,steps,savesteps)
		else:
			self.savesteps = savesteps
		self.usol = [self.uold]
		self.tt = [0]
	def Nsch(self):
		H = -1/2*Df(self.u,self.h)**2/(self.u**2) - df(Df(self.u,self.h)/self.u,self.h)
		umiddle = (np.roll(self.uold,-1)+self.uold)/2
		f = df(umiddle*Df(H,self.h),self.h)
		return f
	def forward_diff(self):
		self.uold = self.u
		self.u = self.u + self.k*self.Nsch()
	def explicit_implicit(self):
		self.uold = self.u
		g = lambda u:(u - self.uold) - self.k* self.Nsch()
		sol=root(g,self.uold,method='df-sane')
		self.u=sol.x
	def run(self,method):
		self.method = method
		for i in range(self.steps+1):
			if method == 'forward_diff':
				self.forward_diff()
			elif method == 'explicit_implicit':
				self.explicit_implicit()
			else:
				raise Exception('Method not defined!')
			if i in self.savesteps:
				self.usol.append(self.u)
				self.tt.append(self.k*self.steps)
		self.usol = np.array(self.usol)
        def saveresult(self, filename = 'a'):
            print "save results to %s" %filename
            usolfile = filename + "_sol" + str(self.h) + '.csv'
            tfile = filename + "_t" + str(self.h) + '.csv'
            xfile = filename + "_x" + str(self.h) + '.csv'
            pd.DataFrame(self.usol).to_csv(usolfile,index=False)
            pd.DataFrame(self.tt).to_csv(tfile,index=False)
            pd.DataFrame(self.x).to_csv(xfile,index=False)

def main(argv):
	# initial parameters
	epsi = args.e #1e-3
	m = args.m #2
	print epsi, m
	u0_fun =  lambda x: (epsi**0.5 + ((1 + np.cos(2*np.pi*x))/2)**m)**2
	# control of the run
	scope = [0,1]
	h = args.h#1e-2
	k = args.k#1e-10
	steps = int(7.2e-4/k)
	plttime =np.array([8e-6, 3.2e-5, 1e-4, 7.2e-4])
	savesteps = plttime/k
	savesteps = map(int,savesteps)
	# build the model
	a = DLSSsolver1d(k,h,scope,u0_fun,steps,savesteps)
	# run


	a.run('explicit_implicit')
	a.saveresult("result/e%.0Em%d" %(epsi,m))
        # plot result
#	linestyles = OrderedDict(
 #   [('solid',               (0, ())),
  #   ('dashed',              (0, (5, 5))),
   #  ('dotted',              (0, (1, 5))),
    # ('dashdotted',          (0, (3, 5, 1, 5))),
     #('densely dashed',      (0, (5, 1)))])
#	lstyle= [ style for i,(name, style) in enumerate(linestyles.items())]
	# x = np.linspace(0,1,10)
	# plt.plot(x,x,linestyle=lstyle[0])

	# lstyle = ['solid', 'dashed', 'dotted', 'dashdotted', 'densely dashed']
	#a.postposs('explicit_implicit.png',lstyle=lstyle)#,[[0,1],[0.0001,1.5]], [np.linspace(0,1,5),[0.0001,0.001,0.01,0.1,1]],lstyle)
	#a.post_energy()
	# a.post_mass()
	# a.post_min()
	# explicit-implicit method
#	b = DLSSsolver1d(k,h,scope,u0_fun,steps,savesteps)

	# b.run('explicit_implicit')
	# b.postposs('explicit_implicit.png')
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--e',nargs='?',default=0.001,type=float,help = 'e')
	parser.add_argument('--m',nargs='?',default=1,type=int,help='m')
	parser.add_argument('--h',nargs='?',default=1e-2,type=float,help='h')
	parser.add_argument('--k',nargs='?',default=1e-10,type=float,help='k')
	args = parser.parse_args()
	main(args)






