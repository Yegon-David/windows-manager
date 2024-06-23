import tkinter as tk 
from PIL import Image,ImageTk
import enum
import os

MAIN_BG = '#1e1e1e'
MAIN_HOVER = '#242323'
MAIN_BD = '#474646'
WHITE_MAIN = '#f0f0f0'
WHITE_FADE = '#8a8686'
DARK_GREY = '#272727'
TRANSPARENT='transparent'
BLUE_TEXT = '#0785ec'
BLUE_FADE = '#264F78'
FONT= 'Segoe UI'

MUSIC_DIR = 'D:\\vids\\music'
BASE_DIR = 'D:\\vids'

class MusicFile:
  is_playing = False
  path = ''
  filename = ''
  suffix = ''

ALLOWED_EXTENSIONS = ('.mp3', '.wav', '.ogg', '.midi')

def open_img(name,size=25,rotate=None,fd = 'images'):
  image = Image.open(f'assets/{fd}/{name}').resize(size=(size,size))
  if rotate:
    image = image.rotate(rotate)
  image_tk = ImageTk.PhotoImage(image)

  return image_tk

def unbind_all_events(widget):
    for tag in widget.bindtags():
        events = widget.bind_class(tag)
        for event in events:
            widget.unbind_class(tag, event)

def hex_color(value):
    """Convert an integer value to a two-digit hex string."""
    return f'{value:02x}'

def get_shade_color(base_color, factor):
    """Darken the base color by a factor (0 to 1)."""
    base_r = int(base_color[1:3], 16)
    base_g = int(base_color[3:5], 16)
    base_b = int(base_color[5:7], 16)

    new_r = int(base_r * factor)
    new_g = int(base_g * factor)
    new_b = int(base_b * factor)

    return f'#{hex_color(new_r)}{hex_color(new_g)}{hex_color(new_b)}'



def bind_hover(label,bg=MAIN_BD,hv=MAIN_BG):
  label.bind('<Enter>',lambda e: label.configure(background=bg))  
  label.bind('<Leave>',lambda e: label.configure(background=hv)) 

def unbind_hover(label,bg=MAIN_BD,hv=MAIN_BG):
  label.unbind('<Enter>')  
  label.unbind('<Leave>') 

def place_end_icons(frame,image_name,size=17,rotate=90,side='right',padx=3,text=None):
  dotted_icon_image = open_img(image_name,size=size,rotate=rotate)
  dotted_icon=tk.Label(frame,text=text if text else '',foreground=WHITE_MAIN,compound='left',image=dotted_icon_image,background=MAIN_BG,cursor='hand2')
  dotted_icon.image = dotted_icon_image
  dotted_icon.pack(side=side,padx=padx)
  bind_hover(dotted_icon) 
  return dotted_icon  


FILE_TYPES = [
            ('All files','*.*'),
            ('Text files','*.txt'),
            ('Python files','*.py'),
            ('Html files','*.html'),
            ('Png Files','*.png')
              ]


OPTIONS = [
  'clipboard','music','Encoder'
]
ENCODER_OPTIONS = [
  'file','folder'
]