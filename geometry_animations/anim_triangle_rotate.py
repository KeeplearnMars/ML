"""7 回転する図形 / ステップ2：三角形绕顶点A旋转，边BC扫过的面积。

思路（课本的想法）：BC 扫过的图形里，靠着 DE 的一小块 DEG，
转回去正好盖住 BCF（两块全等），于是整块面积 = 大扇形 − 小扇形。
"""

import argparse

import numpy as np
from matplotlib.patches import Polygon

from common import (CJK, FIG_FILL, GHOST, INK, NOTE, SWEEP, SWEEP_EDGE,
                    Canvas, arc, rot)

HL = "#f6d97a"  # 被搬动的那一块


def build(ab=6.0, ac=4.0, deg=72.0, ang_c=50.0, name="02_triangle_rotate.gif"):
    th = np.radians(deg)
    a = np.array([0.0, 0.0])
    b = np.array([ab, 0.0])
    ac_ang = np.radians(ang_c)
    c = np.array([ac * np.cos(ac_ang), ac * np.sin(ac_ang)])
    f = np.array([ac, 0.0])            # AB 上到 A 距离为 ac 的点
    tri = np.array([a, b, c])

    def swept(t):
        """BC 从 0 转到 t 扫过的区域。"""
        return np.vstack([arc(a, ab, 0, t), [rot(c, a, t)],
                          arc(a, ac, ac_ang + t, ac_ang)[::-1][1:], [c]])

    # 小块 BCF：BC + 半径 ac 的弧 CF + 线段 FB
    piece = np.vstack([[b], [c], arc(a, ac, ac_ang, 0)])

    lim = ab + 1.6
    cv = Canvas((-1.8, lim), (-1.8, lim - 0.6), size=(6.4, 6.0),
                title=f"三角形ABC绕点A旋转{deg:g}°：边BC扫过的面积")

    def base(ax):
        ax.plot([a[0]], [a[1]], "o", ms=5, color=INK)
        ax.add_patch(Polygon(tri, closed=True, fill=False, ec=GHOST, ls="--",
                             lw=1.2))

    def label(ax, p, s, dx=0.0, dy=0.25, color=INK):
        ax.text(p[0] + dx, p[1] + dy, s, fontproperties=CJK, fontsize=12,
                color=color, ha="center")

    # ---- 第一段：旋转，画出扫过的区域 ----
    steps = 40
    for k in range(steps + 1):
        t = th * k / steps
        ax = cv.begin()
        base(ax)
        if k:
            ax.add_patch(Polygon(swept(t), closed=True, fc=SWEEP, alpha=0.85,
                                 ec=SWEEP_EDGE, lw=1.3))
        cur = rot(tri, a, t)
        ax.add_patch(Polygon(cur, closed=True, fc=FIG_FILL, ec=INK, lw=1.8,
                             alpha=0.9))
        label(ax, a, "A", dy=-0.55)
        label(ax, b, "B", dy=-0.5)
        label(ax, c, "C", dx=0.3, dy=-0.1)
        if k:
            label(ax, cur[1], "D", dx=0.25, dy=0.15)
            label(ax, cur[2], "E", dx=-0.35, dy=0.05)
        ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=1.4)
        ax.text(ab / 2, -0.45, f"{ab:g}cm", fontproperties=CJK, fontsize=10,
                color=INK, ha="center")
        ax.text(c[0] / 2 - 0.35, c[1] / 2, f"{ac:g}cm", fontproperties=CJK,
                fontsize=10, color=INK, ha="center")
        cv.text(0.03, 0.94, f"已转 {np.degrees(t):.0f}°", size=13, color=NOTE)
        cv.snap(1 if k else 10)
    cv.snap(14)

    # ---- 第二段：把 DEG 那一块转回来盖住 BCF ----
    done = swept(th)
    tri_end = rot(tri, a, th)
    for k in range(31):
        t = th * (1 - k / 30)
        ax = cv.begin()
        base(ax)
        ax.add_patch(Polygon(done, closed=True, fc=SWEEP, alpha=0.85,
                             ec=SWEEP_EDGE, lw=1.3))
        # 挖掉搬走的那一块
        ax.add_patch(Polygon(rot(piece, a, th), closed=True, fc="white",
                             ec="white", lw=1.0))
        ax.add_patch(Polygon(rot(piece, a, t), closed=True, fc=HL,
                             ec=SWEEP_EDGE, lw=1.3, alpha=0.95))
        label(ax, a, "A", dy=-0.55)
        label(ax, b, "B", dy=-0.5)
        label(ax, c, "C", dx=0.3, dy=-0.1)
        label(ax, tri_end[1], "D", dx=0.25, dy=0.15)
        label(ax, tri_end[2], "E", dx=-0.35, dy=0.05)
        label(ax, f, "F", dy=-0.5)
        label(ax, rot(f, a, th), "G", dx=-0.3, dy=0.05)
        cv.text(0.03, 0.94, "图形DEG和图形BCF全等 → 搬过去", size=12,
                color=NOTE)
        cv.snap(12 if k == 0 else 1)
    cv.snap(10)

    # ---- 第三段：变成「大扇形 − 小扇形」 ----
    ring = np.vstack([[f], [b], arc(a, ab, 0, th),
                      [rot(f, a, th)], arc(a, ac, th, 0)])
    big = np.vstack([[a], arc(a, ab, 0, th), [a]])
    small = np.vstack([[a], arc(a, ac, 0, th), [a]])
    area = (ab * ab - ac * ac) * 3.14 * deg / 360
    for k in range(3):
        ax = cv.begin()
        base(ax)
        ax.add_patch(Polygon(ring, closed=True, fc=SWEEP, alpha=0.9,
                             ec=SWEEP_EDGE, lw=1.5))
        if k >= 1:
            ax.add_patch(Polygon(big, closed=True, fill=False, ec=INK,
                                 ls="--", lw=1.3))
        if k >= 2:
            ax.add_patch(Polygon(small, closed=True, fc="white", alpha=0.55,
                                 ec=INK, ls="--", lw=1.3))
        label(ax, a, "A", dy=-0.55)
        cv.text(0.03, 0.94,
                f"{ab:g}×{ab:g}×3.14×{deg:g}/360 − "
                f"{ac:g}×{ac:g}×3.14×{deg:g}/360", size=12, color=NOTE)
        if k >= 2:
            cv.text(0.03, 0.88,
                    f"=({ab*ab:g}−{ac*ac:g})×3.14×{deg:g}/360 "
                    f"= {area:.2f} cm²", size=13, color=NOTE)
        cv.snap(18 if k < 2 else 45)
    return cv.save(name, duration=60)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ab", type=float, default=6.0, help="AB（大半径）")
    p.add_argument("--ac", type=float, default=4.0, help="AC（小半径）")
    p.add_argument("--deg", type=float, default=72.0, help="旋转角度")
    p.add_argument("--ang-c", type=float, default=50.0, help="∠CAB，只影响画面")
    p.add_argument("--name", default="02_triangle_rotate.gif")
    a = p.parse_args()
    build(a.ab, a.ac, a.deg, a.ang_c, a.name)
