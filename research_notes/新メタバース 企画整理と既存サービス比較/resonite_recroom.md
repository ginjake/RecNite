# Resonite・Rec Room：利用者とワールド制作者の比較調査

## 1. どの時点・提供状況を比較しているか

### Takeaway

調査日：2026-10-15。Resoniteは現行製品として、Rec Roomは公式が2026-06-01を終了日として告知したサービスの歴史的設計として扱う。公式サイトの検索索引と直接取得結果が異なるため、取得方法を隠さない。

### Cited Findings

- Resonite公式Steamページは無料プレイ・早期アクセスとして公開されており、PCの動作要件とVR対応を掲載する。公式サイト、公式GitHubも閲覧できる。これは公開情報の確認であり、本調査でオンラインセッションへ接続したわけではない。— [公式Steam掲載](https://store.steampowered.com/app/2519830/Resonite/)、[公式サイト](https://resonite.com/)
- Rec Roomの2026-03-30公式告知は2026-06-01のサービス終了、ログイン停止、rec.netとStudioオンライン機能の終了を案内した。費用が収益を上回り持続可能な利益を実現できなかったという事業者自身の説明がある。検索索引に本文を確認できるが、直接openは取得エラー。— [School’s Out for Rec Room](https://blog.recroom.com/posts/schools-out-for-rec-room)
- 元の利用規約も6月1日の利用許諾終了を記載していた。ただし調査日の直接取得結果は「Coming Soon」だけで、旧本文は検索索引から確認した。— [Rec Room利用規約](https://recroom.com/terms-of-service)
- VRChat公式ブログの「We’re Here.」本文でもRec Roomが6月1日に終了すると発表したことを確認できる。これは告知の裏づけであり、6月1日に実際に停止したことの独立検証ではない。— [VRChat公式ブログ](https://hello.vrchat.com/blog)
- 2026-04-06のRec Room公式告知はSteam PC版向けデータ出力を案内したが、サーバーなしで動く完成ルームをダウンロードできるわけではないと明記した。Room/Invention/Cloudデータを使って別環境で再制作するための出力である。本文は検索索引で確認、直接取得は失敗。— [Exporting your creation data](https://blog.recroom.com/posts/2026/4/6/exporting-your-creation-data)

### Inferences

- 利用者数や制作機能の豊富さだけで事業継続性を判断できない。新企画では制作物の持ち出し、サービス終了時の移行、運営費と収益を初期設計に含める。
- 「終了済み」と書く場合は「公式告知上の終了日を過ぎている」と根拠を添える。現在遊べる製品の推薦表にRec Roomを混ぜない。

### Gaps

- Rec Roomの実サーバー停止時刻、返金の実施状況、全クリエイターへの最終支払い完了は独立確認していない。
- Resonite Wikiは公式ドメインの共同編集文書であり、全記述が開発者の最終仕様保証ではない。古い制約ページと新しいノード分類に不整合があるため、バージョンをまたぐ断定は避ける。
- Rec Room旧公式ページ（community-commerce、studio、press、room-moderation-guide等）は検索索引に詳細本文が残る一方、現在の直接取得ではComing Soonとなる。以下のRec Room旧仕様は「当時の公式説明」と明記し、現行仕様とは呼ばない。

## 2. Resoniteは利用者・制作者にどんな長所と制約があるか

### Takeaway

交流中に作り、動かし、保存し、渡す一連の流れが強み。配布手段・外部コード連携は実在する一方、発見性、学習負担、標準表現機能、端末の広がりを新企画で改善できる余地がある。

### Cited Findings

#### 利用者に関わる確認仕様

- 無料プレイでPC/VRに対応。Steamの推奨条件は16GB RAM、RTX 2070相当以上、8コアCPU等で、VRでは要件が増すと注意書きがある。「誰の端末でも軽い」とは読めない。— [公式Steam掲載](https://store.steampowered.com/app/2519830/Resonite/)
- インベントリはアバター、ツール、装飾品等を保存し、フォルダーで管理する。初期クラウド容量は1GB、有料支援で増量。同一保存物の変更は追加部分のみ容量計上されると説明される。既存項目のフォルダー間移動はスポーン→保存し直し等が必要という操作上の制約も記載される。Inventoryは今回直接取得がタイムアウトしたため検索索引本文を使用。— [Inventory](https://wiki.resonite.com/Inventory)
- 公開フォルダーをオブジェクトまたはテキストURLで渡せる。内容の容量負担は所有者側で、受け取る側には加算されない。公開化だけで全ユーザー向け検索一覧に自動掲載されるわけではない。ページ最終更新2026-09-14。— [Public folders](https://wiki.resonite.com/Public_folders)
- アバター・移動・会話のみのSpectator、アイテム出現・操作可能なGuest、管理用Moderator、編集用Builder、全管理Adminという役割がある。原メモにはModeratorが抜けている。— [Permission system](https://wiki.resonite.com/Permission_system)
- Quest ProのSteam Link OSC、Project Babble、Baballonia等に対応する説明がある。Baballoniaネイティブ統合は2026-03-03の版として掲載。機器・接続方法によって外部ソフトやModが必要なケースもあり、「全機器を無設定で標準対応」は言い過ぎ。— [Face and Eye Tracking Setup](https://wiki.resonite.com/Face_and_Eye_Tracking_%28Troubleshooting%29)
- カスタムシェーダーは標準ユーザーコンテンツとして未対応との説明がある。公式GitHubは、Unityで技術的に事前コンパイルすること自体よりも、将来レンダラーを変更した際の長期互換性を理由に挙げる。「実行時JITコンパイルできないから」だけでは不十分。— [Custom shaders](https://wiki.resonite.com/Custom_Shaders)、[公式Resonite.UnityShaders](https://github.com/Yellow-Dog-Man/Resonite.UnityShaders)
- 揺れ物は独自DynamicBoneChainを持ち、調整パラメータ、接触、掴みの設定がある。Wikiはねじりと制約に制限があると記載。「揺れ物がない」ではない。— [DynamicBoneChain](https://wiki.resonite.com/Dynamic_Bone_Chain)

#### ワールド制作者に関わる確認仕様

- ProtoFluxは3D空間で編集するノード言語で、共同編集とその場での応答が特徴。同期されるData Model Storeと非同期のStore/Localを区別する必要があり、「何でも自動同期で考慮不要」ではない。過剰な同期は性能負担になり、非同期の使用には設計が必要。— [ProtoFlux](https://wiki.resonite.com/ProtoFlux)
- ファイルブラウザーからローカル素材を取り込み、オブジェクトをファイルへ出力できる。一部形式にはBlender等が必要。アバターのIKには骨階層・名前の要件がある。— [File Browser](https://wiki.resonite.com/File_Browser)
- `.ResonitePackage`によるオブジェクト出力は可能だが、Unity直接読込用ではなく、外部での独自生成にも内部形式の互換性問題がある。外部編集にはResoniteLinkを推奨する説明がある。— [ResonitePackage](https://wiki.resonite.com/ResonitePackage)
- 2026-01-08のリリースでResoniteLinkを導入。JSON WebSocket経由で外部プログラムからワールドのデータモデルを読み書きできる。公式GitHubはホスト側で外部プログラムを動かす必要と、通常の実行ロジックにはProtoFluxを推奨することを明記する。返却JSONの保存は長期保存形式として保証されない。— [導入リリース](https://wiki.resonite.com/Beta_2026.1.8.6)、[公式ResoniteLink](https://github.com/Yellow-Dog-Man/ResoniteLink)
- Scripting supportはProtoFluxの標準JSON処理不足、コミュニティ製ProtoGraphによるテキストからノード生成、C#プラグインで追加した場合の参加互換性の制約を説明する。これはResoniteLinkによるJSON外部連携の存在と矛盾しない。— [Scripting support](https://wiki.resonite.com/Scripting_support)
- 外部HTTP GET/POST等の通信が可能。JSONの変換は自作処理等が必要というWiki説明がある。外部APIをつなげる余地と、API側の形式・認証・依存性を扱う制作負担を分ける。— [Connecting Resonite to other applications](https://wiki.resonite.com/Connecting_Resonite_to_other_applications)
- 2025-08-25更新の公式Mod規約は開発・配布・導入を認める。ただし保護やモデレーションの回避、他者への悪影響は禁止で、公式サポート対象ではない。代替レンダラー作成も規約を満たす範囲で許容。— [Mod and Plugin Policy](https://policies.resonite.com/ModAndPlugin)
- セッションは通常ユーザーPCやHeadlessがホスト。アカウント、メッセージ、アセット等はクラウドサービスを利用し、直接接続できない場合はリレーを利用する。リレーには遅延・混雑の影響がある。— [Networking information](https://wiki.resonite.com/Networking_Information)
- Headlessは特定支援階層で利用でき、サーバー運用は利用者側。描画不要な常設セッション向けで、運営が代行ホストしてくれる意味ではない。— [Headless server software](https://wiki.resonite.com/Headless_server_software)
- 2025-11-24リリースは.NET 10への移行を明記。原メモの.NET 9というバージョン固定は古い。UnityとFrooxEngineの分離は説明されるが、他サービスより常に軽いというベンチマークにはならない。— [Beta 2025.11.24.1340](https://wiki.resonite.com/Beta_2025.11.24.1340)、[The Performance Updates](https://wiki.resonite.com/The_splittening)

### Inferences

- 利用者の長所：思いついた遊びをその場で共有しやすい。道具・アバターを持ち歩けるため、ワールドごとに体験を閉じずに交流を広げられる。公開フォルダーは作者の更新を届けやすい。
- 利用者の短所：編集・権限・インベントリを理解するまでの操作量が多い。PC中心の配布ではスマートフォンだけの友人を誘いにくい。持ち込めるものが多いほど、負荷や他者への干渉に対する本人の制御が必要。
- 制作者の長所：共同で見ながら編集・試運転でき、長いアップロード待ちを挟まず調整できる。ResoniteLinkは外部スクリプトやAI支援による制作をつなぐ候補になる。
- 制作者の短所：ノードの大規模化、依存関係や同期範囲の理解、従来のテキスト差分レビュー・自動テストとの接続は別途工夫がいる。公開フォルダーがあることと、商品検索・購入・更新管理が一つの公式ストアにまとまることは別問題。
- P2Pは運営側のセッション計算を分散できる可能性があるが、ホストの端末・上り回線・可用性に負担を移す。クラウド保存、配信、リレー、認証、監視の費用は残る。Resoniteの実際の原価を公開資料から断定しない。
- UIやIKやファーを「悪い」と一般化せず、原メモ著者の体験として残す。新企画の検証基準には、足滑り、肘膝の破綻、座位、トラッカー欠落、骨格差、衣服貫通、GPU負荷等の観測項目を置く。

### Gaps

- ProtoFluxに汎用JSON専用ノードが一切ないことを現行バイナリから網羅検証していない。古いWikiのCollections/Arrays不可説明は現在のカテゴリにCollectionsがある点と不整合なので、配列一般を不可能と断定しない。
- Quest単体版の公式公開は今回確認できなかった。非公式GitHubに存在を主張する文書が検索されたが、公式配布の裏付けがなく不採用。PC接続Quest対応と単体アプリ対応を混同しない。
- Resoniteの標準商取引・決済・クリエイター収益分配の現行提供範囲は十分確認できていない。「配布システムがない」「販売が絶対不可能」とは書かず、統合ストアの確認ができないとする。
- 各機種でのFPS、規模別メモリー、消費電力、サービス間のIK・Cloth・物理比較は実測していない。性能と見た目の順位は出さない。

## 3. Rec Roomのどの歴史的設計を参考にできるか

### Takeaway

交流のジェスチャー、ゲーム内制作とUnityの接続、商品発見と購入の導線は設計資料として有用。ただし「自由なトークン送金」「購入物の自由編集」「通常から自由な外部エクスポート」まであったと拡張しない。

### Cited Findings

- 当時の公式Press説明は無料でPC、スマートフォン、VR、ゲーム機に対応としていた。端末をまたいで友人を誘える設計だったが、現在の提供情報には転用しない。— [旧公式Press](https://recroom.com/press)
- 公式Avatar Movement & Gameplay（2023-05-09）はパーティ結成にfist bumpを挙げる。原メモの「ハイタッチでグループ」は、参考元の実仕様としては拳を合わせる操作へ訂正。握手でフレンドという操作は旧Help CenterのVR Controls and Gesturesで説明されていたが、今回取得できたのはrecroom.networkへのミラーで、公式直参照ではなく補助資料扱い。— [公式ジェスチャー説明](https://blog.recroom.com/posts/2023/5/9/avatar-movement-amp-gameplay)、[旧Help Centerミラー](https://zendesk.recroom.network/hc/en-us/articles/4424652450071-VR-Controls-and-Gestures)
- Rec Room StudioはUnity内から公開し、Maker Penと相互に編集する構想・対応を公式説明。素材・テクスチャ、Terrain、ProBuilder、アニメーション、音、Circuitsイベントを列挙。これはUnityの任意C#をそのまま実行できる証明ではない。— [旧公式Studio](https://recroom.com/studio)
- CV2には実行・データのワイヤー点滅や出力ポート確認を使うデバッグ補助の更新記録がある。— [公式Steam更新記録](https://store.steampowered.com/news/posts/?appids=471710&enddate=1650510206&feed=steam_community_announcements)
- 当時のCommunity CommerceはInventions、Room Keys、Room Currencies、繰り返し購入・消費するRoom Consumablesを説明。売上は一週間の保留後70%を販売側へ渡す旧説明がある。有料InventionはUse Onlyで編集等を制限した。保護と購入後カスタマイズのトレードオフを示す。— [旧公式Community Commerce](https://recroom.com/community-commerce)
- 2020-08-17のKeys紹介は、アイテムや衣装の利用権を販売し、販売者側へ70%を配分する設計を説明。これは新企画の手数料5%案と同じ率ではない。— [Earn Tokens by Selling Keys](https://blog.recroom.com/posts/2020/8/11/earn-tokens-by-selling-keys)
- 2023年イベントには衣服を友人へギフトする仕組みがあり、2021-09-07のFriend-O-Tron更新には友人へ一日一回無料ギフトを贈る機能がある。これは任意の保有アイテムを譲渡できた証拠ではない。— [Valentine’s Day 2023](https://recroom.com/valentinesday2023)、[Friend-O-Tron更新](https://recroom.com/ship-notes/2021/9/7/rec-room-patch-the-bento-box-edition)
- 当時の規約ではトークンの取得方法や換金資格を定め、許可された仕組み以外での譲渡・交換等を制限。購入トークンを自由に現金へ戻す制度とは区別されていた。— [旧利用規約](https://recroom.com/terms-of-service)
- 2020-11-30の経済開発ブログは報酬のbot farmingが経済の不安定さとクリエイター報酬の障害になると説明。単純ログイン・滞在報酬に不正対策が必要な直接の参考になる。— [More Rewarding Rewards](https://blog.recroom.com/posts/2020/11/20/more-rewarding-rewards)
- 旧モデレーションガイドは役割による発言権変更、テキスト・音声モデレーションを説明。モデレーター機能があることと有害行動を完全に防げることは別。— [旧Room Moderation Guide](https://recroom.com/room-moderation-guide)

### Inferences

- 利用者の長所（歴史比較）：参加端末の幅、短い身体ジェスチャーからフレンド・パーティにつながる操作、ギフトと遊びの共有。元メモ著者の「UIが最高」「物理が良い」は著者の評価として維持できる。
- 利用者の短所（設計評価）：購入した物がUse Onlyなら自分の用途に合わせて修理・改変しにくい。課金通貨と現金の距離があり、価格・利用範囲・サービス終了リスクを理解する必要がある。
- 制作者の長所（歴史比較）：Maker Penで初心者も制作に入り、Studioで外部DCC/Unity経験を生かせる。販売、アクセス権、消耗品を既存経済の上で設計できた。
- 制作者の短所（設計評価）：規定の実行機能・権限・経済条件に従う必要がある。ノードとUnityの両方を使うほど学ぶ面が増える。公式の持ち出しツールがあっても、動作するサービスの完全移植にはならなかった。
- 新企画に移すなら「発見→試用→権限と負荷の確認→入手→保存→更新通知」を一つの導線にする。編集許可、再配布、商用利用、外部出力、ワールド内での利用を独立に説明する。
- 通貨の参考は「無償配布と有償通貨を混ぜると不正取得が収益分配まで波及する」点。リングの滞在報酬、作者別上限、手数料5%は原企画独自案でありRec Roomの実績で正当化しない。

### Gaps

- Rec Roomの全期間・全商品で同じ分配率だったとは確認していない。旧Community Commerceの70%と終了前の特殊条件を混ぜず、具体的な現行収益モデルの比較には使わない。
- 原メモの「作者がインスペクター閲覧・外部エクスポートの可否を任意設定できた」は今回の公式資料でそのまま裏付けできなかった。確認できるのはInvention編集制限と、終了前の限定的なデータ出力。
- Wishlist、称号、入室時警告の細かなUIや全警告分類は今回公式資料で網羅確認していない。著者の体験・採用したい提案として残す。警告タグを付ければあらゆる表現が許されるという意味にはしない。
- 最新期の任意C#実行可否、ルームの全共同編集競合処理、同期実装・完全な自動テスト環境は確認不足。StudioがUnity製だから自由なUnityプロジェクトと同等とは書かない。
