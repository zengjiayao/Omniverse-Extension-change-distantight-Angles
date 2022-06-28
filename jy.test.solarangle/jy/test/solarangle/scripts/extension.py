import omni.ext
import omni.ui as ui
import omni.usd
import omni.kit.commands
from pxr import Usd, Gf, Tf, Trace
from .dataProcessor import *
import carb
import carb.events
from .Model import *

button_style={"color":0xddccffaa}

class MyExtension(omni.ext.IExt):

    def on_startup(self, ext_id):
        self.context = omni.usd.get_context()
        self.stage = self.context.get_stage()
        self.selection = self.context.get_selection()
        self.dataLib=dataProcessor(self.stage)
        self._window = ui.Window("Change the Light", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
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

    def on_shutdown(self):
        self._window = None 