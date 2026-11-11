from pathlib import Path
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
import difflib
import json
import re
from markdown_it import MarkdownIt

root = Path(__file__).resolve().parents[2]
notes = Path(__file__).resolve().parent
report = root / 'reports' / 'Second Life クライアント設計と互換方針.md'
new_html = root / 'SecondLifeクライアント調査.html'
plan = root / '新メタバース企画.html'
memo = root / '企画書に満たないモノ.txt'
agents = root / 'AGENTS.md'
agents_hash = sha256(agents.read_bytes()).hexdigest()
assert agents_hash.upper() == '0EA9B667ED698353312583E792739C08174C2D9A806A3055038A3961D6766CD9'

source = report.read_text(encoding='utf-8')
md = MarkdownIt('commonmark').enable('table')
tokens = md.parse(source)
navigation = []
section = 0
for i, token in enumerate(tokens):
    if token.type == 'heading_open' and token.tag == 'h2':
        section += 1
        key = f'section-{section}'
        token.attrSet('id', key)
        navigation.append(f'<a href="#{key}">{escape(tokens[i+1].content)}</a>')
body = md.renderer.render(tokens, md.options, {})
body = body.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
css = '''
:root{--ink:#20363d;--muted:#61747b;--accent:#146b66;--line:#d8e4e3;--bg:#f3f7f6;--paper:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.9 "Yu Gothic UI","Meiryo",sans-serif}header,main,footer{max-width:1080px;margin:auto}header{padding:36px 40px 20px}header p{font-size:13px;color:var(--muted);margin:0 0 12px}nav{display:flex;gap:8px 24px;flex-wrap:wrap;font-size:14px}nav a{text-decoration:none}main{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:30px 44px 44px}h1{font-size:clamp(25px,3.5vw,36px);line-height:1.5;margin:0 0 18px}h2{font-size:24px;line-height:1.5;margin:42px 0 20px;padding-bottom:10px;border-bottom:2px solid var(--accent)}p{margin:0 0 18px}main>p:first-of-type{font-size:13px;color:var(--muted)}main>p:nth-of-type(2){background:#edf6f3;padding:18px 22px;border-left:3px solid var(--accent)}a{color:var(--accent);text-underline-offset:3px;overflow-wrap:anywhere}a:hover{color:#08443f}strong{font-weight:700}code{font-family:Consolas,"Yu Gothic UI",monospace;font-size:.9em;overflow-wrap:anywhere}pre{background:#eff3f5;padding:18px;border:1px solid var(--line);border-radius:7px;overflow:auto;line-height:1.7}pre code{white-space:pre;overflow-wrap:normal}.table-wrap{overflow-x:auto;margin:20px 0 24px;border:1px solid var(--line);border-radius:7px}table{border-collapse:collapse;width:100%;font-size:14px;min-width:550px}th,td{padding:13px 16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{background:#edf3f2}tr:last-child td{border-bottom:0}td:first-child{font-weight:650;width:32%}footer{padding:24px 40px 38px;font-size:13px;color:var(--muted)}:focus-visible{outline:3px solid #409b91;outline-offset:4px}
@media(max-width:760px){body{font-size:15px}header{padding:24px 20px 18px}main{margin:0 10px;padding:22px 18px 30px}h2{font-size:21px}main>p:nth-of-type(2){padding:14px 16px}footer{padding:20px}pre{padding:13px;font-size:13px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:white;color:#111;font-size:10pt}header,footer{display:none}main{border:0;border-radius:0;padding:0;max-width:none}h1{font-size:23pt}h2{font-size:16pt;margin-top:24px;break-after:avoid}pre{white-space:pre-wrap;font-size:8pt}pre code{white-space:pre-wrap}.table-wrap{overflow:visible}table{min-width:0;font-size:9pt}th,td{padding:7px}tr{break-inside:avoid}a{color:inherit}}
'''
html = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Second Lifeのクライアント設計と互換方針</title><style>{css}</style></head>
<body><header id="top"><p>クライアント開発の調査・アバター互換要件</p><nav aria-label="目次">{''.join(navigation)}</nav></header><main>{body}</main>
<footer><a href="新メタバース企画.html">企画書：E:\\programing\\新メタバース\\新メタバース企画.html</a>　<a href="#top">先頭へ</a></footer></body></html>
'''
new_html.write_text(html, encoding='utf-8', newline='\n')

all_diffs = []
def patch_file(path, replacements):
    original = path.read_bytes().decode('utf-8')
    newline = '\r\n' if '\r\n' in original else '\n'
    # Recover this script's own completed replacements on a partial-run retry.
    for old, new in reversed(replacements):
        old, new = old.replace('\n', newline), new.replace('\n', newline)
        if original.count(new) == 1:
            original = original.replace(new, old, 1)
    text = original
    applied = []
    for old, new in replacements:
        old, new = old.replace('\n', newline), new.replace('\n', newline)
        assert text.count(old) == 1, (path.name, old[:100], text.count(old))
        text = text.replace(old, new, 1)
        applied.append((old, new))
    inverse = text
    for old, new in reversed(applied):
        assert inverse.count(new) == 1
        inverse = inverse.replace(new, old, 1)
    assert inverse == original, 'unrelated content changed'
    all_diffs.extend(difflib.unified_diff(original.splitlines(True), text.splitlines(True), fromfile=path.name+' before', tofile=path.name+' after'))
    path.write_bytes(text.encode('utf-8'))
    return len(applied)

avatar_box = '''    <div class="box wide"><h3>アバターの取り込み・シェーダー</h3><ul>
      <li>VRMに加え、VRChat向けunitypackageからアバターを取り込む。</li>
      <li>unitypackageの対応範囲は、揺れ物、マテリアル、表示／非表示、円形メニューからのオブジェクトON／OFF、シェイプキー変更とする。</li>
      <li>lilToonは元のシェーダーとマテリアル設定を利用し、元の見た目を再現する。ユーザーが別のシェーダーへ手作業で置き換えることを前提にしない。</li>
      <li>非対応端末やクライアント、描画失敗時にはフォールバックを使用する。</li>
    </ul></div>
