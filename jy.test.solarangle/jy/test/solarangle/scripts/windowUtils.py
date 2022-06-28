import omni.ui as ui
from .dataProcessor import *
from .Model import *
import omni.usd
import omni.kit.commands
import carb
import carb.events

button_style={"color":0xddccffaa}

class windowUtils:
    def __init__(self,_window,stage,dataLib,context) :
        self._window=_window
        self.stage=stage
        self.dataLib=dataLib
        self.context=context
           
    def createWindow(self):
        self.change_Light_Angles_window()
       
    def change_Light_Angles_window(self):
        with ui.VStack():
            with ui.HStack(height=25):
                with ui.ZStack():
                    ui.Label("date",alignment=ui.Alignment.CENTER)
                y=ui.IntDrag(min=2022,step=1,height=0).model
                y.as_int=2022
                ui.Spacer(width=5)
                m=ui.IntDrag(min=1,max=12,step=1,height=0).model
                m.set_value(1)
                ui.Spacer(width=5)
                d=ui.IntDrag(min=1,max=31,step=1,height=0).model
                d.set_value(1)
            ui.Spacer(height=5)
            with ui.HStack(height=25):
                with ui.ZStack():
                    ui.Label("time",alignment=ui.Alignment.CENTER)
                h=ui.IntDrag(min=0,max=23,step=1).model
                ui.Spacer(width=5)
                mi=ui.IntDrag(min=0,max=59,step=1).model
                ui.Spacer(width=5)
                sec=ui.IntDrag(min=0,max=59,step=1).model
            ui.Spacer(height=5)
            with ui.HStack(height=25):
                with ui.ZStack():
                    ui.Label("longtitude",alignment=ui.Alignment.CENTER)
                lon=ui.FloatDrag(min=73,max=135,step=1).model
                with ui.ZStack():
                    ui.Label("latitude",alignment=ui.Alignment.CENTER)
                la=ui.FloatDrag(min=4.15,max=45,step=1).model
            ui.Spacer(height=5)
            with ui.HStack(height=25):
                with ui.ZStack():
                    ui.Label("TimeZone",alignment=ui.Alignment.CENTER)
                tz=ui.FloatDrag(min=1,max=24,step=1).model
              
            ui.Button("Set",height=25,clicked_fn=lambda: self.dataLib.setSolarangles(y,m,d,h,mi,sec,lon,la,tz),style=button_style)

                                                               