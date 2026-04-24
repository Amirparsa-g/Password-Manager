import random
import string
import customtkinter as ctk
from password_manager_security import load_vault, save_vault

cards = []
def open_add_password_popup(parent, add_callback):

    popup = ctk.CTkToplevel(parent)
    popup.title("Add New Password")
    popup.grab_set() 

    popup.geometry("400x360")
    popup.resizable(False, False)

    frame = ctk.CTkFrame(popup, fg_color="#191927", corner_radius=12)
    frame.pack(fill="both", expand=True, padx=15, pady=15)

  
    site_entry = ctk.CTkEntry(frame, placeholder_text="Site / App Name")
    site_entry.pack(fill="x", padx=15, pady=(20,10))

    user_entry = ctk.CTkEntry(frame, placeholder_text="Username / Email")
    user_entry.pack(fill="x", padx=15, pady=10)

    pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="•")
    pass_entry.pack(fill="x", padx=15, pady=10)

    # Toggle show/hide
    def toggle_pass():
        if pass_entry.cget("show") == "•":
            pass_entry.configure(show="")
            toggle_btn.configure(text="Hide")
        else:
            pass_entry.configure(show="•")
            toggle_btn.configure(text="Show")

    toggle_btn = ctk.CTkButton(
        frame,
        text="Show",
        width=60,
        command=toggle_pass
    )
    toggle_btn.pack(padx=15, pady=5)

    # ---------------- Password Generator ----------------
    def generate_password():
        chars = string.ascii_letters + string.digits + "!@#$%&*"
        password = "".join(random.choice(chars) for _ in range(12))
        pass_entry.delete(0, "end")
        pass_entry.insert(0, password)

    gen_btn = ctk.CTkButton(
        frame,
        text="Generate Password",
        fg_color="#6c4cff",
        hover_color="#7f63ff",
        command=generate_password
    )
    gen_btn.pack(padx=15, pady=10)

    # ---------------- Save Button ----------------
    def save():
        site = site_entry.get().strip()
        username = user_entry.get().strip()
        password = pass_entry.get().strip()

        if site == "" or username == "" or password == "":
            return 
     
        add_callback(site, username, password)

        popup.destroy()

    save_btn = ctk.CTkButton(
        frame,
        text="Save",
        fg_color="#3fb950",
        hover_color="#4ccf61",
        height=40,
        command=save
    )
    save_btn.pack(pady=15)


def open_vault_window(app, key):

    cards.clear()

    for widget in app.winfo_children():
        widget.destroy()
    stored_data=load_vault(key)
    app.title("Password Vault")

    # Main frame
    main_frame = ctk.CTkFrame(app, fg_color="#101018")
    main_frame.pack(fill="both", expand=True)

    # Header
    header = ctk.CTkFrame(main_frame, fg_color="#161625", height=70)
    header.pack(fill="x")

    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)

    # Search bar
    search_entry = ctk.CTkEntry(
        header,
        placeholder_text="Search...",
        width=350,
        height=38
    )
    search_entry.grid(row=0, column=0, padx=20, pady=15)

    # Scroll area
    scroll_area = ctk.CTkScrollableFrame(main_frame, fg_color="#151525")
    scroll_area.pack(fill="both", expand=True)

  
    def add_new_card(site, username, password):
        new_entry = {
        "site": site,
        "username": username,
        "password": password
        }
        raw_data = load_vault(key)
        raw_data.append(new_entry)
        save_vault(raw_data, key)
        card_info = create_password_card(scroll_area, site, username, password, key)
        cards.append(card_info)
        
      

 
    add_btn = ctk.CTkButton(
        header,
        text="+ Add Password",
        width=150,
        height=38,
        fg_color="#6c4cff",
        command=lambda: open_add_password_popup(app, add_new_card)
    )
    add_btn.grid(row=0, column=1, padx=20, pady=15)

    # Search logic
    def search_cards(event=None):
        query = search_entry.get().lower().strip()
        for card in cards:
            if query in card["site"] or query in card["username"]:
                card["frame"].pack(fill="x", padx=20, pady=10)
            else:
                card["frame"].pack_forget()

    search_entry.bind("<KeyRelease>", search_cards)

    # Load saved passwords
    for item in stored_data:
        card_info = create_password_card(
            scroll_area, item["site"], item["username"], item["password"], key
        )
        cards.append(card_info)

