import os
import sys
# os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
#os.environ["KIVY_NO_CONSOLELOG"] = "1"

from video_downloader import VideoDownlaoder as vd
from video_downloader import resource_path2
from threading import Thread
from kivy.clock import Clock
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.core.text import LabelBase

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.icon_definitions import md_icons

Window.size=[350,600]

output = open(resource_path2("output.txt"), "wt")
sys.stdout = output
sys.stderr = output

w_flag=False
path_to_download=None
from urllib.parse import urlparse


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        r=relative_path.split("\\")[1]
        base_path = sys._MEIPASS
        return os.path.join(base_path, r)
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

LabelBase.register(name='audiowide', fn_regular=resource_path('assets\\Audiowide-Regular.ttf'))

class UrlVaidation:
    def is_valid_url(self,url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except AttributeError:
            return False
    
    def data_validation(self,url,path):
        if url=="" and path is None:
            toast("Please Specify URL And Path",
                  background=get_color_from_hex("#B03C3F"),
                  duration=1.5)
            return False

        
        elif url =="" or not self.is_valid_url(url):
            toast("Please Enter a Valid URL",
                  background=get_color_from_hex("#B03C3F"),
                  duration=1.5)
            return False

        elif path is None:
                toast("Please Choose A Path",
                  background=get_color_from_hex("#B03C3F"),
                  duration=1.5)
                return False
                
        else:
            return True
                

class LoadingPopup(Popup):
    def __init__(self, **kwargs):
        super(LoadingPopup, self).__init__(**kwargs)
        b=BoxLayout(orientation= 'vertical',padding=[20,20,20,20])    
        self.add_widget(b)
        self.auto_dissmissed=False
        b.add_widget(Image(  source=resource_path("assets\\pp.gif"),
                              size_hint = (.7, .9),
                              pos_hint={'center_x': 0.5,'center_y': 0.5}
                              ))


        
        # b.add_widget(Label(text='Loading, please wait...',
        #                       font_family="audiowide",
        #                       font_size=20,
        #                       bold=True,
        #                       size_hint = (.7, .9),
        #                       pos_hint={'center_x': 0.5,'center_y': 0.5}
        #                       ))
        # b.add_widget(Button(text='Cancel', 
        #                        on_release=self.dismiss,
        #                        size_hint = (.7, .9),
        #                        pos_hint={'center_x': 0.5,'center_y': 0.3}
        #                        ))


class TestScreen(Screen):
    pass


class WelcomeScreen(Screen):
    pass

class HomeScreen(Screen):

    def open_file_chooser_popup(self):
        file_chooser = FileChooserListView(dirselect=True)
        file_chooser.path = os.getcwd() 
        if platform=="android":
            file_chooser.path = "/storage/emulated/0/"
        file_chooser.filters=["! *.*"]
        popup = Popup(title='Select A Directory', content=file_chooser, size_hint=(0.9, 0.9))



        def print_directories(*args):
            selected_dir = str(file_chooser.selection[0])
            #print(selected_dir)
            global path_to_download
            path_to_download=selected_dir
            popup.dismiss()

        file_chooser.bind(selection=print_directories)
        popup.open()

    
class DownloadScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass




class MainApp(MDApp):
    def build(self):
        self.title="HVID Downloader"
        self.icon=resource_path("assets\\hv.png")
        global screen_manager
        screen_manager=WindowManager()
        screen_manager.add_widget(Builder.load_file(resource_path("kv\\welcome.kv")))
        screen_manager.add_widget(Builder.load_file(resource_path("kv\\home.kv")))
        screen_manager.add_widget(Builder.load_file(resource_path("kv\\download.kv")))
        return screen_manager
    
    def on_start(self):
        screen_manager.transition=FadeTransition(duration=1)
        Clock.schedule_once(self.get_home_screen,7)

    def get_home_screen(self,*args):
        screen_manager.get_screen("home").url.text=""
        global path_to_download
        path_to_download=None
        screen_manager.current = "home"
    
    def download_file(self,instance):
        pop=LoadingPopup(size_hint = (.9, .9))
        pop.title="Loading...."
        # Clock.schedule_once(pop.open,1)
        qualities={"HD Quality (.MP4)":1,
                "Low Quality (.MP4)":0,
                "Audio (.MP3)":4}

        res=qualities[instance.text]
        global path_to_download
        url=screen_manager.get_screen("home").url.text

        pop.open()
        downloader=vd(url=url,path=path_to_download)
        try:
            t=Thread(target=downloader.downloadVid,args=(res,pop,))
            t.start()
        except Exception as e:
            print("error!")

        
        


        


    def get_downlod_screen(self): 
        url=screen_manager.get_screen("home").url.text
        global path_to_download
        validation=UrlVaidation().data_validation(url,path_to_download)

        if validation:
            screen_manager.current='download'


                


    def get_dir(self):
        screen_manager.get_screen("home").open_file_chooser_popup()


    def animate_background(self, widget):
        global w_flag
        if w_flag==False:
            anim = Animation(size_hint_y=1) + Animation(size_hint_y=0.5)
            anim.start(widget.ids.bx)
      
    def animate_card(self, widget):
        global w_flag
        if w_flag==False:
            anim = Animation(pos_hint={"center_x": 0.5, "center_y": 0.6}, duration=2)
            anim.start(widget)
            w_flag=True
        
    def get_list(self):
        return ["HD Quality (.MP4)","Low Quality (.MP4)","Audio (.MP3)"]
    
    def exit_app(self):
        toast("Thanks For Using The APP",
                  background=get_color_from_hex("#000000"),
                  duration=3)
        
        Clock.schedule_once(self.stop,4)

    def get_asset(self,n):
        a= {
           0: resource_path("assets\\pp.gif"),
           1: resource_path("assets\\qq.gif"),
           2: resource_path("assets\\h.png")
           }
       
        return a[n]


    
        
     
            



       
        
            
            

if __name__ == '__main__':
    app = MainApp()
    app.run()
    output.close()