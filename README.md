# 醸造ボード（アプリ版）

奈良醸造のタンク状況と今日のタスクを、スマホ・PCでアプリのように使うためのページです（PWA）。

- 公開先: GitHub Pages（`main` ブランチの直下）
- データ: Google Apps Script「醸造ボード」の Web アプリ経由で、スプレッドシート「醸造ボード データ」に保存
- 合言葉: Apps Script のスクリプト プロパティ `BOARD_PASS` で照合（このリポジトリには含まない）

## ファイル
- `index.html` … 画面本体
- `manifest.webmanifest` … アプリ名・アイコンの設定
- `sw.js` … 電波がないときも画面を開けるようにする仕組み
- `icons/` … アイコン
