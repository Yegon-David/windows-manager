from controls import *
from controls.components import LabelComponent
from controls.db_control import Dimensions
from screeninfo import get_monitors

class ActiveWindow(MainWindow):
    def __init__(self, title,x,y) -> None:
        super().__init__(title)
        self.geometry(f'+{x}+{y}') if x is not None else None
        self.window_status = 'window'
        if self.window_status == 'music':
            self.music_mode()
        elif self.window_status == 'window':
            self.window_mode() 
            self.split_main_frame()
            # self.main_menu()  

    def main_menu(self):
        for label in s.OPTIONS:
            icon = s.open_img('add_file.png',size=14)

            option = LabelComponent(self.main_frame,logo=icon,text=label)
            option.pack(anchor='w',pady=2,fill=tk.X)

            option.bind('<Button-1>',lambda e,opt=option: self.open_option(opt))



if __name__ == '__main__':
  
    dimensions = Dimensions()
    x=y=sl=None
    if dimensions.get_dimensions():
        
        x,y,sl = dimensions.get_dimensions() 
        if len(get_monitors()) == 1 and x >= 1366:
            x=y=None
    main_window = ActiveWindow('My Windows Manager',x=x if x is not None else None,y=y if y is not None else None)
    main_window.mainloop()
    if dimensions.get_dimensions() is None:
        dimensions.insert_xy_s(main_window.winfo_x(),main_window.winfo_y(),len(get_monitors()))
    else:        
        dimensions.update_xy_s(main_window.winfo_x(),main_window.winfo_y(),len(get_monitors()))
    