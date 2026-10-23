# 作り直し用の道具（公開ページには関係しない）

- `build.py` … 旧URL用の画面ファイル（Drive「醸造ボード_page.html」を `src/page.html` として置く）から、アプリ版の `index.html` と `version.json` を作る。
  実行するたびに版（日時）が変わり、開いている画面に「新しいバージョンがあります」が出る。
  使い方: `python3 tools/build.py`（`src/page.html` を置いたフォルダで。出力は `app/index.html`）
- `make_icons.py` … アイコンの PNG を作る。
