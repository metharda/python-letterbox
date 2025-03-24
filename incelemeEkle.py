from main import incelemeEkle
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button as TkButton, PhotoImage, StringVar, OptionMenu, messagebox
from PIL import Image, ImageTk
import json

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/incelemeEkle")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_options():
    options = []
    try:
        with open('database.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            if data == {}:
                return "noMedia"
            else:
                for key in data:
                    options.append(key)
    except FileNotFoundError:
        messagebox.showerror("Hata", "Database bulunamadı.")
        return False
    return options

class IncelemeEkleApp:
    def __init__(self, root):
        self.window = root
        self.window.geometry("1280x720")
        self.window.configure(bg="#FFFFFF")
        self.window.title("İnceleme Ekle")
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
        self.background_image = PhotoImage(file=relative_to_assets("image.png"))
        self.button_image = PhotoImage(file=relative_to_assets("button.png"))
        self.entry_image = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))

        self.background = self.canvas.create_image(640.0, 360.0, image=self.background_image)
        rect_image = Image.new("RGBA", (1230, 670), (255, 255, 255, int(255 * 0.6)))
        rect_image = rect_image.convert("RGBA")
        self.rect_image_tk = ImageTk.PhotoImage(rect_image)
        self.canvas.create_image(640.0, 360.0, image=self.rect_image_tk)

        self.entry1 = Entry1(self.canvas, self.window, self.entry_image)
        self.entry2 = Entry2(self.canvas, self.window, self.entry_image)
        self.entry3 = Entry3(self.canvas, self.window, self.entry_image_2)
        self.button = Button(self.canvas, self.window, self.button_image, self.entry1, self.entry2, self.entry3)

        self.window.resizable(False, False)

class Entry1:
    def __init__(self, canvas, window, entry_image):
        self.options = load_options()
        self.selected = StringVar()
        if self.options == "noMedia":
            self.selected.set("Kayıtlı medya bulunamadı.")
        else:
            self.selected.set(self.options[0])
        self.entry_bg = canvas.create_image(
            291.5,
            164.0,
            image=entry_image
        )
        self.option_menu = OptionMenu(
            window,
            self.selected,
            *self.options
        )
        self.option_menu.config(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 12, "bold")
        )
        self.option_menu.place(
            x=128.0,
            y=139.0,
            width=327.0,
            height=48.0
        )
        canvas.create_text(
            120.0,
            95.0,
            anchor="nw",
            text="İnceleme Eklenecek Medya",
            fill="#000000",
            font=("Inter", 30 * -1)
        )

class Entry2:
    def __init__(self, canvas, window, entry_image):
        self.entry_bg = canvas.create_image(
            291.5,
            308.0,
            image=entry_image
        )
        self.entry = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry.place(
            x=128.0,
            y=283.0,
            width=327.0,
            height=48.0
        )
        canvas.create_text(
            120.0,
            240.0,
            anchor="nw",
            text="Verilen Puan",
            fill="#000000",
            font=("Inter", 30 * -1)
        )

class Entry3:
    def __init__(self, canvas, window, entry_image):
        self.entry_bg = canvas.create_image(
            291.5,
            499.5,
            image=entry_image
        )
        self.entry = Text(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 12),
            highlightthickness=0
        )
        self.entry.place(
            x=128.0,
            y=427.0,
            width=327.0,
            height=143.0
        )
        self.entry.insert("1.5", "")
        canvas.create_text(
            120.0,
            384.0,
            anchor="nw",
            text="Ek Not",
            fill="#000000",
            font=("Inter", 30 * -1)
        )

class Button:
    def __init__(self, canvas, window, button_image, entry1, entry2, entry3):
        self.entry1 = entry1
        self.entry2 = entry2
        self.entry3 = entry3
        self.button_1 = TkButton(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.checkInput,
            relief="flat"
        )
        self.button_1.place(
            x=216.0,
            y=600.0,
            width=147.0,
            height=45.0
        )
    def checkInput(self):
        if not self.entry2.entry.get().isdigit():
            messagebox.showerror("Hata", "Puan alanı sayı olmalıdır.")
            return False
        if int(self.entry2.entry.get()) <= 0 or int(self.entry2.entry.get()) > 10:
            messagebox.showerror("Hata", "Puan alanı 1-10 arasında olmalıdır.")
            return False
        if self.entry1.selected.get() not in load_options():
            messagebox.showerror("Hata", "Seçilen medya bulunamadı.")
            return False
        film = self.entry1.selected.get()
        with open('database.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            if "incelemeler" in data.get(film, {}):
                messagebox.showerror("Hata", "Bu filme daha önce inceleme eklenmiş.")
                return False
        puan = self.entry2.entry.get()
        yorum = self.entry3.entry.get("1.0", "end-1c")
        incelemeEkle(film, puan, yorum)
        messagebox.showinfo("Başarılı", f"{film} için inceleme başarıyla eklendi.")

if __name__ == "__main__":
    root = Tk()
    app = IncelemeEkleApp(root)
    root.mainloop()
