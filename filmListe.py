from main import *
from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button, messagebox
from PIL import Image, ImageTk
import json
import requests

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/filmListe")
relative_to_assets = lambda path: ASSETS_PATH / Path(path)

def load_json_data():
    films = {}
    try:
        with open("database.json", 'r') as file:
            data = json.load(file)
            for film in data:
                name = film
                media_type = data[film].get("Medya Tipi")
                genre = data[film].get(f"{media_type} Türü")
                status = data[film].get("İzlenme Durumu")
                banner = data[film].get("Banner")
                films[name] = {"media_type": media_type, "genre": genre, "status": status, "banner": banner}
        return films
    except FileNotFoundError:
        print("JSON file not found.")
        return films

class FilmListApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg="#FFFFFF")
        self.root.title("Film Listesi")

        self.canvas = Canvas(self.root, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(640.0, 360.0, image=self.image_image_1)

        rect_image = Image.new("RGBA", (1230, 670), (255, 255, 255, int(255 * 0.6)))
        rect_image = rect_image.convert("RGBA")
        self.rect_image_tk = ImageTk.PhotoImage(rect_image)
        self.canvas.create_image(640.0, 360.0, image=self.rect_image_tk)

        self.films = load_json_data()
        self.banner_images = []
        self.create_list()
    

    def create_list(self):
        self.canvas.delete("film_item")
        x_position = 50
        y_position = 70
        card_width = 330 
        card_height = 250 
        padding = 20

        for index, film in enumerate(self.films):
            if index % 4 == 0 and index != 0:
                x_position = 50
                y_position += card_height + padding

            self.create_film_card(x_position, y_position, film)
            x_position += card_width + padding

    def create_film_card(self, x, y, film):
        card_width = 330  
        card_height = 250
        name = film
        media_type = self.films[film]["media_type"]
        genre = self.films[film]["genre"]
        status = self.films[film]["status"]
        banner_path = self.films[film]["banner"]

        self.canvas.create_rectangle(x, y, x + card_width, y + card_height, fill="#FFFFFF", outline="#000000", tags="film_item")
        self.canvas.create_text(x + 10, y + 10, anchor="nw", text=name, fill="#000000", font=("Arial", 10, "bold"), tags="film_item")
        self.canvas.create_text(x + 170, y + 40, anchor="nw", text=f"Medya Tipi: {media_type}", fill="#000000", font=("Arial", 10), tags="film_item")
        self.canvas.create_text(x + 170, y + 70, anchor="nw", text=f"Tür: {genre}", fill="#000000", font=("Arial", 10), tags="film_item")
        self.canvas.create_text(x + 170, y + 100, anchor="nw", text=f"Durum: {status}", fill="#000000", font=("Arial", 10), tags="film_item")

        if banner_path:
            banner_image = Image.open(requests.get(banner_path, stream=True).raw)
            banner_image = banner_image.resize((150, 210))
            banner_image_tk = ImageTk.PhotoImage(banner_image)
            self.banner_images.append(banner_image_tk)
            self.canvas.create_image(x + 80, y + card_height - 108, image=banner_image_tk, tags="film_item")

        delButton = Button(self.root, text="Sil", command=lambda name=name: self.confirm_delete(name), bg="#000000", fg="#FFFFFF")
        self.canvas.create_window(x + card_width - 20, y + card_height - 20, window=delButton, tags="film_item")

        statusButton = Button(self.root, text="İzlendi", command=lambda name=name: self.change_status(name), bg="#000000", fg="#FFFFFF")
        self.canvas.create_window(x + card_width - 60, y + card_height - 20, window=statusButton, tags="film_item")

    def change_status(self, name):
        current_status = self.films[name]["status"]
        new_status = "İzlendi" if current_status == "İzlenmedi" or "İzleniyor" else "İzlendi"
        self.films[name]["status"] = new_status

        with open("database.json", 'r+') as file:
            data = json.load(file)
            data[name]["İzlenme Durumu"] = new_status
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

        self.update_list()

    def confirm_delete(self, name):
        if messagebox.askyesno("Silme Onayı", f"{name} filmini silmek istediğinize emin misiniz?"):
            filmSil(name)
            self.update_list()

    def update_list(self):
        self.films.clear()
        self.films.update(load_json_data())
        self.create_list()

if __name__ == "__main__":
    window = Tk()
    app = FilmListApp(window)
    window.mainloop()
