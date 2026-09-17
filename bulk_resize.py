"""
Bulk Image Resizer
-------------------
Standalone GUI tool that resizes every image in an input folder to a fixed
125x125 pixel size and saves the results to an output folder.

Run with:  python bulk_resize.py
Requires:  Pillow  (pip install Pillow)
"""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageOps

TARGET_SIZE = (125, 125)
SUPPORTED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".tif", ".webp"
}


class BulkResizeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bulk Image Resizer (125x125)")
        self.geometry("560x360")
        self.resizable(False, False)

        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.status_text = tk.StringVar(value="Choose an input and output folder to begin.")

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        pad = {"padx": 12, "pady": 8}

        title_label = tk.Label(
            self, text="Bulk Image Resizer", font=("Segoe UI", 16, "bold")
        )
        title_label.pack(anchor="w", padx=12, pady=(14, 0))

        subtitle_label = tk.Label(
            self,
            text=f"Resizes every image to {TARGET_SIZE[0]}x{TARGET_SIZE[1]} px",
            font=("Segoe UI", 10),
            fg="#555555",
        )
        subtitle_label.pack(anchor="w", padx=12, pady=(0, 10))

        # Input folder row
        input_frame = tk.Frame(self)
        input_frame.pack(fill="x", **pad)
        tk.Label(input_frame, text="Input folder:", width=14, anchor="w").pack(side="left")
        tk.Entry(input_frame, textvariable=self.input_folder).pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )
        tk.Button(input_frame, text="Browse...", command=self.browse_input).pack(side="left")

        # Output folder row
        output_frame = tk.Frame(self)
        output_frame.pack(fill="x", **pad)
        tk.Label(output_frame, text="Output folder:", width=14, anchor="w").pack(side="left")
        tk.Entry(output_frame, textvariable=self.output_folder).pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )
        tk.Button(output_frame, text="Browse...", command=self.browse_output).pack(side="left")

        # Options
        options_frame = tk.Frame(self)
        options_frame.pack(fill="x", **pad)
        self.keep_aspect = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Keep aspect ratio (pad with white background to fit 125x125)",
            variable=self.keep_aspect,
        ).pack(anchor="w")

        # Run button
        run_frame = tk.Frame(self)
        run_frame.pack(fill="x", **pad)
        self.run_button = tk.Button(
            run_frame, text="Resize Images", command=self.start_resize,
            bg="#2d6cdf", fg="white", font=("Segoe UI", 11, "bold"), height=2
        )
        self.run_button.pack(fill="x")

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=12, pady=(4, 4))

        # Status label
        status_label = tk.Label(
            self, textvariable=self.status_text, anchor="w", justify="left",
            wraplength=530, fg="#333333"
        )
        status_label.pack(fill="x", padx=12, pady=(4, 12))

    # ---------- Actions ----------
    def browse_input(self):
        folder = filedialog.askdirectory(title="Select input folder")
        if folder:
            self.input_folder.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder.set(folder)

    def start_resize(self):
        in_folder = self.input_folder.get().strip()
        out_folder = self.output_folder.get().strip()

        if not in_folder or not os.path.isdir(in_folder):
            messagebox.showerror("Error", "Please choose a valid input folder.")
            return
        if not out_folder:
            messagebox.showerror("Error", "Please choose an output folder.")
            return

        os.makedirs(out_folder, exist_ok=True)

        self.run_button.config(state="disabled")
        self.status_text.set("Scanning input folder...")
        thread = threading.Thread(
            target=self.resize_all, args=(in_folder, out_folder, self.keep_aspect.get())
        )
        thread.daemon = True
        thread.start()

    def resize_all(self, in_folder, out_folder, keep_aspect):
        files = [
            f for f in sorted(os.listdir(in_folder))
            if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
        ]

        total = len(files)
        if total == 0:
            self.after(0, lambda: self.status_text.set("No supported images found in the input folder."))
            self.after(0, lambda: self.run_button.config(state="normal"))
            return

        self.after(0, lambda: self.progress.config(maximum=total, value=0))

        succeeded = 0
        failed = []

        for index, filename in enumerate(files, start=1):
            src_path = os.path.join(in_folder, filename)
            name, ext = os.path.splitext(filename)
            dest_path = os.path.join(out_folder, f"{name}.png")

            try:
                with Image.open(src_path) as img:
                    img = ImageOps.exif_transpose(img)  # respect rotation metadata
                    has_alpha = img.mode in ("RGBA", "LA") or (
                        img.mode == "P" and "transparency" in img.info
                    )
                    img = img.convert("RGBA") if has_alpha else img.convert("RGB")

                    if keep_aspect:
                        resized = ImageOps.contain(img, TARGET_SIZE)
                        canvas = Image.new("RGBA", TARGET_SIZE, (0, 0, 0, 0))
                        offset = (
                            (TARGET_SIZE[0] - resized.width) // 2,
                            (TARGET_SIZE[1] - resized.height) // 2,
                        )
                        if resized.mode == "RGBA":
                            canvas.paste(resized, offset, resized)
                        else:
                            canvas.paste(resized, offset)
                        if not has_alpha:
                            canvas = canvas.convert("RGB")
                        canvas.save(dest_path)
                    else:
                        stretched = img.resize(TARGET_SIZE, Image.LANCZOS)
                        stretched.save(dest_path)

                succeeded += 1
            except Exception as exc:
                failed.append(f"{filename}: {exc}")

            progress_value = index
            self.after(0, lambda v=progress_value: self.progress.config(value=v))
            self.after(0, lambda i=index, t=total: self.status_text.set(f"Processing {i} of {t}..."))

        summary = f"Done. {succeeded} of {total} images resized to {TARGET_SIZE[0]}x{TARGET_SIZE[1]}."
        if failed:
            summary += f" {len(failed)} failed."
            summary += "\n" + "\n".join(failed[:5])
            if len(failed) > 5:
                summary += f"\n...and {len(failed) - 5} more."

        self.after(0, lambda: self.status_text.set(summary))
        self.after(0, lambda: self.run_button.config(state="normal"))


if __name__ == "__main__":
    app = BulkResizeApp()
    app.mainloop()
