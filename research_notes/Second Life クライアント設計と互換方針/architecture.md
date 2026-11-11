# Second Lifeのビューアーとサーバーの分離

## 第三者クライアントは実際にどう作られているか

### Takeaway
Second Lifeの有力な実例は、公開された公式ビューアーのコードを派生開発する方式です。独立再実装もポリシー上は排除されていませんが、最初から異なる描画エンジンで複数実装を整備することが第三者クライアント対応の前提ではありません。

### Cited Findings
- 公式リポジトリはクライアントのソースを収録し、2007年からオープンソース、現在の表示はLGPL-2.1。READMEは第三者ビューアーを第三者管理のforkとして紹介し、ビルド手順とディレクトリへ案内します。[公式viewer](https://github.com/secondlife/viewer)
- Firestorm公式READMEも、公式Second Lifeクライアントから派生した第三者ビューアーと明記しています。Windows/Mac/Linux向けを配布し、Second LifeとOpenSimを対象にします。[Firestorm公式ソース](https://github.com/FirestormViewer/phoenix-firestorm)
- 第三者ビューアーポリシーは、ソースの由来によらずサーバーへログインするソフトを対象にします。公式ソースに記録されたプロトコルとの互換、異なる点の公開文書化、各版固有の識別子を求めています。ソースライセンスとサービスへの接続条件は別です。[第三者ビューアーポリシー §1](https://go.secondlife.com/corporate/third-party-viewers)
- 同ポリシーは権限・プライバシー回避、作者/所有者メタデータ改変等を禁止し、公式ビューアー利用者にない共有体験の変更にも制約があります。独自UIや描画調整ができることは、サーバー側のルールを自由に変更できることではありません。[同 §2](https://go.secondlife.com/corporate/third-party-viewers)

### Inferences
- **今回のユーザー意図に合うのは、初期は公式クライアント1本を完成させ、後から派生クライアントを作れる構造にすること。** 以前のレビューで独立再実装や別エンジン互換を初期必須に寄せた解釈は修正すべきです。
- 将来の経路は二段階に分けられます。まず公式クライアントを元にUI・入力・描画品質を変更するfork、さらに必要になれば通信/データ層を再利用した別クライアントです。後者のために最初から複数エンジンを完成させる必要はありません。
- fork方式を実現するには、公開するソース・ビルド方法・再配布条件を用意することが重要です。MIT採用を自動決定するものではなく、Second LifeのLGPLをそのまま新企画に採用する必要もありません。
- サービス側の権限判定や共有状態は同一に保ち、UI、カメラ、入力、描画、キャッシュの改善をクライアント側で行える分担が現実的です。

### Gaps
- ビューアーディレクトリ掲載と個人開発・配布の全手続きの詳細は別担当のビルド調査に委ねます。ポリシーの法的助言はしていません。
- Firestormをローカルでビルド・ログインした実証はしていません。コードと一次資料の照合です。

## サーバーとビューアーは何を交換し何を分担するか

### Takeaway
描画とUIはビューアー側、共有空間の物理や状態とワールド内スクリプトは主にリージョンサーバー側にあります。接続は一つの万能APIではなく、UDPメッセージとHTTPのCapabilities、アセット/インベントリサービスなどを組み合わせています。

### Cited Findings
- サーバー構成の公式Wikiは、ログイン、データ管理、シミュレーター等を分けています。シミュレーターはオブジェクト/地形状態、物理・衝突等を担当し、ビューアーへ更新を送ります。公式資料自体に古い記述が混在するため、ホスト数、固定ループ速度、全配信経路の現状証明には用いません。[Server architecture](https://wiki.secondlife.com/wiki/Server_architecture)
- ビューアー構成のWikiには、入力・編集UI・描画・メディア・アセット取得・ローカルキャッシュの各系統があります。ただし1.20系説明やQuickTime等を含む歴史資料なので、現在の全実装とは扱いません。[Viewer Architecture](https://wiki.secondlife.com/wiki/Viewer_architecture)
- 現行developブランチにUDPの`message_template.msg`があり、型、フィールド、メッセージ番号、信頼区分等を定義しています。冒頭はメッセージ番号の保存を要求します。公開コードが通信仕様の具体的な参照になります。[メッセージ定義](https://github.com/secondlife/viewer/blob/develop/scripts/messages/message_template.msg)
- Protocol資料はバイナリUDPとCapabilitiesを説明し、CapabilitiesにはLLSDデータを用いるとします。Capabilitiesは特定機能へアクセスするURLを得る方式で、URLのホスト/パス形式を固定前提にしない説明があります。[Protocol](https://wiki.secondlife.com/wiki/Protocol)、[Capabilities](https://wiki.secondlife.com/wiki/Capabilities)
- 現行`llviewerregion.cpp`はSeedから機能URLを取得し、`EventQueueGet`、`SimulatorFeatures`、`ViewerAsset`等を扱います。HTTP GET/POST用関数と機能有無の確認も存在します。Wikiの概念が現行コードにも残ることを確認できます。[リージョン/Capabilities実装](https://github.com/secondlife/viewer/blob/develop/indra/newview/llviewerregion.cpp)
- `llviewerassetstorage.cpp`ではアセットIDと型からURLを組み、HTTPでバイナリを取得してキャッシュへ書き込みます。アセット本体の取得とリアルタイム状態更新は別経路です。[アセット取得実装](https://github.com/secondlife/viewer/blob/develop/indra/newview/llviewerassetstorage.cpp)
- `llaisapi.cpp`は`InventoryAPIv3`/`LibraryAPIv3`へのインターフェースです。機能が利用可能か確認し、インベントリの作成等をサーバーへ要求します。クライアントに表示用モデルやキャッシュがあっても、それだけを所有権の正本とする構造ではありません。[Inventory API実装](https://github.com/secondlife/viewer/blob/develop/indra/newview/llaisapi.cpp)
- LSLの入門資料は、編集画面はビューアーにあり、スクリプト実行はサーバーで行われ結果が送られると説明します。[LSL入門](https://wiki.secondlife.com/wiki/Getting_started_with_LSL)
- 新しいLua関連のFAQも、リージョン内Luaスクリプトとビューアー側Luaアドオンは別の取り組みで、前者はリージョン側で動くと明示します。公式制作サイトにはLSLとLuaの両方が案内されています。[Lua FAQ](https://wiki.secondlife.com/wiki/SLua_FAQ)、[公式スクリプト案内](https://create.secondlife.com/script/)

### Inferences
- Second Lifeは「サーバーが映像を作りビューアーに配信するクラウドレンダリング」ではありません。サーバーから状態と素材を取得し、クライアント側が画面を作る方式です。
- ビューアーが成立するために、サーバー実装そのもののソースを必ず公開する必要はありません。接続先の契約・通信データ・コンテンツの意味をクライアントが理解できればよく、公式クライアントのソースもその実例になります。
- 権限に関するUI表示と、共有データを変更してよいかのサーバー検証は別です。新企画の改造クライアントでも前者の自由と後者の一貫性を両立させる必要があります。
- VRの掴みやIKまでSecond Lifeの実装に合わせる必要はありません。VRでは手元の予測・追従をクライアント側に持ち、共有結果を別途確定する設計が必要になります。

### Gaps
- リンデン運営サーバーの全ソースを検査したものではないため、内部構成と認証方式の細部は断定しません。Protocol Wikiのログイン説明も歴史的な情報が混在します。
- アセットキャッシュの暗号化・抽出防止の強度は今回測定していません。キャッシュ実装の存在から保護が完全だとは言えません。
- Luaの実際の全グリッド展開率・利用可能なサーバー版は調査対象外です。ワールド実行とビューアー拡張が別、という責務の確認にだけ使用します。

## 新企画で今用意する境界と後からでよいこと

### Takeaway
ユーザーが求める「後から別クライアントを作れる程度」であれば、最初のクライアントとサーバーを明確なデータ・命令で接続し、画面/UI/入力から通信と永続データを分ければよいです。公開SDK、複数描画エンジン、完全な独立再実装を初期必須にする必要はありません。

### Cited Findings
- 公式Second Lifeクライアントはビルド可能なソースを公開し、第三者forkが同じサービスへ接続します。この方式が将来の派生クライアントの具体的先例です。[公式viewer](https://github.com/secondlife/viewer)、[Firestorm](https://github.com/FirestormViewer/phoenix-firestorm)
- 接続互換はソースに記録されたプロトコルで判断し、クライアントの名前/版を区別するという運用です。[Third Party Viewers](https://go.secondlife.com/corporate/third-party-viewers)
- 機能の有無を問い合わせ、アセット・インベントリなどを分けた実装が現存します。新企画でも、内部の描画ノードをそのまま通信・保存の契約にしない参考になります。[機能照会](https://github.com/secondlife/viewer/blob/develop/indra/newview/llviewerregion.cpp)、[Inventory API](https://github.com/secondlife/viewer/blob/develop/indra/newview/llaisapi.cpp)

### Inferences
**現時点で書くとよい方針案（ユーザー要件からの設計提案であり、Second Life仕様の転載ではない）：**

1. 初期提供は公式クライアントを中心にする。Unity等のエンジンは未決定。将来、同じサービスに接続する別クライアントを開発できる設計にする。
2. 接続/認証、オブジェクトIDと状態更新、編集命令、アセット参照、所持品・取引を明示的なAPI/メッセージにする。画面表示の都合で永続データを変えない。
3. プロトコルと保存形式に版を持たせる。必要な時点で機能一覧や代替表示を追加できるようにする。公開仕様の完成版や第三者認証制度は今決定しなくてよい。
4. 描画・UI・入力のコードから通信/データ処理を分ける。別プロセス化や別ライブラリ化は選択肢であり、将来クライアントのために今すべて別プロセスへ分割する必要はない。
5. 派生開発が必要になった時に、公式ソースを公開/提供するか、通信とデータ処理のSDKを公開するかを決められる構成にする。非公開の巨大単一実装だけに依存すると後からの負担が増える。

**先送りできるもの：** 二本目の完成クライアント、別エンジンによる全描画再実装、公開SDKの製品化、全通信仕様の恒久固定、Third-party directoryのような運営制度。

**先送りすると困るもの：** IDと所有の意味、共有状態の確定担当、通信と描画オブジェクトの密結合、公開品/所持品/配置物の混同。これらは公式クライアント1本でも必要です。

### Gaps
- 将来のクライアント公開方式・ライセンスはユーザーがまだ決めていません。オープンソース公開を既決定として企画書へ書き込まないでください。
- この調査はSecond Life互換サービスを作る提案ではありません。UDP、LLSD、リージョン方式、LSL、Havokを採用する必然性はありません。
