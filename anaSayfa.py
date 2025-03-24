from main import *
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Toplevel, Label
from PIL import Image, ImageTk, ImageDraw
import json
import requests

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/anaSayfa")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class AnaSayfaApp:
    def __init__(self, root):
        self.window = root
        self.window.geometry("1280x720")
        self.window.configure(bg="#FFFFFF")
        self.window.title("MarmaraBox")

        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.create_content()

    def create_content(self):
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(640.0, 360.0, image=self.image_image_1)

        rect_image = Image.new("RGBA", (1280, 99), (255, 255, 255, int(255 * 0.6)))
        self.rect_image_tk = ImageTk.PhotoImage(rect_image)
        self.canvas.create_image(640.0, 49.5, image=self.rect_image_tk)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(160.0, 50.0, image=self.image_image_2)

        self.button1 = CustomButton("button_1.png", 372.0, 18.0, 162.0, 66.0, filmListeSayfasi)
        self.button2 = CustomButton("button_2.png", 559.0, 18.0, 162.0, 66.0, filmEkleSayfasi)
        self.button3 = CustomButton("button_3.png", 746.0, 18.0, 162.0, 66.0, incelemeEklemeSayfasi)
        self.button4 = CustomButton("button_4.png", 933.0, 18.0, 162.0, 66.0, incelemeListelemeSayfasi)

        self.canvas.create_text(
            169.0,
            295.0,
            anchor="nw",
            text="Dilediğince listene film ve dizi ekle.\nİnsanların görmesi için yorumla ve puanla.\nFikirlerini diğer insanlarla paylaş.\n",
            fill="#FFFFFF",
            font=("Inter", 50*-1)
        )

class CustomButton:
    def __init__(self, image_path, x, y, width, height, command):
        self.button_image = self.round_button(image_path, width, height)
        self.button = Button(
            image=self.button_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        self.button.place(
            x=x,
            y=y,
            width=width,
            height=height
        )

    def round_button(self, image_path, width, height):
        img = Image.open(relative_to_assets(image_path)).resize((int(width), int(height)), Image.LANCZOS)
        img = img.convert("RGBA")
        corner_radius = 10
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, width, height), corner_radius, fill=255)
        img.putalpha(mask)
        datas = img.getdata()
        new_data = []
        for item in datas:
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        return ImageTk.PhotoImage(img)

if __name__ == "__main__":
    root = Tk()
    app = AnaSayfaApp(root)
    root.resizable(False, False)
    root.mainloop()
