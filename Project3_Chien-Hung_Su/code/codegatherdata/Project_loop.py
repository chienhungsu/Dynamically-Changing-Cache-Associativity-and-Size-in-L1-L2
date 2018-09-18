# L1 32k, 64k
# L1 a 1,2
# L2 size 128k, 256k
# L2 assoc 4, 8
#!/usr/bin/python
import os
import os.path
import sys
import string
import socket


L1Dcache_Icache_size=[32,64]
L2cache_size=[128,256]
L1Dcache_Icache_assoc=[1,2]
L2cache_assoc=[4,8]
#cis=[16,32,64,128]
#cia=[1,2,4,8,16]

filename = "configuration.txt"
con= open(filename,"wb")
c="c"
m=0
for i in range(2):
	for k in range(2):
		for p in range(2):
			for l in range(2):
				#for p in range(3):
				#	for w in range(3):
						
						con.writelines(c+str(m)+"= ["+"32, 32, 64, 64, 64, 24, "+str(L1Dcache_Icache_assoc[p])+","+str(L1Dcache_Icache_size[l])+","+ str(L1Dcache_Icache_assoc[p])+","+str(L1Dcache_Icache_size[l])+",2,1,1, 8, 4,"+str(L2cache_assoc[i])+", "+str(L2cache_size[k])+"]"+"\n")
						m=m+1
con.close()		



