# 转动·滚动 动图（对应课本 7「回転する図形」/ 8「辺にそって転がる円」）

用 Python + matplotlib 生成的教学动图，每个 GIF 最后都会停住并写出算式和答案，
数值与课本答案一致。

## 生成的动图

| 文件 | 对应题目 | 动图内容 | 答案 |
|---|---|---|---|
| `gifs/01_rect_roll.gif` | 7 ステップ1 例 | 长方形（AB=4, BC=3, AC=5）沿直线ℓ滚一周，画出顶点 A 的轨迹 | 18.84 cm |
| `gifs/02_triangle_rotate.gif` | 7 ステップ2 例 | 三角形绕 A 转 72°，边 BC 扫过的面积；并演示把 DEG 那块搬到 BCF，变成「大扇形−小扇形」 | 12.56 cm² |
| `gifs/03_circle_outside.gif` | 8 ステップ3 例 | 半径 1cm 的圆沿 4×6 长方形**外侧**滚一周：中心 O 的轨迹 + 扫过的面积 | 26.28 cm / 52.56 cm² |
| `gifs/04_circle_inside.gif` | 8 ステップ4 例 | 半径 2cm 的圆沿边长 10cm 正方形**内侧**滚一周：扫过的面积（挖掉 4 个角和中间的白色部分）+ 中心轨迹 | 92.56 cm² / 24 cm |
| `gifs/05_rect_roll_ex1.gif` | 7 練習1 | 长方形（AB=6, BC=8, AC=10）滚一周，顶点 B 的轨迹 | 37.68 cm |
| `gifs/06_circle_outside_ex3.gif` | 8 練習3 | 半径 2cm 的圆沿 5×8 长方形外侧滚一周 | 38.56 cm / 154.24 cm² |
| `gifs/07_circle_inside_ex4.gif` | 8 練習4 | 半径 3cm 的圆沿边长 13cm 正方形内侧滚一周 | 160.26 cm² / 28 cm |

几个动图里刻意强调的点（也就是课本的「ポイント」）：

* 顶点绕**支点**转 → 画出的是圆弧，半径 = 顶点到支点的距离；支点正好是这个顶点时，那一段不动。
* 圆在**外侧**滚：拐角处圆心走 90° 的弧，4 段弧合起来 = 一个整圆；扫过的 4 个角合起来 = 半径 2r 的圆。
* 圆在**内侧**滚：拐角处圆心是直角拐弯，**没有弧**；4 个角上留下白色（r×r 的正方形去掉四分之一圆），中间还剩边长 L−4r 的白色正方形。

## 重新生成 / 换数字

```bash
pip install matplotlib numpy pillow
cd geometry_animations

python3 anim_rect_roll.py --ab 4 --bc 3 --track A --name 01_rect_roll.gif
python3 anim_triangle_rotate.py --ab 6 --ac 4 --deg 72 --ang-c 38
python3 anim_circle_outside.py --w 6 --h 4 --r 1
python3 anim_circle_inside.py --side 10 --r 2
```

`--track` 选择要画轨迹的顶点（A/B/C/D，A 左上、B 左下、C 右下、D 右上）；
`--ang-c` 只影响三角形画出来的样子，不影响面积。

## 文件

* `common.py` — 画布、中文字体（用仓库根目录的 `ChineseFont.ttf`）、配色、GIF 输出
* `anim_rect_roll.py` / `anim_triangle_rotate.py` / `anim_circle_outside.py` / `anim_circle_inside.py`
* `gifs/` — 生成结果

## 网页版

`python3 build_page.py` 会把 7 个 GIF 打包成一个单文件网页 `index.html`
（图片用 base64 内嵌，直接用浏览器打开就能看，不需要联网）。
生成的 `index.html` 有 5MB 左右，没有提交进仓库。
