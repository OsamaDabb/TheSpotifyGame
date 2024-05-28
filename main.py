import tkinter as tk

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
        self.window.geometry("1800x1200")

        s = ttk.Style()

        s.configure("grid.TButton", font=("Calibri", 16))

    def start_up(self) -> None:

        title_label = ttk.Label(master=self.window,
                                text="Spotify Game",
                                font="Calibri 24 bold")

        start_button = ttk.Button(master=self.window, text="Start", command=lambda: self.game_step(self.start_song))

        song_path = ttk.Label(master=self.window,
                              text=f'Goal: get from \n\n {self.start_song["name"]} by {self.start_song["artists"][0]["name"]} -> ' +
                              f'{self.target["name"]} by {self.target["artists"][0]["name"]}' +
                              f'\n\n by travelling through song recommendations',
                              font="Calibri 16",
                              justify="center")

        title_label.pack(pady=25)

        song_path.pack(pady=50)

        start_button.pack(pady=100)

    def game_step(self, song: dict) -> None:
        """
        On each choice of the player, calculates the new recommendations and populates the screen accordingly
        :param song: spotipy song dict parameter choosing the new current song
        :return:
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

                """
                for key, val in rec["album"].items():
                    print(f"{key}: {val}")"""
                # generating image for each song using PIL
                url = rec["album"]["images"][0]["url"]
                img = ImageTk.PhotoImage(Image.open(requests.get(url, stream=True).raw))

                rec_name = ttk.Button(master=recommendations_frame,
                                      text=f'{name} by {rec["artists"][0]["name"][:40]}',
                                      command=lambda recommendation=rec: self.game_step(recommendation),
                                      style="grid.TButton")

                rec_name.grid(row=(ind // 3) * 2, column=ind % 3,
                              padx=25, pady=25, sticky='nsew')

                img_label = ttk.Label(master=recommendations_frame,
                                      image=img)

                img_label.grid(row=(ind // 3)*2 + 1, column=ind % 3,
                               padx=25, pady=25, sticky='nsew')

            recommendations_frame.pack()

    def clear_window(self) -> None:

        for widget in self.window.winfo_children():

            widget.destroy()


def main() -> None:

    app = App()

    app.start_up()

    app.window.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
