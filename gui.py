import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageEnhance, ImageOps
import customtkinter as ctk
# =========================
# THEME
# =========================

ctk.set_appearance_mode("dark")

CANVAS_BG = "#0A0A0A"
LEFT_BAR = "#161616"
TOP_BAR = "#171717"
PANEL_BG = "#202020"

PRIMARY = "#CDB4FF"
HOVER = "#BFA2FF"
ACCENT = "#FFCAD4"

TEXT = "#F8F8F8"


# ========================
#  IMAGE VARIABLES
# ========================

original_image = None
current_image = None
displayed_image = None
brightness_base_image = None
contrast_base_image = None


history = []


def save_state(operation_name):
    global current_image, history

    if current_image is not None:
        history.append(
            (current_image.copy(), operation_name)
        )

def undo():
    global current_image, history

    if not history:
        status_label.configure(
            text="Status: Nothing to Undo"
        )
        return

    previous_image, operation = history.pop()

    current_image = previous_image

    update_canvas()

    status_label.configure(
        text=f"Status: Undid {operation}"
    )

def reset_image():
    global original_image, current_image, history

    if original_image is None:
        return

    current_image = original_image.copy()

    history.clear()

    update_canvas()

    status_label.configure(
        text="Status: Image Reset"
    )

def update_canvas():
    global current_image, display_image_obj

    if current_image is None:
        return

    img = current_image.copy()

    # Fit into canvas area
    img.thumbnail((750, 500))

    display_image_obj = ctk.CTkImage(
        light_image=img,
        dark_image=img,
        size=img.size
    )

    canvas_label.configure(image=display_image_obj, text="")

def open_image():
    global original_image, current_image

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )

    if not file_path:
        return

    original_image = Image.open(file_path)
    current_image = original_image.copy()

    update_canvas()

    status_label.configure(text="Status: Image Loaded")

def display_image():
    global current_image, displayed_image

    if current_image is None:
        return

    img = current_image.copy()

    img.thumbnail((700, 500))

    displayed_image = ctk.CTkImage(
        light_image=img,
        dark_image=img,
        size=img.size
    )

    canvas_label.configure(
        image=displayed_image,
        text=""
    )

def save_image():
    global current_image

    if current_image is None:
        status_label.configure(
            text="Status: No Image To Save"
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("BMP Image", "*.bmp")
        ]
    )

    if not file_path:
        return

    current_image.save(file_path)

    status_label.configure(
        text="Status: Image Saved Successfully"
    )

def grayscale():
    global current_image

    if current_image is None:
        return

    save_state("Grayscale")

    current_image = ImageOps.grayscale(
        current_image
    ).convert("RGB")

    update_canvas()

    status_label.configure(
        text="Status: Applied Grayscale"
    )


def darken():
    global current_image

    if current_image is None:
        return

    save_state("Darken")

    enhancer = ImageEnhance.Brightness(
        current_image
    )

    current_image = enhancer.enhance(0.6)

    update_canvas()

    status_label.configure(
        text="Status: Applied Darken"
    )

def negative():
    global current_image

    if current_image is None:
        return

    save_state("Negative")

    current_image = ImageOps.invert(
        current_image
    )

    update_canvas()

    status_label.configure(
        text="Status: Applied Negative"
    )

def red_filter():
    global current_image

    if current_image is None:
        return

    save_state("Red Filter")

    r, g, b = current_image.split()

    current_image = Image.merge(
        "RGB",
        (
            r,
            Image.new("L", g.size, 0),
            Image.new("L", b.size, 0)
        )
    )

    update_canvas()

    status_label.configure(
        text="Status: Applied Red Filter"
    )

def rotate_right():
    global current_image

    if current_image is None:
        return

    save_state("Rotate Right")

    current_image = current_image.rotate(
        -90,
        expand=True
    )

    update_canvas()

    status_label.configure(
        text="Status: Rotated Right"
    )


def rotate_left():
    global current_image

    if current_image is None:
        return

    save_state("Rotate Left")

    current_image = current_image.rotate(
        90,
        expand=True
    )

    update_canvas()

    status_label.configure(
        text="Status: Rotated Left"
    )

