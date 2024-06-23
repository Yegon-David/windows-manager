from settings import ImageTk
from settings import *
from typing import List,Tuple,Dict
import threading

class Song:
    def __init__(self,filepath:str) -> None:
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.suffix = os.path.splitext(filepath)[1]
        self.is_playing = False

class MusicList:
    def __init__(self) -> None:
        self.songs:List[Tuple[Song,bool]] = []

    def add_song(self, song: Song, is_playing: bool = False):
        self.songs.append((song, is_playing))

    def __repr__(self):
        return f"MusicList(songs={self.songs})"    

class UsableFrame(tk.Frame):
    def __init__(self,parent,logo:ImageTk,text) -> None:
        super().__init__(parent,background=MAIN_BG,border=0,cursor='hand2',highlightthickness=0,bd=0)
       
        self.label = tk.Label(self,image=logo,text=text.capitalize(),compound='left',padx=10,anchor='w',background=MAIN_BG,foreground=WHITE_MAIN,font=(FONT,9))
        self.label.image =logo
        self.label.pack(side='left',fill=tk.X,expand=True)

        self.bind('<Enter>',self.hover_label)
        self.bind('<Leave>',self.unhover_label)
        self.bind('<Button-1>',self.label_picked)

    def hover_label(self,e):
      
        self.label['background']=MAIN_BD
       
    def unhover_label(self,e):

        self.label.configure(background=MAIN_BG) 

    def label_picked(self,e):  
        if isinstance(e.widget,tk.Label):
            print(e.widget.cget('text'))
       
class LabelComponent(UsableFrame):
    def __init__(self, parent, logo: ImageTk, text) -> None:
        super().__init__(parent, logo, text)

class Loader(tk.Frame):
    def __init__(self,parent) -> None:
        super().__init__(parent,height=5,background=MAIN_BD)

        self.start_pos = 0
        self.obj_width = 0.3
        self.running =True
        self.animation_speed = 0.6

        self.ani_obj = tk.Frame(self,background='red')
        self.ani_obj.place(relx=self.start_pos,rely=0,relwidth=self.obj_width,relheight=1,anchor='nw')

        try:
            self.animate_obj()
        except Exception as e:
            print(str(e))    
        
    def animate_obj(self):
        if self.start_pos <=1:
            self.start_pos += float(0.002 * self.animation_speed)
        else:
            self.start_pos = -self.obj_width    
        self.ani_obj.place_configure(relx=self.start_pos) 
        
        if self.running:
            self.after(1 ,self.animate_obj)

class ShadowFrame(tk.Frame):
    def __init__(self, parent, x, y, width, height, shadow_thickness, offset=1,root = None,uw=None):
        super().__init__(parent, width=width , height=height,background=MAIN_BG)
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thickness = shadow_thickness
        self.offset = offset
        self.main_frame = None
        self.padding = 10
        self.uw = uw

        root.bind('<Configure>',self.update_dimensions)

    def update_dimensions(self,e):
        if self.main_frame is None:
            return

        for frame in self.winfo_children():
            if isinstance(frame,tk.Frame):
                frame.place_configure(width=e.width - self.padding)
        
        self.main_frame.place_configure(width=e.width - self.padding)
        self.uw(e.width)

    def create_shadow(self):
        for i in range(1, self.thickness + 1):
            y = (self.y + i + self.offset) 
            shadow_frame = tk.Frame(self, bg='black')
            shadow_frame.place(x=self.x + i + self.offset, 
                               y= y,
                               width=self.width, 
                               height=self.height-self.offset)
        
        self.main_frame = tk.Frame(self, background=MAIN_BD)
        self.main_frame.place(x=self.x+ self.thickness , y=self.y-self.thickness-self.offset, width=self.width, height=self.height)     
        return self.main_frame

