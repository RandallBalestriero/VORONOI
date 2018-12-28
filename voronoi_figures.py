from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from numpy import gradient as npgrad





class Voronoi:
    def __init__(self,mu,r):
        self.mu = mu
        self.b  = -(mu**2).sum(1)+r
        self.r  = r
        self.hyperplanes = [Hyperplane(2*mu,b) for mu,b in zip(self.mu,self.b)]
    def cluster(self,x):
        distances = ((x[:,newaxis,:]-self.mu[newaxis,:,:])**2).sum(2)-self.r[newaxis,:]
        return distances.argmin(1).astype('float32')
    def project(self,x):
        return stack([hyperplane.project(x) for hyperplane in self.hyperplanes])


class Hyperplane:
    def __init__(self,slope,bias):
        self.slope = slope
        self.bias  = bias
    def project(self,x):
        return dot(x,self.slope)+self.bias


class Space:
    def __init__(self,MIN_X,MAX_X,MIN_Y,MAX_Y,N):
        self.x,self.y = meshgrid(linspace(MIN_X,MAX_X,N),linspace(MIN_Y,MAX_Y,N))
        self.X        = concatenate([self.x.reshape((-1,1)),self.y.reshape((-1,1))],axis=1)
 

class CircleSpace:
    def __init__(self,CENTER,RADIUS,N):
        x,y    = meshgrid(linspace(CENTER-RADIUS,CENTER+RADIUS,N),linspace(CENTER-RADIUS,CENTER+RADIUS,N))
        mask   = sqrt(x**2+y**2)<=RADIUS
        self.x = x[mask]
        self.y = y[mask]
        self.X = concatenate([self.x.reshape((-1,1)),self.y.reshape((-1,1))],axis=1)
 



def plot1(w,b,name='noname.png'):
	K = len(w)
	V = Voronoi(w,b)
	C = V.cluster(space.X).reshape((N,N))
	C/=C.max()
	#PLOT THE VQ
	ax.contourf(space.x,space.y,C,100,zdir='z',offset=START,alpha=0.7,cmap='RdYlGn')#,levels = levels*0.000001,cmap='Greys')

	C_ = 10
	#PLOT THE PARABOLOID
	cspace = CircleSpace(0,1.6,100)
	ax.plot_trisurf(cspace.x,cspace.y,(cspace.x**2+cspace.y**2)+START+offset,color='royalblue',alpha=0.3,edgecolor='none')
	
	#PLOT THE HYPERPLANES AND CENTROIDS
	for k in range(K):
	    minispace = Space(w[k,0]-DISTANCE/C_,w[k,0]+DISTANCE/C_,w[k,1]-DISTANCE/C_,w[k,1]+DISTANCE/C_,N/4)
