#! /usr/bin/python

import re
import csv
import os 
import math
import xlwt
comma = ','
o=1
cyc=''
instr=''
efficiency=''
target=''

total_power=[3.7426033,3.79792395,3.89189053,3.93845177,3.80932064,3.86464129,3.95860786,4.0051691,4.60592648,4.66124713,4.7552137,4.80177494,4.61627773,4.67159838,4.76556495,4.8121262]

def search_IPC(startID, endID, Filename):
	s=0
	for o in range(endID - startID +1):
			filei = "/home/chien/Desktop/611Project/IPC/"+"bzip_IPC"+str(o)
			#fileIPC1 = open(filei+'.txt' , 'w')
			workbook = xlwt.Workbook()
			sheet = workbook.add_sheet("IPC")

			p=0
			t=0
		#for i in range(endID - startID +1):
			IPC_Data = []
			IPC_Data1 = []
			File1 = Filename + str(o)
			#file2 = Filename1 + str(startID +1)
			with open( File1) as txtFile:
				txtData = txtFile.readlines()
				#print(txtData)
				for line in txtData:
					if line != '\n':
						words = re.split(' |,|= |\n|:|;', line)
						if words[0].startswith('cyc'):
							
							value = str(words[2])
							#print('cyc'+value)
							sheet.write(t,0,str(t))
							sheet.write(t,1,value)
							IPC_Data.append('cyc '+value)
							value4 = str(words[6])
							#value4 = value4+comma+'\n'
							#print('instr'+value4)
							sheet.write(t,2,value4)
							print(str(total_power[s])+'\n')
							sheet.write(t,4,str(total_power[s]))
							IPC_Data.append('instr '+value4)
							if p !=0:

								cyc=float(value)-float(cyc1)
								instr=float(value4)-float(instr1)
								ipc=float(instr)/float(cyc)
								efficiency=str(float(ipc)/float(total_power[s]))
								target=str(float(efficiency)/float(total_power[s]))
								sheet.write(t,3,str(ipc))

								sheet.write(t,5,efficiency)
								sheet.write(t,6,target)
								IPC_Data.append('IPC '+str(ipc)+'\n')
								instr1=float(value4)
								cyc1=float(value)
							if p==0:
								#print(str(total_power[s])+'\n')
								cyc1=float(value)
								instr1=float(value4)
								ipc=float(value4)/float(value)
								efficiency=str(float(ipc)/float(total_power[s]))
								target=str(float(efficiency)/float(total_power[s]))
								sheet.write(t,3,str(ipc))
								#sheet.write(t,4,str(total_power[o]))
								sheet.write(t,5,efficiency)
								sheet.write(t,6,target)
								IPC_Data.append('IPC '+str(ipc)+'\n')
							p=p+1
							t=t+1	
						
				IPC= comma.join(IPC_Data)
	#		fileIPC1.write(IPC)
			workbook.save("/home/chien/Desktop/611Project/IPC/"+"bzip"+str(o)+".xls")
			s=s+1
	#fileIPC1.close()
		#with open(file2) as txtFile1:
		#	Data1 = txtFile1.readlines()





def main():
	search_IPC(0,15,'bzip2_source')

if __name__ =='__main__':
	main()
