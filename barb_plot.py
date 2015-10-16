# -*- coding: utf-8 -*-

"""
read AWS data and plot wind barb 
@author: qzhang
"""

import numpy as np
import string
from array import array
import matplotlib.pyplot as plt
from read_AWS import AWS_extract
from read_RADAR import radar_read
from read_RADAR import sph2cart

AWS_file_path="/media/qzhang/240E5CF90E5CC608/2011_07_18/AWS/11071819.AWS"
station_num,data,record=AWS_extract(AWS_file_path)

for cell in data:
	if cell[3]==9999.0 or cell[4]==9999.0:
		uwnd=None
		vwnd=None
	else:
		if cell[3]<=90:
			uwnd=-cell[4]*np.sin(cell[3]*np.pi/180)
			vwnd=-cell[4]*np.cos(cell[3]*np.pi/180)
		if cell[3]>90 and cell[3]<=180:
			uwnd=-cell[4]*np.sin((180-cell[3])*np.pi/180)
			vwnd=cell[4]*np.cos((180-cell[3])*np.pi/180)
		if cell[3]>180 and cell[3]<=270:
			uwnd=cell[4]*np.sin((cell[3]-180)*np.pi/180)
			vwnd=cell[4]*np.cos((cell[3]-180)*np.pi/180)
		if cell[3]>270 and cell[3]<=360:
			uwnd=cell[4]*np.sin((360-cell[3])*np.pi/180)
			vwnd=-cell[4]*np.cos((360-cell[3])*np.pi/180)
	cell[3]=uwnd
	cell[4]=vwnd

data_to_plot=[]
count=0
while count<record:
	if data[count,1]<=120 and data[count,0]<=33 and data[count,1]>=118 and data[count,0]>=31:
		data_to_plot=data_to_plot+[data[count,1],data[count,0],data[count,3],data[count,4]]
	count+=1
data_to_plot=np.asarray(data_to_plot).reshape([len(data_to_plot)/4,4])

radar_loc={"lon":118.69,"lat":32.19}
radar_file_path="/media/qzhang/240E5CF90E5CC608/2011_07_18/radar/Z_RADR_I_Z9250_20110718110000_O_DOR_SA_CAP.bin"
y,fw,j,fs=radar_read(radar_file_path)
nx,ny,nz=sph2cart(y,fw,j)

"""
ax=plt.subplot(1,1,1)
ax.barbs(data[:,1],data[:,0],data[:,3],data[:,4])
plt.show()
"""
plt.subplot(1,1,1)
plt.pcolor(ny,nx,fs,cmap='gist_ncar',vmin=10,vmax=75)
plt.axis([-80,160,-140,100])
plt.colorbar(ticks=np.linspace(10,75,14))
plt.subplot(1,1,1)
plt.barbs((data_to_plot[:,0]-radar_loc["lon"])*110,(data_to_plot[:,1]-radar_loc["lat"])*110,data_to_plot[:,2],data_to_plot[:,3])
plt.title("2011-07-18_11:00 UTC",fontsize=20)
plt.xlabel("Longitude",fontsize=14)
plt.ylabel("Latitude",fontsize=14)
plt.xticks([-80,-20,40,100,160],[118.0,118.5,119.0,119.5,120.0])
plt.yticks([-140,-80,-20,40,100],[31.0,31.5,32,32.5,33])
plt.show()
