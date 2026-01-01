import customtkinter as ctk
from image_widgets import *
from PIL import Image,ImageTk,ImageOps,ImageEnhance,ImageFilter
from menu import Menu
class App(ctk.CTk):
    def __init__(self,username):

        #setup 
        super().__init__()
        self.username = username  # store logged in user
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Photo editor')
        self.minsize(800,500)

        # Root layout
        self.grid_rowconfigure(0, weight=0)  # profile bar (fixed)
        self.grid_rowconfigure(1, weight=1)  # main content (expandable)

        self.grid_columnconfigure(0, weight=1)

        self.init_parameters()
        self.create_profile_bar() 

        # Main content container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew",  padx=10,pady=10)

        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=0,minsize=220)
        self.main_frame.columnconfigure(1, weight=3)


        #layout
        # self.rowconfigure(0, weight=0)
        # self.rowconfigure(1, weight = 1)
        
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=3)
        # self.columnconfigure(0, weight = 2, uniform='a')
        # self.columnconfigure(1, weight = 6, uniform='a')

        #canvas data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        #widgets
        #ImportButton (Frame with a button)
        self.image_import = ImageImport(self.main_frame, self.import_image)
        self.image_import.grid(row=0, column=0, columnspan=2, sticky="nsew")

        #run
        self.mainloop()

    def init_parameters(self):
        self.pos_vars= {
            'rotate': ctk.DoubleVar(value=ROTATE_DEFAULT),
            'zoom': ctk.DoubleVar(value=ZOOM_DEFAULT),
            'flip': ctk.StringVar(value=FLIP_OPTIONS[0]),
        }
        self.colors_vars= {
            'brightness': ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            'grayscale': ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
            'invert': ctk.BooleanVar(value=INVERT_DEFAULT),
            'vibrance': ctk.DoubleVar(value=VIBRANCE_DEFAULT),
        }
        self.effect_vars= {
            'blur': ctk.DoubleVar(value=BLUR_OPTIONS),
            'contrast': ctk.IntVar(value=CONTRAST_DEFAULT),
            'effect': ctk.StringVar(value=EFFECT_OPTIONS[0])
        }

        #tracing 
        combined_vars= list(self.pos_vars.values()) + list(self.colors_vars.values()) + list(self.effect_vars.values()) 
        for var in combined_vars:
            var.trace('w',self.manipulate_image)
        # self.rotate_float = ctk.DoubleVar(value= ROTATE_DEFAULT)
        # self.zoom_float = ctk.DoubleVar(value = ZOOM_DEFAULT)

        # self.rotate_float.trace('w', self.manipulate_image)
        # self.zoom_float.trace('w', self.manipulate_image)
        #1. connect the var to the slider
        #2. trace the changes to the var
        #3. use the var to change the image
    def manipulate_image(self,*args):
        self.image = self.original
        #only apply the effect if the value is different from the default

        #rotate
        if self.pos_vars['rotate'].get() != ROTATE_DEFAULT:
            self.image = self.image.rotate(self.pos_vars['rotate'].get(),expand=True)
        #zoom
        if self.pos_vars['zoom'].get():
            self.image = ImageOps.crop(image = self.image, border=self.pos_vars['zoom'].get())
        #flip
        if self.pos_vars['flip'].get() != FLIP_OPTIONS:
            if self.pos_vars['flip'].get() == 'X':
                self.image = ImageOps.mirror(self.image)
            if self.pos_vars['flip'].get() == 'Y':
                self.image = ImageOps.flip(self.image)
            if self.pos_vars['flip'].get() == 'Both':
                self.image = ImageOps.flip(self.image)
                self.image = ImageOps.mirror(self.image)

        # brightness & vibrance
        if self.colors_vars['brightness'].get() != BRIGHTNESS_DEFAULT:
            brightness_enhancer = ImageEnhance.Brightness(self.image)
            self.image = brightness_enhancer.enhance(self.colors_vars['brightness'].get())
        if self.colors_vars['vibrance'].get() != VIBRANCE_DEFAULT:
            vibrance_enhancer = ImageEnhance.Color(self.image)
            self.image = vibrance_enhancer.enhance(self.colors_vars['vibrance'].get())

        # grayscale and invert of the colors
        if self.colors_vars['grayscale'].get():
            self.image = ImageOps.grayscale(self.image)
        
        if self.colors_vars['invert'].get():
            self.image = ImageOps.invert(self.image)

        #blur & contrast 
        if self.effect_vars['blur'].get() != BLUR_OPTIONS:
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_vars['blur'].get()))
        if self.effect_vars['contrast'].get() != CONTRAST_DEFAULT:
            self.image = self.image.filter(ImageFilter.UnsharpMask(self.effect_vars['contrast'].get()))
        match self.effect_vars['effect'].get():
            case 'Emboss': self.image = self.image.filter(ImageFilter.EMBOSS)
            case 'Find edges': self.image = self.image.filter(ImageFilter.FIND_EDGES)
            case 'Countour': self.image = self.image.filter(ImageFilter.CONTOUR)
            case 'Edge enhance': self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)

        self.place_image()

    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_import.grid_forget()
        # self.image_output = ImageOutput(self, self.resize_image)
        # self.close_button = CloseOutput(self,self.close_edit)
        # self.menu = Menu(self, self.pos_vars,self.colors_vars,self.effect_vars,self.export_image)
        self.menu = Menu(self.main_frame, self.pos_vars, self.colors_vars, self.effect_vars, self.export_image)
        self.menu.grid(row=0, column=0, sticky="nsew")
        self.image_output = ImageOutput(self.main_frame, self.resize_image)
        self.image_output.grid(row=0, column=1, sticky="nsew")
        
        
        self.close_button = CloseOutput(self.main_frame, self.close_edit)
    def close_edit(self):
        #hide the image and the close button
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        #recreate the import button
        self.image_import = ImageImport(self.main_frame, self.import_image)
        self.image_import.grid(row=0, column=0, columnspan=2, sticky="nsew")


    def resize_image(self,event):
        #current canvas ratio
        canvas_ratio = event.width / event.height

        #update canvas attributes 
        self.canvas_width = event.width
        self.canvas_height = event.height

        #resize
        if canvas_ratio > self.image_ratio: # canvas is wider than image
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else: #canvas is taller than image
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()

    #place image
    def place_image(self):
        self.image_output.delete('all')
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(self.canvas_width / 2,self.canvas_height / 2,image = self.image_tk)
    
    def export_image(self,name,file,path):
        export_string = f'{path}/{name}.{file}'
        self.image.save(export_string)
    def create_profile_bar(self):
        self.configure(fg_color="#0f172a")
        self.profile_frame = ctk.CTkFrame(self, height=55, corner_radius=0, fg_color="#1f2933")
        self.profile_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.profile_frame.grid_propagate(False)
        
        self.profile_frame.grid_columnconfigure(0, weight=1)
        self.profile_frame.grid_columnconfigure(1, weight=1)
        self.profile_frame.grid_columnconfigure(2, weight=1)
        self.profile_frame.configure(fg_color=("#1f2933", "#111827"))
        
        # Username
        self.user_label = ctk.CTkLabel(
            self.profile_frame,
            text=f"👤 {self.username}",
            font=("Segoe UI", 14, "bold"),
            text_color="white",
            fg_color="transparent"
        )
        self.user_label.grid(row=0, column=0, padx=20,pady=10, sticky="w")
        # Logout button
        self.logout_btn = ctk.CTkButton(
            self.profile_frame,
            text="Logout",
            fg_color="#b91c1c",
            hover_color="#991b1b",
            command=self.logout
        )
        self.logout_btn.grid(row=0, column=2, padx=20, sticky="e")
    def logout(self):
        self.destroy()
        from auth import AuthApp
        root = ctk.CTk()
        AuthApp(root)
        root.mainloop()