#	    ax.plot_surface(minispace.x,minispace.y,V.hyperplanes[k].project(minispace.X).reshape((N/4,N/4))+START+offset,facecolors=repeat((cm.RdYlGn([0,1,C[int(N*(w[k,1]-MIN)/DISTANCE),int(N*(w[k,0]-MIN)/DISTANCE)]])[[-1]]),minispace.x.size,0).reshape((minispace.x.shape[0],minispace.x.shape[1],4)),cstride=1,rstride=1,alpha=0.1)
            ax.plot_surface(minispace.x,minispace.y,V.hyperplanes[k].project(minispace.X).reshape((N/4,N/4))+START+offset,facecolors=repeat((cm.RdYlGn([0,1,k*1.0/len(w)])[[-1]]),minispace.x.size,0).reshape((minispace.x.shape[0],minispace.x.shape[1],4)),cstride=1,rstride=1,alpha=0.1)
	    ax.plot([w[k,0],w[k,0]],[w[k,1],w[k,1]],[(w[k]**2).sum()+START+offset,START+0.1],'--k',lw=2,zorder=100)
	    ax.plot([w[k,0]],[w[k,1]],[START+0.1],'ok',zorder=100,ms=6)
	    ax.plot([w[k,0]],[w[k,1]],[START+offset+(w[k]**2).sum()],'ok',zorder=100,ms=6)
	    if(V.r[k]>0):
	        theta = linspace(-1,1,100)
	        for tm,t in zip(theta[:-1],theta[1:]):
	            ax.plot([w[k,0]+sqrt(V.r[k])*tm,w[k,0]+sqrt(V.r[k])*t],[w[k,1]-sqrt(V.r[k]-V.r[k]*tm**2),w[k,1]-sqrt(V.r[k]-V.r[k]*t**2)],[START+0.1,START+0.1],'--k',zorder=100,alpha=0.5)
	            ax.plot([w[k,0]+sqrt(V.r[k])*tm,w[k,0]+sqrt(V.r[k])*t],[w[k,1]+sqrt(V.r[k]-V.r[k]*tm**2),w[k,1]+sqrt(V.r[k]-V.r[k]*t**2)],[START+0.1,START+0.1],'--k',zorder=100,alpha=0.5)
	# PLOT THE PARABOLOID BOUNDARY
	H = stack([V.hyperplanes[k].project(space.X).reshape((N,N)) for k in xrange(K)],axis=0).max(0)+START+2.8*offset
	ax.plot_surface(space.x,space.y,H,facecolors=cm.RdYlGn(C),alpha=0.4,rstride=1, cstride=1)
	
	# PLOT THE POLYGON
	x_ = copy(space.x)
	y_ = copy(space.y)
	z_ = copy(H)
	x_ = concatenate([x_,x_[:,::-1],x_[:,0].reshape((-1,1))],axis=1)
	x_ = concatenate([x_[0].reshape((1,-1)),x_,x_[0].reshape((1,-1))],axis=0)
	#x_ = concatenate([x_[0].reshape((1,-1)),x_,x_,x_[-1].reshape((1,-1))],axis=0)
	y_ = concatenate([y_,y_,y_[:,0].reshape((-1,1))],axis=1)
	y_ = concatenate([y_[0].reshape((1,-1)),y_,y_[-1].reshape((1,-1))],axis=0)
	#y_ = concatenate([y_[0].reshape((1,-1)),y_,y_[::-1],y_[-1].reshape((1,-1))],axis=0)
	z_ = concatenate([z_,z_*0+z_.max()+0.5,z_[:,0].reshape((-1,1))],axis=1)
	z_ = concatenate([z_[0].reshape((1,-1))*0+z_.max(),z_,z_[0].reshape((1,-1))*0+z_.max()],axis=0)
	#z_ = concatenate([z_[0].reshape((1,-1))*0+z_.max(),z_,z_*0+z_.max(),z_[0].reshape((1,-1))*0+z_.max()],axis=0)
	ax.plot_wireframe(x_,y_,z_,color='blue',alpha=0.1,rstride=80, cstride=80)
	ax.plot_surface(x_,y_,z_,color='royalblue',alpha=0.1,rstride=20, cstride=20)
	ax.plot([MIN,MIN],[MIN,MAX],[z_.max(),z_.max()],color='blue',alpha=0.25)
	ax.plot([MAX,MAX],[MIN,MIN],[H[0,-1],z_.max()],color='blue',alpha=0.25)
	
	ax.set_zlim(-0.5,6)
	ax.grid(False)
	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_zticks([])
	axis('off')
	tight_layout()
	ax.view_init(elev=18., azim=145)
	ax.dist = 18
	if(name is not None):
		savefig(name)