'''
client_box = '''    <div class="box wide"><h3>将来の別クライアント</h3><ul>
      <li>まず公式クライアントを開発し、後から別クライアントを作れる構造にする。</li>
      <li>通信・アセット参照・ワールド状態・所持品の処理を、描画・UI・入力から分離する。</li>
      <li>Second Lifeの派生ビューアー開発を参考にする。ソースの公開範囲やライセンスは未決定。</li>
    </ul></div>
'''
research_add = '''  <div class="research"><h3>Second Lifeの派生ビューアー開発</h3><p>Firestormなどは公開された公式ビューアーのソースを元に、UI・描画・入力などを変更して同じサービスへ接続する。公式ビューアーはC++・OpenGLを使い、AutobuildとCMakeでビルドする。本企画も、まず公式クライアントを作り、後から派生・別実装できるよう通信とデータ処理を描画から分ける。初期から複数エンジンや二本目のクライアントを実装する前提は置かない。</p><div class="refs"><a href="https://github.com/secondlife/viewer">Second Life公式ソース</a><a href="https://github.com/FirestormViewer/phoenix-firestorm">Firestorm公式ソース</a><a href="SecondLifeクライアント調査.html">調査詳細：E:\\programing\\新メタバース\\SecondLifeクライアント調査.html</a></div></div>
  <div class="research"><h3>lilToonの元シェーダー利用</h3><p>lilToonの元シェーダーと設定を使うため、採用する描画基盤に合わせて取り込み・展開・コンパイルを設計する。Unity以外では、言語変換だけでなくShaderLab、複数Pass、描画状態、Unity固有の照明や組み込み値を扱う互換層が必要になる。元ソースを保持して内部で変換・再コンパイルする方式は検証前であり、Godot標準でそのまま動くことやUnityのコンパイル済みShaderを無変更で読めることを確認したものではない。元シェーダー利用は要件として維持し、この互換処理の実現性をエンジン選定で比較する。</p><div class="refs"><a href="https://github.com/lilxyzw/lilToon/blob/master/Assets/lilToon/Editor/lilShaderContainerImporter.cs">lilToon公式Importer</a><a href="https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Shader.html">Unity ShaderLab</a></div></div>
'''
html_changes = patch_file(plan, [
('企画メモ・サービス比較　2026.10.15', '企画メモ・サービス比較　初版 2026.10.15／基盤・互換方針更新 2026.11.11'),
('<li>Unityを使用。</li>', '<li>描画エンジンは未決定。Unityは必須条件としない。</li>'),
('    <div class="box"><h3>アバター・移動</h3><ul>', avatar_box+'    <div class="box"><h3>アバター・移動</h3><ul>'),
('Resoniteのインスペクターを参考にし、Unityで作った物との相互編集も目指す。', 'Resoniteのインスペクターを参考にし、Unityで作った物との相互編集も目指す。unitypackageでは上記のアバター機能を対応範囲とし、Animator全機能の互換を前提にはしない。'),
('    <div class="box"><h3>セッション</h3><ul>', client_box+'    <div class="box"><h3>セッション</h3><ul>'),
('<li>ポリシーの範囲で第三者ビューアーを開発できる。<a class="source" href="https://go.secondlife.com/corporate/third-party-viewers">第三者ビューアー ↗</a></li>', '<li>公開された公式ビューアーを元に、UI・描画・入力などを改変して第三者ビューアーを開発できる。Firestormも公式クライアントから派生している。<a class="source" href="https://github.com/secondlife/viewer">公式ソース ↗</a><a class="source" href="https://github.com/FirestormViewer/phoenix-firestorm">Firestorm ↗</a><a class="source" href="https://go.secondlife.com/corporate/third-party-viewers">接続ポリシー ↗</a></li>'),
('  <h2><span class="n">04</span>技術調査</h2>\n', '  <h2><span class="n">04</span>技術調査</h2>\n'+research_add),
])

memo_avatar = '''- VRMをインポート可能にする。VRMの基本表現と、読込後に付ける独自ギミックを分ける。
- VRChat向けunitypackageからアバターを取り込み、揺れ物、マテリアル、表示／非表示、円形メニューからのオブジェクトON／OFF、シェイプキー変更に対応する。
- lilToonは元のシェーダーとマテリアル設定を利用し、元の見た目を再現する。ユーザーが別のシェーダーへ手作業で置き換えることを前提にしない。
- 非対応端末やクライアント、描画失敗時にはフォールバックを使用する。'''
memo_client = '''## 7. セッションと運営基盤

