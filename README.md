# ImageTools

## generate_png_image_size.py
- 指定した容量(KB)前後のPNGファイルを生成するツールです。
　　- PNGファイルは`./output/size_spec/`配下に`output_{指定容量}.png`で保存されます。
- 1pxごとの色RGBAをランダムで設定することでPNGの圧縮効果をなくし、なるべく早く指定した容量に達するようになります。
- 容量が増えるたびに生成完了までの時間がかかります。
例：10KB, 50KB, 100KBのファイルを生成します。
```python
create_pngs_with_sizes([100, 10, 50])
```

## generate_qr.py
- 入力した文字列からQRコードを生成してプレビュー出力と画像の出力ができる


- 実行するとGUIが表示される
- 文字列タブ
  - 入力した文字列をそのままQRコードとして出力する
- 内部テスト共有タブ
  - 入力したAndroidの内部テストビルド番号を元に共有用URLのQRコードとして出力
  - アプリのパッケージはコード内の`application_id`へ入力する
- Generateボタン
  - QRコードを生成しプレビュー表示
- Export QRボタン
  - プレビュー表示したQRコードをPNG画像で保存