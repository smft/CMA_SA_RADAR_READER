# -*- coding: utf-8 -*-

"""
read radar data
@author: qzhang
"""

import numpy as np
import string
from array import array
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# read radar binary data
def radar_read(file_path):
	pi=np.pi
	# 读数据
	flag=open(file_path,"r")
	data=np.asarray(array("B",flag.read()))
	data=data.reshape([len(data)/2432,2432])
	# 找仰角
	if data[0,72]==11:
		phi=[0.50,0.50,1.45,1.45,2.40,3.35,4.30,5.25,6.2,7.5,8.7,10,12,14,16.7,19.5]
	if data[0,72]==21:
		phi=[0.50,0.50,1.45,1.45,2.40,3.35,4.30,6.00,9.00,14.6,19.5]
	if data[0,72]==31:
		phi=[0.50,0.50,1.50,1.50,2.50,2.50,3.50,4.50]
	if data[0,72]==32:
		phi=[0.50,0.50,2.50,3.50,4.50]
	g1=np.zeros([len(data),460])
	h1=np.zeros([len(data),460])
	i1=np.zeros([len(data),460])
	j1=np.zeros([len(data),460])
	count=0
	while count<len(data):
		print "径向数据编号 : ",count
		b1=data[count,44]+256*data[count,45]				#仰角序数
		c1=(data[count,36]+256*data[count,37])/8*180/4096				#方位角
		d1=data[count,54]+256*data[count,55]				#径向库
		print "仰角序数,方位角,径向库 : ",b1,c1,d1
		if d1==0:
			count+=1
			continue
		else:
			count+=1
		i=0
		while i<460:
			g1[count-1,i]=phi[b1-1]									#仰角
			h1[count-1,i]=c1												#方位角
			i1[count-1,i]=0.5+i-1											#径向
			if i>d1:																	#反射率
				j1[count-1,i]=0
			else:
				if data[count-1,128+i]==0:							#无数据
					j1[count-1,i]=0
				else:
					if data[count-1,128+i]==1:						#距离模糊
						j1[count-1,i]=0
					else:																#数据正常
						j1[count-1,i]=(data[count-1,128+i]-2)/2-32
			i+=1
	n=3
	a2=0															#仰角序数
	while a2<len(data):
		if data[a2,44]>(n-1):
			break
		a2+=1
	a3=a2
	while a3<len(data):
		if data[a3,44]>n:
			break
		a3+=1
	yj=g1[a2:a3,:]
	fwj=h1[a2:a3,:]
	jx=i1[a2:a3,:]
	fsl=j1[a2:a3,:]
	return yj,fwj,jx,fsl
	
def sph2cart(elevation,azimuth,r):
	ele,a= np.deg2rad([elevation,azimuth])
	x=r*np.cos(ele)*np.cos(a)
	y= r * np.cos(ele) * np.sin(a)
	z = r * np.sin(ele)
	return x,y,z
"""
# test
y,fw,j,fs=radar_read("/media/qzhang/240E5CF90E5CC608/2011_07_18/radar/Z_RADR_I_Z9250_20110718075900_O_DOR_SA_CAP.bin")
nx,ny,nz=sph2cart(y,fw,j)
plt.subplot(1, 1, 1)
plt.pcolor(ny, nx, fs, cmap='Accent')
plt.axis([ny.min(), ny.max(), nx.min(), nx.max()])
plt.show()
"""
