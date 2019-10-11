from urllib import request
import urllib.request
import os
import math
import cv2
import numpy as np

agents = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1']
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)#根据坐标计算行列号
def getimg(Tpath, Spath, x, y):
    a = 0
    for a in range(0, 7):
        try:
            f = open(Spath, 'wb')
            req = urllib.request.Request(Tpath)
            req.add_header('User-Agent', agents[a])  #  请求头循环8次
            pic = urllib.request.urlopen(req, timeout=60)
            f.write(pic.read())
            f.close()
            print(str(x) + '_' + str(y) + 'downloading success')
            break
        except Exception:
            print(str(x) + '_' + str(y) + 'downloading fail,retrying')
            print('retrying' + str(a + 1))
            continue

def pinjie(save_path, dir2,n,dir3):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    filenames = os.listdir(dir3)
    for filename in filenames:
        try:
            if not os.path.exists(save_path + filename):
                a = int(filename.find('_'))
                e = int(filename.find('.'))
                x = int(filename[0:a])
                y = int(filename[a+1:e])
                x = x*n
                y = y*n
                imrow = []
                for a in range(0,n):
                    imcolumn = []
                    for e in range(0,n):
                        print(dir2 + '/' +str(x+a) + '_'+ str(y+e)+ '.png')
                        im = cv2.imread(dir2 +'/'+ str(x+a) + '_'+ str(y+e)+ '.png')
                    #print (dir2 + str(x+a) + '_'+ str(y+b)+ '.png', im.shape)
                        imcolumn.append(im)
                    imstripe = np.vstack(imcolumn)
                    imrow.append(imstripe)
                imwhole = np.hstack(imrow)
                cv2.imwrite(save_path + filename, imwhole)#高分辨率地图合成对应的低分辨率地图
        except Exception:
            continue

