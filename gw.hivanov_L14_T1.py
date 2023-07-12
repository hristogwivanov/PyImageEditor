from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageOps, ImageFilter
import os

class ResizeDialog(simpledialog.Dialog):
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        super().__init__(parent)

    def body(self, master):
        Label(master, text="Width:").grid(row=0)
        Label(master, text="Height:").grid(row=1)

        self.width_entry = Entry(master)
        self.height_entry = Entry(master)

        self.width_entry.insert(0, self.width)
        self.height_entry.insert(0, self.height)

        self.width_entry.grid(row=0, column=1)
        self.height_entry.grid(row=1, column=1)

        return self.width_entry  # initial focus

    def apply(self):
        self.width = int(self.width_entry.get())
        self.height = int(self.height_entry.get())


class ImageViewer: 
    def __init__(self, root):
        self.root=root
        self.root.title('GW Image Viewer')
        self.current_image = None
        self.current_image_path = None
        self.current_image_display = None
        self.display = Label(self.root)
        self.display.pack()

        self.menu = Menu(self.root)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save", command=self.save_image, state=DISABLED)
        self.file_menu.add_command(label="Clear Changes", command=self.clear_changes, state=DISABLED)
        self.file_menu.add_command(label="Image Info", command=self.show_image_info, state=DISABLED)
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = Menu(self.menu, tearoff=0)
        self.rotate_menu = Menu(self.edit_menu, tearoff=0)
        self.rotate_menu.add_command(label="Rotate Left", command=lambda:self.transform_image("rotate_left"))
        self.rotate_menu.add_command(label="Rotate Right", command=lambda:self.transform_image("rotate_right"))
        self.rotate_menu.add_command(label="Rotate 180", command=lambda:self.transform_image("rotate_180"))
        self.rotate_menu.add_command(label="Custom Rotation", command=self.custom_rotation)
        self.edit_menu.add_cascade(label="Rotate", menu=self.rotate_menu, state=DISABLED)
        self.edit_menu.add_command(label="Flip Horizontal", command=lambda: self.transform_image("flip_horizontal"), state=DISABLED)
        self.edit_menu.add_command(label="Flip Vertical", command=lambda: self.transform_image("flip_vertical"), state=DISABLED)
        self.edit_menu.add_command(label="Resize", command=self.resize_image, state=DISABLED)

        # FILTERS
        self.filters_menu = Menu(self.edit_menu, tearoff=0)
        self.filters_menu.add_command(label="Apply Custom BLUR Filter", command=lambda: self.apply_filter('custom_blur'))
        self.filters_menu.add_command(label="Apply Custom MEDIAN Filter", command=lambda: self.apply_filter('custom_median'))
        self.filters_menu.add_command(label="Apply Custom EDGE Filter", command=lambda: self.apply_filter('custom_edge'))

        self.filters_menu.add_command(label="Apply BLUR Filter", command=lambda: self.apply_filter(ImageFilter.BLUR))
        self.filters_menu.add_command(label="Apply CONTOUR Filter", command=lambda: self.apply_filter(ImageFilter.CONTOUR))
        self.filters_menu.add_command(label="Apply DETAIL Filter", command=lambda: self.apply_filter(ImageFilter.DETAIL))
        self.filters_menu.add_command(label="Apply EDGE ENHANCE Filter", command=lambda: self.apply_filter(ImageFilter.EDGE_ENHANCE))
        self.filters_menu.add_command(label="Apply EDGE ENHANCE MORE Filter", command=lambda: self.apply_filter(ImageFilter.EDGE_ENHANCE_MORE))
        self.filters_menu.add_command(label="Apply EMBOSS Filter", command=lambda: self.apply_filter(ImageFilter.EMBOSS))
        self.filters_menu.add_command(label="Apply FIND EDGES Filter", command=lambda: self.apply_filter(ImageFilter.FIND_EDGES))
        self.filters_menu.add_command(label="Apply SMOOTH Filter", command=lambda: self.apply_filter(ImageFilter.SMOOTH))
        self.filters_menu.add_command(label="Apply SMOOTH MORE Filter", command=lambda: self.apply_filter(ImageFilter.SMOOTH_MORE))
        self.filters_menu.add_command(label="Apply SHARPEN Filter", command=lambda: self.apply_filter(ImageFilter.SHARPEN))
        self.edit_menu.add_cascade(label="Filters", menu=self.filters_menu, state=DISABLED)
        
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)

        self.root.config(menu=self.menu)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_image_path = file_path  
            self.current_image = Image.open(file_path)
            self.display_image()
            self.file_menu.entryconfig("Save", state=NORMAL)
            self.file_menu.entryconfig("Image Info", state=NORMAL)
            self.file_menu.entryconfig("Clear Changes", state=NORMAL)
            self.edit_menu.entryconfig("Rotate", state=NORMAL)
            self.edit_menu.entryconfig("Flip Horizontal", state=NORMAL)
            self.edit_menu.entryconfig("Flip Vertical", state=NORMAL)
            self.edit_menu.entryconfig("Resize", state=NORMAL)
            self.edit_menu.entryconfig("Filters", state=NORMAL)


    def save_image(self):
        if self.current_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            self.current_image.save(save_path)


    def display_image(self):
        tk_img = ImageTk.PhotoImage(self.current_image)
        self.display.config(image=tk_img)
        self.display.image = tk_img

    def clear_changes(self):
        if self.current_image_path:
            self.current_image = Image.open(self.current_image_path)
            self.display_image()
    
    def show_image_info(self):
        if self.current_image:
            info_window = Toplevel(self.root)
            info_window.title("Image Info")

            Label(info_window, text=f"Image name: {os.path.basename(self.current_image_path)}", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)
            Label(info_window, text=f"Image size: {self.current_image.size}", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)
            Label(info_window, text=f"Image mode: {self.current_image.mode}", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)

            # Displaying image format
            if self.current_image.format:
                Label(info_window, text=f"Image format: {self.current_image.format}", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)
            else:
                Label(info_window, text="Image format: Unknown", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)
                
            # Displaying the number of color channels
            num_channels = len(self.current_image.getbands())
            Label(info_window, text=f"Number of color channels: {num_channels}", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)
            
            # Displaying the image palette
            if self.current_image.palette:
                Label(info_window, text=f"Image palette: {self.current_image.palette}", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)
            else:
                Label(info_window, text="Image palette: None", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)

            # Checking for image transparency
            if self.current_image.mode in ("RGBA", "LA") or (self.current_image.mode == "P" and 'transparency' in self.current_image.info):
                Label(info_window, text="Image transparency: Yes", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)
            else:
                Label(info_window, text="Image transparency: No", anchor="w", justify=LEFT).pack(fill=BOTH, padx=10, pady=5)
            


            Button(info_window, text="OK", command=info_window.destroy, width=20).pack(pady=10) 

    def transform_image(self, operation):
        if self.current_image:
            if operation == "rotate_left":
                self.current_image = self.current_image.rotate(90)
            elif operation == "rotate_right":
                self.current_image = self.current_image.rotate(-90)
            elif operation == "rotate_180":
                self.current_image = self.current_image.rotate(180)
            elif operation == "flip_horizontal":
                self.current_image = ImageOps.mirror(self.current_image)
            elif operation == "flip_vertical":
                self.current_image = ImageOps.flip(self.current_image)
        self.display_image()

    def custom_rotation(self):
        if self.current_image:
            angle = simpledialog.askfloat("Custom Rotation", "Enter rotation angle:", initialvalue=0)
            self.current_image = self.current_image.rotate(angle)
            self.display_image()

    def resize_image(self):
        if self.current_image:
            width, height = self.current_image.size
            resize_dialog = ResizeDialog(self.root, width, height)
            if resize_dialog.width and resize_dialog.height:
                new_size = (resize_dialog.width, resize_dialog.height)
                self.current_image = self.current_image.resize(new_size)
                self.display_image()

    def apply_filter(self, filter_type):
        if self.current_image:
            if filter_type == 'custom_blur':
                self.current_image = custom_blur(self.current_image)
            elif filter_type == 'custom_median':
                self.current_image = custom_median(self.current_image)
            elif filter_type == 'custom_edge':
                self.current_image = custom_edge(self.current_image)
            else:
                self.current_image = self.current_image.filter(filter_type)
            self.display_image()




