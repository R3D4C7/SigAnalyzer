import tkinter as tk
import pyautogui
import keyboard
import threading

# Color mapping for each rarity tier
RARITY_COLORS_LIGHT = {
    "JUNK": "#808080",      # Grey
    "COMMON": "#000000",    # Black (swaps to white in Dark Mode)
    "UNCOMMON": "#2EA44F",  # Green
    "RARE": "#0070DD",      # Blue
    "EPIC": "#A335EE",      # Purple
    "LEGENDARY": "#FF8000", # Gold / Orange
}

RARITY_COLORS_DARK = {
    **RARITY_COLORS_LIGHT,
    "COMMON": "#FFFFFF",    # White for dark mode readability
}

# Base materials structured as: Base Value: (Name, Rarity)
MATERIALS = {
    2000: ("Scrap", "JUNK"),
    3885: ("Agricium", "UNCOMMON"),
    4285: ("Aluminum", "COMMON"),
    3840: ("Aslarite", "UNCOMMON"),
    3540: ("Beryl", "RARE"),
    3600: ("Bexalite", "RARE"),
    3570: ("Borase", "RARE"),
    4240: ("Copper", "COMMON"),
    4225: ("Corundrum", "COMMON"),
    3585: ("Gold", "RARE"),
    4180: ("Hephaestanite", "COMMON"),
    4300: ("Ice", "COMMON"),
    4270: ("Iron", "COMMON"),
    3825: ("Laranite", "UNCOMMON"),
    3400: ("Lindinium", "EPIC"),
    3370: ("Ouratite", "EPIC"),
    3170: ("Quantanium", "LEGENDARY"),
    4210: ("Quartz", "COMMON"),
    3385: ("Riccite", "EPIC"),
    3200: ("Savrilium", "LEGENDARY"),
    4255: ("Silicon", "COMMON"),
    3185: ("Stileron", "LEGENDARY"),
    3555: ("Taranite", "RARE"),
    4195: ("Tin", "COMMON"),
    3855: ("Titanium", "UNCOMMON"),
    3900: ("Torite", "UNCOMMON"),
    3870: ("Tungsten", "UNCOMMON"),
    3000: ("FPS Mineable", "COMMON"),
    4000: ("ROC Mineable", "COMMON"),
}

