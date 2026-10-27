# 原料棚卸カウンター（アプリ版）

モルト・酵母の月末棚卸を、スマホで数えて受払簿と突合するためのページです（PWA。醸造ボードのアプリ版と同じ作り）。

- 公開先: https://narabrewing2018.github.io/brew-board/genryo/ （このフォルダ）
- データ: Google Apps Script「原料棚卸カウンター（アプリ版の通信先）」の Web アプリ経由。
  記録はスプレッドシート「原料棚卸カウンター（スマホ用）」の受付シートに入り、PCの claude.ai「原料棚卸カウンター」が取り込む。合言葉なし。
- 画面は claude.ai の「原料棚卸カウンター」の gen/build.py で作る（このフォルダの index.html を直接直さない）。

## ファイル
- `index.html` … 画面本体（build.py の出力 phone.html）
- `version.json` … 版。変わると開いている画面に「新しいバージョンがあります」
- `manifest.webmanifest` / `sw.js` / `icons/`
