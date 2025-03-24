from main import *
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
from PIL import Image, ImageTk
import json
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/incelemeListe")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
def load_json_data():
    review = {}
    try:
        with open("database.json", 'r') as file:
            data = json.load(file)
            for film in data:
                if 'incelemeler' in data[film]:
                    name = film
                    rate = data[film]["incelemeler"][0][film].get("Puan")
                    note = data[film]["incelemeler"][0][film].get("Yorum")
                    review[name] = {"Puan": rate, "Yorum": note}
        return review
    except FileNotFoundError:
        print("JSON file not found.")
        return review
    
class IncelemeListApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg="#FFFFFF")
        self.root.title("İnceleme Listesi")

        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(640.0, 360.0, image=self.image_image_1)

        rect_image = Image.new("RGBA", (1230, 670), (255, 255, 255, int(255 * 0.6)))
        rect_image = rect_image.convert("RGBA")
        self.rect_image_tk = ImageTk.PhotoImage(rect_image)
        self.canvas.create_image(640.0, 360.0, image=self.rect_image_tk)

        self.review = load_json_data()
        self.top_bar = self.create_top_bar()
        self.canvas.coords(self.top_bar, 25, 25, 1255, 80)
        self.create_list()

    def create_top_bar(self):
        top_bar = self.canvas.create_rectangle(0, 0, 1280, 50, fill="#FFFFFF", outline="")
        self.canvas.create_text(100, 50, anchor="w", text="Film Adı", fill="#000000", font=("Arial", 12, "bold"))
        self.canvas.create_text(400, 50, anchor="w", text="Puan", fill="#000000", font=("Arial", 12, "bold"))
        self.canvas.create_text(700, 50, anchor="w", text="Yorum", fill="#000000", font=("Arial", 12, "bold"))
        self.canvas.create_line(25, 75, 1255, 75, fill="#000000")
        return top_bar

    def create_list(self):
        self.canvas.delete("film_item")
        y_position = 100
        for film in self.review:
            name = film
            rate = self.review[film]["Puan"]
            note = self.review[film]["Yorum"]
            self.canvas.create_text(100, y_position, anchor="w", text=name, fill="#000000", font=("Arial", 12), tags="film_item")
            self.canvas.create_text(400, y_position, anchor="w", text=rate, fill="#000000", font=("Arial", 12), tags="film_item")
            self.canvas.create_text(700, y_position, anchor="w", text=note, fill="#000000", font=("Arial", 12), tags="film_item")
            delButton = Button(self.root, text="Sil", command=lambda name=name: self.confirm_delete(name))
            self.canvas.create_window(1200, y_position, window=delButton, tags="film_item")
            y_position += 30

    def confirm_delete(self, name):
        if messagebox.askyesno("Silme Onayı", f"{name} filmini silmek istediğinize emin misiniz?"):
            filmSil(name)
            self.update_list()

    def update_list(self):
        self.review.clear()
        self.review.update(load_json_data())
        self.create_list()


if __name__ == "__main__":
    window = Tk()
    app = IncelemeListApp(window)
    window.resizable(False, False)
    window.mainloop()
