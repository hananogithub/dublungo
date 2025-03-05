import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import PhotoImage

# メインウィンドウ作成
root = tk.Tk()
root.title("Dublungo Translator")
root.geometry("1200x400")

up_image = PhotoImage(file="./pics/up.png")
down_image = PhotoImage(file="./pics/down.png")
speaker_image = PhotoImage(file="./pics/speaker.png")

# 原文エリア
label_input = tk.Label(root, text="原文:", bg = 'pink1')
label_input.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
orig_file_button1 = tk.Button(root, text="ファイル読みこみ")
orig_file_button1.grid(row=0, column=1, padx=10, pady=5, sticky=tk.E)
text_input = scrolledtext.ScrolledText(root, width=40, height=15)
text_input.grid(row=1, column=0, padx=10, pady=5, columnspan=2, rowspan=2)

orig_up_button = tk.Button(root, image=up_image)
orig_up_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.N)
orig_down_button = tk.Button(root, image=down_image)
orig_down_button.grid(row=2, column=2, padx=5, pady=5, sticky=tk.S)
orig_speaker_button = tk.Button(root, image=speaker_image)
orig_speaker_button.grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)

# 自動翻訳エリア
label_autotrans = tk.Label(root, text="自動翻訳:", bg = 'green1')
label_autotrans.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)
option = ["", "日本語", "英語"]
combo = ttk.Combobox(root, values=option, textvariable=tk.StringVar( ), state="readonly", width=10)
combo.grid(row=0, column=4, padx=5, pady=5, sticky=tk.E)
text_autotrans = scrolledtext.ScrolledText(root, width=40, height=15)
text_autotrans.grid(row=1, column=3, padx=10, pady=5, columnspan=2, rowspan=2, sticky=tk.S)

autotrans_speaker_button = tk.Button(root, image=speaker_image)
autotrans_speaker_button.grid(row=3, column=4, padx=5, pady=5, sticky=tk.E)

# 翻訳1エリア
label_trans1 = tk.Label(root, text="翻訳1:", bg = 'cyan')
label_trans1.grid(row=0, column=5, padx=10, pady=5, sticky=tk.W)
trans1_file_button = tk.Button(root, text="ファイル読みこみ")
trans1_file_button.grid(row=0, column=6, padx=10, pady=5, sticky=tk.E)
text_trans1 = scrolledtext.ScrolledText(root, width=40, height=15)
text_trans1.grid(row=1, column=5, padx=10, pady=5, columnspan=2,rowspan=2)
label_similarity1 = tk.Label(root, text="類似度:", bg = 'cyan')
label_similarity1.grid(row=3, column=5, padx=10, pady=5, sticky=tk.W)

trans1_up_button = tk.Button(root, image=up_image)
trans1_up_button.grid(row=1, column=7, padx=5, pady=5, sticky=tk.N)
trans1_down_button = tk.Button(root, image=down_image)
trans1_down_button.grid(row=2, column=7, padx=5, pady=5, sticky=tk.S)
orig_speaker_button = tk.Button(root, image=speaker_image)
orig_speaker_button.grid(row=3, column=6, padx=5, pady=5, sticky=tk.E)

# 翻訳2エリア
label_translation2 = tk.Label(root, text="翻訳2:", bg = 'yellow')
label_translation2.grid(row=0, column=8, padx=10, pady=5, sticky=tk.W)
trans_file2_button = tk.Button(root, text="ファイル読みこみ")
trans_file2_button.grid(row=0, column=9, padx=10, pady=5, sticky=tk.E)
text_translation2 = scrolledtext.ScrolledText(root, width=40, height=15)
text_translation2.grid(row=1, column=8, padx=10, pady=5, columnspan=2, rowspan=2)
label_similarity2 = tk.Label(root, text="類似度:", bg = 'yellow')
label_similarity2.grid(row=3, column=8, padx=10, pady=5, sticky=tk.W)

trans2_up_button = tk.Button(root, image=up_image)
trans2_up_button.grid(row=1, column=10, padx=5, pady=5, sticky=tk.N)
trans2_down_button = tk.Button(root, image=down_image)
trans2_down_button.grid(row=2, column=10, padx=5, pady=5, sticky=tk.S)
orig_speaker_button = tk.Button(root, image=speaker_image)
orig_speaker_button.grid(row=3, column=9, padx=5, pady=5, sticky=tk.E)

# メインループ実行
root.attributes('-fullscreen',True)
root.mainloop()


from dublungo import speak_text

def read_original():
    text = original_text_widget.get("1.0", tk.END)
    speak_text(text, lang="fr")  # フランス語の原文を読み上げ

def read_translation():
    text = translated_text_widget.get("1.0", tk.END)
    speak_text(text, lang="en")  # 英語の翻訳を読み上げ

# TkinterのGUI構築（仮のレイアウト）
root = tk.Tk()
root.title("Dublungo - 対訳管理")

original_text_widget = tk.Text(root, height=10, width=50)
translated_text_widget = tk.Text(root, height=10, width=50)

read_original_button = tk.Button(root, text="原文を読み上げ", command=read_original)
read_translation_button = tk.Button(root, text="訳文を読み上げ", command=read_translation)

original_text_widget.pack()
read_original_button.pack()
translated_text_widget.pack()
read_translation_button.pack()

root.mainloop()