まず公式クライアントを開発し、後から別クライアントを作れる構造にする。通信・アセット参照・ワールド状態・所持品の処理を、描画・UI・入力から分離する。初期から複数エンジンや二本目のクライアントを実装する前提は置かない。ソースの公開範囲やライセンスは未決定。

Second Lifeでは公開された公式ビューアーを元に、Firestormなどの派生ビューアーが作られている。公式ビューアーはC++・OpenGLを使い、AutobuildとCMakeでビルドする。この派生開発の仕組みを参考にする。
出典：https://github.com/secondlife/viewer
出典：https://github.com/FirestormViewer/phoenix-firestorm
調査詳細：E:\\programing\\新メタバース\\SecondLifeクライアント調査.html'''
memo_compat = '''

lilToonの元シェーダーを利用するための取り込み・展開・コンパイル方式は、採用する描画基盤に合わせて設計する。Unity以外では、ShaderLab、複数Pass、描画状態、Unity固有の照明や組み込み値を扱う互換層が必要になる。元ソースを保持して内部変換・再コンパイルする方式は検証前であり、Godot標準やUnityのコンパイル済みShaderとの無変更互換を確認したものではない。元シェーダー利用は要件として維持し、実現性をエンジン選定で比較する。
出典：https://github.com/lilxyzw/lilToon/blob/master/Assets/lilToon/Editor/lilShaderContainerImporter.cs
出典：https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Shader.html
'''
memo_changes = patch_file(memo, [
('整理・調査日：2026年10月15日', '整理・調査日：2026年10月15日／基盤・互換方針更新：2026年11月11日'),
('- Unityを使用する案。', '- 描画エンジンは未決定。Unityは必須条件としない。'),
('- VRMをインポート可能にする。VRMの基本表現と、読込後に付ける独自ギミックを分ける。', memo_avatar),
('Resoniteのインスペクターを参考にし、Unityで作った物との相互編集も目指す。', 'Resoniteのインスペクターを参考にし、Unityで作った物との相互編集も目指す。unitypackageでは上記のアバター機能を対応範囲とし、Animator全機能の互換を前提にはしない。'),
('## 7. セッションと運営基盤', memo_client),
('## 4. ワールド・アイテム・制作', memo_compat+'\n## 4. ワールド・アイテム・制作'),
])

class CheckHTML(HTMLParser):
    void = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):
        super().__init__(); self.stack=[]; self.ids=[]; self.links=[]; self.errors=[]; self.external_assets=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag=='a' and 'href' in attrs: self.links.append(attrs['href'])
        if tag in {'script','img','iframe','link'} and any(attrs.get(k,'').startswith(('http:','https:','//')) for k in ('src','href')): self.external_assets.append(attrs)
        if tag not in self.void: self.stack.append(tag)
    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1]!=tag: self.errors.append((tag,list(self.stack)))
        else: self.stack.pop()

checks={}
for path in (plan,new_html):
    s=path.read_bytes().decode('utf-8')
    assert '\ufffd' not in s
    p=CheckHTML(); p.feed(s)
    assert not p.errors and not p.stack, (path.name,p.errors,p.stack)
    assert len(p.ids)==len(set(p.ids))
    assert all(link[1:] in p.ids for link in p.links if link.startswith('#'))
    local=[link for link in p.links if not link.startswith(('#','http:','https:','mailto:'))]
    assert all((path.parent/link).exists() for link in local),local
    assert not p.external_assets
    checks[path.name]={'headings_or_ids':len(p.ids),'links':len(p.links),'local_links':local,'structure':'ok'}
for path in (plan,memo):
    s=path.read_text(encoding='utf-8')
    for need in ('Unityは必須条件としない','揺れ物','マテリアル','表示／非表示','円形メニューからのオブジェクトON／OFF','シェイプキー変更','元のシェーダーとマテリアル設定','後から別クライアント','元ソースを保持'):
        assert need in s,(path.name,need)
assert sha256(agents.read_bytes()).hexdigest()==agents_hash
checks['changes']={'plan_replacements':html_changes,'memo_replacements':memo_changes,'outside_replacements_unchanged':True,'AGENTS_sha256':agents_hash,'browser_visual_check':False,'engine_build':False}
(notes/'changes.diff').write_text(''.join(all_diffs),encoding='utf-8',newline='')
(notes/'validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
