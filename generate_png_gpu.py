import torch
import numpy as np
import os
import cv2


def create_pngs_with_sizes(target_sizes_kb):
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    target_sizes_kb.sort()  # サイズを昇順にソート
    size = 10  # 初期画像サイズを10x10に設定
    increase_step = 10  # 一度に増やすピクセル数
    tmp_file = 'tmp.npy'  # 一時ファイル名

    # 初期画像の作成
    img = torch.randint(0, 256, (size, size, 4), dtype=torch.uint8, device=device)  # 初期画像を作成

    # 一時ファイルに保存
    np.save(tmp_file, img.cpu().numpy())

    for target_size_kb in target_sizes_kb:
        current_size_kb = os.path.getsize(tmp_file) / 1024

        # 目標サイズに達するまで画像サイズを拡張
        while current_size_kb < target_size_kb:
            # サイズを増やす
            new_size = size + increase_step
            new_img = torch.zeros((new_size, new_size, 4), dtype=torch.uint8, device=device)  # 新しい画像を作成

            # 既存の画像を新しい画像に貼り付け
            new_img[:size, :size, :] = img

            # 新しいピクセルにランダムな色と透明度を設定
            for i in range(size, new_size, increase_step):
                new_img[i:i + increase_step, :new_size, :] = torch.randint(0, 256, (increase_step, new_size, 4),
                                                                           dtype=torch.uint8, device=device)
                new_img[:new_size, i:i + increase_step, :] = torch.randint(0, 256, (new_size, increase_step, 4),
                                                                           dtype=torch.uint8, device=device)

            # 新しい画像を一時ファイルに保存
            np.save(tmp_file, new_img.cpu().numpy())
            current_size_kb = os.path.getsize(tmp_file) / 1024

            # 更新
            img = new_img
            size = new_size

            # メモリ解放
            del new_img
            torch.mps.empty_cache()

        # ディレクトリパスを設定
        directory_path = 'output/size_spec_gpu2'
        os.makedirs(directory_path, exist_ok=True)  # ディレクトリがなければ作成

        # 目標サイズに達したらファイルを保存
        output_filename = os.path.join(directory_path, f'output_{target_size_kb}.png')
        cv2.imwrite(output_filename, img.cpu().numpy())
        print(f"目標サイズ {target_size_kb} KB に達しました: {current_size_kb:.2f} KB, サイズ: {size}x{size}")

    # 一時ファイルを削除
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
        print(f"{tmp_file}が削除されました。")


# 例：10KB, 50KB, 100KBのPNGファイルを生成
target_sizes_kb = ([1000, 2000, 3000, 4000, 5000
, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 60000])
# 70000, 80000, 90000, 90500, 91000, 91500, 92000, 92500, 93000, 93500, 94000, 94500, 95000, 95500,
# 96000, 96500, 97000, 97500, 98000, 98500, 99000, 99500, 100000, 112500, 125000, 137500, 150000,
# 162500, 175000, 182500, 200000]
create_pngs_with_sizes(target_sizes_kb)