def focus_and_click_entry():
    """Moves the mouse to the center of the entry box, clicks it, and sets focus."""
    try:
        root.update_idletasks()
        
        # Get absolute position and size of entry widget
        entry_x = entry.winfo_rootx()
        entry_y = entry.winfo_rooty()
        entry_w = entry.winfo_width()
        entry_h = entry.winfo_height()

        # Calculate exact center point of the input box
        click_x = entry_x + (entry_w // 2)
        click_y = entry_y + (entry_h // 2)

        # Move cursor and click inside entry box
        pyautogui.click(click_x, click_y)
        
        # Ensure window and input box gain focus
        root.focus_force()
        entry.focus_set()
    except Exception as e:
        print(f"Error focusing entry box: {e}")

def listen_for_right_ctrl():
    """Background thread to listen for Right Ctrl keypress globally."""
    keyboard.add_hotkey("right ctrl", focus_and_click_entry)

def lookup_material(event=None):
    raw_input = entry.get().strip().lstrip("!")
    
    # Clear the input field immediately
    entry.delete(0, tk.END)
    
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    if raw_input.isdigit():
        value = int(raw_input)
        matches = []

        # Find ALL matching items or multiplier matches
        for base_val, item in MATERIALS.items():
            if value == base_val:
                matches.append((item, None))  # Exact match (1x)
            elif value > base_val and value % base_val == 0:
                multiplier = value // base_val
                matches.append((item, multiplier))

        if matches:
            for idx, (item, multiplier) in enumerate(matches):
                name, rarity = item
                
                # Insert newline before subsequent matches
                if idx > 0:
                    output_text.insert(tk.END, "\n")
                
                # 1. Insert Material Name
                output_text.insert(tk.END, f"{name} ")
                
                # 2. Insert colored square symbol for Rarity
                output_text.insert(tk.END, "■", rarity)
                
                # 3. Insert Multiplier if applicable
                if multiplier:
                    output_text.insert(tk.END, f" ({multiplier}x)")
        else:
            output_text.insert(tk.END, "Unknown")
    else:
        output_text.insert(tk.END, "Unknown")

    output_text.config(state="disabled")

def toggle_always_on_top():
    root.attributes("-topmost", always_on_top_var.get())

def update_opacity(val):
    # Scale ranges between 0.3 (30%) and 1.0 (100%)
    root.attributes("-alpha", float(val))

def toggle_dark_mode():
    is_dark = dark_mode_var.get()
    
    bg_color = "#1E1E1E" if is_dark else "#F0F0F0"
    fg_color = "#FFFFFF" if is_dark else "#000000"
    input_bg = "#2D2D2D" if is_dark else "#FFFFFF"
    btn_bg = "#3A3A3A" if is_dark else "#E1E1E1"
    active_btn_bg = "#4A4A4A" if is_dark else "#ECECEC"
    
    colors_dict = RARITY_COLORS_DARK if is_dark else RARITY_COLORS_LIGHT

    # Main window and frames
    root.config(bg=bg_color)
    footer_frame.config(bg=bg_color)
    options_frame.config(bg=bg_color)
    opacity_frame.config(bg=bg_color)
    legend_frame.config(bg=bg_color, fg=fg_color)

    # Labels
    title_label.config(bg=bg_color, fg=fg_color)
    creator_label.config(bg=bg_color, fg=fg_color)
    opacity_label.config(bg=bg_color, fg=fg_color)

    # Inputs and Text Box
    entry.config(bg=input_bg, fg=fg_color, insertbackground=fg_color)
    output_text.config(bg=input_bg, fg=fg_color)

    # Buttons, Checkbuttons & Scale
    btn.config(bg=btn_bg, fg=fg_color, activebackground=active_btn_bg, activeforeground=fg_color)
    ontop_check.config(bg=bg_color, fg=fg_color, selectcolor=input_bg, activebackground=bg_color, activeforeground=fg_color)
    dark_check.config(bg=bg_color, fg=fg_color, selectcolor=input_bg, activebackground=bg_color, activeforeground=fg_color)
    opacity_scale.config(bg=bg_color, fg=fg_color, activebackground=bg_color, troughcolor=btn_bg)

    # Update Output Text Tags
    for rarity, color in colors_dict.items():
        output_text.tag_config(rarity, foreground=color)

    # Update Legend Items
    for rarity, (item_frame, sq_label, txt_label) in legend_widgets.items():
        item_frame.config(bg=bg_color)
        sq_label.config(bg=bg_color, fg=colors_dict[rarity])
        txt_label.config(bg=bg_color, fg=fg_color)

def on_close():
    """Unbind hotkeys on exit to prevent leftover listeners."""
    keyboard.unhook_all()
    root.destroy()

# Create GUI window
root = tk.Tk()
root.title("SigAnalyzer")
root.geometry("320x390")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_close)

# --- Focused Fallback Keybind ---
# Works within Tkinter natively when window has focus
root.bind("<Control_R>", lambda e: focus_and_click_entry())

# --- Global Hotkey Listener ---
# Listens in a daemon thread so it catches Right Ctrl even when unfocused
hotkey_thread = threading.Thread(target=listen_for_right_ctrl, daemon=True)
hotkey_thread.start()

# --- Footer / Credit Section (Packed FIRST to stick to bottom) ---
footer_frame = tk.Frame(root)
footer_frame.pack(side="bottom", pady=(0, 3))

creator_label = tk.Label(footer_frame, text="Made by the community.", font=("Arial", 8))
creator_label.pack(side="left")

# --- Top and Center Widgets ---
# Input Field
title_label = tk.Label(root, text="Enter signature value:", font=("Arial", 10, "bold"))
title_label.pack(pady=(12, 4))

entry = tk.Entry(root, font=("Arial", 12), justify="center", width=20)
entry.pack(pady=4)
entry.bind("<Return>", lookup_material)

# Lookup Button
btn = tk.Button(
    root,
    text="Search",
    command=lookup_material,
    font=("Arial", 10),
)
btn.pack(pady=4)

# Options Frame (Always On Top & Dark Mode)
options_frame = tk.Frame(root)
options_frame.pack(pady=2)

always_on_top_var = tk.BooleanVar(value=False)
ontop_check = tk.Checkbutton(
    options_frame,
    text="Always On Top",
    variable=always_on_top_var,
    command=toggle_always_on_top,
    font=("Arial", 8)
)
ontop_check.pack(side="left", padx=5)

dark_mode_var = tk.BooleanVar(value=False)
dark_check = tk.Checkbutton(
    options_frame,
    text="Dark Mode",
    variable=dark_mode_var,
    command=toggle_dark_mode,
    font=("Arial", 8)
)
dark_check.pack(side="left", padx=5)

# --- Opacity Slider (Center-aligned directly under the two checkbuttons) ---
opacity_frame = tk.Frame(root)
opacity_frame.pack(pady=(2, 4))

opacity_label = tk.Label(opacity_frame, text="Opacity:", font=("Arial", 8))
opacity_label.pack(side="left", padx=(0, 5))

opacity_scale = tk.Scale(
    opacity_frame,
    from_=1.0,          # 100% Opacity
    to=0.3,            # Minimum opacity capped at 30%
    resolution=0.05,
    orient="horizontal",
    showvalue=False,   # Keep layout clean
    length=110,
    width=10,
    command=update_opacity
)
opacity_scale.set(1.0)
opacity_scale.pack(side="left")

# Output Text Box
output_text = tk.Text(
    root,
    height=4,
    width=25,
    font=("Arial", 10, "bold"),
    wrap="word",
    relief="solid",
    bd=1,
)
output_text.pack(pady=(6, 10))

# Configure Text Tags for colors
for rarity, color in RARITY_COLORS_LIGHT.items():
    output_text.tag_config(rarity, foreground=color)

output_text.config(state="disabled")

# --- Rarity Legend Key ---
legend_frame = tk.LabelFrame(root, text=" Rarity Legend ", font=("Arial", 8, "bold"))
legend_frame.pack(pady=(0, 6), padx=15)

legend_widgets = {}

# Grid layout for legend (2 rows x 3 columns)
for idx, (rarity, color) in enumerate(RARITY_COLORS_LIGHT.items()):
    row = idx // 3
    col = idx % 3
    
    item_frame = tk.Frame(legend_frame)
    item_frame.grid(row=row, column=col, padx=6, pady=2, sticky="w")
    
    # Colored Square Symbol
    sq_label = tk.Label(item_frame, text="■", fg=color, font=("Arial", 9, "bold"))
    sq_label.pack(side="left")
    
    # Rarity Name Label
    txt_label = tk.Label(item_frame, text=rarity.title(), font=("Arial", 8))
    txt_label.pack(side="left", padx=(2, 0))

    legend_widgets[rarity] = (item_frame, sq_label, txt_label)

root.mainloop()