class TopLevelMenu(tk.Toplevel):
    def __init__(self,text,x:int,y:int)->None:
        super().__init__()
        self.overrideredirect(True)
        self.wm_attributes('-topmost',True)
        self.geometry(f'+{x}+{y}')

        self.label = tk.Label(self,text=text.capitalize(),background=MAIN_HOVER,foreground=WHITE_MAIN,font=(FONT,8))
        self.label.pack(fill=tk.BOTH,expand=True)
         
    def close(self):
        try:
            self.label.pack_forget()
            self.destroy()
        except Exception as e:
            print(str(e))    

class MenuComponent(tk.Frame):
    def __init__(self,parent,image:ImageTk,label:str,root,b=None) -> None:
        super().__init__(parent,height=5,background=MAIN_BD,cursor='hand2')
        self.label = label
        self.top = None
        self.root = root
        self.b = b 
        self.active = False
        self.l = None

        self.place_label(image)
 
        self.bind('<Button-1>',lambda e: self.b_click())

        self.bind('<Enter>',self.hover_menu)
        self.bind('<Leave>',self.unhover_menu)

        self.hover_l()

    def hover_l(self):    
        if not self.active:
            bind_hover(self.l)
        else:
            unbind_hover(self.l)


    def place_label(self,image): 
        if self.l is not None and isinstance(self.l,tk.Label):
            return
        self.l = tk.Label(self,text='',image=image,background=MAIN_BG if not self.active else MAIN_BG)
        self.l.image = image
        self.l.pack(fill=tk.BOTH,expand=True)
        self.l.bind('<Button-1>',lambda e: self.b_click())

    def hover_menu(self,e):
        self.top = TopLevelMenu(self.label,
                                int(self.root.winfo_x()+self.winfo_x()+self.winfo_width()+5),
                                int(self.root.winfo_y() + self.winfo_y()+self.winfo_height()+5))
          

    def unhover_menu(self,e):
        if self.top is not None:
            self.top.close() 
            self.top = None

    def b_click(self)->None:
        if self.l is not None and isinstance(self.l,tk.Label):
            self.active = True
            self.hover_l()
            self.l.configure(background=MAIN_BD)
        self.b(self.label)  

    def active_reconf(self):
        self.l['background'] = MAIN_BD if self.active else MAIN_BG          

class MusicLabel(UsableFrame):
    def __init__(self, parent, logo: ImageTk, text,id=None) -> None:
        super().__init__(parent, logo, text)
        self.id = id

    def label_picked(self,e):  
        if isinstance(e.widget,tk.Label):
            print(e.widget.cget('text'),self.id)
       
class ScrollableFrame(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent,background=MAIN_BG,bd=0,border=0,highlightthickness=0)
        self.canvas = tk.Canvas(self,background=MAIN_BG,bd=0,highlightthickness=0)
        self.canvas.pack(expand=True,fill='both',side='right')

        self.sb = tk.Scrollbar(self,orient='vertical',background=MAIN_BG,command=self.canvas.yview,width=10,cursor='hand2',elementborderwidth=0)
        self.sb.pack(side='right',fill='y',before=self.canvas,padx=(0,1))

        self.canvas.configure(yscrollcommand=self.sb.set)
        
        self.frame = tk.Frame(self.canvas,background=MAIN_BG,height=40,highlightthickness=0,bd=0)
        self.canvas_window = self.canvas.create_window((0,0),window=self.frame,anchor='nw')
        
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.frame.bind("<Configure>", self.on_frame_configure)
        
        self.bind_mouse_wheel()

    def on_frame_configure(self, event):
        # Update the scroll region of the canvas to encompass the entire scrollable frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def bind_mouse_wheel(self):
        # Windows and Linux use '<MouseWheel>' event, macOS uses '<Button-4>' and '<Button-5>' events
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        if self.frame.winfo_height() > 40:
            if event.num == 4 or event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.canvas.yview_scroll(1, "units") 

    def on_canvas_configure(self, event):
        # Update the window size to match the canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)           

class TaskManager:
    def __init__(self,task,loader:tuple) -> None:
        self.task=task
        self.loader = loader


    def start_task(self,*args)->None:
        process = threading.Thread(target=self.task,args=(args))
        process.start()
        self.loader[0]()

    def end_task(self)->None:
        self.loader[1]()        
               