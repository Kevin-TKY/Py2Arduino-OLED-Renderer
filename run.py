
import cv2
import os

def to_a(n):
    d = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return d[n//26]+d[n%26]

def to_i(s):
    d = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return d.index(s[0])*26+d.index(s[1])

def utils(path):
    with open(path+'/utils.ino', 'w') as fii:
        j = [2**n for n in range(8)]
        now = 0
        t = 8
        fu = 0
        print('''void w(int x){oled.writePixel(x,y,1);}
void e(){if(x==120){y+=1;x=0;}else{x+=8;}}
''', file=fii)
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    for d in range(2):
                        for e in range(2):
                            for f in range(2):
                                for g in range(2):
                                    for h in range(2):
                                        if t!=8:
                                            print('void ',to_a(now),'(){', sep='',end='',file=fii)
                                            print('w(x','+'+str(t) if t!=0 else '',');', to_a(fu) if fu>0 else 'e','();}',sep='',file=fii)
                                        fu+=1
                                        now+=1
                                        if now in j:
                                            t-=1
                                            fu = 0

def jpeg_writer(path, img_name, brightness=0.3, resolution=None):
    '''
    Parameters
    ----------
    path : output file name
    img_name : input image name
    brightness : the higher the lighter (more white parts, 0 ~ 1)
    resolution : resolution (0 ~ 1)
    ----------
    '''
    
    if not os.path.isdir(path):
        os.makedirs(path)
    
    img_t = cv2.imread(img_name)
    
    if img_t.shape[1] > img_t.shape[0]:
        img_t = cv2.transpose(img_t)
    
    if resolution:
        img_t = cv2.resize(img_t, (int(64*resolution), int(128*resolution)))
    
    img_t = cv2.resize(img_t, (64, 128))
    
    img_t = img_t/255.0
    
    with open(os.path.join(path, path)+'.ino', 'w') as fi:
        print('''
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#include <Adafruit_BusIO_Register.h>
Adafruit_SSD1306 oled(128,64,&Wire,-1);
int x=0,y=0;
void setup(){
oled.begin(SSD1306_SWITCHCAPVCC,0x3C);
oled.clearDisplay();
oled.display();
''', end='', file=fi)
        temp = 0
        total = 0
        for n in range(64):
            for p in range(128):
                dep = (img_t[p][n][0]+img_t[p][n][1]+img_t[p][n][2]) / 3
                
                if 1 - dep < brightness:
                    total += 128//(2**temp)
                temp += 1
                if temp==8:
                    print(to_a(total) if total>0 else 'e','();',sep='',end='',file=fi)
                    temp = 0
                    total = 0
        print('''
oled.display();
}
void loop(){}
''', file=fi)
        fi.close()
    utils(path)



path = 'file_name'
img = 'img.jpg'
jpeg_writer(path, img, 0.2)
