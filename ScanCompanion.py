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

# Default Window Size Configuration
BASE_WIDTH = 300
BASE_HEIGHT = 440

def focus_and_click_entry():
    """Moves the mouse to the center of the entry box, clicks it, and sets focus."""
    try:
        root.update_idletasks()
        
        entry_x = entry.winfo_rootx()
        entry_y = entry.winfo_rooty()
        entry_w = entry.winfo_width()
        entry_h = entry.winfo_height()

        click_x = entry_x + (entry_w // 2)
        click_y = entry_y + (entry_h // 2)

        pyautogui.click(click_x, click_y)
        
        root.focus_force()
        entry.focus_set()
    except Exception as e:
        print(f"Error focusing entry box: {e}")

def listen_for_caps_lock():
    """Background thread to listen for Caps Lock keypress globally."""
    keyboard.add_hotkey("caps lock", focus_and_click_entry)

def lookup_material(event=None):
    raw_input = entry.get().strip().lstrip("!")
    
    entry.delete(0, tk.END)
    
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    if raw_input.isdigit():
        value = int(raw_input)
        matches = []

        for base_val, item in MATERIALS.items():
            if value == base_val:
                matches.append((item, None))  # Exact match (1x)
            elif value > base_val and value % base_val == 0:
                multiplier = value // base_val
                matches.append((item, multiplier))

        if matches:
            for idx, (item, multiplier) in enumerate(matches):
                name, rarity = item
                
                if idx > 0:
                    output_text.insert(tk.END, "\n")
                
                output_text.insert(tk.END, f"{name} ")
                output_text.insert(tk.END, "■", rarity)
                
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
    root.attributes("-alpha", float(val))

def update_scale(val):
    """Dynamically resizes the window while keeping top-left position standard."""
    factor = float(val)
    new_w = int(BASE_WIDTH * factor)
    new_h = int(BASE_HEIGHT * factor)
    
    x = root.winfo_x()
    y = root.winfo_y()
    root.geometry(f"{new_w}x{new_h}+{x}+{y}")

def toggle_dark_mode():
    is_dark = dark_mode_var.get()
    
    bg_color = "#1E1E1E" if is_dark else "#F0F0F0"
    fg_color = "#FFFFFF" if is_dark else "#000000"
    border_color = "#444444" if is_dark else "#A0A0A0"
    input_bg = "#2D2D2D" if is_dark else "#FFFFFF"
    btn_bg = "#3A3A3A" if is_dark else "#E1E1E1"
    active_btn_bg = "#4A4A4A" if is_dark else "#ECECEC"
    
    colors_dict = RARITY_COLORS_DARK if is_dark else RARITY_COLORS_LIGHT

    # Main window and frames
    root.config(bg=bg_color)
    main_container.config(bg=bg_color, highlightbackground=border_color)
    header_frame.config(bg=bg_color)
    footer_frame.config(bg=bg_color)
    options_frame.config(bg=bg_color)
    sliders_frame.config(bg=bg_color)
    opacity_frame.config(bg=bg_color)
    scale_frame.config(bg=bg_color)
    legend_frame.config(bg=bg_color, fg=fg_color)

    # Labels & Title
    app_title_label.config(bg=bg_color, fg=fg_color)
    title_label.config(bg=bg_color, fg=fg_color)
    creator_label.config(bg=bg_color, fg=fg_color)
    opacity_label.config(bg=bg_color, fg=fg_color)
    size_label.config(bg=bg_color, fg=fg_color)

    # Close Button
    close_btn.config(bg=bg_color, fg=fg_color, activebackground="#FF4D4D", activeforeground="#FFFFFF")

    # Inputs and Text Box
    entry.config(bg=input_bg, fg=fg_color, insertbackground=fg_color)
    output_text.config(bg=input_bg, fg=fg_color)

    # Buttons, Checkbuttons & Scale
    btn.config(bg=btn_bg, fg=fg_color, activebackground=active_btn_bg, activeforeground=fg_color)
    ontop_check.config(bg=bg_color, fg=fg_color, selectcolor=input_bg, activebackground=bg_color, activeforeground=fg_color)
    dark_check.config(bg=bg_color, fg=fg_color, selectcolor=input_bg, activebackground=bg_color, activeforeground=fg_color)
    lock_check.config(bg=bg_color, fg=fg_color, selectcolor=input_bg, activebackground=bg_color, activeforeground=fg_color)
    opacity_scale.config(bg=bg_color, fg=fg_color, activebackground=bg_color, troughcolor=btn_bg)
    size_scale.config(bg=bg_color, fg=fg_color, activebackground=bg_color, troughcolor=btn_bg)

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
    try:
        keyboard.unhook_all()
    except Exception:
        pass
    root.destroy()

# --- Drag Mechanics ---
def start_drag(event):
    if lock_pos_var.get():
        return
    root._drag_start_x = event.x_root - root.winfo_x()
    root._drag_start_y = event.y_root - root.winfo_y()

def do_drag(event):
    if lock_pos_var.get():
        return
    x = event.x_root - root._drag_start_x
    y = event.y_root - root._drag_start_y
    root.geometry(f"+{x}+{y}")

def bind_drag_events(widget):
    """Recursively binds drag events to background/label widgets."""
    if not isinstance(widget, (tk.Entry, tk.Button, tk.Checkbutton, tk.Scale, tk.Text)):
        widget.bind("<Button-1>", start_drag)
        widget.bind("<B1-Motion>", do_drag)
    for child in widget.winfo_children():
        bind_drag_events(child)

# Create GUI window
root = tk.Tk()
root.title("ScanCompanion")

# Remove Title Bar & Window Controls
root.overrideredirect(True)

root.geometry(f"{BASE_WIDTH}x{BASE_HEIGHT}")
root.resizable(False, False)

# --- Outer Border Container Frame ---
main_container = tk.Frame(root, highlightthickness=2, highlightbackground="#A0A0A0", bg="#F0F0F0")
main_container.pack(fill="both", expand=True)

# --- Focused Fallback Keybind ---
root.bind("\\", lambda e: focus_and_click_entry())

# --- Global Hotkey Listener ---
hotkey_thread = threading.Thread(target=listen_for_caps_lock, daemon=True)
hotkey_thread.start()

# --- Header Section (App Title + Close Button) ---
header_frame = tk.Frame(main_container, bg="#F0F0F0")
header_frame.pack(fill="x", padx=5, pady=(4, 0))

app_title_label = tk.Label(header_frame, text="ScanCompanion", font=("Arial", 12, "bold"), bg="#F0F0F0")
app_title_label.pack(side="left", padx=(5, 0))

close_btn = tk.Button(
    header_frame,
    text="✕",
    font=("Arial", 10, "bold"),
    bg="#F0F0F0",
    fg="#000000",
    bd=0,
    padx=6,
    pady=0,
    activebackground="#FF4D4D",
    activeforeground="#FFFFFF",
    command=on_close,
    cursor="hand2"
)
close_btn.pack(side="right")

# --- Footer Section (Trimmed Space) ---
footer_frame = tk.Frame(main_container, bg="#F0F0F0")
footer_frame.pack(side="bottom", pady=(0, 2))

creator_label = tk.Label(footer_frame, text="Made by The Community.", font=("Arial", 7), bg="#F0F0F0")
creator_label.pack()

# --- Core Content Area ---
title_label = tk.Label(main_container, text="Enter signature value:", font=("Arial", 8, "bold"))
title_label.pack(pady=(2, 2))

entry = tk.Entry(main_container, font=("Arial", 11), justify="center", width=18)
entry.pack(pady=2)
entry.bind("<Return>", lookup_material)

btn = tk.Button(
    main_container,
    text="Search",
    command=lookup_material,
    font=("Arial", 9),
    pady=1
)
btn.pack(pady=2)

# --- Checkbox Controls Area ---
options_frame = tk.Frame(main_container)
options_frame.pack(pady=1)

always_on_top_var = tk.BooleanVar(value=False)
ontop_check = tk.Checkbutton(
    options_frame,
    text="Always On Top",
    variable=always_on_top_var,
    command=toggle_always_on_top,
    font=("Arial", 8)
)
ontop_check.grid(row=0, column=0, padx=3, pady=0)

dark_mode_var = tk.BooleanVar(value=False)
dark_check = tk.Checkbutton(
    options_frame,
    text="Dark Mode",
    variable=dark_mode_var,
    command=toggle_dark_mode,
    font=("Arial", 8)
)
dark_check.grid(row=0, column=1, padx=3, pady=0)

lock_pos_var = tk.BooleanVar(value=False)
lock_check = tk.Checkbutton(
    options_frame,
    text="Lock Position",
    variable=lock_pos_var,
    font=("Arial", 8)
)
lock_check.grid(row=1, column=0, columnspan=2, pady=0)

# --- Combined Sliders Frame (Opacity & Size) ---
sliders_frame = tk.Frame(main_container)
sliders_frame.pack(pady=2)

# Opacity Row
opacity_frame = tk.Frame(sliders_frame)
opacity_frame.pack(anchor="e", pady=1)

opacity_label = tk.Label(opacity_frame, text="Opacity:", font=("Arial", 8))
opacity_label.pack(side="left", padx=(0, 4))

opacity_scale = tk.Scale(
    opacity_frame,
    from_=1.0,
    to=0.3,
    resolution=0.05,
    orient="horizontal",
    showvalue=False,
    length=100,
    width=8,
    command=update_opacity
)
opacity_scale.set(1.0)
opacity_scale.pack(side="left")

# Size Row
scale_frame = tk.Frame(sliders_frame)
scale_frame.pack(anchor="e", pady=1)

size_label = tk.Label(scale_frame, text="Size:", font=("Arial", 8))
size_label.pack(side="left", padx=(0, 4))

size_scale = tk.Scale(
    scale_frame,
    from_=1.0,
    to=0.7,
    resolution=0.05,
    orient="horizontal",
    showvalue=False,
    length=100,
    width=8,
    command=update_scale
)
size_scale.set(1.0)
size_scale.pack(side="left")

# Output Text Area
output_text = tk.Text(
    main_container,
    height=3,
    width=24,
    font=("Arial", 9, "bold"),
    wrap="word",
    relief="solid",
    bd=1,
)
output_text.pack(pady=(4, 4))

for rarity, color in RARITY_COLORS_LIGHT.items():
    output_text.tag_config(rarity, foreground=color)

output_text.config(state="disabled")

# --- Rarity Legend Frame ---
legend_frame = tk.LabelFrame(main_container, text=" Rarity Legend ", font=("Arial", 8, "bold"))
legend_frame.pack(pady=(0, 2), padx=10)

legend_widgets = {}

for idx, (rarity, color) in enumerate(RARITY_COLORS_LIGHT.items()):
    row = idx // 3
    col = idx % 3
    
    item_frame = tk.Frame(legend_frame)
    item_frame.grid(row=row, column=col, padx=4, pady=1, sticky="w")
    
    sq_label = tk.Label(item_frame, text="■", fg=color, font=("Arial", 8, "bold"))
    sq_label.pack(side="left")
    
    txt_label = tk.Label(item_frame, text=rarity.title(), font=("Arial", 7))
    txt_label.pack(side="left", padx=(1, 0))

    legend_widgets[rarity] = (item_frame, sq_label, txt_label)

# Attach click-and-drag logic automatically to all non-interactive background areas
bind_drag_events(main_container)

root.mainloop()
