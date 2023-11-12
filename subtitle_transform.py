import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

def transform_to_sentence_case_refined(text):
    if text.startswith('[') and text.endswith(']'):
        return text
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    transformed_text = ' '.join([sentence.capitalize() for sentence in sentences])
    # Replace standalone 'i' with 'I'
    transformed_text = re.sub(r'\bi\b', 'I', transformed_text)
    return transformed_text

def process_srt_file_refined(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        inside_subtitle_block = False
        subtitle_lines = []
        for line in infile:
            line = line.rstrip()
            if line.strip().isdigit():
                if inside_subtitle_block:
                    transformed_block = transform_to_sentence_case_refined(" ".join(subtitle_lines))
                    outfile.write(transformed_block + "\n")
                    subtitle_lines = []
                outfile.write(line + "\n")
                inside_subtitle_block = True
            elif re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
                outfile.write(line + "\n")
            elif inside_subtitle_block and line == "":
                transformed_block = transform_to_sentence_case_refined(" ".join(subtitle_lines))
                outfile.write(transformed_block + "\n\n")
                inside_subtitle_block = False
                subtitle_lines = []
            elif inside_subtitle_block:
                subtitle_lines.append(line)
            else:
                outfile.write(line + "\n")

def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("SRT Files", "*.srt"), ("All Files", "*.*")])
    if filepath:
        entry_filepath.delete(0, tk.END)
        entry_filepath.insert(0, filepath)

def process_and_download():
    input_path = entry_filepath.get()
    if not input_path:
        messagebox.showwarning("Warning", "Please select an SRT file first!")
        return
    output_path = os.path.splitext(input_path)[0] + "_transformed.srt"
    process_srt_file_refined(input_path, output_path)
    messagebox.showinfo("Success", f"File processed successfully! Saved as: {output_path}")

app = tk.Tk()
app.title("Subtitle Transformer")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

lbl_intro = tk.Label(frame, text="Select an SRT file to transform subtitles to sentence case:")
lbl_intro.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

entry_filepath = tk.Entry(frame, width=50)
entry_filepath.grid(row=1, column=0, padx=(0, 10))

btn_browse = tk.Button(frame, text="Browse File", command=browse_file)
btn_browse.grid(row=1, column=1)

btn_process = tk.Button(frame, text="Process and Download", command=process_and_download)
btn_process.grid(row=2, column=0, columnspan=2, pady=(10, 0))

app.mainloop()