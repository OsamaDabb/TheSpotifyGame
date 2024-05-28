import tkinter as tk
from io import BytesIO

import requests
import ttkbootstrap as ttk

from backend import SpotipyInstance
from PIL import Image, ImageTk


class App:

    def __init__(self):
        self.sp = SpotipyInstance(user=False)

        self.start_song, self.target = self.sp.get_targets()

        self.curr_song = self.start_song

        self.window = ttk.Window(themename="darkly")
        self.window.title("Spotify Game")
        self.window.geometry("2200x1600")

        self.images: list = []

        self.step_count = 0

        s = ttk.Style()

        s.configure("grid.TButton", font=("Calibri", 16))

    def start_up(self) -> None:

        title_label = ttk.Label(master=self.window,
                                text="Spotify Game",
                                font="Calibri 24 bold")

        start_button = ttk.Button(master=self.window, text="Start",
                                  command=lambda: self.game_step(self.start_song),
                                  style="grid.TButton")

        images_container = ttk.Frame(master=self.window)

        for ind, song in enumerate((self.start_song, self.target)):

            url = song["album"]["images"][0]["url"]
            response = requests.get(url, stream=True)
            test_im = Image.open(BytesIO(response.content)).resize((300,300))

            self.images.append(ImageTk.PhotoImage(image=test_im))
            image_label = ttk.Label(
                master=images_container,
                image=self.images[-1]
            )

            text_label = ttk.Label(
                master=images_container,
                text=f'{song["name"]} by {song["artists"][0]["name"]}'
            )

            image_label.grid(row=0, column=ind, pady=20, padx=20)

            text_label.grid(row=1, column=ind, pady=20, padx=20)

        description_label = ttk.Label(master=self.window,
                              text=f'Goal: get between the following songs by travelling through song recommendations',
                              font="Calibri 16",
                              justify="center")

        title_label.pack(pady=25)

        description_label.pack(pady=50)

        images_container.pack(pady=15)

        start_button.pack(pady=100)

    def game_step(self, song: dict) -> None:
        """
        On each choice of the player, calculates the new recommendations and populates the screen accordingly
        :param song: spotipy song dict parameter choosing the new current song
        :return: None
        """

        self.curr_song = song

        self.clear_window()

        # end state
        if self.curr_song["name"] == self.target["name"]:

            self.clear_window()

            win_label = ttk.Label(master=self.window, text="You Win!",
                                  font="Calibri 24 bold")

            win_label.grid()

        # non-end state
        else:

            current_song_label = ttk.Label(master=self.window,
                                           text=f'Current Song: {self.curr_song["name"]} by {self.curr_song["artists"][0]["name"]}',
                                           font="Calibri 22 bold")

            current_song_label.pack(pady=25)

            target_song_label = ttk.Label(master=self.window,
                                          text=f'Target: {self.target["name"][:40]} by {self.target["artists"][0]["name"]}',
                                          font="Calibri 18")

            target_song_label.pack(pady=25)

            recommendations = self.sp.get_recommendations(self.curr_song)

            choices_label = ttk.Label(master=self.window, text="Choices",
                                      font="Calibri 18 bold")

            recommendations_frame = ttk.Frame(master=self.window)

            choices_label.pack(pady=20)

            for ind, rec in enumerate(recommendations[:9]):

                name = ""

                # generating song name excluding featured artists and truncating longer titles
                for word in rec["name"].split(" "):

                    if len(name) > 30 or "feat" in word or "with" in word:

                        name += "..."
                        break

                    name += word + " "

                name = name[:-1]

                # generating image for each song using PIL
                url = rec["album"]["images"][0]["url"]
                img = Image.open(requests.get(url, stream=True).raw).resize((200, 200))
                self.images.append(ImageTk.PhotoImage(img))

                rec_name = ttk.Button(master=recommendations_frame,
                                      text=f'{name} by {rec["artists"][0]["name"][:40]}',
                                      command=lambda recommendation=rec: self.game_step(recommendation),
                                      style="grid.TButton")

                rec_name.grid(row=(ind // 3) * 2, column=ind % 3,
                              padx=25, pady=10, sticky='nsew')

                img_label = ttk.Label(master=recommendations_frame,
                                      image=self.images[-1])

                img_label.grid(row=(ind // 3)*2 + 1, column=ind % 3,
                               padx=250, pady=10, sticky='nsew')

            recommendations_frame.pack()

    def clear_window(self) -> None:

        self.images = []

        for widget in self.window.winfo_children():

            widget.destroy()


def main() -> None:

    app = App()

    app.start_up()

    app.window.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
