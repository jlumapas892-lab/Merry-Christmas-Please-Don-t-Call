
import tkinter as tk
import time
import math
import random
import pygame
import os


# ==============================
# MUSIC SETTINGS
# ==============================
MUSIC_FILE = "pasko.mp3"
MUSIC_VOLUME = 1.0


# ==============================
# LYRICS
# ==============================
LYRICS = [
    (0.00, "|"),
    (0.00, "I"),
    (0.00, "want"),
    (0.65, "one"),
    (0.85, "ticket"),
    (1.50, "out"),
    (1.60, "of"),
    (1.75, "your"),
    (2.20, "heavy"),
    (2.45, "gaze"),

    (3.00, "|"),
    (3.50, "I"),
    (3.50, "want"),
    (4.60, "one"),
    (4.90, "ticket"),
    (5.20, "off"),
    (5.50, "of"),
    (5.70, "your"),
    (5.90, "carousel"),

    (8.80, "|"),
    (8.80, "But"),
    (9.25, "should"),
    (9.40, "you"),
    (10.15, "know"),
    (11.20, "that"),
    (11.45, "I"),
    (11.70, "die"),
    (12.20, "slow"),

    (13.00, "|"),
    (13.00, "Running"),
    (13.45, "through"),
    (13.75, "the"),
    (14.00, "halls"),
    (14.50, "of"),
    (14.70, "your"),
    (15.00, "haunted"),
    (15.70, "home"),

    (17.00, "|"),
    (17.00, "And"),
    (17.30, "the"),
    (17.55, "toughest"),
    (18.15, "part"),
    (19.60, "is"),
    (19.85, "that"),
    (20.15, "we"),
    (20.40, "both"),
    (20.90, "know"),

    (21.80, "|"),
    (21.80, "What"),
    (22.45, "happened"),
    (23.10, "to"),
    (23.35, "you"),

    (24.00, "|"),
    (24.00, "Why"),
    (24.35, "you're"),
    (24.70, "out"),
    (25.00, "on"),
    (25.20, "your"),
    (25.50, "own"),

    (26.00, "|"),
    (26.90, "Merry"),
    (26.95, "Christmas,"),
    (28.20, "please"),
    (28.65, "don't"),
    (29.15, "call"),

    (31.00, "|"),
    (31.00, "Merry"),
    (31.05, "Christmas,"),
    (32.20, "I'm"),
    (32.50, "not"),
    (32.85, "yours"),
    (33.40, "at"),
    (33.65, "all"),

    (35.00, "|"),
    (35.00, "Merry"),
    (35.05, "Christmas,"),
    (37.20, "please"),
    (37.65, "don't"),
    (38.15, "call"),
    (38.65, "me"),

    (40.70, "|"),
    (40.70, "Please"),
    (41.60, "don't"),
    (42.20, "call"),
    (42.80, "me"),

    (45.70, "|"),
    (45.60, "Please"),
    (45.70, "don't"),
    (46.20, "call"),
    (46.80, "me"),

    (49.10, "|"),
    (49.10, "Please"),
    (49.60, "don't"),
    (50.20, "call"),
    (50.80, "me"),
]



BOX_W, BOX_H = 300, 250
FONT = ("Times New Roman", 22, "bold")

BG_COLOR = "#ce1408"
FG_COLOR = "#dda183"

RISE_SPEED = 67
BOTTOM_SPAWN_OFFSET = 150



SNOWFLAKE_CHARS = ["❄", "❅", "❆"]

NOTE_FONT_SIZES = [16, 22, 28, 34, 40, 46, 52]


NOTE_COLORS = [
    "#FFFFFF",
    "#F8FAFC",
    "#F0F4F8",
    "#E2E8F0",
    "#D6E4F0",
]

NOTE_MIN_SPAWN_GAP = 0.25
NOTE_MAX_SPAWN_GAP = 0.6

NOTE_SPEED_RANGE = (35, 95)
NOTE_WOBBLE_AMP_RANGE = (12, 45)
NOTE_WOBBLE_FREQ_RANGE = (0.8, 2.4)

NOTE_SPAWN_TAIL_BUFFER = 8


class LyricCard:

    def __init__(self, parent, x, y):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=BG_COLOR)

        self.win.geometry(
            f"{BOX_W}x{BOX_H}+{int(x)}+{int(y)}"
        )

        self.win.resizable(False, False)

        self.label = tk.Label(
            self.win,
            text="",
            font=FONT,
            bg=BG_COLOR,
            fg=FG_COLOR,
            wraplength=BOX_W - 25,
            justify="center"
        )

        self.label.pack(
            expand=True,
            fill="both",
            padx=15,
            pady=15
        )

        self.words = []

        self.x = x
        self.y = float(y)

   
    def add_word(self, word):
        self.words.append(word)

        displayed_text = " ".join(self.words)
        self.label.config(text=displayed_text)

    
    def rise(self, dy):
        self.y -= dy

        self.win.geometry(
            f"{BOX_W}x{BOX_H}+{int(self.x)}+{int(self.y)}"
        )

    def is_offscreen(self):
        return self.y + BOX_H < -50