def plot2(w,b,name='noname.png'):
	K = len(w)
	V = Voronoi(w,b)
	C = V.cluster(space.X).reshape((N,N))
	C/=C.max()
	#PLOT THE VQ
	ax.contourf(space.x,space.y,C,100,zdir='z',offset=START,alpha=0.7,cmap='RdYlGn')#,levels = levels*0.000001,cmap='Greys')
	C_ = 10
	#PLOT THE HYPERPLANES AND CENTROIDS
	for k in range(K):
	    ax.plot([w[k,0]],[w[k,1]],[START+0.1],'ok',zorder=100,ms=6)
	    if(V.r[k]>0):
	        theta = linspace(-1,1,100)
	        for tm,t in zip(theta[:-1],theta[1:]):
	            ax.plot([w[k,0]+sqrt(V.r[k])*tm,w[k,0]+sqrt(V.r[k])*t],[w[k,1]-sqrt(V.r[k]-V.r[k]*tm**2),w[k,1]-sqrt(V.r[k]-V.r[k]*t**2)],[START+0.1,START+0.1],'--k',zorder=100,alpha=0.5)
	            ax.plot([w[k,0]+sqrt(V.r[k])*tm,w[k,0]+sqrt(V.r[k])*t],[w[k,1]+sqrt(V.r[k]-V.r[k]*tm**2),w[k,1]+sqrt(V.r[k]-V.r[k]*t**2)],[START+0.1,START+0.1],'--k',zorder=100,alpha=0.5)
	            ax.plot([w[k,0]+sqrt(V.r[k])*tm,w[k,0]+sqrt(V.r[k])*t],[w[k,1]-sqrt(V.r[k]-V.r[k]*tm**2),w[k,1]-sqrt(V.r[k]-V.r[k]*t**2)],[(w[k,0]+sqrt(V.r[k])*tm)**2+(w[k,1]-sqrt(V.r[k]-V.r[k]*tm**2))**2+START+offset,(w[k,0]+sqrt(V.r[k])*t)**2+(w[k,1]-sqrt(V.r[k]-V.r[k]*t**2))**2+START+offset],'--k',zorder=100,alpha=0.8)
	            ax.plot([w[k,0]+sqrt(V.r[k])*tm,w[k,0]+sqrt(V.r[k])*t],[w[k,1]+sqrt(V.r[k]-V.r[k]*tm**2),w[k,1]+sqrt(V.r[k]-V.r[k]*t**2)],[(w[k,0]+sqrt(V.r[k])*tm)**2+(w[k,1]+sqrt(V.r[k]-V.r[k]*tm**2))**2+START+offset,(w[k,0]+sqrt(V.r[k])*t)**2+(w[k,1]+sqrt(V.r[k]-V.r[k]*t**2))**2+START+offset],'--k',zorder=100,alpha=0.8)
	
	# PLOT THE PARABOLOID BOUNDARY
	H = stack([V.hyperplanes[k].project(space.X).reshape((N,N)) for k in xrange(K)],axis=0).max(0)+START+offset
	ax.plot_surface(space.x,space.y,H,facecolors=cm.RdYlGn(C),alpha=0.4,rstride=1, cstride=1)
	
	# PLOT THE POLYGON
	x_ = copy(space.x)
	y_ = copy(space.y)
	z_ = copy(H)
	x_ = concatenate([x_,x_[:,::-1],x_[:,0].reshape((-1,1))],axis=1)
	x_ = concatenate([x_[0].reshape((1,-1)),x_,x_[0].reshape((1,-1))],axis=0)
	#x_ = concatenate([x_[0].reshape((1,-1)),x_,x_,x_[-1].reshape((1,-1))],axis=0)
	y_ = concatenate([y_,y_,y_[:,0].reshape((-1,1))],axis=1)
	y_ = concatenate([y_[0].reshape((1,-1)),y_,y_[-1].reshape((1,-1))],axis=0)
	#y_ = concatenate([y_[0].reshape((1,-1)),y_,y_[::-1],y_[-1].reshape((1,-1))],axis=0)
	z_ = concatenate([z_,z_*0+z_.max()+0.5,z_[:,0].reshape((-1,1))],axis=1)
	z_ = concatenate([z_[0].reshape((1,-1))*0+z_.max(),z_,z_[0].reshape((1,-1))*0+z_.max()],axis=0)
	#z_ = concatenate([z_[0].reshape((1,-1))*0+z_.max(),z_,z_*0+z_.max(),z_[0].reshape((1,-1))*0+z_.max()],axis=0)
	ax.plot_wireframe(x_,y_,z_,color='blue',alpha=0.1,rstride=80, cstride=80)
	ax.plot_surface(x_,y_,z_,color='royalblue',alpha=0.1,rstride=20, cstride=20)
	ax.plot([MIN,MIN],[MIN,MAX],[z_.max(),z_.max()],color='blue',alpha=0.25)
	ax.plot([MAX,MAX],[MIN,MIN],[H[0,-1],z_.max()],color='blue',alpha=0.25)
	
	ax.set_zlim(-0.5,6)
	ax.grid(False)
	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_zticks([])
	axis('off')
	tight_layout()
	ax.view_init(elev=18., azim=145)
	ax.dist = 11.5
	if(name is not None):
		savefig(name)




def plot3(w,b,name='noname.png'):
        K = len(w)
        V = Voronoi(w,b)
        C = V.cluster(space.X).reshape((N,N))
        C/=C.max()
        #PLOT THE VQ
        imshow(C,aspect='auto',interpolation='nearest',cmap='RdYlGn',extent=[MIN,MAX,MIN,MAX])#,levels = levels*0.000001,cmap='Greys')
