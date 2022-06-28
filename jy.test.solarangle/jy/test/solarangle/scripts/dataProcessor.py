import json
from urllib.request import urlopen,quote
import omni.ext
import omni.ui as ui
import math
import omni.usd
import omni.kit.commands
from pxr import Usd, Gf, Tf, Trace

class dataProcessor:
    def __init__(self, stage):   
        self.stage = stage

    def getDistantLight(self):
        stage=self.stage
        for p in stage.Traverse():
            if p.GetTypeName()=='DistantLight':
                return p

    def getLightAngles(self,y1,m1,d1,h1,mi1,s1,lon1,la1,TimeZ1):
            y=y1.as_int
            m=m1.as_int
            d=d1.as_int
            h=h1.as_int
            mi=mi1.as_int
            s=s1.as_int
            lon=lon1.as_float
            la=la1.as_float
            TimeZ=TimeZ1.as_int
            #儒略日 Julian day(由通用时转换到儒略日)conda create -n superset python=3.6
            JD0 = int(365.25*(y-1))+int(30.6001*(1+13))+1+h/24+1720981.5
            if m<=2:
                JD2 = int(365.25*(y-1))+int(30.6001*(m+13))+d+h/24+1720981.5
            else:
                JD2 = int(365.25*y)+int(30.6001*(m+1))+d+h/24+1720981.5
            #年积日 Day of year
            DOY = JD2-JD0+1
            N0 = 79.6764 + 0.2422*(y-1985) - int((y-1985)/4.0)
            sitar = 2*math.pi*(DOY-N0)/365.2422
            ED1 = 0.3723 + 23.2567*math.sin(sitar) + 0.1149*math.sin(2*sitar) - 0.1712*math.sin(3*sitar)- 0.758*math.cos(sitar) + 0.3656*math.cos(2*sitar) + 0.0201*math.cos(3*sitar)
            ED = ED1*math.pi/180           #ED本身有符号
            if lon >= 0:
                if TimeZ == -13:
                    dLon = lon - (math.floor((lon*10-75)/150)+1)*15.0
                else:
                    dLon = lon - TimeZ*15.0   #地球上某一点与其所在时区中心的经度差
            else:
                if TimeZ== -13:
                    dLon =  (math.floor((lon*10-75)/150)+1)*15.0- lon
                else:
                    dLon =  TimeZ*15.0- lon
            #时差
            Et = 0.0028 - 1.9857*math.sin(sitar) + 9.9059*math.sin(2*sitar) - 7.0924*math.cos(sitar)- 0.6882*math.cos(2*sitar)
            gtdt1 = h + mi/60.0 + s/3600.0 + dLon/15        #地方时
            gtdt = gtdt1 + Et/60.0
            dTimeAngle1 = 15.0*(gtdt-12)
            dTimeAngle = dTimeAngle1*math.pi/180
            latitudeArc = la*math.pi/180
            HeightAngleArc = math.asin(math.sin(latitudeArc)*math.sin(ED)+math.cos(latitudeArc)*math.cos(ED)*math.cos(dTimeAngle))
            CosAzimuthAngle = (math.sin(HeightAngleArc)*math.sin(latitudeArc)-math.sin(ED))/math.cos(HeightAngleArc)/math.cos(latitudeArc)
            AzimuthAngleArc = math.acos(CosAzimuthAngle)
            HeightAngle = HeightAngleArc*180/math.pi
            AzimuthAngle1 = AzimuthAngleArc *180 /math.pi
            if dTimeAngle < 0:
                AzimuthAngle = 180 - AzimuthAngle1
            else:
                AzimuthAngle = 180 + AzimuthAngle1
            return[HeightAngle,AzimuthAngle]

    def setSolarangles(self,y1,m1,d1,h1,mi1,s1,lon1,la1,TimeZ1):
            angles=self.getLightAngles(y1,m1,d1,h1,mi1,s1,lon1,la1,TimeZ1)
            HeightAngle=angles[0]
            AzimuthAngle=angles[1]
            light=self.getDistantLight()
            if light.GetAttribute('xformOp:rotateXYZ').IsValid():
                light.GetAttribute('xformOp:rotateXYZ').Set(Gf.Vec3f(AzimuthAngle,150,HeightAngle))
            elif light.GetAttribute('xformOp:rotateXZY').IsValid():
                light.GetAttribute('xformOp:rotateXZY').Set(Gf.Vec3f(AzimuthAngle,HeightAngle,150))
            elif light.GetAttribute('xformOp:rotateYZX').IsValid():
                light.GetAttribute('xformOp:rotateYZX').Set(Gf.Vec3f(AzimuthAngle,HeightAngle,150))
            elif light.GetAttribute('xformOp:rotateYXZ').IsValid():
                light.GetAttribute('xformOp:rotateYXZ').Set(Gf.Vec3f(150,AzimuthAngle,HeightAngle))
            elif light.GetAttribute('xformOp:rotateZXY').IsValid():
                light.GetAttribute('xformOp:rotateZXY').Set(Gf.Vec3f(HeightAngle,AzimuthAngle,150,))
            else :
                light.GetAttribute('xformOp:rotateZYX').Set(Gf.Vec3f(HeightAngle,AzimuthAngle,150)) 