def flip_horizontal():
    global current_image

    if current_image is None:
        return

    save_state("Flip Horizontal")

    current_image = current_image.transpose(
        Image.FLIP_LEFT_RIGHT
    )

    update_canvas()

    status_label.configure(
        text="Status: Flipped Horizontal"
    )

def flip_horizontal():
    global current_image

    if current_image is None:
        return

    save_state("Flip Horizontal")

    current_image = current_image.transpose(
        Image.FLIP_LEFT_RIGHT
    )

    update_canvas()

    status_label.configure(
        text="Status: Flipped Horizontal"
    )

def flip_vertical():
    global current_image

    if current_image is None:
        return

    save_state("Flip Vertical")

    current_image = current_image.transpose(
        Image.FLIP_TOP_BOTTOM
    )

    update_canvas()

    status_label.configure(
        text="Status: Flipped Vertical"
    )

def clear_right_panel():
    for widget in right_panel.winfo_children():
        widget.destroy()

def show_brightness_panel():
    global brightness_base_image

    if current_image is None:
        return

    brightness_base_image = current_image.copy()

    clear_right_panel()

    title = ctk.CTkLabel(
        right_panel,
        text="Brightness",
        text_color=TEXT
    )
    title.pack(pady=15)

    value_label = ctk.CTkLabel(
        right_panel,
        text="1.0",
        text_color=TEXT
    )
    value_label.pack()

    def update_brightness(value):
        global current_image

        factor = float(value)

        enhanced = ImageEnhance.Brightness(
            brightness_base_image
        ).enhance(factor)

        current_image = enhanced

        update_canvas()

        value_label.configure(
            text=f"{factor:.2f}"
        )

        status_label.configure(
            text=f"Status: Brightness {factor:.2f}"
        )
    slider = ctk.CTkSlider(
        right_panel,
        from_=0.1,
        to=2.0,
        command=update_brightness
    )

    slider.set(1.0)

    slider.pack(
        padx=20,
        pady=15,
        fill="x"
    )


def show_contrast_panel():
    global contrast_base_image

    if current_image is None:
        return

    contrast_base_image = current_image.copy()

    clear_right_panel()

    title = ctk.CTkLabel(
        right_panel,
        text="Contrast",
        text_color=TEXT
    )
    title.pack(pady=15)

    value_label = ctk.CTkLabel(
        right_panel,
        text="1.0",
        text_color=TEXT
    )
    value_label.pack()

    def update_contrast(value):
        global current_image

        factor = float(value)

        enhanced = ImageEnhance.Contrast(
            contrast_base_image
        ).enhance(factor)

        current_image = enhanced

        update_canvas()

        value_label.configure(
            text=f"{factor:.2f}"
        )

        status_label.configure(
            text=f"Status: Contrast {factor:.2f}"
        )
    slider = ctk.CTkSlider(
        right_panel,
        from_=0.1,
        to=2.0,
        command=update_contrast
    )

    slider.set(1.0)

    slider.pack(
        padx=20,
        pady=15,
        fill="x"
    )

def show_crop_panel():

    if current_image is None:
        return

    clear_right_panel()

    title = ctk.CTkLabel(
        right_panel,
        text="Crop",
        text_color=TEXT
    )
    title.pack(pady=10)

    # ENTRY BOXES GO HERE

    left_entry = ctk.CTkEntry(
        right_panel,
        placeholder_text="Left"
    )
    left_entry.pack(padx=10, pady=5)

    top_entry = ctk.CTkEntry(
        right_panel,
        placeholder_text="Top"
    )
    top_entry.pack(padx=10, pady=5)

    right_entry = ctk.CTkEntry(
        right_panel,
        placeholder_text="Right"
    )
    right_entry.pack(padx=10, pady=5)

    bottom_entry = ctk.CTkEntry(
        right_panel,
        placeholder_text="Bottom"
    )
    bottom_entry.pack(padx=10, pady=5)

    # APPLY CROP FUNCTION GOES HERE

    def apply_crop():
        global current_image

        try:
            left = int(left_entry.get() or 0)
            top = int(top_entry.get() or 0)
            right = int(right_entry.get() or 0)
            bottom = int(bottom_entry.get() or 0)

            save_state("Crop")

            width, height = current_image.size

            current_image = current_image.crop(
                (
                    left,
                    top,
                    width - right,
                    height - bottom
                )
            )

            update_canvas()

            status_label.configure(
                text="Status: Crop Applied"
            )

        except ValueError:
            status_label.configure(
                text="Status: Invalid Crop Values"
            )
    
    # APPLY BUTTON GOES HERE

    apply_btn = ctk.CTkButton(
        right_panel,
        text="Apply Crop",
        text_color="black",
        fg_color=PRIMARY,
        command=apply_crop
    )
    apply_btn.pack(pady=15)