#        for k in range(K):
#            ax.plot([w[k,0]],[w[k,1]],'ok',ms=6)
#            if(V.r[k]>0):
#                theta = linspace(-1,1,100)
#                for tm,t in zip(theta[:-1],theta[1:]):
#                    ax.plot([w[k,0]+sqrt(V.r[k])*tm,w[k,0]+sqrt(V.r[k])*t],[w[k,1]-sqrt(V.r[k]-V.r[k]*tm**2),w[k,1]-sqrt(V.r[k]-V.r[k]*t**2)],'--k',alpha=0.5)
#                    ax.plot([w[k,0]+sqrt(V.r[k])*tm,w[k,0]+sqrt(V.r[k])*t],[w[k,1]+sqrt(V.r[k]-V.r[k]*tm**2),w[k,1]+sqrt(V.r[k]-V.r[k]*t**2)],'--k',alpha=0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        tight_layout()
        if(name is not None):
                savefig(name)


def find_closest(a,b):
	index = [0,0]
	dist  = sum((a[0]-b[0])**2)
	for i in xrange(len(a)):
		for j in xrange(len(b)):
			if sum((a[i]-b[j])**2)<dist:
				index=[i,j]
				dist = sum((a[i]-b[j])**2)
	return index,a[index[0]]

def plotPD(w,b,name='noname.png',DO=True):
        K = len(w)
        V = Voronoi(w,b)
        C = V.cluster(space.X).reshape((N,N))
        C/=C.max()
        #PLOT THE VQ
        Q = array([0.8,-0.8])
        imshow(flipud(C),aspect='auto',interpolation='nearest',cmap='RdYlGn',extent=[MIN,MAX,MIN,MAX])#,levels = levels*0.000001,cmap='Greys')
	CIRCLE_POINTS = []
        for k in range(K):
	    if(DO):
                plot([w[k,0]],[w[k,1]],'ok',ms=6)
	    else:
                plot([w[k,0]],[w[k,1]],'ok',ms=4)
            if(V.r[k]>0):
                theta  = linspace(-1,1,400)
                POINTS = []
                for t in theta:
                    POINTS.append([sqrt(V.r[k])*t,sqrt(V.r[k]-V.r[k]*t**2)])
                POINTS = asarray(POINTS)
                POINTS = concatenate([POINTS,flipud(POINTS[1:]),array([POINTS[0,0],POINTS[0,1]]).reshape((1,-1))],0)
                POINTS[400:,1]*=-1
                POINTS+= w[k].reshape((1,-1))
		CIRCLE_POINTS.append(copy(POINTS[argsort(POINTS[:,0])]))
                for a,ab in zip(POINTS[:-1],POINTS[1:]):
                    plot([a[0],ab[0]],[a[1],ab[1]],'k',alpha=0.8)
	    if(DO):
                DISTANCES = ((POINTS-Q.reshape((1,-1)))**2).sum(1)
                print shape(w),shape(b)
                POSI = argsort((DISTANCES-((w[k]-Q)**2).sum()+b[k])**2)
                plot([POINTS[POSI[0],0],Q[0]],[POINTS[POSI[0],1],Q[1]],color='k',linestyle='solid')
                plot([POINTS[POSI[1],0],Q[0]],[POINTS[POSI[1],1],Q[1]],color='k',linestyle='solid')
                plot([POINTS[POSI[2],0],Q[0]],[POINTS[POSI[2],1],Q[1]],color='k',linestyle='solid')
                #
                plot([w[k,0],Q[0]],[w[k,1],Q[1]],color='k',linestyle='dotted')
                #
                plot([POINTS[POSI[0],0],w[k,0]],[POINTS[POSI[0],1],w[k,1]],color='k',linestyle='dashed')
                plot([POINTS[POSI[1],0],w[k,0]],[POINTS[POSI[1],1],w[k,1]],color='k',linestyle='dashed')
                plot([POINTS[POSI[2],0],w[k,0]],[POINTS[POSI[2],1],w[k,1]],color='k',linestyle='dashed')
        xticks([])
        yticks([])
	if(DO):
            plot([Q[0]],[Q[1]],'xb',ms=14)
            plot([Q[0]],[Q[1]],'ob',ms=6)
	else:
	    for i in xrange(K):
		for j in xrange(i+1,K):
		    INDEX1,CLOSEST1 = find_closest(CIRCLE_POINTS[i],CIRCLE_POINTS[j])
		    CIRCLE_POINTS[i][INDEX1[0]]+=100
                    INDEX2,CLOSEST2 = find_closest(CIRCLE_POINTS[i],CIRCLE_POINTS[j])
		    CIRCLE_POINTS[i][INDEX1[0]]-=100
		    director = (CLOSEST1[1]-CLOSEST2[1])/(CLOSEST1[0]-CLOSEST2[0]+0.0000000000000000001)
		    bias     = CLOSEST1[1]-CLOSEST1[0]*director
		    print director,bias,CLOSEST1,CLOSEST2
	            plot([MIN,MAX],[MIN*director+bias,MAX*director+bias],color='r',linestyle='dotted',ms=6,lw=4)
	ylim([MIN,MAX])
        tight_layout()
        if(name is not None):
                savefig(name)






