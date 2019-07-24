from __future__ import division
import numpy as np
from scipy.optimize import root, fsolve, broyden1
from functools import partial
import matplotlib.style as mplstyle
import matplotlib.pyplot as plt
import matplotlib
from collections import OrderedDict

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
		sol=root(g,self.uold)
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
	def postposs(self, filename = 'a.png', plotrange = None, plotticks = None, lstyle = None):
		print "------Plot Result------"
		print "solved using %s" % self.method
		print len(self.usol)
		for i in range(len(self.usol)):
			# plt.semilogy(self.x,np.transpose(self.usol),linestyle=lstyle)
			plt.semilogy(self.x,np.transpose(self.usol),linestyle=lstyle[i])
		axes = plt.gca()
		if plotrange != None: 
			axes.set_xlim(plotrange[0])
			axes.set_ylim(plotrange[1])
			axes.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
		if plotticks != None:
			plt.xticks(plotticks[0])
			plt.yticks(plotticks[1])
		# if lstyle != None:
			# plt.set(linestyle=lstyle)
		plt.savefig(filename,dpi=1000)
		plt.show()

		print "figure saved to %s" % filename		
	def post_energy(self):
		print "plot energy decay over time"
		energy_fun = lambda u:self.h**2*np.sum(Df(u,1)**2/u)
		uenergy = [energy_fun(i) for i in self.usol]
		plt.plot(self.tt,uenergy)
		# plt.show()
	def post_mass(self):
		print "plot mass over time"
		mass_fun = lambda u: np.sum(u)
		umass = [mass_fun(i) for i in self.usol]
		plt.plot(self.tt,umass)
		# plt.show()



def main():
	# initial parameters
	epsi = 1e-6
	m = 20
	u0_fun =  lambda x: (epsi**0.5 + ((1 + np.cos(2*np.pi*x))/2)**m)**2
	# control of the run
	scope = [0,1]
	h = 1e-2
	k = 1e-10
	steps = int(8e-6/k)#int(7.2e-4/k)
	plttime =np.array([8e-6])#, 3.2e-5, 1e-4, 7.2e-4])
	savesteps = plttime/k
	savesteps = map(int,savesteps)
	# build the model
	a = DLSSsolver1d(k,h,scope,u0_fun,steps,savesteps)
	# run
	a.run('forward_diff')
	# plot result
	linestyles = OrderedDict(
    [('solid',               (0, ())),
     ('dashed',              (0, (5, 5))),
     ('dotted',              (0, (1, 5))),
     ('dashdotted',          (0, (3, 5, 1, 5))),
     ('densely dashed',      (0, (5, 1)))])
	lstyle= [ style for i,(name, style) in enumerate(linestyles.items())]
	# x = np.linspace(0,1,10)
	# plt.plot(x,x,linestyle=lstyle[0])

	# lstyle = ['solid', 'dashed', 'dotted', 'dashdotted', 'densely dashed']
	a.postposs('forward_diff.png',lstyle=lstyle)#,[[0,1],[0.0001,1.5]], [np.linspace(0,1,5),[0.0001,0.001,0.01,0.1,1]],lstyle)
	a.post_energy()
	a.post_mass()
	# explicit-implicit method
	b = DLSSsolver1d(k,h,scope,u0_fun,steps,savesteps)

	# b.run('explicit_implicit')
	# b.postposs('explicit_implicit.png')

if __name__ == "__main__":
	main()