def custom_blur(image):
    px = image.load()
    sizeX, sizeY = image.size
    new_image = Image.new('RGB', (sizeX, sizeY))
    px2 = new_image.load()
    
    for i in range(1, sizeX-1):
        for j in range(1, sizeY-1):
            r = g = b = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    r += px[i+k, j+l][0]
                    g += px[i+k, j+l][1]
                    b += px[i+k, j+l][2]
            px2[i, j] = r // 9, g // 9, b // 9
    return new_image

def custom_median(image):
    px = image.load()
    sizeX, sizeY = image.size
    new_image = Image.new('RGB', (sizeX, sizeY))
    px2 = new_image.load()

    for i in range(1, sizeX-1):
        for j in range(1, sizeY-1):
            r = []
            g = []
            b = []
            for k in range(-1, 2):
                for l in range(-1, 2):
                    r.append(px[i+k, j+l][0])
                    g.append(px[i+k, j+l][1])
                    b.append(px[i+k, j+l][2])
            r.sort()
            g.sort()
            b.sort()
            px2[i, j] = r[4], g[4], b[4] # Select the median value
    return new_image


def custom_edge(image):
    px = image.load()
    sizeX, sizeY = image.size
    new_image = Image.new('RGB', (sizeX, sizeY))
    px2 = new_image.load()

    for i in range(1, sizeX-1):
        for j in range(1, sizeY-1):
            r = g = b = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if k==l==0:
                        r += px[i+k, j+l][0] * 8
                        g += px[i+k, j+l][1] * 8
                        b += px[i+k, j+l][2] * 8
                    else:
                        r -= px[i+k, j+l][0]
                        g -= px[i+k, j+l][1]
                        b -= px[i+k, j+l][2]
            # clip the values between 0 and 255
            r = min(255, max(0, r))
            g = min(255, max(0, g))
            b = min(255, max(0, b))
            px2[i, j] = r, g, b

    return new_image



root = Tk()
root.title('GW Image Viewer')
root.geometry('500x500')
app = ImageViewer(root)
root.mainloop()