N        = 300
K        = 3
MIN,MAX  = -2.,2.
DISTANCE = MAX-MIN
START    = -3.1
offset   = 2.6
space    = Space(MIN,MAX,MIN,MAX,N)
w        = array([[-0.45,-0.6],[0.2,0.1],[0.3,0.5],[-0.2,-0.1],[0.8,0.4]])#array([[-1,1],[1,1],[-1,-1],[0,0]])
K        = len(w)

# WITH BIAS
#figure(figsize=(10,12))#,dpi=20)
#ax = subplot(111,projection='3d')
#plot(w,array([0.1,0.05,0.3,0.2,0.3]),'VQ_bias.png')
#close()

# WITHOUT BIAS
#figure(figsize=(10,12))#,dpi=20)
#ax = subplot(111,projection='3d')
#plot(w,zeros(K),'VQ_nobias.png')
#close()

# ZERO BIAS
#figure(figsize=(10,12))#,dpi=20)
#ax = subplot(111,projection='3d')
#plot(w,(w**2).sum(1),'VQ_zerobias.png')
#close()



# NEURONS AND LAYER RANDOM
MIN,MAX  = -3.5,3.5
DISTANCE = MAX-MIN
offset   = 3.5
space    = Space(MIN,MAX,MIN,MAX,N)

seed(5)
W = randn(3,3,2)/3
B = rand(3,3)/5

####################################################################################
# PLOT FOR NEURON AND LAYER WITH THE THREE THINGS
WW = []
BB = []
for a in xrange(3):
	for b in xrange(3):
		for c in xrange(3):
			WW.append(W[0,a]+W[1,b]+W[2,c])
                        BB.append(B[0,a]+B[1,b]+B[2,c]-2*sum(W[0,a]*W[1,b])-2*sum(W[0,a]*W[2,c])-2*sum(W[1,b]*W[2,c]))

WW = asarray(WW)
BB = asarray(BB)


#figure(figsize=(30,12))#,dpi=20)
#ax = subplot(131,projection='3d')
#plot2(W[0],B[0],None)
#ax = subplot(132,projection='3d')
#plot2(W[1],B[1],None)
#ax = subplot(133,projection='3d')
#plot2(W[2],B[2],'VQ_neurons.png')
#close()


#figure(figsize=(10,8))#,dpi=20)
#ax = subplot(111,projection='3d')
#plot2(WW,BB,'VQ_layer.png')

###############################################################################################################
# NEURONS AND LAYER FOR ABS
W = W[:,:2]
W[:,0]=-W[:,1]
B = B[:,:2]
B[:,0]=-B[:,1]
WW = []
BB = []
for a in xrange(2):
        for b in xrange(2):
                for c in xrange(2):
                        WW.append(W[0,a]+W[1,b]+W[2,c])
                        BB.append(B[0,a]+B[1,b]+B[2,c]-2*sum(W[0,a]*W[1,b])-2*sum(W[0,a]*W[2,c])-2*sum(W[1,b]*W[2,c]))

WW = asarray(WW)
BB = asarray(BB)

#figure(figsize=(30,12))#,dpi=20)
#ax = subplot(131,projection='3d')
#plot2(W[0],B[0],None)
#ax = subplot(132,projection='3d')
#plot2(W[1],B[1],None)
#ax = subplot(133,projection='3d')
#plot2(W[2],B[2],'VQ_neurons_abs.png')
#close()

