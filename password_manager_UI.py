import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import tkinter as tk

from password_manager_security import hash_password, load_master_password, save_master_password
from vault_window import open_vault_window
from encryption_handler import derive_key, load_or_create_salt


ctk.set_appearance_mode("dark")

# ------------------ Splash Video ------------------

def play_intro_video():

    cap = cv2.VideoCapture("vid1.mov")

    splash = tk.Tk()
    splash.attributes("-fullscreen", True)
    splash.configure(bg="black")

    label = tk.Label(splash)
    label.pack()

    def update():

        ret, frame = cap.read()

        if ret:

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = cv2.resize(
                frame,
                (splash.winfo_screenwidth(), splash.winfo_screenheight())
            )

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            label.imgtk = imgtk
            label.configure(image=imgtk)

            splash.after(15, update)

        else:
            cap.release()
            splash.destroy()
            start_app()

    update()
    splash.mainloop()


# ------------------ Main App ------------------

def start_app():

    global app

    app = ctk.CTk()
    app.title("Secure Password Vault")

    def go_fullscreen():
        app.update_idletasks()
        app.state("zoomed")

    app.after(10, go_fullscreen)

    # ------------------ Background ------------------

    bg_image = Image.open("back1.png")
    bg = ctk.CTkImage(dark_image=bg_image, light_image=bg_image, size=(1920,1080))

    bg_label = ctk.CTkLabel(app, image=bg, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ------------------ Login UI ------------------

    container = ctk.CTkFrame(app, fg_color="transparent")
    container.place(relx=0.5, rely=0.5, anchor="center")

    title = ctk.CTkLabel(
        container,
        text="Secure Vault",
        font=("Segoe UI",42,"bold"),
        text_color="#d6b3ff"
    )
    title.pack(pady=30)

    card = ctk.CTkFrame(container, width=420, height=300, corner_radius=18, fg_color="#14142b")
    card.pack()
    card.pack_propagate(False)

    # ------------------ Password ------------------

    def toggle_password():
        password_entry.configure(show="" if password_entry.cget("show")=="●" else "●")

    def toggle_confirm():
        confirm_entry.configure(show="" if confirm_entry.cget("show")=="●" else "●")

    label1 = ctk.CTkLabel(card, text="Master Password", text_color="#c9b6ff")
    label1.pack(pady=(30,5))

    frame1 = ctk.CTkFrame(card, fg_color="transparent")
    frame1.pack()

    password_entry = ctk.CTkEntry(frame1, width=260, height=38, show="●", corner_radius=10)
    password_entry.pack(side="left", padx=5)

    show1 = ctk.CTkButton(frame1, text="👁", width=42, height=38,
                          fg_color="#6c4cff", hover_color="#7e66ff", command=toggle_password)
    show1.pack(side="left")

    # ------------------ confirm ------------------

    label2 = ctk.CTkLabel(card, text="Confirm Password", text_color="#c9b6ff")
    label2.pack(pady=(15,5))

    frame2 = ctk.CTkFrame(card, fg_color="transparent")
    frame2.pack()

    confirm_entry = ctk.CTkEntry(frame2, width=260, height=38, show="●", corner_radius=10)
    confirm_entry.pack(side="left", padx=5)

    show2 = ctk.CTkButton(frame2, text="👁", width=42, height=38,
                          fg_color="#6c4cff", hover_color="#7e66ff", command=toggle_confirm)
    show2.pack(side="left")

    status = ctk.CTkLabel(card, text="")
    status.pack(pady=10)

    # ------------------ Login Logic ------------------

    def login():

        p1 = password_entry.get()
        p2 = confirm_entry.get()

        if p1 == "" or p2 == "":
            status.configure(text="Please fill all fields", text_color="#ff6b6b")
            return

        if p1 != p2:
            status.configure(text="Passwords do not match", text_color="#ff6b6b")
            return

        stored = load_master_password()

        if stored is None:
            hashed = hash_password(p1)
            save_master_password(hashed)

            salt = load_or_create_salt()
            key = derive_key(p1, salt)

            status.configure(text="Master password created!", text_color="#7dffb3")
            app.after(600, lambda: open_vault_window(app, key))
            return

        hashed = hash_password(p1)

        if hashed == stored:
            status.configure(text="Access Granted", text_color="#7dffb3")
            salt = load_or_create_salt()
            key = derive_key(p1, salt)
            app.after(600, lambda: open_vault_window(app,key))
        else:
            status.configure(text="Wrong password!", text_color="#ff6b6b")

    login_btn = ctk.CTkButton(card, text="Unlock Vault", width=280, height=40,
                              corner_radius=12, fg_color="#7c5cff", hover_color="#9373ff",
                              command=login)
    login_btn.pack(padx=15)

    app.mainloop()


# ------------------ Start Program ------------------

play_intro_video()

