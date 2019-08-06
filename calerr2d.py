import numpy as np
import pandas as pd
from scipy.interpolate import interp2d

def calerror(x,u,x_r,u_r):
	f = interp2d(x,x,u,"cubic")
	err = lambda x,y: np.sum((x-y)**2)
        #err = lambda x,y: np.max(np.abs(x-y))
	return np.sqrt(err(f(x_r,x_r),u_r))
def main(args):
	x = pd.read_csv(args.x)
	u = pd.read_csv(args.u)
	xr = pd.read_csv(args.xr)
	ur = pd.read_csv(args.ur)	
	x =np.array(x['0'])
	xr = np.array(xr['0'])
        u = np.array(u.iloc[-1])
        ur = np.array(ur.iloc[-1])
	print calerror(x,u.reshape((len(x),len(x))),xr,ur.reshape((len(xr),len(xr))))

import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--x',type=str)
	parser.add_argument('--u',type=str)
	parser.add_argument('--xr',type=str)
	parser.add_argument('--ur',type=str)
	args = parser.parse_args()
	main(args)


