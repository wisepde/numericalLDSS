import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def calerror(x,u,x_r,u_r):
	f = interp1d(x,u)
	err = lambda x,y: np.sum((x-y)**2)
	return err(f(x_r),u_r)
def main(args):
	x = pd.read_csv(args.x)
	u = pd.read_csv(args.u)
	xr = pd.read_csv(args.xr)
	ur = pd.read_csv(args.ur)	
	x = x['0']
	xr = xr['0']
	print calerror(x,u.iloc[0],xr,ur.iloc[0])

import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--x',type=str)
	parser.add_argument('--u',type=str)
	parser.add_argument('--xr',type=str)
	parser.add_argument('--ur',type=str)
	args = parser.parse_args()
	main(args)


