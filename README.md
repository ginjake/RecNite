# RecNite

新しいVR SNSの企画書と調査資料。企画段階のため、記載された機能は実装済みではありません。

## 資料

- [新メタバース企画](新メタバース企画.html)：現在の企画書。
- [企画メモ](企画書に満たないモノ.txt)：要望や検討事項。
- [企画レビュー](新メタバース企画レビュー.html)：仕様照合時点のレビュー。
- [Second Lifeクライアント調査](SecondLifeクライアント調査.html)：クライアント設計の参考資料。
- `reports/`：調査レポート。
- `research_notes/`：調査記録・生成スクリプト・原文バックアップ。

## ローカルでの閲覧

`index.html` をブラウザで開くと企画書へ移動します。HTMLの閲覧にビルドや依存パッケージのインストールは不要です。

## GitHub Pagesでの公開

リポジトリの **Settings → Pages** で、次の設定を保存します。

- Source：**Deploy from a branch**
- Branch：**main**
- Folder：**/(root)**

公開後のURL：<https://ginjake.github.io/RecNite/>

以降は `main` へのpushで更新されます。企画書の編集先は `新メタバース企画.html` です。`index.html` はそのファイルへの転送に使います。