def create_password_card(parent, site, username, password , key):

    card = ctk.CTkFrame(
        parent,
        fg_color="#1b1b2b",
        corner_radius=14,
        height=110
    )
    card.pack(fill="x", padx=20, pady=10)
    card_data = {
        "frame": card,
        "site": site.lower(),
        "username": username.lower(),
        "password" : password
    }
    # ---------------- Site ----------------
    site_label = ctk.CTkLabel(
        card,
        text=site,
        font=("Arial", 18, "bold")
    )
    site_label.pack(anchor="w", padx=15, pady=(10,0))

    # ---------------- Username ----------------
    user_label = ctk.CTkLabel(
        card,
        text=f"Username: {username}",
        text_color="#b8b8c8"
    )
    user_label.pack(anchor="w", padx=15)

    # ---------------- Password ----------------
    password_var = ctk.StringVar(value="•"*10)

    pass_label = ctk.CTkLabel(
        card,
        textvariable=password_var,
        font=("Arial", 14)
    )
    pass_label.pack(anchor="w", padx=15, pady=(0,10))

    # ---------------- Buttons Frame ----------------
    btn_frame = ctk.CTkFrame(card, fg_color="transparent")
    btn_frame.pack(anchor="e", padx=15, pady=(0,10))

    # ---------- Copy Button ----------
    def copy_password():
        card.clipboard_clear()
        card.clipboard_append(password)

    copy_btn = ctk.CTkButton(
        btn_frame,
        text="Copy",
        width=70,
        height=30
    )
    copy_btn.pack(side="left", padx=5)

    copy_btn.configure(command=copy_password)

   
    visible = False
    

    def toggle_password():
        nonlocal visible

        visible = not visible

        if visible:
            password_var.set(password)
            show_btn.configure(text="Hide")
        else:
            password_var.set("•"*10)
            show_btn.configure(text="Show")

    show_btn = ctk.CTkButton(
        btn_frame,
        text="Show",
        width=70,
        height=30,
        command=toggle_password
    )
    
    def delete_password():
        card.destroy()
        cards.remove(card_data)
        raw_data = load_vault(key)
        new_data = [
            item for item in raw_data
            if not(
            item["site"] == site and
            item["username"] == username and
            item["password"] == password
            )
        ]

        save_vault(new_data, key)
    delete_btn = ctk.CTkButton(
    btn_frame,
    text="Delete",
    fg_color="#ff4b4b",
    hover_color="#ff6b6b",
    width=70,
    height=30,
    command=delete_password
    )
    delete_btn.pack(side="left", padx=5)
    
   
    def start_edit():
    
        site_label.pack_forget()
        user_label.pack_forget()
        pass_label.pack_forget()

        site_entry = ctk.CTkEntry(card)
        site_entry.insert(0, site)
        site_entry.pack(pady=3)

        username_entry = ctk.CTkEntry(card)
        username_entry.insert(0, username)
        username_entry.pack(pady=3)

        password_entry = ctk.CTkEntry(card)
        password_entry.insert(0, password)
        password_entry.pack(pady=3)

        # ---------- Save ----------
        def save_edit():
            new_site = site_entry.get().strip()
            new_user = username_entry.get().strip()
            new_pass = password_entry.get().strip()

         
            site_label.configure(text=new_site)
            user_label.configure(text=f"Username: {new_user}")
            password_var.set("•" * 10)

     
            site_label.pack(anchor="w", padx=15, pady=(10, 0))
            user_label.pack(anchor="w", padx=15)
            pass_label.pack(anchor="w", padx=15, pady=(0, 10))

            site_entry.destroy()
            username_entry.destroy()
            password_entry.destroy()
            save_btn.destroy()

         
            btn_frame.pack_forget()
            btn_frame.pack(anchor="e", padx=15, pady=(0, 10))

      
            raw_data = load_vault(key)
            for item in raw_data:
                if (
                    item["site"] == site and
                    item["username"] == username and
                    item["password"] == password
                ):
                    item["site"] = new_site
                    item["username"] = new_user
                    item["password"] = new_pass
                    break

            save_vault(raw_data, key)

        
            card_data["site"] = new_site
            card_data["username"] = new_user
            card_data["password"] = new_pass

        save_btn = ctk.CTkButton(card, text="Save", fg_color="#4CAF50", height=33, command=save_edit)
        save_btn.pack(pady=5)

    edit_btn = ctk.CTkButton(btn_frame, text="Edit", width=70, height=30, command=start_edit)
    edit_btn.pack(side="left", padx=5)

  
    show_btn.pack(side="left", padx=5)

    return card_data