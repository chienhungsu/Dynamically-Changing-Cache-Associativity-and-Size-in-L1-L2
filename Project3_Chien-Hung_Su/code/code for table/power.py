#! /usr/bin/python

import re
import csv
import os 
import math
import xlwt
import xlrd
comma = ','

k=[]
o=[]

def search_IPC(startID, endID, Filename):
	path="/home/chien/Desktop/611Project/html/"
	pa='/home/chien/Desktop/611Project/html/'
	ss=pa+"powerl2"
	pp=ss+".csv"
	if(Filename=="outputl1"):
		ss=pa+"powerl1"
		pp=ss+".csv"
	if(Filename=="l3"):
		ss=pa+"powerl3"
		pp=ss+".csv"
	IPC = open(pp , 'w')
	filedata=[]
	finaldata=[]
	
	for i in range(endID - startID +1):
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet("power")
		path=''
		File1 = str(i+1)+Filename+'.htm' 
		if(Filename=="l3"):
			File1 = Filename+'.htm' 
		path=path+File1
		g=0
		#file2 = Filename1 + str(startID +1)
		with open( path) as txtFile:
			txtData = str(txtFile.read())
			b=txtData.find('Total read dynamic power per read port at max freq (W):',0)
			txtFile.seek(b,0)
			value=txtFile.readline()
			s=str(value)
			word1=re.split(':|\n',s)
			print(str(word1[1]))#+', '+str(word1[1]))#+', '+str(word1[2])+', '+str(word1[3]))
			#print("Total read dynamic power per read port at max freq (W):"+s)
			b1=txtData.find('Total standby leakage power per bank (W):',0)
			txtFile.seek(b1,0)
			value1=txtFile.readline()
			s1=str(value1)
			word=re.split(':|<br>',s1)
			#g=0
			g=g+1
			print(str(word[1]))	
			a='{},{}'.format(word1[1],word[1]+'\n')
			k=float(word1[1])+float(word[1])
			sheet.write(g,0,str(word1[1]))
			sheet.write(g,1,str(word[1]))
			sheet.write(g,2,str(k))

		
			#IPC.write(a)
			sheet.write(0,0,"L1_dynamic power")
			sheet.write(0,1,"L1_leakage power")
			sheet.write(0,2,"L1_total_power")
		workbook.save(ss+str(i)+".xls")	
	#IPC.close()


def main():
	search_IPC(1, 4, "outputl1")
	search_IPC(1, 4, "outputl2")
	search_IPC(1,1,"l3")


if __name__ =='__main__':
	main()
