#-*- using:utf-8 -*-
import os
import time
import cv2

def capture(camids,fps=30,fourcc=cv2.VideoWriter_fourcc(*'XVID'),fext='.avi',path='../capture',novout=False):
    fint=1/fps
    cams={}
    vouts={}

    try:
        os.makedirs(path, exist_ok=True)

        f=open(path+'/timestamp.txt','w')

        if not hasattr(camids, '__iter__'):
            camids=[camids]
        else:
            camids=sorted(set(camids), key=camids.index)

        prep=True
        for camid in camids:
            if prep==False:
                break
            cams[camid]=cv2.VideoCapture(camid)
            prep=prep and cams[camid].isOpened()
            if prep:
                #TEMPERATURE=(cams[camid].get(cv2.CAP_PROP_TEMPERATURE))
                #print('Camera '+str(camid)+': TEMPERATURE='+str(TEMPERATURE))

                width=int(cams[camid].get(cv2.CAP_PROP_FRAME_WIDTH))
                height=int(cams[camid].get(cv2.CAP_PROP_FRAME_HEIGHT))
                if width==0 or height==0:
                    print('Camera '+str(camid)+': successfully opened but dimensions of frame are inappropriate')
                    prep=False
                print('Camera '+str(camid)+': dimensions='+str(width)+','+str(height))

                if not novout:
                    vouts[camid]=cv2.VideoWriter(path+'/Camera'+format(camid,'02d')+fext,fourcc,fps,(width,height))
                    prep=prep and vouts[camid].isOpened()

        while prep:
            start=time.time()
            for camid,cam in cams.items():
                ret=cam.grab()
            f.write(str(time.time())+"\n")
            for camid,cam in cams.items():
                ret,img=cam.retrieve()
                if ret==True:
                    if not novout:
                        vouts[camid].write(img)
                    cv2.imshow('Camera '+str(camid),img)
            elapsed=time.time()-start
            waittime=int((fint-elapsed)*1000)
            if waittime<1:
                waittime=1
            k=cv2.waitKey(waittime)
            if k==ord('q'):
                break

    finally:
        cv2.destroyAllWindows() 
        for cam in cams.values():
            cam.release()
        if not novout:
            for vout in vouts.values():
                vout.release()
        f.close()

if __name__=='__main__':
    cv_major_ver=int(cv2.__version__.split('.')[0])
    print('opencv: ver='+str(cv2.__version__))
    capture([0,1],novout=True)