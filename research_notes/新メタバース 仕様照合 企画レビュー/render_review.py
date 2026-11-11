from pathlib import Path
import re
import html
from html.parser import HTMLParser
from collections import Counter

root = Path(__file__).resolve().parents[2]
source = root / 'reports' / '新メタバース 仕様照合 企画レビュー.md'
target = root / '新メタバース企画レビュー.html'
md = source.read_text(encoding='utf-8')

def inline(s):
    parts = re.split(r'(`[^`]+`|\[[^\]]+\]\(https?://[^\s]+?\))', s)
    out = []
    for p in parts:
        if p.startswith('`') and p.endswith('`'):
            out.append('<code>' + html.escape(p[1:-1]) + '</code>')
        elif re.fullmatch(r'\[[^\]]+\]\(https?://[^\s]+?\)', p):
            label, url = re.fullmatch(r'\[([^\]]+)\]\((https?://[^\s]+?)\)', p).groups()
            out.append('<a href="' + html.escape(url, quote=True) + '">' + html.escape(label) + '</a>')
        else:
            out.append(re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html.escape(p)))
    return ''.join(out)

lines = md.splitlines()
title = lines[0][2:]
body = []
toc = []
section = 0
point = 0
i = 1
while i < len(lines):
    line = lines[i]
    if not line.strip():
        i += 1
        continue
    if line.startswith('## '):
        section += 1
        text = line[3:]
        toc.append((f'section-{section}', text))
        body.append(f'<h2 id="section-{section}">{inline(text)}</h2>')
        i += 1
    elif line.startswith('### '):
        point += 1
        text = line[4:]
        label, rest = text.split('：', 1)
        body.append(f'<h3 id="point-{point}"><span class="priority {"high" if label == "高" else "medium"}">優先度 {label}</span>{inline(rest)}</h3>')
        i += 1
    elif line.startswith('|'):
        table = []
        while i < len(lines) and lines[i].startswith('|'):
            table.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
            i += 1
        header = table[0]
        rows = table[2:]
        body.append('<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">' + inline(c) + '</th>' for c in header) + '</tr></thead><tbody>')
        for row in rows:
            body.append('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in row) + '</tr>')
        body.append('</tbody></table></div>')
    else:
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', '|')):
            paragraph.append(lines[i])
            i += 1
        text = ' '.join(paragraph)
        cls = ' class="proposal"' if text.startswith('**修正案：**') else (' class="correction"' if text.startswith('**以前のアシスタント説明の訂正：**') else '')
        body.append(f'<p{cls}>' + inline(text) + '</p>')

css = '''
:root{--ink:#20343b;--muted:#5c6e75;--paper:#fff;--bg:#f3f6f6;--line:#d9e3e4;--accent:#116a67;--tint:#edf6f4;--warm:#8b4c28}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:20px}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Yu Gothic UI","Meiryo",sans-serif;font-size:16px;line-height:1.9}header,main,footer{max-width:1120px;margin:auto}header{padding:48px 48px 26px}.eyebrow{color:var(--accent);font-size:13px;letter-spacing:.12em}h1{font-size:clamp(25px,3.6vw,36px);line-height:1.5;margin:10px 0 20px}nav{display:flex;flex-wrap:wrap;gap:8px 22px;font-size:14px}nav a{text-decoration:none}main{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:28px 48px 42px}p{margin:0 0 18px}main>p:first-child{color:var(--muted);font-size:13px}main>p:nth-child(2){font-size:17px;line-height:2}main>p:nth-child(3){font-size:13px;color:var(--muted)}h2{font-size:25px;line-height:1.5;margin:52px 0 20px;padding-bottom:12px;border-bottom:2px solid var(--accent)}h3{font-size:20px;line-height:1.6;margin:32px 0 16px;padding-top:24px;border-top:1px solid var(--line)}.priority{display:inline-block;vertical-align:middle;font-size:12px;line-height:1.6;padding:3px 9px;border-radius:5px;margin:0 12px 4px 0;white-space:nowrap}.high{background:#faeee6;color:var(--warm)}.medium{background:#eaf2f5;color:#365d6d}.proposal{background:var(--tint);padding:16px 20px;border-left:3px solid #65a49c;border-radius:0 5px 5px 0}.correction{background:#fff7e7;padding:15px 20px;border-left:3px solid #c6943d}a{color:var(--accent);text-underline-offset:3px;overflow-wrap:anywhere}a:hover{color:#064643}strong{font-weight:700}code{font-family:Consolas,"Yu Gothic UI",monospace;font-size:.92em;overflow-wrap:anywhere}.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:7px;margin:20px 0 24px}table{border-collapse:collapse;width:100%;min-width:740px;font-size:14px;line-height:1.8}th,td{padding:14px 16px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:#eef3f3}td:first-child{font-weight:650;min-width:120px}tr:last-child td{border-bottom:0}footer{padding:22px 48px 40px;font-size:13px;color:var(--muted)}:focus-visible{outline:3px solid #3b9992;outline-offset:4px}::selection{background:#d3ebe7}
@media(max-width:760px){body{font-size:15px}header{padding:26px 20px 22px}main{margin:0 10px;padding:20px 18px 30px}h2{font-size:21px;margin-top:36px}h3{font-size:18px}.proposal,.correction{padding:13px 15px}footer{padding:20px}.table-wrap{margin-inline:-4px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:white;color:#111;font-size:10pt}header{padding:0 0 14px}main{border:0;border-radius:0;padding:0;max-width:none}h1{font-size:23pt}h2{font-size:16pt;margin-top:22px}h3{font-size:13pt;break-after:avoid}nav,footer{display:none}.table-wrap{overflow:visible}table{min-width:0;font-size:9pt}th,td{padding:7px}thead{display:table-header-group}tr{break-inside:avoid}.proposal,.correction{padding:10px 12px}a{color:inherit}}
'''
page = '<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>' + html.escape(title) + '</title>\n<style>' + css + '</style>\n</head>\n<body>\n<header id="top"><div class="eyebrow">企画レビュー・公式仕様との照合</div><h1>' + html.escape(title) + '</h1><nav aria-label="目次">' + ''.join('<a href="#' + anchor + '">' + html.escape(label) + '</a>' for anchor, label in toc) + '</nav></header>\n<main>\n' + '\n'.join(body) + '\n</main>\n<footer><a href="#top">ページ先頭へ</a>　出典は各記述の近くに掲載。</footer>\n</body>\n</html>\n'
target.write_text(page, encoding='utf-8')

class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.hrefs=[]; self.stack=[]; self.errors=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if 'href' in attrs:self.hrefs.append(attrs['href'])
        if tag not in {'meta','br','hr','img','link','input','source','wbr'}: self.stack.append(tag)
    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1]!=tag:self.errors.append(('unexpected_end',tag,self.stack[-3:]))
        else:self.stack.pop()

c=Checker();c.feed(page)
assert not c.errors and not c.stack, (c.errors,c.stack)
assert len(c.ids)==len(set(c.ids))
assert all(h[1:] in c.ids for h in c.hrefs if h.startswith('#'))
md_links=re.findall(r'\[[^\]]+\]\((https?://[^\s]+?)\)',md)
assert Counter(md_links)==Counter(h for h in c.hrefs if h.startswith('http'))
assert '\ufffd' not in md and '\ufffd' not in page
assert '<script' not in page and '<link' not in page
assert len(re.findall(r'^### ',md,re.M))==10
assert len(re.findall(r'^## ',md,re.M))==5
print('Generated HTML and verified UTF-8, tag nesting, anchors, all source links, 10 findings, 5 sections, no external dependencies.')
print('Markdown characters:',len(md),'HTML bytes:',target.stat().st_size,'Source links:',len(md_links))
print(str(target))
