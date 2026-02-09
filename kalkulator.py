import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re
# ██╗  ██╗ █████╗ ██╗     ██╗  ██╗██╗   ██╗██╗      █████╗ ████████╗ ██████╗ ██████╗
# ██║ ██╔╝██╔══██╗██║     ██║ ██╔╝██║   ██║██║     ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
# █████╔╝ ███████║██║     █████╔╝ ██║   ██║██║     ███████║   ██║   ██║   ██║██████╔╝
# ██╔═██╗ ██╔══██║██║     ██╔═██╗ ██║   ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
# ██║  ██╗██║  ██║███████╗██║  ██╗╚██████╔╝███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
# ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

# =========================
# COORDINATES
# =========================

HAND_POINTS = [
    (22, 72), (65, 33), (87, 19), (128, 39), (184, 143),
    (217, 143), (270, 35), (311, 21), (333, 33), (376, 72)
]

FOOT_POINTS = [
    (15, 70), (28, 50), (43, 31), (69, 18), (96, 10),
    (305, 9), (332, 20), (354, 32), (372, 49), (387, 70)
]

# =========================
# WINDOW 1
# =========================

def mulai_berhitung():
    soal = entry.get().replace(" ", "")

    if not re.match(r"^\d+\+\d+$", soal):
        messagebox.showerror("Error", "Example: 3+3 or 6+6")
        return

    a, b = map(int, soal.split("+"))
    hasil = a + b

    max_points = len(HAND_POINTS) + len(FOOT_POINTS)
    if hasil > max_points:
        messagebox.showerror(
            "Error",
            f"Maximum result is {max_points}"
        )
        return

    buka_window_menghitung(a, b, hasil, soal)

root = tk.Tk()
root.title("Kalkulator")
root.geometry("320x220")
root.resizable(False, False)

tk.Label(
    root,
    text="Kalkulator",
    font=("Arial", 26, "bold")
).pack(pady=(15, 5))

entry = tk.Entry(
    root,
    font=("Arial", 30),
    justify="left",
    width=10)
entry.pack(pady=10)

tk.Button(
    root,
    text="Hitung",
    font=("Arial", 11),
    padx=10, pady=4,
    command=mulai_berhitung
).pack(pady=10)

# =========================
# WINDOW 2 - VISUAL COUNT
# =========================

def buka_window_menghitung(a, b, hasil, soal):
    WIDTH = 400
    HEIGHT = 250 if hasil <= 10 else 500

    win = tk.Toplevel(root)
    win.title("Menghitung")
    win.geometry(f"{WIDTH}x{HEIGHT}")
    win.resizable(False, False)

    canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT, highlightthickness=0)
    canvas.pack()

    # Images
    try:
        tangan_img = Image.open("tangan.png").resize((400, 250))
    except FileNotFoundError:
        messagebox.showerror("Error", "tangan.png not found")
        win.destroy()
        return

    tangan_photo = ImageTk.PhotoImage(tangan_img)
    canvas.create_image(0, 0, anchor="nw", image=tangan_photo)
    canvas.tangan = tangan_photo

    if hasil > 10:
        try:
            kaki_img = Image.open("kaki.png").resize((400, 250))
        except FileNotFoundError:
            messagebox.showerror("Error", "kaki.png not found")
            win.destroy()
            return

        kaki_photo = ImageTk.PhotoImage(kaki_img)
        canvas.create_image(0, 250, anchor="nw", image=kaki_photo)
        canvas.kaki = kaki_photo

    # =========================
    # BUILD POSITION LIST
    # =========================

    positions = []

    # hands first
    for p in HAND_POINTS:
        positions.append(p)

    # feet if needed
    if hasil > 10:
        for p in FOOT_POINTS:
            positions.append((p[0], p[1] + 250))

    positions = positions[:hasil]

    drawn_items = []

    # =========================
    # STEP 1 – RED then GREEN
    # =========================

    def step1(index=0):
        if index >= hasil:
            win.after(600, step2)
            return

        x, y = positions[index]

        if index < a:
            color = "red"
            text = index + 1
        else:
            color = "green"
            text = index - a + 1

        item_id = canvas.create_text(
            x, y,
            text=str(text),
            fill=color,
            font=("Arial", 16, "bold")
        )

        drawn_items.append(item_id)

        win.after(300, step1, index + 1)

    # =========================
    # STEP 2 – BLUE RECOUNT
    # =========================
    
    def step2():
        def recount(i=0):
            if i >= hasil:
                win.after(
                    800,
                    lambda: messagebox.showinfo("Hasil", f"{soal} = {hasil}")
                )
                return

            canvas.itemconfig(
                drawn_items[i],
                fill="blue",
                text=str(i + 1)
            )

            win.after(250, recount, i + 1)

        recount()

    step1()

root.mainloop()
