# Second Lifeを参考にクライアントの拡張性を設計する

調査・要件整理：2026年11月11日

**Second Lifeの代表的な第三者ビューアーは、公開された公式クライアントを改造して作られています。** Firestormも公式クライアントからの派生を明記しています。今回の企画も、まず公式クライアントを開発し、後から別のクライアントを作れる構造にする、という理解で整理します。初期から複数エンジンの完全互換実装を用意する前提は置きません。Unityは必須条件ではなく、指定されたアバター機能と元シェーダー利用を満たせるかを基盤選定の条件にします。([公式Viewer](https://github.com/secondlife/viewer)、[Firestorm](https://github.com/FirestormViewer/phoenix-firestorm))

## 公式ビューアーをビルドし、必要な部分を改造する

Second Lifeの現行公式ソースはC++20を指定し、描画にはOpenGLを使っています。UnityやGodotのプロジェクトを取り込む方式ではありません。公式ソースを取得して動く状態を作り、画面、入力、カメラ、描画などを変更して、同じSecond Lifeサービスへ接続するのが派生開発の経路です。通信やアセット処理を既存コードから引き継げるため、毎回サーバー仕様を一から再実装する必要はありません。([CMake設定](https://github.com/secondlife/viewer/blob/develop/indra/CMakeLists.txt)、[描画ライブラリ](https://github.com/secondlife/viewer/blob/develop/indra/llrender/CMakeLists.txt))

WindowsではVisual StudioのC++開発環境、CMake、Git、Python、Autobuildを準備します。Autobuildは依存関係の取得とビルドの呼び出しをまとめる道具です。以下は公式文書と現行設定に基づく**コマンドプロンプト用の例で、今回実行した手順ではありません**。保存先も説明用です。([Windowsビルド資料](https://wiki.secondlife.com/wiki/Build_the_Viewer_on_Windows)、[Autobuild](https://github.com/secondlife/autobuild)、[現行構成](https://github.com/secondlife/viewer/blob/develop/autobuild.xml))

```bat
git clone https://github.com/secondlife/viewer.git "E:\programing\sl-viewer-source"
git clone https://github.com/secondlife/build-variables.git "E:\programing\sl-build-variables"
set "AUTOBUILD_VARIABLES_FILE=E:\programing\sl-build-variables\variables"
cd /d "E:\programing\sl-viewer-source"
autobuild configure -A 64 -c RelWithDebInfoOS
autobuild build -A 64 -c RelWithDebInfoOS --no-configure
```

実際の作業では対象リビジョンを固定し、その版のコンパイラ・依存関係・CI設定に合わせます。古いWikiには32bitや旧ツール版、現在取得できないブランチ指定も残るため、そのまま現行のセットアップ手順にはできません。まず無変更でビルドし、小さなUI変更から始め、ログイン・移動・素材表示を確認する進め方が適しています。([現在のビルド変数](https://github.com/secondlife/build-variables/blob/master/variables))

| 改変する部分 | 公式リポジトリ内の位置 |
|---|---|
| ビューアー本体・カメラ・各種操作 | `indra/newview` |
| OpenGL・シェーダー・描画先の処理 | `indra/llrender` |
| メッセージ・HTTP通信 | `indra/llmessage`、`indra/llcorehttp` |
| UI部品・画面レイアウト | `indra/llui`、`indra/newview/skins/default/xui/en` |

上表は公開ソース内の位置です。たとえば設定画面はXMLの配置とC++側の処理を組み合わせて変更できます。独自クライアント開発は、まずこうした既存実装の利用から始められます。([設定画面XML](https://github.com/secondlife/viewer/blob/develop/indra/newview/skins/default/xui/en/floater_preferences.xml)、[全体構成](https://github.com/secondlife/viewer/blob/develop/indra/CMakeLists.txt))

## サーバーの共有状態と、ビューアーの表示を分ける

Second Lifeでは、ビューアーが素材と状態を受け取り、自分の端末で描画します。サーバーから完成した映像を受け取る方式ではありません。描画、UI、入力、素材取得とキャッシュはビューアー側、共有空間の状態・物理・ワールド内スクリプトはサーバー側が中心です。スクリプトを編集する画面と、実行する場所も分かれています。([サーバー構成](https://wiki.secondlife.com/wiki/Server_architecture)、[LSLの実行](https://wiki.secondlife.com/wiki/Getting_started_with_LSL))

接続は単一の万能APIではなく、UDPメッセージとHTTPのCapabilitiesなどを組み合わせています。現行ソースにはメッセージの型・番号を定義するテンプレート、利用可能な機能のURLを取得する処理があります。アセット本体はアセットIDと型で取得し、所持品はInventory APIへ要求します。**表示用のキャッシュ、インベントリの操作、ワールドの状態更新が別の役割を持つ**点が参考になります。([メッセージ定義](https://github.com/secondlife/viewer/blob/develop/scripts/messages/message_template.msg)、[Capabilities](https://github.com/secondlife/viewer/blob/develop/indra/newview/llviewerregion.cpp)、[アセット取得](https://github.com/secondlife/viewer/blob/develop/indra/newview/llviewerassetstorage.cpp)、[Inventory API](https://github.com/secondlife/viewer/blob/develop/indra/newview/llaisapi.cpp))

この分担を新企画へ応用するなら、通信・アセット参照・共有状態・所持品の処理を、描画やメニュー表示から分けます。オブジェクトID、編集命令、状態を確定する担当、形式の版を明示しておけば、後からUIや描画を変える際の影響を限定できます。これは設計提案であり、Second LifeのUDP、LLSD、リージョン方式や物理実装をそのまま採用する決定ではありません。VRの掴み操作やIKは、手元で即座に反応する処理も必要です。

## 将来の別クライアントに必要な余地を残す

今回の方針は、**公式クライアントを先に作り、後から派生・別実装できるようにする**ことです。通信と永続データを描画エンジンの内部オブジェクトに密結合させず、ビルド方法と依存関係を記録します。二本目の完成クライアント、全描画エンジンへの対応、公開SDKの製品化、全処理の別プロセス化は、初期必須条件に含めません。

将来フォークを認める場合には、ソースの提供範囲や再配布条件を定めることになります。Second LifeとFirestormはLGPL-2.1の公開コードを基盤にしていますが、この企画のコードやライセンスは未決定です。サービスへの接続条件もソースのライセンスとは別です。Second Lifeの第三者ポリシーは、通信互換性やクライアント識別を求め、権限の回避や作者情報の改変を認めていません。([Viewerライセンス](https://github.com/secondlife/viewer/blob/develop/LICENSE)、[第三者ビューアーポリシー](https://go.secondlife.com/corporate/third-party-viewers))

## アバターの対応範囲と元シェーダー利用を要件にする

**Unity使用は必須ではありません。** VRMに加え、VRChat向けunitypackageの取り込みでは、次の機能を対応範囲とします。これは企画上の要件であり、実装済みという意味ではありません。

| 対応機能 | 引き継ぐ対象 |
|---|---|
| 揺れ物 | 骨チェーン、係数、カーブ、コライダーなど |
| マテリアル | シェーダー参照、テクスチャ、色、数値、描画設定 |
| 表示／非表示 | オブジェクトやRendererの対象と状態 |
| 円形メニューのオブジェクトON／OFF | 項目、階層、アイコン、パラメーターと対象の対応 |
| シェイプキー変更 | 対象メッシュ、BlendShape、変更値と操作の対応 |

メニューが操作する値と、その値で変わる対象を引き継ぐことが必要です。関連するAnimatorの条件やAnimationClipを変換に利用する方法はありますが、Animatorの全機能互換まで要求を拡大しません。([VRChatのメニュー仕様](https://creators.vrchat.com/avatars/expression-menu-and-controls/)、[PhysBones](https://creators.vrchat.com/common-components/physbones/)、[BlendShape操作](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SkinnedMeshRenderer.SetBlendShapeWeight.html))

**lilToonは元のシェーダーとマテリアル設定を利用して、元の見た目を再現する要件です。** 別の標準マテリアルへの近似置換を通常の取り込み経路にはしません。公式実装ではUnity Editorのインポーターが`.lilcontainer`からShaderLabを生成し、描画パイプライン別のinclude、複数Pass、StencilやBlendなどを組み合わせています。単にHLSLの計算式だけを読み込む問題ではありません。([lilToon Importer](https://github.com/lilxyzw/lilToon/blob/master/Assets/lilToon/Editor/lilShaderContainerImporter.cs)、[Pass定義](https://github.com/lilxyzw/lilToon/blob/master/Assets/lilToon/CustomShaderResources/BRP/Default.lilblock))

元ソースを入力として保持し、内部で展開・変換・再コンパイルする方式は検証する価値があります。Godot等では、ShaderLabの構造やUnity固有の描画状態・照明・組み込み値を扱う互換層も必要です。Godot標準でそのまま読めることや、Unity用のコンパイル済みShaderを無変更でロードできることを確認したわけではありません。フォールバックは非対応端末や失敗時の代替として残します。([ShaderLab](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Shader.html)、[Godotのシェーダー言語](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html))

エンジン選定では、この互換処理をどこまで既存基盤で賄え、どこを自作するかを比較します。Second Lifeの派生ビューアー方式は将来のクライアント開発の参考であり、Unityシェーダー互換を自動的に実現するものではありません。

## 確認した範囲

公式ソースと開発資料を照合しました。古いWikiの構成説明は現行コードで補強しています。ローカルへのSecond Life環境導入、ビルド、ログイン、アバター変換、lilToonの別エンジンでのコンパイル・描画比較は未実施です。新企画のエンジン、ソース公開方式、互換層の実装方式は未決定です。
