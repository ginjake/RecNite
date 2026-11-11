# Unityアバター取り込みとlilToon元シェーダー利用

調査日：2026年11月11日。ユーザーの今回の指定を要件として扱い、実装済みとはしていない。調査は公式資料と公式ソースの閲覧であり、コンパイル・描画比較・変換実験は行っていない。

## 1. 「シェーダーをそのまま使う」はどう成立するか

### Takeaway

ユーザーが求めるのは、lilToonを似た標準マテリアルに置き換えることではなく、元のシェーダーとマテリアル設定を使って描画すること。この要件を維持する。元ソースを入力として内部でコンパイルする経路と、Unity向けビルド済みデータを別エンジンへ無変更で渡す経路は区別する必要がある。

### Cited Findings

- lilToonはUnityへunitypackageまたはUPMで導入する実装として公開される。Godot向けの完成実装をこの公式リポジトリで確認したわけではない。— [公式README](https://github.com/lilxyzw/lilToon)
- `lilShaderContainerImporter.cs`の19～36行相当では、Unity EditorのScriptedImporterとして`.lilcontainer`を展開し、`ShaderUtil.CreateShaderAsset`でShaderを作る。44～50行相当には展開したShaderソースを保存する処理がある。94～97行相当にはBRP/LWRP/URP/HDRPのinclude切り替えがある。単一のGPU計算式だけではなく、インポート処理を伴う。— [公式Importer](https://github.com/lilxyzw/lilToon/blob/master/Assets/lilToon/Editor/lilShaderContainerImporter.cs)
- BRP用`Default.lilblock`はSubShader/Passを構成し、Forward、Outline、ForwardAdd、ShadowCasterを持つ。Stencil、Cull、ZWrite、ZTest、Blendなども指定している。— [公式BRPテンプレート](https://github.com/lilxyzw/lilToon/blob/master/Assets/lilToon/CustomShaderResources/BRP/Default.lilblock)
- `lil_pipeline_brp.hlsl`は`UnityCG.cginc`、`AutoLight.cginc`、`Lighting.cginc`、`UnityMetaPass.cginc`を参照する。`lil_common.hlsl`にも入力・関数include、照明・カメラ・画面座標などのデータがある。— [BRP依存](https://github.com/lilxyzw/lilToon/blob/master/Assets/lilToon/Shader/Includes/lil_pipeline_brp.hlsl)、[共通処理](https://github.com/lilxyzw/lilToon/blob/master/Assets/lilToon/Shader/Includes/lil_common.hlsl)
- Unity公式はShader objectをUnity固有のラッパーとして説明し、SubShader・Pass・Properties等を内包する。HLSLプログラムだけを扱えば同等になるという仕様ではない。— [ShaderLabのShaderブロック](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Shader.html)
- Unity自身も必要なvariantとgraphics APIごとにシェーダーをコンパイルする。Editorでの取り込み・キャッシュと、Playerビルド時のコンパイルが説明されている。「元シェーダー利用」は「一切コンパイルしない」ことを意味しない。— [Unity Shader compilation](https://docs.unity.com/en-us/engine/6000.7/manual/materials-and-shaders/shaders/shader-troubleshooting/shader-reducing/shader-compilation)
- Godot標準のシェーダー言語はGLSL ES 3.0に似た独自言語である。— [Godot Shading language](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html)

### Inferences

- **要件を保った設計案：** 元のlilToonソース・依存include・マテリアル設定を入力とし、採用する描画基盤に合わせて内部で展開・コンパイルする。ユーザーに別シェーダーへの手作業置換を要求しない経路を目指す。この案の実現性は、上記ソース構造を踏まえた検証課題であり、既に完成した変換器があるという意味ではない。
- Unityを描画に使う場合は元のインポーター／パイプラインを利用できる候補となり、互換層の一部を自作する負担は減り得る。ただしレンダーパイプライン、Unity版、lilToon版、実行時配信まで含めて確認が必要。Unity使用そのものを今回の決定事項にしない。
- Godot等を使う場合は、シェーダー言語の変換だけでなく、ShaderLabの構造と描画状態、Unityの組み込み値・照明・シャドウ、複数Pass、依存includeの意味を満たす互換層が必要になる。元ソースを保持して内部変換する方法は検討できるが、Godot標準へファイルを置くだけで動くとは言えない。
- 「Unityのコンパイル済みShaderをそのまま他エンジンでロードできる」とは約束しない。GPU向けバイナリと、その周囲の描画状態・binding・Unity側オブジェクトの互換性は別問題である。
- フォールバックは非対応クライアント／端末・失敗時の代替経路であり、lilToonの正規対応を近似表示に置き換える理由にしない。

### Gaps

- 他エンジンでのlilToon元ソース利用、機能別の一致率、性能、必要工数は実験していない。現在確認した資料だけから「簡単」「不可能」「完全互換」とは判定できない。
- Unity標準includeやコンパイラーを別製品へ配布する権利は、lilToon自身の公開ライセンスと別に確認が必要。今回、その配布条件を確定していない。
- Second LifeがユーザーのUnityシェーダーを取り込む機能はこの調査の根拠にしていない。ビューアーの改造可能性とUnity Shader互換性は独立した話である。

## 2. unitypackageから取り込む機能をどう明文化するか

### Takeaway

今回、揺れ物、マテリアル、表示／非表示、円形メニューからのオブジェクトON/OFF、シェイプキー変更が対応範囲として指定された。これらを「できれば」へ後退させず仕様へ記載する。Animatorの全機能再現へ範囲を拡大する必要はない。

### Cited Findings

- VRChatのExpressions MenuはExpression Parametersと組み合わせてAnimatorを操作する。値には型・初期値・Saved・Syncedがあり、Toggle、Sub-Menu、Radial Puppet等の操作を持つ。— [Expressions Menu and Controls](https://creators.vrchat.com/avatars/expression-menu-and-controls/)
- PhysBonesは骨チェーンの揺れ物に加え、衝突・掴み・姿勢固定などを持ち、設定と本人のinteraction設定によって他者との相互作用が変わる。バージョンごとに挙動差もある。— [PhysBones](https://creators.vrchat.com/common-components/physbones/)
- UnityではSkinnedMeshRendererのBlendShape weightを指定して変形を制御する。ユーザーの「シェイプキー」はこの取り込み文脈ではBlendShapeとして対応付けられる。— [SetBlendShapeWeight](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/SkinnedMeshRenderer.SetBlendShapeWeight.html)

### Inferences

以下は機能を実装するための変換設計案で、ユーザーが内部形式まで決定したという意味ではない。

| 指定された対応機能 | 引き継ぐデータと動作 |
|---|---|
| 揺れ物 | 骨チェーン、基準姿勢、各係数・カーブ、コライダーと対象骨。元の揺れ方を比較し、PhysBones由来の場合はその仕様と新実装の対応を定義する |
| マテリアル | 元シェーダーへの参照、テクスチャ、数値・色・キーワード、描画設定。lilToonは元シェーダー利用の経路につなぐ |
| 表示／非表示 | 対象オブジェクトと有効状態、必要ならRendererの表示状態を区別して保持する |
| 円形メニューからのON/OFF | メニュー階層、名前、アイコン、パラメーターと対象オブジェクトの関連、初期値・保存・同期設定 |
| シェイプキー変更 | 対象メッシュ、BlendShape名／対応付け、値、メニューからの段階／連続値操作 |

- 必要なのは上記動作の意味を引き継ぐことで、Unity Animatorそのものを丸ごと新ランタイムへ持ち込むこととは限らない。関係するAnimationClipの値変更と条件を解析して、対象プロパティの操作へ変換する方式が候補。
- 対象外の複雑なAnimator処理は、要求されているON/OFFやシェイプキー変更の対応を放棄する理由にせず、別の未対応項目として知らせる。
- 揺れ物の見た目だけでなく掴み・固定まで含めるかは、今回の『揺れ物』指定だけから追加で確定しない。既に会話で定めた相互作用方針と揃えて決める。

### Gaps

- 代表アバターのunitypackageを使う変換検証は未実施。外部ビルド拡張が生成する最終Prefabをどの段階で取得するかも未決定。
- シェイプキーの複数同時適用、カーブ補間、値の範囲、表示切替に伴う揺れ物の再初期化などは、テスト対象として定義する余地がある。

## 3. 企画書の修正文とエンジン選定への影響

### Takeaway

エンジン名を先に固定せず、指定された互換機能と、将来クライアントを追加できる構造を要求として記述する。lilToonの元シェーダー利用とアバター機能の実現負担は、採用基盤を比較する材料になる。

### Cited Findings

- 公式lilToonの生成・依存構造、Unity Shader objectの構造、Godotの言語仕様は、ソース互換性と描画環境の互換性を分けて検討する根拠となる。— [lilToon Importer](https://github.com/lilxyzw/lilToon/blob/master/Assets/lilToon/Editor/lilShaderContainerImporter.cs)、[ShaderLab](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Shader.html)、[Godot](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html)

### Inferences

企画書へ反映する要件文案（実装済みという意味ではない）：

> 使用エンジンは未決定であり、Unityを必須としない。VRMに加え、VRChat向けunitypackageからアバターを取り込む。取り込みでは、揺れ物、マテリアル、表示／非表示、円形メニューによるオブジェクトのON/OFFとシェイプキー変更に対応する。lilToonは元のシェーダーとマテリアル設定を利用し、元の見た目を再現する。シェーダーを実行するための取り込み・コンパイル方式は、採用する描画基盤に合わせて設計する。

説明用に補足する場合の文案：

> 元シェーダーを利用するため、Unity以外の描画基盤ではShaderLabやUnity固有の描画処理を扱う互換層が必要になる。これは対応要件を近似表示へ変更する話ではなく、要件を満たすために実装する部分である。フォールバックは対応できない端末やクライアント向けに用意する。

将来クライアントの要件文案（他担当のSecond Life調査と統合）：

> まず公式クライアントを作り、後から別クライアントを開発できる構造にする。通信・アセット・ワールド状態の扱いを描画とUIから分ける。初期段階から複数の描画エンジンやクライアントを実装することは要件に含めない。

### Gaps

- 本ノートは技術調査と要件整理。具体的エンジン、コンパイラー、配信形式、独自クライアント向けSDKの公開時期を決定していない。
