import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

f = open("arcsizeEdges.txt")	# values from calcDisp
lines = f.readlines()
f.close()

i = 0				# line counter

a = np.zeros(791)		# 791 edges in this dataset

for step in range(50):		# 50 steps in Parse2_Animation.py
   totalLength = 0.
   for edge in range(791):
      totalLength += float(lines[i])
      a[edge] = float(lines[i])
      i += 1

   print(step, totalLength, a.min(), a.max())     # print min-max per step

   # histogram
   nBins = 50
   n, bins, patches = plt.hist(a, nBins, facecolor='blue', alpha=0.5)
   plt.xlim(0., 6.)
   plt.ylim(0., 50.)
   plt.pause(0.001)
   imageName = "movie/pic" + str(step).zfill(4) + ".png"
   plt.savefig(imageName,dpi=80)

   if step < 49:
      plt.clf()		# clear the plot
