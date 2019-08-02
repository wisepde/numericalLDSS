from __future__ import division
import numpy as np
from scipy.optimize import root, fsolve, broyden1
from functools import partial
import matplotlib.pyplot as plt
import pandas as pd

#defined for 2d use
def Dx(u,h):
	return np.diff(np.column_stack((u,u[:,0])))/h
def Dy(u,h):
	return np.diff(np.vstack((u,u[0])),axis=0)/h
def dx(u,h):	return np.diff(np.column_stack((u[:,-1],u)))/h
def dy(u,h):
	return np.diff(np.vstack((u[-1],u)),axis=0)/h
def Dh(u,h):
	return np.array([Dx(u,h),Dy(u,h)])
def dh(f,h):
	return dx(f[0],h) + dy(f[1],h)

class DLSSsolver2d():
	def __init__(self, k, h, scope, uinitial, steps = 1000, savesteps = [10]):
		self.h = h
		self.k = k
		self.x = np.linspace(scope[0,0],scope[0,1],(scope[0,1]-scope[0,0])/h+1)
		self.y = np.linspace(scope[1,0],scope[1,1],(scope[1,1]-scope[1,0])/h+1)
		self.gridpt = np.meshgrid(self.x,self.y)
		self.u0 = np.array([[uinitial([x,y]) for x in self.x] for y in self.y])
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
		H = -1/2*(Dx(self.u,self.h)**2/(self.u**2) + Dy(self.u,self.h)**2/(self.u**2))- dx(Dx(self.u,self.h)/self.u,self.h)-dy(Dy(self.u,self.h)/self.u,self.h)
		umiddlex = (np.roll(self.uold,-1)+self.uold)/2
		umiddley = (np.roll(self.uold,-1,axis=0)+self.uold)/2
		f = dx(umiddlex*Dx(H,self.h),self.h) + dy(umiddlex*Dy(H,self.h),self.h)
		return f
	def forward_diff(self):
		self.uold = self.u
		self.u = self.u + self.k*self.Nsch()
	def explicit_implicit(self):
		self.uold = self.u
		g = lambda u:(u - self.uold.flatten()) - self.k* self.Nsch().flatten()
		sol=root(g,self.uold)
		self.u=sol.x.reshape(self.uold.shape)
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
		usol2 = [sol.flatten() for sol in self.usol] 
		pd.DataFrame(usol2).to_csv(usolfile,index=False)
		pd.DataFrame(self.tt).to_csv(tfile,index=False)
		pd.DataFrame(self.x).to_csv(xfile,index=False)

	def postposs(self, filename = 'a.png'):
		print "------Plot Result------"
		print "solved using %s" % self.method
		X,Y = np.meshgrid(self.x,self.y)
		ax = plt.axes(projection='3d')
		ax.plot_surface(X,Y,self.usol[0])
		ax.plot_surface(X,Y,self.usol[50])

		ax.plot_surface(X,Y,self.usol[-1])
		plt.savefig(filename)
		plt.show()

		print "figure saved to %s" % filename
def main():
	# initial parameters
	epsi = 1e-3
	m = 8
	u0_fun =  lambda x: (epsi**0.5 + ((1 + np.cos(2*np.pi*x[0])*np.cos(2*np.pi*x[1]))/2)**m)**2
	# u0_fun =  lambda x: (epsi**0.5 + ((1 + np.cos(2*np.pi*x[0]))/2)**m)**2
	# control of the run
	scope = np.array([[0,1],[0,1]])
	h = 1e-1
	k = 1e-10
	steps = int(8e-6/k)#(7.2e-4/k)
	plttime =np.array([8e-6])#6, 3.2e-5, 1e-4, 7.2e-4])
	savesteps = plttime/k
	savesteps = map(int,savesteps)
	# build the model
	a = DLSSsolver2d(k,h,scope,u0_fun,steps,savesteps)
	# run
	# a.run('explicit_implicit')
	a.run('forward_diff')
	a.saveresult("e2d-3m8")

if __name__ == '__main__':
	main()