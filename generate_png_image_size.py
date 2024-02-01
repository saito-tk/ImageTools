# pip install Pillow
from PIL import Image
import os
import random


def create_pngs_with_sizes(target_sizes_kb):
    target_sizes_kb.sort()  # サイズを昇順にソート
    size = 10  # 初期画像サイズを10x10に設定
    increase_step = 10  # 一度に増やすピクセル数
    tmp_file = 'tmp.png'  # 一時ファイル名

    # 初期画像の作成
    img = Image.new('RGBA', (size, size))  # RGBAモード（32ビット）で新しい画像を作成
    pixels = img.load()
    for i in range(size):
        for j in range(size):
            # RGBA値をランダムに設定（透明度も含む）
            pixels[i, j] = (
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    img.save(tmp_file, 'PNG')

    for target_size_kb in target_sizes_kb:
        current_size_kb = os.path.getsize(tmp_file) / 1024

        # 目標サイズに達するまで画像サイズを拡張
        while current_size_kb < target_size_kb:
            # サイズを増やす
            new_size = size + increase_step
            new_img = Image.new('RGBA', (new_size, new_size))  # RGBAモード
            new_img.paste(img, (0, 0))

            # 新しいピクセルにランダムな色と透明度を設定
            pixels = new_img.load()
            for i in range(size, new_size):
                for j in range(new_size):
                    pixels[i, j] = (
                    random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for j in range(size, new_size):
                for i in range(size):
                    pixels[i, j] = (
                    random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            new_img.save(tmp_file, 'PNG')
            current_size_kb = os.path.getsize(tmp_file) / 1024
            img = new_img
            size = new_size

        # ディレクトリパスを設定
        directory_path = f'output/size_spec'
        os.makedirs(directory_path, exist_ok=True)  # ディレクトリがなければ作成

        # 目標サイズに達したらファイルを保存
        output_filename = os.path.join(directory_path, f'output_{target_size_kb}.png')
        img.save(output_filename, 'PNG')
        print(f"目標サイズ {target_size_kb} KB に達しました: {current_size_kb:.2f} KB, サイズ: {size}x{size}")


# 例：10KB, 50KB, 100KBのPNGファイルを生成
create_pngs_with_sizes([100, 10, 50])
