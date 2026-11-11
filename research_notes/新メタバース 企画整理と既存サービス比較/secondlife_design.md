# Second Lifeと新メタバースの設計論点

調査日：2026-10-15。原メモとAGENTS.mdをUTF-8で確認した。以下は公式文書の確認内容と、そこから導く企画上の提案を分離した調査ノート。ページの更新日が確認できないものは「閲覧日現在の表示」と扱い、検索エンジンのクロール日を更新日とはしない。料金は契約条件で変わるため企画段階の比較用。

## 1. Second Lifeをユーザー・ワールド制作者から見るとどうか

### 要点

Second Lifeは、生活空間・創作物の取引・権限管理・第三者ビューアーを比較する対象として有用。VRヘッドセット向け操作を標準とするサービスと同一視せず、PC等で利用する3D仮想世界として比較する。

### 出典付きの確認事項

- **参加端末**：公式ダウンロードページはデスクトップ版とiOS/Android版を案内し、Mobileは全員無料と記載。システム要件にはWindows、macOS、コミュニティ支援のLinuxについて記載がある。これらの公式ページでは現在の標準HMD対応を確認できなかった。「3D空間に入れる」と「SteamVR等で手・頭をトラッキングできる」は別の比較項目にする。[公式Downloads](https://www.secondlife.com/downloads)、[System Requirements](https://www.secondlife.com/system-requirements)（いずれも更新日不明、2026-10-15閲覧）。
- **モバイル版の注意**：公式Mobile FAQの改訂表示は2026-08-04だが、未対応機能欄は「2024年11月時点」と書かれたまま。ここにあるInventory、Marketplace、Building等の未対応一覧を2026年の確定情報として転載してはいけない。[Mobile FAQ](https://lindenlab.freshdesk.com/support/solutions/articles/31000173486-second-life-mobile-public-beta-faq)。
- **生活・経済**：L$はコンテンツ、土地、チップ、サービス報酬などに使われる。公式LindeXではL$を売買でき、取引は住民間で成立し、手数料や為替変動、成立待ちがある。単に「遊んだら現金がもらえる」仕組みではない。[Buying and selling Linden dollars](https://community.secondlife.com/knowledgebase/english/buying-and-selling-linden-dollars-r46/)（初出2011-02-24、2026-10-15閲覧）。
- **表示の負荷対策**：アバター複雑度の上限を利用者が設定し、超過アバターを簡易表示できる。高負荷アバターはビューアー性能に影響する。公式自身も複雑度の絶対的な善悪ではなく、見る側の設定との関係を説明している。[Avatar Rendering Complexity](https://community.secondlife.com/knowledgebase/english/avatar-rendering-complexity-r770/)（初出2015-09-28、2026-10-15閲覧）。
- **ワールド内制作**：建築が許可された土地ではプリミティブを生成し、位置・大きさ・回転等を編集できる。どの土地でも無条件に生成できるわけではない。[Build Tools](https://community.secondlife.com/knowledgebase/english/build-tools-r12/)（2026-10-15閲覧）。
- **プログラム・外部制作**：LSLはオブジェクトに相互作用やゲームの挙動を追加する言語。外部制作メッシュはCOLLADA/DAE形式で取り込み、LOD、物理形状、land impact、アップロード費用等を考慮する。[Scripting object behavior](https://community.secondlife.com/knowledgebase/english/scripting-object-behavior-r62/)、[Uploading a mesh model](https://community.secondlife.com/knowledgebase/english/uploading-a-mesh-model-r274/)（2026-10-15閲覧）。
- **土地の継続費**：公式Private Region価格表のFull Regionは65,536m²、初期349米ドル、月額199米ドルと表示されている。これは専用リージョンの一例であり、参加者全員や小区画の利用料金ではない。税・条件・別プランは別途確認が必要。[Private Region Pricing](https://go.secondlife.com/land/private-pricing)（更新日不明、2026-10-15閲覧）。
- **購入物の権限**：次所有者向けにCopy、Modify、Transferを別々に設定。Copyなしではワールドに出した品がインベントリから移り、回収すると戻る。これは自動消費アイテムとは異なる。権限の組合せ・内包物との関係にも注意が必要。[Object permissions](https://community.secondlife.com/knowledgebase/english/object-permissions-r57/)（初出2011-02-24、公式一覧で更新2025-01-09、2026-10-15閲覧）。
- **カスタムクライアント**：第三者ビューアーを認めるが、固有識別子、配布時の説明、プライバシー等の条件がある。権限回避、作者情報の改変などは禁止。独自エクスポートには各構成要素が利用者自身の制作物であることの確認を要求しており、Full Permissionsと自由な外部出力は同義ではない。[Third Party Viewer Policy](https://go.secondlife.com/corporate/third-party-viewers)（更新日不明、2026-10-15閲覧）。

### 推論・企画への提案

| 視点 | メリットとして参考にする点 | デメリット・負担として扱う点 |
|---|---|---|
| ユーザー | 住居、服、家具、イベント等を通じて長く生活する体験を設計できる。購入物のコピー・編集・譲渡条件を表示できる。表示負荷を自分で調整できる。 | 服・アタッチメント・インベントリ・土地・購入条件を理解する手間がある。条件を知らず購入すると「買ったのに編集／譲渡できない」が起こりうる。HMD前提の身体操作との適合は別途検証が必要。 |
| ワールド制作者 | 空間内の建築、LSL、外部モデルを組み合わせられる。作品を継続的に配置し販売する運用を考えやすい。 | 土地維持費、性能予算、LOD・物理形状・アップロード費、権限確認までが制作コストになる。常設空間と無料の一時セッションは同じ費用モデルで比較できない。 |

上表の使いやすさ・学習負担は仕様からの推論であり、今回の実機評価ではない。新企画では購入前に「使える／改造できる／コピーできる／譲れる／外へ出せる」を短い日本語で表示し、原メモのBuilder/Guestと作品の権利を別欄にするとよい。

### 未確認・留意点

- 標準VRヘッドセット対応、現在のモバイル機能網羅性、実測FPS、利用者数、売上分布は今回確定できていない。
- 「カスタムクライアントを自由に作れる」は「運営ポリシーとソースコードのライセンス条件の範囲で開発・接続できる」に修正すると正確。
- Second LifeのLSLや土地維持モデルを、そのまま新企画へ採用する提案ではない。

## 2. 原メモの技術的前提はどう整理するか

### 要点

Unityのビルド時間、P2Pの安さ、VRMの表現範囲、ポリゴン数、キャッシュ保護には条件がある。原メモでは「採用したい体験」と「検証が必要な実現方法」を分ける。

### 出典付きの確認事項

- **Unityビルド**：Unityは変更された入力に依存する工程を再実行する増分ビルドを説明している。コード、IL2CPP、圧縮等は別工程であり、全ビルドと小さな変更後のビルドを同一視できない。[Unity増分ビルド解説](https://unity.com/blog/engine-platform/accelerating-player-builds-with-incremental-build-pipeline)（2022-12-20）。
- **コードとコンテンツの分割**：Assembly DefinitionはC#コードをアセンブリに分け、依存関係を管理する。Addressablesはアセット・シーンのグループ単位でビルドや配布を扱う。asmdefとAddressablesは目的が異なり、どちらも全工程を必ず高速化する魔法ではない。[Assembly definitions](https://docs.unity.com/en-us/engine/6000.5/manual/scripting/compilation-and-code-reload/script-compilation/assembly-definition-files/assembly-definitions-intro)、[Unity増分ビルド解説](https://unity.com/blog/engine-platform/accelerating-player-builds-with-incremental-build-pipeline)（2026-10-15閲覧）。
- **参加者ホスト方式**：専用シミュレーションサーバーの費用を減らせる一方、ホストの回線・端末性能に左右され、ホストに不正上の優位が生じる。NAT越えやRelayの採用が必要になり得て、Relayには費用がかかる。[Listen server and host architecture](https://mp-docs.dl.it.unity3d.com/netcode/2.1.1/learn/listen-server-host-architecture/)（更新2025-01-13、旧版公式資料。一般原理にのみ使用）。
- **権威の置き場所**：専用サーバーを中央の判定役にする構成は、不正な参加者への耐性と引き換えに維持費が増える。[Client-server topologies](https://mp-docs.dl.it.unity3d.com/netcode/2.1.1/terms-concepts/client-server/)（更新2025-01-13、旧版公式資料）。
- **ホスト離脱**：最新のUnity Multiplayer Services資料では「新ホストを選ぶこと」と「同期済みデータを移すこと」を分けている。選出だけではワールド状態は移らず、方式ごとの実装が必要。[Migrate session host](https://docs.unity.com/en-us/mps-sdk/session-host-migration)（2026-10-15閲覧）。
- **VRM**：VRMはプラットフォーム非依存の人型アバターファイル形式。表情・視線・SpringBone等の情報を共通化する一方、任意のUnityコンポーネントやゲームの仕組み全体を移植する形式ではない。[VRMの特徴・内容](https://vrm.dev/vrm/vrm_features/)（更新日不明、2026-10-15閲覧）。
- **性能評価**：Unity公式はまずプロファイルで原因を特定するよう勧める。描画コマンド、透明物の重なり、シェーダー、影等も負荷要因であり、三角形数だけでは性能を説明できない。[描画処理の最適化](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/optimizing-graphics-performance)（6000.3文書、2026-10-15閲覧）。
- **キャッシュ・抽出防止**：Unityの旧公式文書は、暗号化してもクライアントへ渡った描画用データの抽出を完全には止められないと説明する。古いAPIの実装例は採用せず、この原理のみ参照する。[Protecting Content](https://docs.unity.cn/550/Documentation/Manual/protectingcontent.html)（Unity 5.5の旧文書、2026-10-15閲覧）。
- **ノードとコード**：Unity Visual ScriptingはC#でカスタムノードを作り、グラフから使う仕組みを公式に提供する。「ノードとコードは必ずどちらか一方」という前提は不要。[Custom C# nodes](https://docs.unity.cn/Packages/com.unity.visualscripting@1.7/manual/vs-create-custom-node.html)（文書生成2022-05-10、旧パッケージ版の存在証明として使用）。

### 推論・企画への提案

1. 「Unityだと1時間かかる」は断定せず、**初回フルビルド／コード1件変更／アセット1件変更／実機へ反映**を別に測る。初期構想ではUI、通信、保存、制作ツールの責務を分けるが、分割し過ぎる設計も避ける。
2. 「P2P」は通信経路と判定権限を混同しやすい。参加者の1人がホストになるのか、オブジェクトごとに権威を持つのかを別途決める。認証・ストレージ・配信・Relay・監視費を含めて運用費を見積もる。
3. リング、オーブ、消費アイテム、所有権の最終記録は、任意のホストから自己申告された結果だけで更新しない構成を検討する。これは提案であり原メモの確定仕様ではない。
4. VRMは「他サービスから入る入口」、独自ギミックは「読み込んだ後にサービス側で付ける機能」と分ける。VRM採用だけを理由にプラットフォーム全体の自由度が低いとは断定しない。
5. 「ホーム5万ポリゴン以下」は暫定目安として残し、対象端末、フレーム時間、メモリ、読込時間、同時表示人数、スクリプト／物理負荷も評価項目にする。
6. 「キャッシュから絶対復元できない」は保証しない。「無断保存・再配布をUIとサーバー権限で制限し、抽出の手間を増やし、作者情報と通報対応を整える」に置き換える。
7. AI編集は読み書き可能なテキスト/API、空間内編集はノードやインスペクター、と役割分担できる。共通データモデル、安定ID、差分・Undo、権限チェックを先に検討する。任意のC#と任意のノードを完全に往復変換できるとは約束せず、対応範囲を定義する。

### 未確認・留意点

- 新企画の実装、Unity版、ホスト人数、転送量、基準端末が未定のため、所要時間・運用料金・FPSは算出していない。
- ここで示したネットワークの一般論からResoniteの実運用費や特定の現在実装を推測しない。
- 原メモの1GB、日次10リング、初期100リング、1ワールド50／同作者500、手数料5%はすべて独自の未確定案。既存サービスの確認済み数値と混ぜない。

## 3. 自由度と作品保全をどう両立するか

### 要点

「持ち物を使う権利」「内部構造を見る権利」「再配布」「外部に出す権利」「編集の操作権」は別に整理すると、利用者と制作者の双方が理解しやすい。サービス終了時にも残したいものを、初期設計から決める価値がある。

### 出典付きの確認事項

- Second Lifeの次所有者権限と第三者ビューアーのエクスポート条件は別に定められている。[Object permissions](https://community.secondlife.com/knowledgebase/english/object-permissions-r57/)、[Third Party Viewer Policy](https://go.secondlife.com/corporate/third-party-viewers)（2026-10-15閲覧、前節と同一出典）。
- VRMは対応アプリ間でアバターデータを共有するための形式として説明される。[VRMとは](https://vrm.dev/vrm/vrm_about/)（2026-10-15閲覧）。

### 推論・企画への提案

- **ユーザー視点**：購入条件を見て選べること、誤削除から戻せること、購入済みアイテムの再取得、ホスト離脱時の扱い、サービス終了時の保存範囲を優先する。
- **制作者視点**：作者・編集者の履歴は有用だが、それだけでは権利許諾の証明にならない。素材単位のライセンスと外部出力可否を保持し、共同編集権限と販売・再配布権限を分離する。
- 「ゲーム内制作物／Unity制作物／コード制作物の相互編集」は、まず位置・構造・対応パラメータ等の共通範囲を決める。Unity固有機能や任意コードまで完全再現することは別の開発課題として扱う。
- サービス終了時の移行性は、作者自身のモデル・テクスチャ・挙動データ・購入履歴・共同編集履歴のどれを出力できるか、出力形式、オフライン再生可能範囲に分解する。利用者が購入した他作者作品を無条件で出力可能にすることとは分ける。
- カスタムクライアントは拡張性の長所がある一方、互換性・安全性・購入物権限・サポートの境界が必要。最初は公開APIや許可制プラグイン、将来の第三者クライアント対応など、段階的導入も選択肢。

### 未確認・留意点

- Rec Roomの終了告知の個別検証は別担当に委ねている。本ノートでは終了日等を根拠として再引用しない。
- 上記は設計判断を助ける提案。金銭・年齢・法制度の具体的要件はこの技術調査で確定していない。
