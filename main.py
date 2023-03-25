from PIL import Image, ImageSequence
import os
import tkinter as tk
from tkinter import filedialog

# Prompt the user to select the folder containing the images
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory()

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        # Get the file extension
        file_ext = os.path.splitext(filename)[1].lower()
        # Convert webp to png if not animated, or to gif if animated
        if file_ext == '.webp':
            im = Image.open(file_path)
            # Check if the webp image is animated
            is_animated = False
            try:
                for _ in ImageSequence.Iterator(im):
                    is_animated = True
            except:
                pass
            # Convert webp to png if not animated
            if not is_animated:
                im.save(os.path.splitext(file_path)[0] + '.png')
                print(f"Converted {filename} to png")
                os.remove(file_path)
            # Convert webp to gif if animated
            else:
                # Preserve transparency in the gif format
                if im.mode == 'RGBA':
                    im.save(os.path.splitext(file_path)[0] + '.gif', transparency=0)
                    print(f"Converted {filename} to gif (preserving transparency)")
                else:
                    im.convert('RGB').save(os.path.splitext(file_path)[0] + '.gif', transparency=0)
                    print(f"Converted {filename} to gif")
                os.remove(file_path)
        # Convert jfif to png
        elif file_ext == '.jfif':
            im = Image.open(file_path)
            print(f"Converted {filename} to png")
            im.save(os.path.splitext(file_path)[0] + '.png')
            os.remove(file_path)
