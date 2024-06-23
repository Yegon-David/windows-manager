import tkinter as tk
import threading
import os 
import sys
from screeninfo import get_monitors
from .components import Loader,LabelComponent,MenuComponent,MusicLabel,ScrollableFrame,Song,MusicList,Dict,TaskManager,ShadowFrame

sys.path.append('..')


import settings as s



class MainWindow(tk.Tk):
    def __init__(self,title)->None:
        super().__init__()
        monitors = get_monitors()
        self.overrideredirect(True)
        self.minsize(200,150)
        self.configure(background=s.MAIN_BG,highlightthickness=0,border=0,borderwidth=0)
        self.wm_attributes('-topmost',1)

        self.bind_all('<Button-1>',self.click_info)
        self.bind_all('<Button-3>',self.click_info2)
   
        
     

        # self.geometry(f'+{1166}+{84}')

        self.title_bar = None
        self.main_frame = None
        self.loader = None
        self.lable_title = title
        self.default_title = 'Window Mode'
        self.start_x = 0
        self.start_y = 0
        self.sidebar = None
        self.container = None
        self.clip_cont = None
        self.music_playlist = {}

        self.mode_options = ['menu','music','clipboard','security']

        self.mode = self.mode_options[self.mode_options.index('music')]
        
        self.window_check()

    def change_window_mode(self,mode:str)->None:
        self.mode = self.mode_options[self.mode_options.index(mode)]    
       
    def window_check(self):
        if len(get_monitors()) == 1 and self.winfo_x() >= 1366:
            self.geometry(f'+{100}+{100}')

        self.after(3000,self.window_check)   

    def click_info(self,e):
        # self.loading()
        pass
        
    def click_info2(self,e):
      
        # self.unloading()
        pass

    def open_option(self,option:LabelComponent):
        print('clicked',option.label.cget('text'))

    def window_mode(self) -> None:
        self.title_bar = tk.Frame(self,background=s.MAIN_BG,highlightcolor=s.DARK_GREY)
        self.title_bar.place(x=0,y=0,anchor='nw',relwidth=1,relheight=0.13)

        self.placing_title_labels(self.title_bar)
        self.title_bar.bind('<ButtonPress-1>',self.on_press)
        self.title_bar.bind('<B1-Motion>',self.on_motion)
        

        self.main_frame = tk.Frame(self,background=s.DARK_GREY,highlightcolor=s.DARK_GREY)
        self.main_frame.place(x=0,rely=0.14,anchor='nw',relwidth=1,relheight=0.86)

    def split_main_frame(self):
        self.sidebar = tk.Frame(self.main_frame,background=s.MAIN_BG,width=20)
        self.sidebar.pack(side='left',fill=tk.Y)  
        self.place_menu()
        self.active_periodic_check()
        
        border = tk.Frame(self.main_frame,background=s.MAIN_BD)
        border.pack(side='left',fill=tk.Y) 
        
        self.place_container()

    def place_container(self):
        if self.container is not None:
            return   
        self.container = ScrollableFrame(self.main_frame)
        self.container.pack(side='left',fill=tk.BOTH,expand=True)

    def active_periodic_check(self):
        for widget in self.sidebar.winfo_children():
            if isinstance(widget,MenuComponent):
                if widget.label != self.mode:
                    widget.active = False
                    widget.active_reconf()
                  
        self.after(1000,self.active_periodic_check) 

   
    def render_playlist(self,container:tk.Frame):
        self.load_music_playlist()
        if not self.music_playlist:
            empty =  MusicLabel(container,s.open_img('radio.png',size=15,fd='ms'),'No music..') 
            empty.pack(fill=tk.X) 

        for k, song in self.music_playlist.items():            
            label = MusicLabel(container, 
                               s.open_img('ms_icon.png', size=15, fd='ms'), 
                               song.filename[:15] + ' ..' + song.suffix, 
                               id=k)
            label.pack(fill=tk.X)

        self.ms_load.end_task()

    def end_music_window(self):
        if self.container is None:
            return
        for widget in self.container.winfo_children():
            s.unbind_all_events(widget)
            widget.destroy()
        self.container.pack_forget() 
        self.container = None


    def load_music_playlist(self):
        songs = []
        for filepath,folder,files in os.walk(s.BASE_DIR):
            for file in files:
                if file.endswith(s.ALLOWED_EXTENSIONS):
                    songs.append(Song(os.path.join(filepath,file)))

        for i,song in enumerate(set(songs)):
            self.music_playlist[i] = song 
  
    def place_menu(self):
        self.clip_b=MenuComponent(self.sidebar,s.open_img('clipboard.png',size=15,fd='ms'),'clipboard',self,b=self.clip_option)   
        self.clip_b.pack(pady=2)   
       
        self.ms=MenuComponent(self.sidebar,s.open_img('ms_icon.png',size=15,fd='ms'),'music',self,b=self.music_option)   
        self.ms.pack(pady=2)   
        
        self.sec=MenuComponent(self.sidebar,s.open_img('sec_iris.png',size=15,fd='sec'),'security',self,b=self.sec_option)   
        self.sec.pack(pady=2)

    def clip_container(self):
        if self.clip_cont is not None:
            return
        self.clip_cont = tk.Listbox(self.main_frame,background=s.MAIN_BG,highlightthickness=0) 
        self.clip_cont.pack(side='left',fill=tk.BOTH,expand=True)

        
        self.place_single_clipboard()
        self.place_single_clipboard()
        self.place_single_clipboard()
    
    def place_single_clipboard(self):
        self.sf = ShadowFrame(self.clip_cont,0,0,150,30,5,1,self.clip_cont,uw=self.cw)
        self.s_frame = self.sf.create_shadow()
        self.sf.pack(anchor='nw',fill=tk.X,pady=5)

    def cw(self,w):    
        self.sf.configure(width=w)

    def close_clipboard(self):
        if self.clip_cont is None:
            return
        for widget in self.clip_cont.winfo_children():
            widget.destroy()
        self.clip_cont.pack_forget()        
     
    def music_option(self,label):
        self.change_window_mode(label)
        self.place_container()
        self.ms_load = TaskManager(self.render_playlist,(self.load,self.unload)) 
        self.ms_load.start_task(self.container.frame)

    def clip_option(self,label):
        self.change_window_mode(label)
        self.end_music_window()
        self.clip_container()

        # self.clip=tk.Button(self.s_frame,text='testin',bg=s.MAIN_BD,bd=0,highlightthickness=0,cursor='hand2')
        # self.clip.pack(fill=tk.BOTH,expand=True)
     

    def sec_option(self,label):
        self.change_window_mode(label)
        print(label)

    def load(self):    
        #loading
        if self.loader is None:
            self.loader=Loader(self)
            self.loader.place(relwidth=1,relheight=0.01,relx=0,rely=0.13)  
        else:
            pass    
    
    def unload(self):
        if self.loader is not None:
            self.loader.running = False    
            self.loader.ani_obj.place_forget()

            self.loader.place_forget()   
            self.loader = None 

    def placing_title_labels(self,frame:tk.Frame) -> None:
        label = tk.Label(frame,text=self.lable_title.capitalize() if self.lable_title else self.default_title.capitalize(),font=(s.FONT,9),anchor='w',background=s.MAIN_BG,foreground=s.WHITE_MAIN)
        label.pack(side='left',padx=10)

        close_icon = s.open_img('plus.png',size=16,rotate=45)
        close_btn = tk.Button(frame,image=close_icon,text='',background=s.MAIN_BG,command=self.close_window,cursor='hand2',bd=0,border=0,highlightthickness=0)
        close_btn.image = close_icon
        close_btn.pack(side='right',padx=10)
        s.bind_hover(close_btn)

    def close_window(self) -> None:
        self.quit()   
    
    def on_press(self,e):
        self.start_x = e.x
        self.start_y = e.y

    def on_motion(self,e):
        dx = e.x - self.start_x
        dy = e.y - self.start_y

        self.geometry(f'+{int(self.winfo_x()+dx)}+{int(self.winfo_y()+dy)}')
        # print(self.winfo_x())
        # print(self.winfo_y())
        
    def music_mode(self):
        pass  

