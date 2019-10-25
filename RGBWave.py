import numpy as np
import scipy.misc as smp
import sys
import math

if  len(sys.argv) > 1: file_name = sys.argv[1]
f = open("ULT_31TX.txt")
lines = f.readlines()
x_index = []
y_index = []
real = []
imag = []

for l in lines:
    if(len(l.split('\t'))>1):
        x_index.append(int(l.split('\t')[0]))
        y_index.append(int(l.split('\t')[1]))
        real.append(2*int(l.split('\t')[4]))
        imag.append(int(l.split('\t')[5]))

f.close()
mag=[]

for i in range(len(real)):
    mag.append(math.sqrt(real[i]**2+imag[i]**2))

height_max = np.max(y_index)+1
width_max = np.max(x_index)+1

mag_max=np.max(mag)

# Create raster array
data = np.zeros( (height_max,width_max,3), dtype=np.uint8 )

print ('\n Height Max: '+ str(height_max) + ' Width Max: ' + str(width_max))

#Yellow Angle
y=96
#Green Angle
g=144
#Blue 
b=252

mod = 0
for i in range(width_max-2):
    
    for j in range(height_max):
        norm = math.sqrt(math.pow(real[i*(height_max)+j],2)+math.pow(imag[i*(height_max)+j],2))
        n_norm = norm/mag_max
        angle = math.atan2(imag[i*(height_max)+j],(real[i*(height_max)+j]+0.0001))
        angle=angle*180/math.pi
        if(angle<0):
            angle=angle+360

        j1=(height_max-1)*mod+j*(-1)**mod
        
        if(angle<y):
            data[j1,i] = [int(255*n_norm), int(255*n_norm*(angle/y)), 0]
        elif(angle<g):
            data[j1,i] = [int(255*n_norm*(1-(angle-y)/(g-y))), int(255*n_norm), 0]
        elif(angle<b):
            data[j1,i] = [0, int(255*n_norm*(1-(angle-g)/(b-g))), int(255*n_norm*(angle-g)/(b-g))]
        elif(angle<360):
            data[j1,i] = [int(255*n_norm*((angle-b)/(360-b))),0, int(255*n_norm*(1-(angle-b)/(360-b)))]
    if(mod==0):
        mod=1
    else:
        mod=0

img = smp.toimage( data )
img.format = "PNG"
img = smp.imresize(img,(1600,1800))
img = smp.toimage( img )
img.save("ULT_31TX.png")
img.show()


