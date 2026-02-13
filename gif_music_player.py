import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import ctypes
import os
import sys

# ==== CONFIGURATION ====
IMAGE_FILE = "FishIsForever (1).gif"    # Path to GIF file
MUSIC_FILE = "a.mp3"                    # Path to MP3 file
WINDOW_WIDTH = 600                      # Window width
WINDOW_HEIGHT = 400                     # Window height
INITIAL_ANIMATION_SPEED = 50            # Initial animation interval in milliseconds
WINDOW_TITLE = "Fish"
ALWAYS_ON_TOP = False                   # Keep window always on top
RESIZABLE = False                       # Make window resizable

# ==== HIDE CMD WINDOW (WINDOWS ONLY) ====
if sys.platform == "win32":
    import subprocess
    if os.getenv('PYTHONUNBUFFERED') != '1':
        # Re-run without console window
        CREATE_NO_WINDOW = 0x08000000
        subprocess.Popen([sys.executable] + sys.argv, creationflags=CREATE_NO_WINDOW)
        sys.exit()

# ==== MUSIC CONTROL (WINDOWS ONLY) ====
winmm = ctypes.windll.winmm

def play_mp3_loop(path):
    """Plays an MP3 file in loop using Windows MCI."""
    try:
        winmm.mciSendStringW(f'open "{path}" type mpegvideo alias music', None, 0, None)
        winmm.mciSendStringW('play music repeat', None, 0, None)
        print("[OK] Music playing")
    except Exception as e:
        print(f"[ERROR] Could not play music: {e}")

def stop_mp3():
    """Stops and closes the MP3 music."""
    try:
        winmm.mciSendStringW('stop music', None, 0, None)
        winmm.mciSendStringW('close music', None, 0, None)
        print("[OK] Music stopped")
    except Exception as e:
        print(f"[ERROR] Could not stop music: {e}")

def on_close():
    """Handles the close window event."""
    print("Attempted to close 😈")

# ==== START MUSIC ====
if os.name == "nt":
    play_mp3_loop(os.path.abspath(MUSIC_FILE))
else:
    print("[WARN] MP3 playback only works on Windows.")

# ==== WINDOW SETUP ====
root = tk.Tk()
root.title(WINDOW_TITLE)
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT + 60}")
root.protocol("WM_DELETE_WINDOW", on_close)
root.resizable(RESIZABLE, RESIZABLE)
if ALWAYS_ON_TOP:
    root.attributes("-topmost", True)

# ==== ANIMATION CONTROL FRAME ====
control_frame = tk.Frame(root, bg="gray20", height=60)
control_frame.pack(side=tk.BOTTOM, fill=tk.X)
control_frame.pack_propagate(False)

speed_label = tk.Label(control_frame, text="Animation Speed:", fg="white", bg="gray20")
speed_label.pack(side=tk.LEFT, padx=10, pady=5)

# Store current animation speed as a variable
animation_speed = tk.IntVar(value=INITIAL_ANIMATION_SPEED)

def update_speed(value):
    """Update animation speed from slider."""
    animation_speed.set(int(float(value)))
speed_value_label.config(text=f"{int(float(value))} ms")

speed_slider = tk.Scale(
    control_frame,
    from_=10,
    to=200,
    orient=tk.HORIZONTAL,
    command=update_speed,
    bg="gray40",
    fg="white",
    highlightthickness=0,
    length=300
)
speed_slider.set(INITIAL_ANIMATION_SPEED)
speed_slider.pack(side=tk.LEFT, padx=10, pady=5)

speed_value_label = tk.Label(control_frame, text=f"{INITIAL_ANIMATION_SPEED} ms", fg="white", bg="gray20", width=8)
speed_value_label.pack(side=tk.LEFT, padx=5, pady=5)

# Button to reset speed
reset_btn = tk.Button(
    control_frame,
    text="Reset",
    command=lambda: speed_slider.set(INITIAL_ANIMATION_SPEED),
    bg="gray40",
    fg="white",
    relief=tk.FLAT,
    padx=10
)
reset_btn.pack(side=tk.LEFT, padx=5, pady=5)

# ==== GIF DISPLAY FRAME ====
gif_frame = tk.Frame(root, bg="black")
gif_frame.pack(fill=tk.BOTH, expand=True)

label = tk.Label(gif_frame, bg="black")
label.pack(fill="both", expand=True)

# ==== GIF ANIMATION ====
try:
    gif = Image.open(IMAGE_FILE)
except Exception as e:
    print(f"[ERROR] Could not open GIF file: {e}")
    root.destroy()
    sys.exit(1)

frames = []
for frame in ImageSequence.Iterator(gif):
    frame = frame.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
    frames.append(ImageTk.PhotoImage(frame))

print(f"[OK] Loaded {len(frames)} frames from GIF")

current_frame = [0]  # Use list to allow modification in nested function

def animate():
    """Animate GIF frames with dynamic speed control."""
    label.config(image=frames[current_frame[0]])
    current_frame[0] = (current_frame[0] + 1) % len(frames)
    root.after(animation_speed.get(), animate)

animate()

# ==== CLEANUP ON EXIT ====
def on_destroy(event=None):
    stop_mp3()
    print("[OK] Clean exit.")
    root.destroy()

root.bind("<Destroy>", on_destroy)

root.mainloop()