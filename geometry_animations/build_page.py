"""把 gifs/ 里的动图打包成一个单文件网页（GIF 用 base64 内嵌）。"""

import base64
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "index.html")

SECTIONS = [
    {
        "num": "7",
        "kicker": "対称, 折り返し, 回転",
        "title": "回転する図形",
        "point": "旋转时顶点画出的是圆弧 —— 半径就是「顶点到支点的距离」。"
                 "支点正好落在这个顶点上时，它原地不动，那一段没有弧。",
        "cards": [
            {
                "src": "01_rect_roll.gif",
                "tag": "例",
                "title": "长方形沿直线滚一周，顶点 A 的轨迹",
                "desc": "长方形每次绕着「贴在直线上的那个角」转 90°，一共转 4 次。"
                        "红色的虚线就是当前的半径：先是 AC=5，再是 AD=3，"
                        "第三次支点正好是 A 本身（半径 0，所以轨迹落到直线上），"
                        "最后是 AB=4。",
                "answers": [("轨迹长", "18.84 cm")],
            },
            {
                "src": "02_triangle_rotate.gif",
                "tag": "例",
                "title": "三角形绕点 A 转 72°，边 BC 扫过的面积",
                "desc": "先看 BC 扫出来的那一片；再把贴着 DE 的一小块 DEG 转回去，"
                        "它正好盖住 BCF（两块全等）。搬完以后就是一个规规矩矩的"
                        "「大扇形减小扇形」。",
                "answers": [("面积", "12.56 cm²")],
            },
            {
                "src": "05_rect_roll_ex1.gif",
                "tag": "練習 1",
                "title": "AB=6, BC=8, AC=10，顶点 B 的轨迹",
                "desc": "换成追踪顶点 B。半径依次是 BC=8、BD=10、BA=6，"
                        "最后一次支点是 B 自己。",
                "answers": [("轨迹长", "37.68 cm")],
            },
        ],
    },
    {
        "num": "8",
        "kicker": "対称, 折り返し, 回転",
        "title": "辺にそって転がる円",
        "point": "走在角上时看圆心：在外侧滚，圆心画 90° 的弧（4 段合起来是一个整圆）；"
                 "在内侧滚，圆心是直角拐弯，一段弧都没有。",
        "cards": [
            {
                "src": "03_circle_outside.gif",
                "tag": "例 · 外侧",
                "title": "半径 1cm 的圆沿 4×6 长方形的外侧滚一周",
                "desc": "先跟着圆心走一圈看轨迹，再看扫过的整片区域怎么拆："
                        "4 个角上的扇形合起来正好是半径 2cm 的一个圆，"
                        "剩下的是贴着 4 条边的长方形。",
                "answers": [("中心O", "26.28 cm"), ("面积", "52.56 cm²")],
            },
            {
                "src": "04_circle_inside.gif",
                "tag": "例 · 内侧",
                "title": "半径 2cm 的圆沿边长 10cm 正方形的内侧滚一周",
                "desc": "内侧滚的时候圆够不到 4 个角，中间也留下一块够不到的正方形。"
                        "所以用整个正方形减掉这两处白色部分。",
                "answers": [("面积", "92.56 cm²"), ("中心O", "24 cm")],
            },
            {
                "src": "06_circle_outside_ex3.gif",
                "tag": "練習 3",
                "title": "半径 2cm 的圆沿 5×8 长方形的外侧滚一周",
                "desc": "半径变大以后，4 个角上的扇形合起来是半径 4cm 的圆，"
                        "直线部分的宽度也跟着变成 4cm。",
                "answers": [("中心O", "38.56 cm"), ("面积", "154.24 cm²")],
            },
            {
                "src": "07_circle_inside_ex4.gif",
                "tag": "練習 4",
                "title": "半径 3cm 的圆沿边长 13cm 正方形的内侧滚一周",
                "desc": "中间够不到的正方形只剩 13−3×4=1，边长 1cm 的一小块；"
                        "圆心走的是边长 13−3×2=7 的正方形。",
                "answers": [("面积", "160.26 cm²"), ("中心O", "28 cm")],
            },
        ],
    },
]