# =========================
# MAIN WINDOW
# =========================

root = ctk.CTk()
root.title("Image Editor")
root.geometry("1200x700")
root.minsize(900, 600)

# =========================
# TOP BAR
# =========================

top_bar = ctk.CTkFrame(
    root,
    fg_color=TOP_BAR,
    height=60,
    corner_radius=0
)

top_bar.pack(fill="x")

logo_label = ctk.CTkLabel(
    top_bar,
    text="ImageEditor",
    text_color="red",
    font=("Snell Roundhand", 30, "bold")
)

logo_label.pack(
    side="left",
    padx=(15, 30),
    pady=10
)
# Open button (left)

open_btn = ctk.CTkButton(
    top_bar,
    text="Open",
    fg_color="#FFFFE4",
    hover_color="#EDEDCB",
    text_color="black",
    command=open_image
)
open_btn.pack(
    side="left",
    padx=15,
    pady=10
)

# Right-side buttons

right_buttons = ctk.CTkFrame(
    top_bar,
    fg_color="transparent"
)

right_buttons.pack(
    side="right",
    padx=15
)

save_btn = ctk.CTkButton(
    right_buttons,
    text="Save",
    fg_color="#70DB70",
    hover_color="#52D452",
    text_color="black",
    width=90,
    command=save_image
)

undo_btn = ctk.CTkButton(
    right_buttons,
    text="Undo",
    fg_color=PRIMARY,
    hover_color=HOVER,
    text_color="black",
    width=90,
    command=undo
)



reset_btn = ctk.CTkButton(
    right_buttons,
    text="Reset",
    fg_color=PRIMARY,
    hover_color=HOVER,
    text_color="black",
    width=90,
    command=reset_image
)

exit_btn = ctk.CTkButton(
    right_buttons,
    text="Exit",
    fg_color="#FFCBE1",
    hover_color="#FC8EAC",
    text_color="black",
    width=90,
    command=root.destroy
)


undo_btn.pack(side="left", padx=5)
reset_btn.pack(side="left", padx=5)
save_btn.pack(side="left", padx=5)
exit_btn.pack(side="left", padx=5)

# =========================
# WORKSPACE
# =========================

workspace = ctk.CTkFrame(
    root,
    fg_color="transparent"
)

workspace.pack(
    fill="both",
    expand=True
)

# =========================
# LEFT TOOLBAR (ACCORDION)
# =========================

left_panel = ctk.CTkFrame(
    workspace,
    fg_color=LEFT_BAR,
    width=180,
    corner_radius=0
)
left_panel.pack(side="left", fill="y")
left_panel.pack_propagate(False)

#------------------filters----------------------
filters_label = ctk.CTkLabel(left_panel, text="Filters", text_color=TEXT)
filters_label.pack(pady=(15,5))


filters_btn = ctk.CTkButton(
    left_panel,
    text="Filters",
    fg_color="#202020",
    hover_color="#2A2A2A",
    text_color=TEXT,
    
)



ctk.CTkButton(left_panel, text="Grayscale", command=grayscale, fg_color=PRIMARY, hover_color=HOVER,
              text_color="black").pack(fill="x", padx=10, pady=2)

