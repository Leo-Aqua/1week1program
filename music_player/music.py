import tkinter as tk
from tkinter import filedialog
import pygame
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import ImageTk, Image

def extract_cover_art(file_path):
    global found_cover
    try:
        audio = MP3(file_path, ID3=ID3)
        tags = audio.tags
        if 'APIC:' in tags:
            # Extract the first APIC frame (cover art)
            apic = tags['APIC:'].data
            # Write the cover art to a file

            with open(os.path.dirname(os.path.realpath(__file__)) + "\cover_art.jpg", "wb") as f:
                f.write(apic)
            found_cover = True
        else:
            found_cover = False

    except Exception as e:
        print("An error occurred:", e)
found_cover = False
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player")
        self.root.geometry("300x300")  # Adjusted window size for cover art display

        self.music_file = None
        self.paused = False

        pygame.init()

        self.play_button = tk.Button(root, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Music", command=self.stop_music)
        self.stop_button.pack(pady=5)

        self.choose_button = tk.Button(root, text="Choose Music", command=self.choose_music)
        self.choose_button.pack(pady=5)

        self.current_song_label = tk.Label(root, text="No music currently playing")
        self.current_song_label.pack(pady=5)


        self.cover_frame = tk.Frame(root)
        self.cover_label = tk.Label(self.cover_frame)
        self.cover_frame.pack(pady=5)

    def choose_music(self):
        self.music_file = filedialog.askopenfilename(defaultextension=".mp3",
                                                      filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
        if self.music_file:
            self.current_song_label.config(text=os.path.basename(self.music_file))
            extract_cover_art(self.music_file)
            self.update_cover_art()
            self.cover_frame.pack()  # Show cover art frame when a song is selected
        else:
            self.current_song_label.config(text="No music selected")

    def update_cover_art(self):
        # Update cover art image
        if found_cover == True:
            self.cover_image = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\cover_art.jpg").resize((100, 100)))
            self.cover_label.config(image=self.cover_image)
            self.cover_label.pack()
        elif found_cover == False:
        
            self.cover_label.pack_forget()

    def play_music(self):
        if self.music_file:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play()
            self.paused = False

    def pause_music(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_song_label.config(text="No music currently playing")
        self.cover_frame.pack_forget()  # Hide cover art frame when music is stopped


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()