if __name__ == "__main__":
    path = input('pls input save path')
    zooml_list = eval('['+input('pls input raw data zoom')+']')
    zoomh_list = eval('['+input('pls input aligned zoom')+']')
    location = input('pls input location')
    lat_deg1 = float(input('pls input lat_deg of lefttop'))
    lon_deg1 = float(input('pls input lon_deg of lefttop'))
    lat_deg2 = float(input('pls input lat_deg of rightbottom'))
    lon_deg2 = float(input('pls input lon_deg of rightbottom'))
    path1=path + '/' + location
    if not os.path.exists(path1):
        os.mkdir(path1)
    coordinatefile = open(path1 + '/' + 'coordinate.txt', 'w')
    coordinatefile.write('lefttop lat_deg:' + str(lat_deg1) + ' lon_deg:' + str(lon_deg1) +'\n' + 'rightbottome lat_deg:'+str(lat_deg2)+' lon_deg:' + str(lon_deg2))
    coordinatefile.close()#记录左上角和右下角坐标值
    imagetypelist = ('streetmap', 'sateliteimage')#, 'osmvector')

    for zooml in zooml_list:
        path2=path1 + '/' + location + str(zooml)
        if not os.path.exists(path2):
            os.mkdir(path2)
        for it in imagetypelist:
            path3 = path2 + '/' + it + str(zooml)
            if not os.path.exists(path3):
                os.mkdir(path3)
            path4 = path3 + '/' + it + str(zooml)
            if not os.path.exists(path4):
                os.mkdir(path4)
            lefttop = deg2num(lat_deg1, lon_deg1, zooml)
            rightbottom = deg2num(lat_deg2, lon_deg2, zooml)

            print(str(lefttop[0]))
            print(str(rightbottom[0]))
            print(str(lefttop[1]))
            print(str(rightbottom[1]))
            print("共" + str(lefttop[0] - rightbottom[0]+1))
            print("共" + str(lefttop[1] - rightbottom[1]+1))
            for x in range(lefttop[0], rightbottom[0]+1):
                for y in range(lefttop[1], rightbottom[1]+1):
                    apidict = {
                    'streetmap': "http://mt2.google.cn/vt/lyrs=m&scale=2&hl=zh-CN&gl=cn&x=" + str(x) + "&y=" + str(
                        y) + "&z=" + str(
                        zooml) + "&apistyle=s.t:0%3A3%7Cs.e%3Al.t%7Cp.v%3Aoff%2Cs.t%3A2%7Cp.v%3Aoff%2Cs.t%3A1%7Cs.e%3Al%7Cp.v%3Aoff%2Cs.t%3A5%7Cs.e%3Al%7Cp.v%3Aoff%2Cs.e%3Al%7Cp.v%3Aoff&style=api%7Csmartmaps",
                    'sateliteimage': "http://mt2.google.cn/vt/lyrs=s&scale=2&hl=zh-CN&gl=cn&x=" + str(x) + "&y=" + str(
                        y) + "&z=" + str(zooml)}#'osmvector': osmapi}

                    file = os.path.join(path4, str(x) + "_" + str(y) + ".png")
                    if os.access(file, os.F_OK) == True:
                        print ( str(file) + 'has been downloaded')
                        continue
                    else:
                        tilepath = apidict[it]
                        getimg(tilepath,file, x, y)
                        try:
                            im = cv2.imread(file)
                            conf_value=im.shape
                            continue
                        except Exception:
                            os.remove(file)
                            getimg(tilepath,file,x,y)

            for zoomh in zoomh_list:
                path5 = path1 + '/' + location + str(zoomh)
                if not os.path.exists(path5):
                    os.mkdir(path5)
                path6 = path5+'/'+it+str(zoomh)
                if not os.path.exists(path6):
                    os.mkdir(path6)
                path7 = path6+'/'+it+str(zoomh)
                if not os.path.exists(path7):
                    os.mkdir(path7)
                filenames = os.listdir(path4)
                for filename in filenames:
                    c = filename.find('_')
                    d = filename.find('.')
                    x = int(filename[0:c])
                    y = int(filename[c + 1:d])
                    t = 2 ** (int(zoomh) - int(zooml))
                    x = x * t
                    y = y * t
                    for b in range(0,t):
                        for a in range(0,t):
                            apidict = {'streetmap': "http://mt2.google.cn/vt/lyrs=m&scale=2&hl=zh-CN&gl=cn&x=" + str(
                                x + a) + "&y=" + str(y + b) + "&z=" + str(
                                zoomh) + "&apistyle=s.t:0%3A3%7Cs.e%3Al.t%7Cp.v%3Aoff%2Cs.t%3A2%7Cp.v%3Aoff%2Cs.t%3A1%7Cs.e%3Al%7Cp.v%3Aoff%2Cs.t%3A5%7Cs.e%3Al%7Cp.v%3Aoff%2Cs.e%3Al%7Cp.v%3Aoff&style=api%7Csmartmaps",
                                       'sateliteimage': "http://mt2.google.cn/vt/lyrs=s&scale=2&hl=zh-CN&gl=cn&x=" + str(
                                           x + a) + "&y=" + str(y + b) + "&z=" + str(zoomh)}  # 'osmvector': osmapi}
                            file = os.path.join(path7, str(x + a) + "_" + str(y + b) + ".png")
                            if os.access(file, os.F_OK) == True:
                                print(str(file) + 'has been downloaded')
                                continue
                            else:
                                tilepath = apidict[it]
                                getimg(tilepath, file, x + a, y + b)
                                try:
                                    im = cv2.imread(file)
                                    conf_value = im.shape
                                    continue
                                except Exception:
                                    os.remove(file)
                                    getimg(tilepath, file, x+a, y+b)#根据低zoom瓦片的文件名下载高zoom瓦片
                if int(zooml) >= int(zoomh):
                    continue
                else:
                    n = 2 ** (int(zoomh) - int(zooml))
                    save_path = os.path.join(path3, it + str(zoomh)+'_'+str(zooml)+'_'+'aligned/')
                    pinjie(save_path,path7,n,path4)


    print ('mission completed')
