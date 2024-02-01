import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import qrcode


def generate_qr():
    global qr_image, current_tab, test_number
    input_value = ""
    app_id = "abc"

    if current_tab == "文字列":
        input_value = str_entry.get()
        if not input_value:  # 文字列タブで空文字が入力された場合
            qr_label.image = None
            qr_label.configure(image='')
            return

    elif current_tab == "内部テスト共有":
        test_number = test_entry.get()
        if test_number.isdigit():  # 数字のみの場合
            input_value = f"https://play.google.com/apps/test/{app_id}/{test_number}"
        else:  # 数字以外、または空文字が入力された場合
            qr_label.image = None
            qr_label.configure(image='')
            return

    # QRコードの生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        border=1,
    )
    qr.add_data(input_value)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # QRコード画像をTkinterウィンドウに表示
    tkimage = ImageTk.PhotoImage(qr_image)
    qr_label.configure(image=tkimage)
    qr_label.image = tkimage


def export_qr():
    global current_tab

    # ディレクトリパスを設定
    directory_path = f'output/qr'
    os.makedirs(directory_path, exist_ok=True)  # ディレクトリがなければ作成

    if qr_image:
        if current_tab == "文字列":
            file_path = "str_qr"
        elif current_tab == "内部テスト共有":
            file_path = f'internal_test_qr{test_number}'
        else:
            return

        output_filename = os.path.join(directory_path, f'output_{file_path}.png')
        qr_image.save(output_filename, 'PNG')

        print(f"QR Code saved as {file_path}")
    else:
        print("Please generate a QR Code first.")


def on_tab_selected(event):
    global current_tab
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    current_tab = tab_text


# Tkinterウィンドウの作成
window = tk.Tk()
window.title("QR Code Generator")

tab_control = ttk.Notebook(window)

# 文字列タブの作成
str_tab = ttk.Frame(tab_control)
tab_control.add(str_tab, text="文字列")
str_entry = tk.Entry(str_tab)
str_entry.pack()

# 内部テスト共有タブの作成
test_tab = ttk.Frame(tab_control)
tab_control.add(test_tab, text="内部テスト共有")
test_entry = tk.Entry(test_tab)
test_entry.pack()

tab_control.pack(expand=1, fill="both")

# Generateボタンの作成
generate_button = tk.Button(window, text="Generate", command=generate_qr)
generate_button.pack()

# Export QRボタンの作成
export_button = tk.Button(window, text="Export QR", command=export_qr)
export_button.pack()

# QRコード表示用ラベル
qr_label = tk.Label(window)
qr_label.pack()

# タブ選択イベント
tab_control.bind("<<NotebookTabChanged>>", on_tab_selected)

# 初期化
qr_image = None
current_tab = "文字列"

# ウィンドウの実行
window.mainloop()
