from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button as TkButton, PhotoImage, StringVar, OptionMenu, messagebox, Radiobutton
from PIL import Image, ImageTk
from main import *
import requests
from tkinter import Label


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/filmEkle")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def checkInput(app):
    if app.entry2.entry.get() == "":
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
        return False
    medya_turu = app.entry1.selected.get()
    film_adi = app.entry2.entry.get().strip()
    izlenme_durumu = app.entry3.selected.get()
    filmEkle(medya_turu, film_adi, izlenme_durumu)
    messagebox.showinfo("Başarılı", f"{film_adi} başarıyla eklendi.")

class FilmEkleApp:
    def __init__(self, window):
        self.window = window
        self.window.geometry("1280x720")
        self.window.configure(bg="#FFFFFF")
        self.window.title("Film Ekle")
        
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
        self.background = PhotoImage(file=relative_to_assets("image.png"))
        self.button_image = PhotoImage(file=relative_to_assets("button.png"))
        self.entry_image = PhotoImage(file=relative_to_assets("entry.png"))
        self.image_1 = self.canvas.create_image(640.0, 360.0, image=self.background)
        rect_image = Image.new("RGBA", (1230, 670), (255, 255, 255, int(255 * 0.6)))
        rect_image = rect_image.convert("RGBA")
        self.rect_image_tk = ImageTk.PhotoImage(rect_image)
        self.canvas.create_image(640.0, 360.0, image=self.rect_image_tk)
        self.create_widgets()

    def create_widgets(self):
        self.button = TkButton(
            image=self.button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: checkInput(self),
            relief="flat"
        )
        self.button.place(
            x=177.0,
            y=554.0,
            width=147.0,
            height=45.0
        )
        self.button1 = TkButton(
            borderwidth=0,
            highlightthickness=0,
            command=self.ara,
            relief="flat",
            text="Ara"
        )
        self.button1.place(
            x=440.0,
            y=324.0,
            width=30.0,
            height=30.0
        )
        self.entry1 = Entry1(self.canvas, self.window, self.entry_image)
        self.entry2 = Entry2(self.canvas, self.entry_image)
        self.entry3 = Entry3(self.canvas, self.window, self.entry_image)

    def ara(self):
        if hasattr(self, 'banner_label'):
            self.banner_label.destroy()
        if hasattr(self, 'info_text'):
            self.canvas.delete(self.info_text)
        if hasattr(self, 'info_bg'):
            self.canvas.delete(self.info_bg)
        if self.entry1.selected.get() == "Film":
            film_bilgileri = filmBul(self.entry2.entry.get())
        else:
            film_bilgileri = diziBul(self.entry2.entry.get())
        
        if film_bilgileri:
            self.canvas.create_text(
            600.0,
            115.0,
            text="Aranan Dizi/Film Bilgileri",
            font=("Inter", 30 * -1),
            fill="#000716"
            )
            banner_image = Image.open(requests.get(film_bilgileri['banner'], stream=True).raw)
            banner_image = banner_image.resize((300, 450))
            banner_image_tk = ImageTk.PhotoImage(banner_image)
            
            self.banner_label = Label(self.window, image=banner_image_tk)
            self.banner_label.image = banner_image_tk
            self.banner_label.place(x=520.0, y=150.0, width=300, height=450)
            
            self.info_bg = self.canvas.create_rectangle(
            510.0, 140.0, 1150.0, 610.0,
            fill="#333333", outline=""
            )
            
            self.info_text = self.canvas.create_text(
            840.0,
            150.0,
            anchor="nw",
            text=f"İsmi: {film_bilgileri['title']}\n\nTürü: {film_bilgileri['genre']}\n\nÖzeti: {film_bilgileri['summary']}",
            fill="#FFFFFF",
            font=("Inter", 14 * -1),
            width=300
            )
        else:
            messagebox.showerror("Hata", "Film bulunamadı.")

class Entry1:
    def __init__(self, canvas, window, entry_image):
        self.canvas = canvas
        self.window = window
        self.entry_bg = self.canvas.create_image(
            260.5,
            195.0,
            image=entry_image
        )
        self.option = ["Film", "Dizi"]
        self.selected = StringVar()
        self.selected.set(self.option[0])
        
        self.radio_button1 = Radiobutton(
            self.window,
            text="Film",
            variable=self.selected,
            value="Film",
            bg="#D9D9D9",
            fg="#000716",
            font=("Arial", 12, "bold")
        )
        self.radio_button1.place(
            x=97.0,
            y=170.0,
            width=150.0,
            height=48.0
        )
        
        self.radio_button2 = Radiobutton(
            self.window,
            text="Dizi",
            variable=self.selected,
            value="Dizi",
            bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 12, "bold")
        )
        self.radio_button2.place(
            x=274.0,
            y=170.0,
            width=150.0,
            height=48.0
        )
        
        self.canvas.create_text(
            150.0,
            132.0,
            text="Dizi/Film",
            font=("Inter", 30 * -1),
            fill="#000716"
        )

class Entry2:
    def __init__(self, canvas, entry_image):
        self.canvas = canvas
        self.entry_bg = self.canvas.create_image(
            260.5,
            339.0,
            image=entry_image
        )
        self.entry = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry.place(
            x=97.0,
            y=314.0,
            width=327.0,
            height=48.0
        )
        self.canvas.create_text(
            89.0,
            266.0,
            anchor="nw",
            text="Film/Dizi Adı",
            fill="#000000",
            font=("Inter", 30 * -1)
        )

class Entry3:
    def __init__(self, canvas, window, entry_image):
        self.canvas = canvas
        self.window = window
        self.entry_bg = self.canvas.create_image(
            260.5,
            483.0,
            image=entry_image
        )
        self.options = ["İzlenmedi", "İzleniyor", "İzlendi"]
        self.selected = StringVar()
        self.selected.set(self.options[0])
        self.optionMenu = OptionMenu(self.window, self.selected, *self.options)
        self.optionMenu.config(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            font=("Arial", 12, "bold"),
            highlightthickness=0
        )
        self.optionMenu.place(
            x=97.0,
            y=458.0,
            width=327.0,
            height=48.0
        )
        self.canvas.create_text(
            89.0,
            414.0,
            anchor="nw",
            text="İzlenme Durumu",
            fill="#000000",
            font=("Inter", 30 * -1)
        )

if __name__ == "__main__":
    window = Tk()
    app = FilmEkleApp(window)
    window.resizable(False, False)
    window.mainloop()