import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
h = [0.1,0.05,0.025,0.0125]
err = pd.read_csv("log.csv",header=None)
err = err[0]
err = np.array(err)
print err
print h
print err
plt.plot(h,err,'.-')
plt.savefig("err1d.pdf",dpi=1000)