class MusicNote:

    def __init__(self, parent, screen_w, screen_h):
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)

        try:
            self.win.attributes(
                "-transparentcolor", "#000000"
            )
        except tk.TclError:
            pass

        try:
            self.win.attributes("-alpha", 0.88)
        except tk.TclError:
            pass

        
        char = random.choice(SNOWFLAKE_CHARS)
        size = random.choice(NOTE_FONT_SIZES)
        color = random.choice(NOTE_COLORS)

        self.win.configure(bg="#000000")

        label = tk.Label(
            self.win,
            text=char,
            font=("Segoe UI Symbol", size, "bold"),
            bg="#000000",
            fg=color
        )

        label.pack(padx=3, pady=3)

        self.screen_h = screen_h

        self.base_x = random.uniform(
            10, max(10, screen_w - 60)
        )

        
        self.y = float(
            random.uniform(-120, -10)
        )

        self.spawn_time = time.time()

       
        self.wobble_phase = random.uniform(
            0, math.tau
        )

        self.wobble_freq = random.uniform(
            *NOTE_WOBBLE_FREQ_RANGE
        )

        self.wobble_amp = random.uniform(
            *NOTE_WOBBLE_AMP_RANGE
        )

       
        self.speed = random.uniform(
            *NOTE_SPEED_RANGE
        )

        self._update_pos()

    def _update_pos(self):
        t = time.time() - self.spawn_time

       
        x = self.base_x + math.sin(
            t * self.wobble_freq + self.wobble_phase
        ) * self.wobble_amp

        self.win.geometry(
            f"+{int(x)}+{int(self.y)}"
        )

    
    def rise(self, dt):
        self.y += self.speed * dt
        self._update_pos()

    
    def is_offscreen(self):
        return self.y > self.screen_h + 60

    def destroy(self):
        try:
            self.win.destroy()
        except tk.TclError:
            pass



class LyricFloatApp:

    def __init__(self, root):
        self.root = root

        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

        self.next_lyric_idx = 0

        self.boxes = []
        self.notes = []

        self.last_frame_time = None

        self.current_side = "left"
        self.current_card = None

        self.next_note_spawn_time = 0.0

        self.last_lyric_time = max(
            (t for t, _ in LYRICS), default=0
        )

        self.music_ready = False

        
        if MUSIC_FILE.strip():
            try:
                if not os.path.exists(MUSIC_FILE):
                    raise FileNotFoundError(
                        f"Music file not found: {MUSIC_FILE}"
                    )

                pygame.mixer.init()
                pygame.mixer.music.load(MUSIC_FILE)

                pygame.mixer.music.set_volume(
                    max(0.0, min(1.0, MUSIC_VOLUME))
                )

                self.music_ready = True

            except (pygame.error, OSError) as e:
                print("Music could not be loaded:", e)

        self.start()

    
    def get_music_time(self):
        if self.music_ready:
            position = pygame.mixer.music.get_pos()

            if position >= 0:
                return position / 1000.0

        return time.time() - self.start_time

    def random_safe_x(self):
        center_x = self.screen_w // 2
        spacing = BOX_W + 60

        left_x = center_x - spacing
        right_x = center_x + 60

        if self.current_side == "left":
            self.current_side = "right"
            return left_x
        else:
            self.current_side = "left"
            return right_x

   
    def start(self):
        self.root.iconify()

        self.start_time = time.time()
        self.last_frame_time = self.start_time
        self.next_note_spawn_time = self.start_time

        if self.music_ready:
            pygame.mixer.music.play()

        self.root.after(16, self.tick)

    
    def create_lyric_card(self):
        x = self.random_safe_x()

        y = (
            self.screen_h
            - BOX_H
            - BOTTOM_SPAWN_OFFSET
        )

        box = LyricCard(
            self.root,
            x,
            y
        )

        self.boxes.append(box)
        self.current_card = box

 
    def _maybe_spawn_note(self, now, elapsed):
        if elapsed > (
            self.last_lyric_time + NOTE_SPAWN_TAIL_BUFFER
        ):
            return

        if now >= self.next_note_spawn_time:
            note = MusicNote(
                self.root,
                self.screen_w,
                self.screen_h
            )

            self.notes.append(note)

            self.next_note_spawn_time = (
                now + random.uniform(
                    NOTE_MIN_SPAWN_GAP,
                    NOTE_MAX_SPAWN_GAP
                )
            )

   
    def process_lyrics(self, elapsed):
        while (
            self.next_lyric_idx < len(LYRICS)
            and LYRICS[self.next_lyric_idx][0] <= elapsed
        ):
            timestamp, word = LYRICS[self.next_lyric_idx]

            if word == "|":
                self.current_card = None

            else:
                if self.current_card is None:
                    self.create_lyric_card()

                self.current_card.add_word(word)

            self.next_lyric_idx += 1

 
    def tick(self):
        now = time.time()

        elapsed = self.get_music_time()

        dt = min(now - self.last_frame_time, 0.1)
        self.last_frame_time = now

        self.process_lyrics(elapsed)

        
        dy = RISE_SPEED * dt

        for box in self.boxes:
            box.rise(dy)

     
        still_visible = []

        for box in self.boxes:
            if box.is_offscreen():
                try:
                    box.win.destroy()
                except tk.TclError:
                    pass

                if self.current_card == box:
                    self.current_card = None

            else:
                still_visible.append(box)

        self.boxes = still_visible

  
        self._maybe_spawn_note(now, elapsed)

     
        for note in self.notes:
            note.rise(dt)

       
        still_floating_notes = []

        for note in self.notes:
            if note.is_offscreen():
                note.destroy()
            else:
                still_floating_notes.append(note)

        self.notes = still_floating_notes

        
        if (
            self.next_lyric_idx < len(LYRICS)
            or self.boxes
            or self.notes
        ):
            self.root.after(16, self.tick)

        else:
            self.cleanup()

    
    def cleanup(self):
        if self.music_ready:
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()

    app = LyricFloatApp(root)

    root.mainloop()
