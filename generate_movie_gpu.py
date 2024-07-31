import torch
import numpy as np
import os
import cv2


def create_videos_with_sizes(target_sizes_mb, resolution=(1920, 1080), fps=60):
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

    for idx, target_size_mb in enumerate(target_sizes_mb):
        tmp_file = f'tmp_{idx}.mp4'  # 一時ファイル名

        # 動画の初期設定
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(tmp_file, fourcc, fps, resolution)

        frame_count = 0
        while os.path.getsize(tmp_file) / (1024 * 1024) < target_size_mb:
            # ランダムフレームを生成
            frame = torch.randint(0, 256, (resolution[1], resolution[0], 3), dtype=torch.uint8, device=device)
            frame = frame.cpu().numpy()

            # フレームを動画に書き込み
            video_writer.write(frame)
            frame_count += 1

            if frame_count % fps == 0:
                current_size_mb = os.path.getsize(tmp_file) / (1024 * 1024)
                print(
                    f"動画 {idx + 1}/{len(target_sizes_mb)} 現在のサイズ: {current_size_mb:.2f} MB, フレーム数: {frame_count}")

        video_writer.release()

        # 出力ディレクトリを作成
        directory_path = 'output/video_spec_gpu'
        os.makedirs(directory_path, exist_ok=True)  # ディレクトリがなければ作成

        # 出力ファイルにリネーム
        output_filename = os.path.join(directory_path, f'output_{target_size_mb}MB.mp4')
        os.rename(tmp_file, output_filename)
        print(f"目標サイズ {target_size_mb} MB に達しました。ファイル: {output_filename} 動画時間：{frames_to_time(frame_count, fps)}")

        # メモリ解放
        torch.mps.empty_cache()


def frames_to_time(frames, fps):
    total_seconds = frames / fps
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    # return hours, minutes, seconds
    return f"{hours:02d}:{minutes:02d}:{seconds:.2f}"


# 使用例
# target_sizes_mb = [150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200]  # 10MB, 20MB, 50MBの動画を作成
target_sizes_mb = [300]
create_videos_with_sizes(target_sizes_mb)