#figure(figsize=(10,8))#,dpi=20)
#ax = subplot(111,projection='3d')
#plot2(WW,BB,'VQ_layer_abs.png')



###############################################################################################################
# NEURONS AND LAYER FOR RELU
W[:,0]=0.*W[:,1]
B[:,0]=0.*B[:,1]
WW = []
BB = []
for a in xrange(2):
        for b in xrange(2):
                for c in xrange(2):
                        WW.append(W[0,a]+W[1,b]+W[2,c])
                        BB.append(B[0,a]+B[1,b]+B[2,c]-2*sum(W[0,a]*W[1,b])-2*sum(W[0,a]*W[2,c])-2*sum(W[1,b]*W[2,c]))

WW = asarray(WW)
BB = asarray(BB)
#
#figure(figsize=(30,12))#,dpi=20)
#ax = subplot(131,projection='3d')
#plot2(W[0],B[0],None)
#ax = subplot(132,projection='3d')
#plot2(W[1],B[1],None)
#ax = subplot(133,projection='3d')
#plot2(W[2],B[2],'VQ_neurons_relu.png')
#close()

#figure(figsize=(10,8))#,dpi=20)
#ax = subplot(111,projection='3d')
#plot2(WW,BB,'VQ_layer_relu.png')





################################################################################################
# PLOT IN 2D OF THE REGIONS FOR DIFFERENT WEIGHTS CONSTRAINTS

seed(18)
W = randn(3,3,2)/3
B = rand(3,3)/5
W[:,0]=0.*W[:,1]
B[:,0]=0.*B[:,1]

W[[0,1,2],[1,1,1],[0,1,0]]=W[[0,1,2],[1,1,1],[1,0,1]]*array([1,-1,-1])
WW = []
BB = []
for a in xrange(2):
        for b in xrange(2):
                for c in xrange(2):
                        WW.append(W[0,a]+W[1,b]+W[2,c])
                        BB.append(B[0,a]+B[1,b]+B[2,c]-2*sum(W[0,a]*W[1,b])-2*sum(W[0,a]*W[2,c])-2*sum(W[1,b]*W[2,c]))

WW = asarray(WW)
BB = asarray(BB)

#figure(figsize=(4,4))#,dpi=20)
#ax = subplot(111)
#plot3(WW,BB,'VQ_layer_diag.png')
#close()


seed(100)
W = randn(3,3,2)/3
B = rand(3,3)/3
W[:,0]=0.*W[:,1]
B[:,0]=0.*B[:,1]

W[[0,1,2],[1,1,1],[0,1,0]]=0
WW = []
BB = []
for a in xrange(2):
        for b in xrange(2):
                for c in xrange(2):
                        WW.append(W[0,a]+W[1,b]+W[2,c])
                        BB.append(B[0,a]+B[1,b]+B[2,c]-2*sum(W[0,a]*W[1,b])-2*sum(W[0,a]*W[2,c])-2*sum(W[1,b]*W[2,c]))

WW = asarray(WW)
BB = asarray(BB)

#figure(figsize=(4,4))#,dpi=20)
#ax = subplot(111)
#plot3(WW,BB,'VQ_layer_parallel.png')
#close()


seed(100)
W = randn(3,3,2)/3
B = rand(3,3)/3
W[:,0]=0.*W[:,1]
B[:,0]=0.*B[:,1]

WW = []
BB = []
for a in xrange(2):
        for b in xrange(2):
                for c in xrange(2):
                        WW.append(W[0,a]+W[1,b]+W[2,c])
                        BB.append(B[0,a]+B[1,b]+B[2,c]-2*sum(W[0,a]*W[1,b])-2*sum(W[0,a]*W[2,c])-2*sum(W[1,b]*W[2,c]))

WW = asarray(WW)
BB = asarray(BB)

#figure(figsize=(4,4))#,dpi=20)
#ax = subplot(111)
#plot3(WW,BB,'VQ_layer_random.png')
#close()






#####################################################
# PLOT POWER DIAGRAM
W = array([[-1.8,-1.8],[1.2,1.2],[-1.5,1.2]])/2#randn(3,2)*1.3
B = 0.1+rand(3)/3
B[0]*=2.2

figure(figsize=(4,4))#,dpi=20)
plotPD(W,B,'PD_random_1.png')
close()


B+=1.1
figure(figsize=(4,4))#,dpi=20)
plotPD(W,B,'PD_random_2.png',DO=False)
close()