ctk.CTkButton(left_panel, text="Darken", command=darken, fg_color=PRIMARY, hover_color=HOVER,
              text_color="black").pack(fill="x", padx=10, pady=2)

ctk.CTkButton(left_panel, text="Negative", command=negative,fg_color=PRIMARY, hover_color=HOVER,
              text_color="black").pack(fill="x", padx=10, pady=2)

ctk.CTkButton(left_panel, text="Red Filter", command=red_filter, fg_color=PRIMARY, hover_color=HOVER,
              text_color="black").pack(fill="x", padx=10, pady=(2,15))


#------------------------effects---------------------------------




effects_btn = ctk.CTkButton(
    left_panel,
    text="Effects",
    fg_color="#202020",
    hover_color="#2A2A2A",
    text_color=TEXT,
    
)

ctk.CTkLabel(left_panel, text="Effects", text_color=TEXT).pack(pady=(10,5))

ctk.CTkButton(left_panel, text="Brightness", command=show_brightness_panel, fg_color=PRIMARY,
              hover_color=HOVER, text_color="black").pack(fill="x", padx=10, pady=2)

ctk.CTkButton(left_panel, text="Contrast", command=show_contrast_panel, fg_color=PRIMARY,
              hover_color=HOVER, text_color="black").pack(fill="x", padx=10, pady=(2,15))


#----------------------transform---------------------------------





transform_btn = ctk.CTkButton(
    left_panel,
    text="Transform",
    fg_color="#202020",
    hover_color="#2A2A2A",
    text_color=TEXT,
    
)

ctk.CTkLabel(left_panel, text="Transform", text_color=TEXT).pack(pady=(10,5))

ctk.CTkButton(left_panel, text="Rotate Right", command=rotate_right, fg_color=PRIMARY,
              hover_color=HOVER, text_color="black").pack(fill="x", padx=10, pady=2)

ctk.CTkButton(left_panel, text="Rotate Left", command=rotate_left, fg_color=PRIMARY,
              hover_color=HOVER, text_color="black").pack(fill="x", padx=10, pady=2)

ctk.CTkButton(left_panel, text="Flip Horizontal", command=flip_horizontal, fg_color=PRIMARY,
              hover_color=HOVER, text_color="black").pack(fill="x", padx=10, pady=2)

ctk.CTkButton(left_panel, text="Flip Vertical", command=flip_vertical, fg_color=PRIMARY,
              hover_color=HOVER, text_color="black").pack(fill="x", padx=10, pady=15)
ctk.CTkButton(
    left_panel,
    text="Crop",
    command=show_crop_panel,
    fg_color=PRIMARY,
    hover_color=HOVER,
    text_color="black"
).pack(fill="x", padx=10, pady=2)



# =========================
# CENTER CANVAS
# =========================

canvas_frame = ctk.CTkFrame(
    workspace,
    fg_color=CANVAS_BG,
    corner_radius=0
)

canvas_frame.pack(
    side="left",
    fill="both",
    expand=True
)

canvas_label = ctk.CTkLabel(
    canvas_frame,
    text="CANVAS AREA",
    text_color=TEXT,
    font=("Arial", 22)
)

canvas_label.pack(expand=True)

# =========================
# RIGHT PANEL
# =========================

right_panel = ctk.CTkFrame(
    workspace,
    fg_color=PANEL_BG,
    width=220,
    corner_radius=0
)

right_panel.pack(
    side="right",
    fill="y"
)

right_panel.pack_propagate(False)

future_label = ctk.CTkLabel(
    right_panel,
    text="Future Panel",
    text_color=TEXT
)

future_label.pack(pady=20)

# =========================
# STATUS BAR
# =========================

status_bar = ctk.CTkFrame(
    root,
    fg_color=TOP_BAR,
    height=35,
    corner_radius=0
)

status_bar.pack(fill="x")

status_label = ctk.CTkLabel(
    status_bar,
    text="Status: Ready",
    text_color=TEXT
)

status_label.pack(
    side="left",
    padx=10
)

# =========================
# RUN
# =========================

root.mainloop()