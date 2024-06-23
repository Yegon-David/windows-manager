import tkinter as tk

class ShadowFrame(tk.Frame):
    def __init__(self, parent, x, y, width, height, shadow_thickness, offset=1):
        super().__init__(parent, width=width + shadow_thickness + offset, height=height + shadow_thickness + offset)
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thickness = shadow_thickness
        self.offset = offset

        self.create_shadow()

    def create_shadow(self):
        for i in range(1, self.thickness + 1):
            shadow_frame = tk.Frame(self, bg='black')
            shadow_frame.place(x=self.x + i + self.offset, y=self.y +i + self.offset, width=self.width, height=self.height)
        
        main_frame = tk.Frame(self, background='white')
        main_frame.place(x=self.x, y=self.y, width=self.width, height=self.height)
        
        return main_frame

# Example usage
root = tk.Tk()
root.geometry("400x400")

shadow_frame = ShadowFrame(root, x=50, y=50, width=200, height=100, shadow_thickness=50, offset=1)
shadow_frame.pack()

root.mainloop()
