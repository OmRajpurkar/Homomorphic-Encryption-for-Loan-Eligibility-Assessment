import matplotlib.pyplot as plt

title=""

def getPoints(x1,y1,x2,y2):
    xval=[]
    yval=[]
    xval.append(0)
    yval.append(0)
    for a in range(-10,10):
      for b in range(-10,10):
        xnew=a*x1+b*x2
        xval.append(xnew)
        ynew=a*y1+b*y2
        yval.append(ynew)

    return xval,yval

x1=6
y1=9
x2=11
y2=11

# Standard Basis
# x1=1
# y1=0
# x2=0
# y2=1

title="x1="+str(x1)+",y1="+str(y1)+"  x2="+str(x2)+",y2="+str(y2)

print (title)
print ("Saving to file.png")

xval,yval=getPoints(x1,y1,x2,y2)

plt.title(title)
plt.xlabel('x')
plt.ylabel('y')
plt.axis([0,max(xval)/2,0,max(yval)/2])
# plt.axis([min(xval),max(xval),min(yval),max(yval)])   # Plotting the entire range

plt.scatter(xval,yval)

plt.savefig('file')
plt.show()
