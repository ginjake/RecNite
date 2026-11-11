# Second Lifeビューアーの作成手順と派生開発

調査日：2026年11月11日。公式リポジトリ・公式開発文書を照合。環境構築、クローン、ビルド、ログインは実施していない。

## どうやって別のクライアントを作るのか

### Takeaway
Second Lifeの代表的な経路は、公開されている公式ビューアーを派生させ、描画・UI・入力等を変更して同じサービスへ接続すること。Firestormは公式クライアント由来と明記しており、毎回別エンジンで全プロトコルをゼロから実装する仕組みではない。

### Cited Findings
- 公式READMEはクライアントコードの公開と、第三者が保守するforkを案内する。Firestorm自身のREADMEもSecond Life公式クライアント由来と説明し、Second LifeとOpenSimへの対応を区別している。— [Second Life公式リポジトリ](https://github.com/secondlife/viewer)、[Firestorm公式リポジトリ](https://github.com/FirestormViewer/phoenix-firestorm)
- 開発手順はソース取得、開発環境、Autobuild設定、ビルド、実行という通常のネイティブアプリ開発。Autobuildは依存関係の取得とビルドの呼び出しを統一する道具で、コンパイラやCMakeそのものの代替ではない。— [Windows手順](https://wiki.secondlife.com/wiki/Build_the_Viewer_on_Windows)、[Autobuild README](https://github.com/secondlife/autobuild)
- 現行公式CMakeはC++20を指定し、描画ライブラリはOpenGLを使用する。Unity/Godot用プロジェクトではない。— [トップCMake](https://github.com/secondlife/viewer/blob/develop/indra/CMakeLists.txt)、[llrender CMake](https://github.com/secondlife/viewer/blob/develop/indra/llrender/CMakeLists.txt)
- Firestormはmasterをnightly開発版とし、個人利用を超えて派生ビューアーに使用する場合にはリリースブランチを使うよう案内する。これはFirestormプロジェクトの案内であり、新企画の決定ではない。— [Firestorm README](https://github.com/FirestormViewer/phoenix-firestorm)

### Inferences
- ユーザーの「後から別クライアントを作れる程度」は、この派生開発モデルで理解できる。今すぐ複数エンジンの互換クライアントや独立SDKを完成させる必要を意味しない。
- 本企画では、まず公式クライアントを作り、通信処理・共有データとUI・描画・入力を分けて保守する。後からソースの派生利用を認める場合の公開範囲とライセンスは、その時点までに決める設計課題であり、既にオープンソース化が決定したとはしない。
- 独自クライアントで同じワールドに入ることと、任意のシェーダーを他エンジンでそのまま動かすことは別の互換性問題。

### Gaps
- この調査ではコンパイルとログインを試していない。別エンジンで独立実装された全機能クライアントが現在どこまで存在するかは対象外。

## Windowsでの具体的なビルド経路は何か

### Takeaway
公式文書にはWindowsビルドの手順がある。ただし古いツール版・32bit・旧branch説明が混在しているため、実作業では対象リビジョンの設定とCIを確認する。以下は文書と現行設定に存在するコマンドの例であり、動作確認済みの一括導入手順ではない。

### Cited Findings
- 公式WindowsページはVisual StudioのC++デスクトップ開発、CMake、Git、Python、Autobuildを挙げる。`autobuild configure`で依存パッケージを取得し、Visual StudioまたはCLIでビルドする。— [公式Windowsビルド](https://wiki.secondlife.com/wiki/Build_the_Viewer_on_Windows)
- 現行`autobuild.xml`には`RelWithDebInfoOS`があり、Windows向けは独自ライブラリの導入を無効にする設定などを持つ。CMakeを呼び出す構成も確認した。— [現行autobuild.xml](https://github.com/secondlife/viewer/blob/develop/autobuild.xml)
- compiler flagsは別の`build-variables`リポジトリで管理される。古いwikiは`viewer`ブランチを案内するが、今回そのraw URLは404で、現在の既定`master`の`variables`を確認できた。古いbranch指定をコピーしない。— [公式build-variables](https://github.com/secondlife/build-variables)、[現行variables](https://github.com/secondlife/build-variables/blob/master/variables)、[旧記述が残るAutobuild案内](https://wiki.secondlife.com/wiki/Building_the_Viewer_with_Autobuild)
- `build.sh`はLinden Labのビルド環境から呼ばれることを前提とする記述がある。単にこれを直接実行すれば全環境が整うとは案内しない。— [build.sh](https://github.com/secondlife/viewer/blob/develop/build.sh)
- Firestorm公式Windows手順は64bit専用、cmd.exe使用を明記し、現在のページではVS2026、CMake4.1.2以上等を案内する。`ReleaseFS_open`と`ReleaseOS`は別の構成である。— [Firestorm Windows手順](https://github.com/FirestormViewer/phoenix-firestorm/blob/master/doc/building_windows.md)

文書に基づく公式ビューアーの例。`E:\programing\sl-viewer-source`と`E:\programing\sl-build-variables`は説明用の保存先で、今回作成していない。依存環境が準備済みのWindowsコマンドプロンプトで行う想定。

```bat
git clone https://github.com/secondlife/viewer.git "E:\programing\sl-viewer-source"
git clone https://github.com/secondlife/build-variables.git "E:\programing\sl-build-variables"
set "AUTOBUILD_VARIABLES_FILE=E:\programing\sl-build-variables\variables"
cd /d "E:\programing\sl-viewer-source"
autobuild configure -A 64 -c RelWithDebInfoOS
autobuild build -A 64 -c RelWithDebInfoOS --no-configure
```

構成名は公式文書と現行XMLから確認した。対象版の依存関係・コンパイラ設定の調整は別途必要になり得る。— [Windows手順](https://wiki.secondlife.com/wiki/Build_the_Viewer_on_Windows)、[autobuild.xml](https://github.com/secondlife/viewer/blob/develop/autobuild.xml)

### Inferences
- 実際に派生クライアントを開発するなら、最初は無変更のビルドを通し、次にUIの小さな変更を行い、ログイン・移動・アセット表示を確認する。この順序なら環境の問題と変更の問題を分けられる。
- 新企画が今用意すると有益なのは再現できる公式クライアントのビルド手順、依存関係、版の記録。最初からあらゆる言語のSDKを用意することではない。

### Gaps
- 指定リビジョンを固定した実ビルド成功は未確認。古い公式wikiのVS2017既定・32bit等を、現行推奨環境として引き継がない。

## 何を改変でき、ライセンスはどう扱うのか

### Takeaway
公開コードには描画、通信、UI、インベントリ等の実装が含まれるため、それらを再利用して派生できる。コードの利用条件と、Second Lifeサービスへの接続条件は別。Second Lifeのライセンスを新企画へ自動的に採用する理由はない。

### Cited Findings
下記はオンラインリポジトリ内の位置であり、ユーザーPC上に作成したパスではない。

| リポジトリ内の位置 | 確認できる内容・変更例 |
|---|---|
| `indra/newview` | ビューアー本体、カメラ、表示、インベントリ操作等。たとえば操作UIと対応するC++処理を変更する。[CMakeのソース一覧](https://github.com/secondlife/viewer/blob/develop/indra/newview/CMakeLists.txt) |
| `indra/llrender` | OpenGL、GLSL shader、texture、render target等の描画処理。[描画ライブラリ](https://github.com/secondlife/viewer/blob/develop/indra/llrender/CMakeLists.txt) |
| `indra/llmessage`、`indra/llcorehttp` | メッセージとHTTP通信。共有データを受信する処理を既存実装として利用できる。[通信ライブラリ](https://github.com/secondlife/viewer/blob/develop/indra/llmessage/CMakeLists.txt)、[全体構成](https://github.com/secondlife/viewer/blob/develop/indra/CMakeLists.txt) |
| `indra/llui`、`indra/newview/skins/default/xui/en` | UI部品とXMLによる画面構造。設定画面の項目や配置変更が例になる。[UIライブラリ](https://github.com/secondlife/viewer/blob/develop/indra/llui/CMakeLists.txt)、[設定画面XML](https://github.com/secondlife/viewer/blob/develop/indra/newview/skins/default/xui/en/floater_preferences.xml) |
| `indra/llinventory` | インベントリの基礎コード。[全体構成](https://github.com/secondlife/viewer/blob/develop/indra/CMakeLists.txt) |

- 公式viewerとFirestormのLICENSE現物はLGPL2.1。公式ソース中にはversion 2.1 onlyと書かれたファイルもある。MITではない。— [Second Life LICENSE](https://github.com/secondlife/viewer/blob/develop/LICENSE)、[Firestorm LICENSE](https://github.com/FirestormViewer/phoenix-firestorm/blob/master/LICENSE)、[ファイル内表示例](https://github.com/secondlife/viewer/blob/develop/indra/newview/app_settings/shaders/class1/deferred/pbralphaF.glsl)
- 実行ファイル配布等にはライセンス上のソース提供等の条件がある。依存ライブラリにもそれぞれライセンスがあり、公開クライアントのLICENSEだけで全依存物の利用許諾が一括決定するわけではない。現行XMLに依存物のライセンス情報が記録される。— [LICENSE](https://github.com/secondlife/viewer/blob/develop/LICENSE)、[依存関係一覧](https://github.com/secondlife/viewer/blob/develop/autobuild.xml)
- Firestormの公開構成とKakadu/Havok/FMOD等を使う構成は区別されている。公開ソースがあることと、すべての公式ビルド機能・第三者ライブラリが無条件に使えることは異なる。— [Firestormビルド資料](https://github.com/FirestormViewer/phoenix-firestorm/blob/master/doc/building_windows.md)

### Inferences
- 「後からクライアントを作れる」方針を、初期段階から完全な別エンジン実装の保証へ膨らませる必要はない。公式クライアントの派生・再構築経路を残すことが第一段階になる。
- Second Lifeの構造を参考にするだけなら、そのコードやLGPLを採用したと扱わない。本企画でコードを公開するか、どの範囲を再利用可能にするか、SDKだけを配布するかは別途決定する。

### Gaps
- ライセンスの個別適用に関する法的判断はしていない。今回の調査は公開実装と開発文書の確認であり、配布許諾や商用利用の個別審査ではない。