CSS = """
:root {
  color-scheme: light dark;
  --paper: #f2f4f7;
  --grid: #dde5ee;
  --card: #ffffff;
  --sheet: #ffffff;
  --line: #d5dde6;
  --ink: #1b2733;
  --ink-2: #4a5a6a;
  --ink-3: #74869a;
  --accent: #cf3a55;
  --accent-soft: #fbe6ea;
  --blue: #2f7fd1;
  --blue-soft: #e6f0fa;
  --green: #1f6f4a;
  --shadow: 0 1px 2px rgba(27, 39, 51, .06), 0 8px 24px rgba(27, 39, 51, .07);
  --cjk: "PingFang SC", "Hiragino Sans", "Hiragino Sans GB",
         "Noto Sans CJK SC", "Source Han Sans SC", "Microsoft YaHei",
         system-ui, sans-serif;
  --num: ui-monospace, "SF Mono", "DejaVu Sans Mono", Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #10161d;
    --grid: #1b242e;
    --card: #172029;
    --line: #27333f;
    --ink: #e6edf4;
    --ink-2: #a9b8c6;
    --ink-3: #7e8f9f;
    --accent: #f0798d;
    --accent-soft: #33202a;
    --blue: #74b3ec;
    --blue-soft: #1a2733;
    --green: #6fc79c;
    --shadow: 0 1px 2px rgba(0, 0, 0, .4), 0 10px 28px rgba(0, 0, 0, .35);
  }
}
:root[data-theme="dark"] {
  --paper: #10161d;
  --grid: #1b242e;
  --card: #172029;
  --line: #27333f;
  --ink: #e6edf4;
  --ink-2: #a9b8c6;
  --ink-3: #7e8f9f;
  --accent: #f0798d;
  --accent-soft: #33202a;
  --blue: #74b3ec;
  --blue-soft: #1a2733;
  --green: #6fc79c;
  --shadow: 0 1px 2px rgba(0, 0, 0, .4), 0 10px 28px rgba(0, 0, 0, .35);
}

* { box-sizing: border-box; }

body {
  margin: 0;
  padding: 0 20px 72px;
  font-family: var(--cjk);
  color: var(--ink);
  background-color: var(--paper);
  background-image:
    linear-gradient(var(--grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 22px 22px;
  line-height: 1.75;
  -webkit-font-smoothing: antialiased;
}

.wrap { max-width: 940px; margin: 0 auto; }

header.top {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 56px 0 34px;
}
.eyebrow {
  font-size: 12px;
  letter-spacing: .22em;
  text-transform: uppercase;
  color: var(--ink-3);
}
h1 {
  margin: 0;
  font-size: clamp(28px, 4.4vw, 42px);
  font-weight: 700;
  letter-spacing: -.01em;
  text-wrap: balance;
}
.lede {
  margin: 0;
  max-width: 62ch;
  color: var(--ink-2);
  font-size: 16px;
}
.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
  margin-top: 6px;
  font-size: 13px;
  color: var(--ink-3);
}

section.lesson {
  display: flex;
  flex-direction: column;
  gap: 22px;
  margin-top: 42px;
}
.lesson-head {
  display: flex;
  align-items: baseline;
  gap: 14px;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--ink);
}
.badge {
  flex: none;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: var(--ink);
  color: var(--card);
  display: grid;
  place-items: center;
  font-family: var(--num);
  font-size: 17px;
  font-weight: 600;
  align-self: center;
}
.lesson-head h2 {
  margin: 0;
  font-size: clamp(20px, 2.6vw, 26px);
  font-weight: 700;
  letter-spacing: .01em;
}
.lesson-head .jp {
  font-size: 13px;
  color: var(--ink-3);
  margin-left: auto;
  white-space: nowrap;
}
.point {
  border-left: 3px solid var(--accent);
  background: var(--accent-soft);
  padding: 12px 16px;
  font-size: 15px;
  color: var(--ink);
}
.point b {
  display: block;
  font-size: 12px;
  letter-spacing: .18em;
  color: var(--accent);
  margin-bottom: 2px;
}

.cards { display: flex; flex-direction: column; gap: 22px; }
article.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 4px;
  box-shadow: var(--shadow);
  overflow: hidden;
}
.card-head {
  display: flex;
  align-items: baseline;
  gap: 12px;
  flex-wrap: wrap;
  padding: 16px 20px 12px;
}
.tag {
  flex: none;
  font-size: 12px;
  letter-spacing: .08em;
  padding: 2px 9px;
  border: 1px solid var(--blue);
  color: var(--blue);
  background: var(--blue-soft);
  border-radius: 2px;
}
.card-head h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  text-wrap: balance;
}
.sheet {
  background: #ffffff;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  padding: 10px;
  text-align: center;
}
.sheet img {
  max-width: 100%;
  height: auto;
  display: inline-block;
}
.card-foot {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  align-items: flex-start;
  padding: 16px 20px 18px;
}
.desc {
  margin: 0;
  flex: 1 1 320px;
  font-size: 15px;
  color: var(--ink-2);
}
.answers {
  flex: 0 1 auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 150px;
}
.ans {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: baseline;
  border-top: 1px solid var(--line);
  padding-top: 6px;
}
.ans span { font-size: 12px; color: var(--ink-3); letter-spacing: .1em; }
.ans strong {
  font-family: var(--num);
  font-variant-numeric: tabular-nums;
  font-size: 16px;
  color: var(--green);
  font-weight: 600;
}

footer {
  margin-top: 48px;
  padding-top: 20px;
  border-top: 1px solid var(--line);
  font-size: 14px;
  color: var(--ink-2);
}
footer h4 { margin: 0 0 8px; font-size: 13px; letter-spacing: .16em;
            color: var(--ink-3); font-weight: 600; }
pre {
  margin: 0;
  overflow-x: auto;
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 3px;
  padding: 12px 14px;
  font-family: var(--num);
  font-size: 13px;
  line-height: 1.7;
  color: var(--ink);
}
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; }
}
@media (max-width: 620px) {
  .card-foot { flex-direction: column; }
  .lesson-head .jp { display: none; }
}
"""


