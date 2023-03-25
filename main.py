import subprocess

from PIL import Image, ImageSequence
import os
import tkinter as tk

from tkinter import filedialog, messagebox
def is_animated_check(im):
    try:
        # Find the number of frames in the image
        im.seek(1)
    except EOFError:
        return False
    else:
        return True

def convert_webp(file_path, output_path):
    # Open the webp image
    with Image.open(file_path) as im:
        # Check if the webp image is animated
        is_animated = is_animated_check(im=im)
        try:
            for _ in ImageSequence.Iterator(im):
                is_animated = True
        except:
            pass
        # Convert webp to png if not animated
        if not is_animated:
            im.save(output_path)
            print(f"Converted {file_path} to png")
        # Convert webp to gif if animated
        else:
            # Extract each frame and save it as png
            frames = []
            for frame in ImageSequence.Iterator(im):
                frames.append(frame.convert("RGBA"))
            # Save each frame as png
            for i, frame in enumerate(frames):
                frame.save(f"{output_path[:-4]}_{i}.png")
            # Convert the png frames to gif
            with Image.open(f"{output_path[:-4]}_0.png") as first_frame:
                first_frame.save(output_path, save_all=True, append_images=frames[1:], optimize=False, duration=im.info['duration'], loop=0)
            # Remove the png frames
            for i in range(len(frames)):
                os.remove(f"{output_path[:-4]}_{i}.png")
            print(f"Converted {file_path} to gif")


# Prompt the user to select the folder containing the images
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory()
confirmation_to_delete_the_previous = messagebox.askyesno("Confirmation", "Do you want to delete the previous images?")
# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        # Get the file extension
        file_ext = os.path.splitext(filename)[1].lower()
        # Convert webp to png if not animated, or to gif if animated
        if file_ext == '.webp':
            if file_ext == '.webp':
                output_path = os.path.splitext(file_path)[0] + '.gif' if is_animated_check else os.path.splitext(file_path)[
                                                                                              0] + '.png'
                convert_webp(file_path, output_path)
                if confirmation_to_delete_the_previous:
                    os.remove(file_path)


        # Convert jfif to png
        elif file_ext == '.jfif':
            im = Image.open(file_path)
            print(f"Converted {filename} to png")
            im.save(os.path.splitext(file_path)[0] + '.png')
            if confirmation_to_delete_the_previous:
                os.remove(file_path)
