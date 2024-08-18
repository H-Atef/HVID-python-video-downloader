
import os
#os.environ["KIVY_NO_CONSOLELOG"] = "1"
import pathlib
from pytubefix import YouTube
import wget
import requests
import moviepy.editor as mp
import chromedriver_autoinstaller




import datetime


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from datetime import datetime



from kivy.utils import get_color_from_hex
from kivy.clock import mainthread
from kivymd.toast.kivytoast.kivytoast import toast
import sys



def resource_path2(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        return os.path.join(base_path, relative_path)
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)



# PATH=str(pathlib.Path(__file__).parent.resolve())+"\\YT_Downloads\\"
# PATH2=str(pathlib.Path(__file__).parent.resolve())+"\\ANY_Downloads\\"
# LINK="https://youtube.com/shorts/akL53YfPTfI?si=ju1ohfkBdFSInLNj"
# LINK2="https://assets.mixkit.co/videos/preview/mixkit-siamese-cat-inside-a-hat-4103-large.mp4"






class DriverInit:
    def initialize_driver(self,driver="firefox"):
        if driver.lower()=="firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")
            # options.add_argument('--no-proxy-server')
            # options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--disable-gpu')
            # options.add_argument('log-level=3')
            driver = webdriver.Firefox(options=options)
            return driver
        
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 
                            'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
            chrome_options.add_experimental_option('prefs', prefs)
            #chrome_options.add_experimental_option('androidPackage', 'com.android.chrome')
            chrome_options.add_argument('--no-proxy-server')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument('log-level=3')
            driver = webdriver.Chrome(options=chrome_options)
            chromedriver_autoinstaller.install() 
            return driver
        

class DownloadMessage:
    @mainthread
    def download_state(self,f):
        if f=="warning":
            toast("Downloading Failed!",get_color_from_hex("#990F02"),3)

        elif f=="good":
            toast("Successful Process",get_color_from_hex("#00FF00"),3)

        else:
            toast("Invalid Inputs!",get_color_from_hex("#000000"),3)



        

class YouTubeDownlaoder():

    def __init__(self,link=None,path=None):
        self.link=link
        self.path=path
        


    def download(self,res,pop_up):

        global f,mp3_file_name,file_name,current_dt

        current_dt= datetime.now().strftime("%Y%m%d%H%M%S")



        if res==4:
            mp3_file_name= str(self.path)+'\\aud'+str(current_dt)+'.mp3' 

        file_name = str(self.path)+'\\vid'+str(current_dt)+'.mp4' 

        if self.path is None or self.link is  None:
            print("Download Failed, please check your inputs!!!")

        
        try: 
            # object creation using YouTube 
            yt = YouTube(self.link) 
        except: 
           
            f="invalid"

            
            

        if res==4:
            

            try:
                mp3=yt.streams.filter(only_audio=True).first()
                d_file=mp3.download(output_path=self.path,filename=mp3_file_name)

                base, ext = os.path.splitext(d_file)
                new_file = base + '.mp3'
                os.rename(d_file, new_file)

                f="good"
                

            except Exception as e:
                
                f="warning"

        else:
            try:
                # Get all streams and filter for mp4 files
                mp4_streams = yt.streams.filter(file_extension='mp4',progressive=True)

                video_resolutions=sorted(list(dict.fromkeys([st.resolution for st in mp4_streams 
                                                    if st.resolution is not None])))
            
                #print(video_resolutions)
                # specified_res=int(input("Choose from available resolutions: "))
                #specified_res=0
                # get the video with specified resolution

                if res==0:
                    d_video = mp4_streams[len(video_resolutions)//2]

                elif res==1:
                    d_video=mp4_streams.order_by('resolution').desc().first()

                    

                
                    # downloading the video 
                d_video.download(output_path=self.path,filename=file_name)
                f="good"
            except: 
                #print(e)
                f="warning"
                
        pop_up.dismiss()
        DownloadMessage().download_state(f)





class UrlVidDownloader():
    def __init__(self,url=None,path=None):
        self.url=url
        self.path=path


    def download(self,res,pop_up):
        global sf,mp3_file_name,file_name
        try:
            if self.path is None or self.url is  None:
                print("Download Failed, please check your inputs!!!") 

            current_dt= datetime.now().strftime("%Y%m%d%H%M%S")

            if res==4:
                mp3_file_name= str(self.path)+'\\aud'+str(current_dt)+'.mp3' 

            file_name = str(self.path)+'\\vid'+str(current_dt)+'.mp4' 


            try:
                drv=DriverInit().initialize_driver("google")
                drv.get("https://getvideo.at/en/")
                #print(drv.title)
            except Exception as e:
                sf="invalid"
                drv.close()

            try:
                text_field=drv.find_element(By.ID,"search-text")
                text_field.send_keys(self.url)
                drv.find_element(By.ID,"search-button").click()

                lst=WebDriverWait(drv, 20).until(
                ec.presence_of_element_located((By.XPATH,
                                                '//*[@id="search-results"]/div/div/div[2]/div')))
                
                
                highest=str(len(lst.find_elements(By.TAG_NAME,"a")))
                

                if res==0 or res==4:
                    btn=drv.find_element(By.XPATH,'//*[@id="search-results"]/div/div/div[2]/div/a[1]')

                if res==1:
                    btn=drv.find_element(By.XPATH,'//*[@id="search-results"]/div/div/div[2]/div/a[{}]'.format(highest))
                    


                
                f_url=btn.get_attribute("href")
                if res==4:
                        vv=resource_path2('vid'+str(current_dt)+'.mp4')
                        wget.download(str(f_url),vv)
                        clip = mp.VideoFileClip(vv)
                        clip.audio.write_audiofile(mp3_file_name)
                        clip.close()
                        os.remove(vv)

                else:
                    wget.download(str(f_url),file_name)

                sf="good"
                drv.quit()
            except Exception as e:
                sf="warning"
                drv.close()
                
            
            pop_up.dismiss()
            DownloadMessage().download_state(sf)


        
        except Exception as e:
            sf="warning"
            #print(e)
            pop_up.dismiss()
            DownloadMessage().download_state(sf)
                    






class VideoDownlaoder():

    def __init__(self,url,path):
        self.url=url
        self.path=path
        if "yout" in url:
            self.platform=YouTubeDownlaoder(url,path)

        else:
         self.platform=UrlVidDownloader(url,path)



    def downloadVid(self,res,pop_up):
        self.platform.download(res,pop_up)


# vidD=VideoDownlaoder(LINK2)
# vidD.downloadVid(1)

# v=UrlVidDownloader(LINK3,PATH2)
# v.download(4,2)