def data_uri(fname):
    with open(os.path.join(HERE, "gifs", fname), "rb") as f:
        return "data:image/gif;base64," + base64.b64encode(f.read()).decode()


def card_html(c):
    ans = "".join(
        f'<div class="ans"><span>{html.escape(k)}</span>'
        f"<strong>{html.escape(v)}</strong></div>"
        for k, v in c["answers"])
    return f"""      <article class="card">
        <div class="card-head">
          <span class="tag">{html.escape(c['tag'])}</span>
          <h3>{html.escape(c['title'])}</h3>
        </div>
        <div class="sheet">
          <img src="{data_uri(c['src'])}" alt="{html.escape(c['title'])}">
        </div>
        <div class="card-foot">
          <p class="desc">{html.escape(c['desc'])}</p>
          <div class="answers">{ans}</div>
        </div>
      </article>"""


def main():
    body = []
    for s in SECTIONS:
        cards = "\n".join(card_html(c) for c in s["cards"])
        body.append(f"""    <section class="lesson">
      <div class="lesson-head">
        <span class="badge">{s['num']}</span>
        <h2>{html.escape(s['title'])}</h2>
        <span class="jp">{html.escape(s['kicker'])}</span>
      </div>
      <div class="point"><b>ポイント</b>{html.escape(s['point'])}</div>
      <div class="cards">
{cards}
      </div>
    </section>""")

    page = f"""<title>转动的图形 · 滚动的圆</title>
<style>{CSS}</style>
<div class="wrap">
  <header class="top">
    <p class="eyebrow">第 7 · 8 课 · 动画讲解</p>
    <h1>转动的图形 · 滚动的圆</h1>
    <p class="lede">把课本上这两节的图动起来：顶点怎么画出弧、圆滚过去到底扫到了哪些地方。
      每段动画最后都会停下来，把算式和答案写在画面上，数值跟课本答案一致。</p>
    <div class="meta">
      <span>7 段动画</span><span>例题 + 練習</span><span>圆周率取 3.14</span>
    </div>
  </header>
{chr(10).join(body)}
  <footer>
    <h4>换个数字自己生成</h4>
    <pre>pip install matplotlib numpy pillow
cd geometry_animations
python3 anim_rect_roll.py --ab 4 --bc 3 --track A
python3 anim_triangle_rotate.py --ab 6 --ac 4 --deg 72
python3 anim_circle_outside.py --w 6 --h 4 --r 1
python3 anim_circle_inside.py --side 10 --r 2</pre>
  </footer>
</div>
"""
    with open(OUT, "w") as f:
        f.write(page)
    print(f"{OUT}  {os.path.getsize(OUT) / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
