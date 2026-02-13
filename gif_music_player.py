import os
import tkinter as tk
from tkinter import filedialog
import vlc

class GifMusicPlayer:
    def __init__(self, gif_path, music_path):
        """Initialize the player with the gif and music file paths."""
        self.gif_path = gif_path
        self.music_path = music_path
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.root = tk.Tk()
        self.root.title("GIF Music Player")

    def load_and_play(self):
        """Load the GIF and music, then start playback."""
        # Load and start playing the music
        media = self.instance.media_new(self.music_path)
        self.player.set_media(media)
        self.player.play()
        
        # Load and display the GIF
        self.load_gif()

    def load_gif(self):
        """Load and display the GIF in the Tkinter window."""
        gif_label = tk.Label(self.root)
        gif_label.pack()
        gif = tk.PhotoImage(file=self.gif_path)
        gif_label.config(image=gif)
        gif_label.image = gif  # Keep a reference to avoid garbage collection

    def run(self):
        """Run the Tkinter event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    # Configurable options
    gif_file = filedialog.askopenfilename(title="Select a GIF file", filetypes=[("GIF files", "*.gif")])
    music_file = filedialog.askopenfilename(title="Select a Music file", filetypes=[("Music files", "*.mp3;*.wav")])
    
    player = GifMusicPlayer(gif_file, music_file)
    player.load_and_play()
    player.run()