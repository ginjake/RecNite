# VRChatとclusterの仕様照合

調査日：2026年11月11日。公式ヘルプ・公式開発者資料・作者の実装を確認。実機比較、互換変換の実装検証、性能測定は未実施。既存企画は編集していない。引用位置は `E:\programing\新メタバース\新メタバース企画.html` と `E:\programing\新メタバース\企画書に満たないモノ.txt`。

## 1 アイテムと公開ストアの差別化は成立するか

### Takeaway

ユーザーの「インベントリ＝所持品、ストア＝公開作品」「消費／無限」という整理は妥当な設計案。ただし、VRChatにアイテムがない、clusterはワールド内制作だけ、といった比較は避ける。差別化の軸は、ユーザー制作アイテムを持ち運び、編集・公開までつなげる一連の体験になる。

### Cited Findings

- VRChat公式Items FAQは今回の取得時点でも全ItemsはVRChatが制作・配布し、ユーザー制作Itemsは未対応と明記。Inventoryからスポーンでき、各利用者は非表示、権限を持つグループ管理者は撤去・持ち込み禁止を設定できる。ページ更新日は2025年10月29日。既存HTML 49・53行、txt 36行はこの公式ページと一致するが、「2026年にも実機確認した」とは言えない。[Items FAQ](https://help.vrchat.com/hc/en-us/articles/45059565610387-Items-FAQ)
- clusterはクラフトアイテム・アクセサリー・アバター・ワールド内課金を商品として扱う。クラフトアイテムは所持品を配置して使い、許可されたCCKワールドでも利用可能。ストア、個別商品ページ、ワールド内ディスプレイなど入手経路が複数ある。[商品販売の公式案内](https://creator.cluster.mu/products-2/)
- clusterの公式制作記事は、Unityからのアップロード後にWeb上で商品登録し、説明・価格等を入力、申請・審査を経て公開する流れを説明している。記事初出は2022年なので、現在の必須入力欄の完全な一覧の根拠にはしない。[商品登録手順](https://creator.cluster.mu/2022/08/18/craftitem/)
- cluster公式の2025年2月の事例では、ストア商品の更新が配置済みクラフトアイテムに自動適用されるわけではなく、表示仕様変更に伴い特別な差し替え対応が行われた。[更新と既存配置の扱い](https://note.com/cluster_official/n/n55da944c8b58)

### Inferences

- 【優先度高／新企画の具体化】HTML 198行「同じアセットは重複保存せず参照を共有」、216行のストア案を、原本アセット・公開商品の版・ユーザーの所持権・ワールド内配置の4つに分けることを提案する。共通バイナリは共有できても、所持権や購入時ライセンス、消費残数まで共有してはいけない。
- バージョンを必須入力にするだけでは更新方針が決まらない。配置済み作品が旧版に固定されるか、自動追従するか、作者が公開停止した場合に所持者は再利用できるかを決める必要がある。ユーザーには購入後の安定性、制作者には更新による既存ワールド破損の防止という効果がある。
- 「無限」は何度でも使用できることであり、無制限の同時スポーン・コピー・譲渡・再配布を意味しない。用途の分類と権利・負荷上限は別属性にする提案。
- 作者名・版・ライセンス・注意事項・タグ・説明はユーザー自身の要件であり、clusterの既存必須項目から導いたものとは書かない。

### Gaps

- VRChat FAQは古い更新日が残る。別の公式発表でUGC Itemsが一般開放されたという裏付けは今回見つからず、断言は「確認できた公式FAQでは未対応」に限定する。
- clusterの現行商品入力フォームをログインして実査していない。審査時間、販売手数料、各商品の厳密な再利用権は今回の調査対象外。

## 2 同期と共同編集の仕様は十分か

### Takeaway

「誰でもその場で作れる」を実現するには、作者が毎回同期処理を書く範囲を小さくする必要がある。一方で、共有状態・その場のイベント・保存する状態は分離して設計する。既存の同期に対する不満は、新企画の同期モデルと受け入れ条件へ落とし込める。

### Cited Findings

- VRChatではネットワークオブジェクトに所有者があり、その所有者だけが同期Udon変数を変更する。所有権は移譲可能で、離脱時には新所有者が割り当てられる。この通信上の所有者は作品の作者や購入者を意味しない。[Object Ownership](https://creators.vrchat.com/worlds/udon/networking/ownership/)
- VRChatの途中参加者には最新の同期変数と所有者が送られるが、過去のイベントは再実行されない。重要状態は同期変数で保持する設計が公式に示される。[Late Joiners](https://creators.vrchat.com/worlds/udon/networking/late-joiners/)
- clusterのItemScriptによる処理結果は同じ空間の参加者へ共有され、途中参加にも反映される。PlayerScriptはプレイヤー内処理やローカルUI、デバイス機能を扱う。スクリプトの内部状態はアイテム／プレイヤーごとに分離し、相互通信にはAPIを使う。[ClusterScript](https://docs.cluster.mu/creatorkit/world/cluster-script/)
- cluster WorldCraftは共同配置でき、無人になっても状態を保持する一方、計算や物理処理は停止する。公開ワールドのセッションは公開時のコピーから開始し、終了時の状態は制作元へ戻らない。[ワールドとWorldCraft](https://docs.cluster.mu/creatorkit/world/)
- clusterではScriptable Itemを付けてアップロードしたアイテムについて、アプリ内のスクリプトエディタで編集できる。任意のUnityコンポーネントの相互編集と同義ではない。[スクリプトエディタ](https://help.cluster.mu/hc/ja/articles/11837305328281-スクリプトエディタ-コンソール)

### Inferences

- 【優先度高】HTML 206行の「VR内の編集内容とコードを相互変換」は、共通データ形式をノード・ブロック・コードの複数UIで編集する方向が候補。対応する型、分岐、繰り返し、非同期処理、外部API、権限を定める必要がある。任意のC#やUnityコンポーネント全体の完全往復を保証する仕様にはしない。
- 【優先度高】「作者／所持者／編集許可者／現在掴んでいる人／同期処理の担当者」を別概念にする。独自クライアントでも最終的な権限判断は一致させる。二人同時に掴む、掴んだまま切断する、共同編集とUndoが衝突する場面を検証例にする。
- ギミックの受け入れ試験案：既に開いた扉が途中参加者にも開いている／動画の現在位置が途中参加者に反映される／持ち主離脱後もアイテム状態が保たれる／一時的な効果音が途中参加時に再発火しない。
- 制作中の共有データ、公開版、遊んでいるセッション内状態、永続セーブを分けることで、ゲーム中の変更が作者の原本を壊さず、共同制作結果は保存できる。

### Gaps

- 新企画の共通コア、言語、保存モデル、ホスト方式は未実装・未決定。参考サービスの自動同期をそのまま移植できるわけではない。

## 3 VRChatアバターとlilToonの移行で何を再現すべきか

### Takeaway

VRMとunitypackageのギミック移行は別の入口として設計し、unitypackage側ではメニューの形状だけでなく操作の意味と状態遷移を変換する。lilToon対応は新企画の要件として維持し、Godot採用だけで互換性が得られるとはしない。

### Cited Findings

- Expressions MenuはExpression Parametersと組み合わせてAnimatorを操作する。SavedとSyncedは別設定。Button、Toggle、Sub-Menu、2軸／4軸／Radial Puppetにそれぞれ異なる動作がある。Buttonはクリック後にパラメーターを設定し、送信後リセットする動作で、長押し保持ではない。ページは2026年10月26日更新。[Expressions Menu](https://creators.vrchat.com/avatars/expression-menu-and-controls/)
- PhysBonesには揺れだけでなく、掴み・固定・他者との相互作用の設定がある。コンポーネントの版でも挙動が異なる。[PhysBones](https://creators.vrchat.com/common-components/physbones/)
- VRChatには独自Constraintsがあり、Unity Constraintsからの置き換えと追加機能がある。アバターのUnity Constraintsはゲーム内で変換されるため、Unityの見た目だけを基準にすると差が生じ得る。[Constraints](https://creators.vrchat.com/common-components/constraints/)
- lilToon公式配布はUnity向け。公式サイトはUnityライティングへの対応、機能を除外してビルドサイズ・負荷を抑える仕組みを説明している。MITライセンスは改変・配布を認め、表示等の条件を定める。[公式サイト](https://lilxyzw.github.io/lilToon/)、[ライセンス](https://raw.githubusercontent.com/lilxyzw/lilToon/master/LICENSE)
- VRChat自身にもShader Blocking/Fallbackがあり、シェーダーのタグで代替方式を指定する。Toon、Cutout、Transparent、DoubleSidedなどを扱い、代替時に元と同じ表現になるとは限らない。[Shader Fallback](https://creators.vrchat.com/avatars/shader-fallback-system/)

### Inferences

- 【優先度高】HTML 184行「Unityを使用」は直近会話と不整合。Godotも含めエンジン未決定、共通仕様と描画を分離する方向としてレビューする。unitypackage変換やlilToonの移植費用もエンジン比較の評価項目に含める。MITかどうかだけでは開発工数を判断できない。
- 互換変換の初期対象として、アクセサリー表示、表情BlendShape、衣装切り替え、マテリアル値変更、トグル、Puppetによる連続値を明記すると測定しやすい。対応していないAnimatorの条件やステート動作は一覧で報告し、元データも保持する案。
- lilToonは対応版と機能範囲を指定し、照明・透明ソート・輪郭線・描画パスを含めて比較する必要がある。「カスタムシェーダーを使える」は「UnityのShaderLab/HLSLをそのまま同じ見た目で実行できる」とは違う。標準マテリアルへの縮退は作者の意図を失うことがあるため、作者指定代替を残す。
- 独自クライアント向けに、共通マテリアル属性だけでなく、対応シェーダーID／版・要求機能・フォールバック指定を仕様化する案。未知の項目を黙って捨てない。

#### 会話中のアシスタント説明の訂正

以前の回答の「ボタン・トグル：押している間の動作、オン／オフ状態を再現」は、VRChat Buttonの説明として不正確。これはユーザー案の誤りではない。正しくは「Buttonは押下後に値を設定し、その後リセット。Toggleはオン／オフを保持」。変換仕様ではこの差を再現する。出典は上記Expressions Menu。

### Gaps

- 実アバターで変換は行っていない。lilToonのGodot移植に必要な全機能、サードパーティビルドツールが生成するAnimatorを含む網羅的互換性は未検証。

## 4 複数端末と軽量化の比較は正確か

### Takeaway

表現の自由度と負荷制御を両方設ける方針は参考サービスとも整合する。容量削減、VRAM削減、CPU/GPU負荷削減、通信削減を同じ指標で扱わず、端末別の表示品質と作者プレビューを用意するのが重要。

### Cited Findings

- VRChatのAndroid／Quest向けアバターはSDK内の対応シェーダーに制限され、Cloth等が使えない。ワールドとアバターでは利用可能機能が異なる。[Android Content Limitations](https://creators.vrchat.com/platforms/android/quest-content-limitations/)
- VRChat Performance Rankはコンポーネント等の静的評価であり、実性能の最終判断ではないと公式に明記される。Excellentでも重い場合、Very Poorでもよく最適化された場合がある。[Performance Ranks](https://creators.vrchat.com/avatars/avatar-performance-ranking-system/)
- clusterはVRM 0.xと1.0を受け付ける。VRM1.0の制限例はファイル100MB、ポリゴン72,000、マテリアル25。1.0では品質設定に応じて主にテクスチャを調整し、0.xのような自動メッシュ削減・材質統合はしない。Standard系はUniUnlitへ変換表示される。[VRM制限](https://help.cluster.mu/hc/ja/articles/360029465811)

### Inferences

- HTML 241行とtxt 102行にある「ポリゴンだけで重さは決まらない」は維持。ダウンロード量、常駐VRAM、描画時間、物理・ギミック時間を別々に測る案が良い。ホーム5万ポリゴンは目安であり、それだけでVR目標FPS達成とはしない。
- PC／Quest用の配信版が別でも、原本は共通にできる。データの重複排除は同一バイナリの保存・転送量を減らすが、配置数に比例する物理・ギミック処理は残る。
- clusterの自動最適化は利用者の参加しやすさに寄与する一方、作者の見た目を変える可能性がある。新企画は原本を保持し、派生版のプレビューと選択を付ける案がユーザー要望に合う。

### Gaps

- 同じ機器・人数・アバターでの比較ベンチマークなし。「Godotだから軽い」「clusterが一律高速」とは結論できない。

## 5 公式資料の更新差に注意すべき箇所はあるか

### Takeaway

clusterの古いFAQには、現在の専用仕様ページと食い違う記述が残る。古いFAQを根拠に「WorldCraftとCCKは完全に無関係」「背景・BGM不可」「ギミックなし」と断定しない。

### Cited Findings

- 古いWorldCraft FAQにはCCKとの互換なし、背景・BGM変更不可、ギミック未対応などが書かれている。[FAQ](https://help.cluster.mu/hc/ja/articles/4427741277465-ワールドクラフトのよくある質問)
- 一方、現在のベースワールド仕様はCCKワールドをWorldCraftの土台にでき、背景・BGM等の設定も説明する。2026年8月時点の制限として、ベースワールド内の課金や一部セーブ状態は引き継がれず、クラフトアイテムとワールドアイテムで状態保存範囲が異なる。参照中のベースワールドは削除できない。[ベースワールド仕様](https://docs.cluster.mu/creatorkit/world/craft-base/)

### Inferences

- 企画の「外部ツールとVR内制作の連携」はclusterにも先例があるが、双方向に全データを編集できる証明にはならない。新企画では、読み込み専用部分と編集可能部分、保存対象、元データ更新時の挙動を明記する。
- 共有アセット参照には、参照中のデータを削除してよいか、利用中の版を保持するかというライフサイクルが必要。clusterのベースワールド削除制限は具体的な参考になる。

### Gaps

- FAQの各項目の更新時点は確認できない。現在の管理権限を全て古いFAQだけから断定しない。今回のレビューでは具体的な専用仕様ページを優先する。
