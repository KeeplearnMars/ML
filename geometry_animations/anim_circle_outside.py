"""8 辺にそって転がる円 / ステップ3：圆沿长方形的外侧滚一周。

(1) 中心O的轨迹：直线部分 + 4 段 90° 弧（合起来正好是半径 r 的一个整圆）
(2) 圆扫过的面积：4 个角上的扇形合起来 = 半径 2r 的圆，其余是 4 个长方形
"""

import argparse

import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle, Wedge

from common import (CJK, FIG_FILL, INK, NOTE, SWEEP, SWEEP_EDGE, TRACE,
                    CIRCLE, Canvas, arc, resample)

HL = "#f6d97a"


def center_path(w, h, r, n=90):
    """圆心走过的「圆角长方形」，逆时针。"""
    seg = [np.stack([np.linspace(0, w, n), np.full(n, -r)], axis=1),
           arc((w, 0), r, -np.pi / 2, 0, n),
           np.stack([np.full(n, w + r), np.linspace(0, h, n)], axis=1),
           arc((w, h), r, 0, np.pi / 2, n),
           np.stack([np.linspace(w, 0, n), np.full(n, h + r)], axis=1),
           arc((0, h), r, np.pi / 2, np.pi, n),
           np.stack([np.full(n, -r), np.linspace(h, 0, n)], axis=1),
           arc((0, 0), r, np.pi, 1.5 * np.pi, n)]
    return np.vstack(seg)


def band(pts, r):
    """路径 pts 两侧各 r 的「加粗」区域（路径为凸时精确）。"""
    d = np.gradient(pts, axis=0)
    t = d / np.linalg.norm(d, axis=1)[:, None]
    nrm = np.stack([t[:, 1], -t[:, 0]], axis=1)          # 向外的法线
    outer, inner = pts + r * nrm, pts - r * nrm
    a_end = np.arctan2(nrm[-1, 1], nrm[-1, 0])
    a_0 = np.arctan2(nrm[0, 1], nrm[0, 0])
    return np.vstack([outer, arc(pts[-1], r, a_end, a_end + np.pi, 20),
                      inner[::-1], arc(pts[0], r, a_0 + np.pi, a_0 + 2 * np.pi,
                                       20)])


def build(w=6.0, h=4.0, r=1.0, name="03_circle_outside.gif"):
    path, s = resample(center_path(w, h, r), 0.04)
    total = s[-1]
    frames = 96

    cv = Canvas((-r - 1.4, w + r + 1.4), (-r - 1.6, h + r + 4.0),
                size=(6.6, 6.2),
                title=f"半径{r:g}cm的圆沿{h:g}×{w:g}长方形的外侧滚一周")

    def base(ax):
        ax.add_patch(Rectangle((0, 0), w, h, fc=FIG_FILL, ec=INK, lw=1.8,
                               zorder=3))
        ax.text(w / 2, 0.28, f"{w:g}cm", fontproperties=CJK, fontsize=10,
                color=INK, ha="center", zorder=6)
        ax.text(0.35, h / 2, f"{h:g}cm", fontproperties=CJK, fontsize=10,
                color=INK, va="center", ha="left", zorder=6)

    for k in range(frames + 1):
        i = max(1, int(len(path) * k / frames))
        ax = cv.begin()
        if k:
            ax.add_patch(Polygon(band(path[:i], r), closed=True, fc=SWEEP,
                                 alpha=0.85, ec="none", zorder=1))
        base(ax)
        ax.plot(path[:i, 0], path[:i, 1], color=TRACE, lw=2.0, zorder=4)
        c = path[i - 1]
        ax.add_patch(Circle(c, r, fc="none", ec=CIRCLE, lw=2.0, zorder=5))
        sp = -s[i - 1] / r                       # 滚动时圆自身的转角
        ax.plot([c[0], c[0] + r * np.cos(sp)], [c[1], c[1] + r * np.sin(sp)],
                color=CIRCLE, lw=1.4, zorder=5)
        ax.plot([c[0]], [c[1]], "o", ms=4, color=CIRCLE, zorder=6)
        ax.text(c[0] + 0.18, c[1] + 0.18, "O", fontproperties=CJK, fontsize=11,
                color=CIRCLE, zorder=6)
        cv.text(0.03, 0.96, f"中心O已经走了 {s[i-1]:.2f} cm", size=12,
                color=NOTE)
        cv.snap(10 if k == 0 else 1)
    cv.snap(16)

    line_len = 2 * (w + h)
    arc_len = 2 * 3.14 * r
    area = line_len * 2 * r + 3.14 * (2 * r) ** 2

    # (1) 轨迹的长度
    for k in range(2):
        ax = cv.begin()
        ax.add_patch(Polygon(band(path, r), closed=True, fc=SWEEP, alpha=0.35,
                             ec="none", zorder=1))
        base(ax)
        ax.plot(path[:, 0], path[:, 1], color=TRACE, lw=2.0, zorder=4)
        if k:  # 把 4 段弧挑出来
            for cx, cy, a0 in [(w, 0, -90), (w, h, 0), (0, h, 90), (0, 0, 180)]:
                ax.add_patch(Wedge((cx, cy), r, a0, a0 + 90, width=0.001,
                                   ec=SWEEP_EDGE, lw=4, zorder=5))
            cv.text(0.03, 0.85, "4段弧合起来 = 半径1个圆周", size=11,
                    color=SWEEP_EDGE)
        cv.text(0.03, 0.96, "(1) 中心O动过的线的长度", size=12, color=NOTE)
        cv.text(0.03, 0.79 if k else 0.90,
                f"({r:g}×2)×3.14+({h:g}+{w:g})×2 = {arc_len + line_len:.2f} cm",
                size=12, color=NOTE)
        cv.snap(30)

    # (2) 扫过的面积
    for k in range(3):
        ax = cv.begin()
        ax.add_patch(Polygon(band(path, r), closed=True, fc=SWEEP, alpha=0.85,
                             ec=SWEEP_EDGE, lw=1.2, zorder=1))
        if k >= 1:  # 4 个角上的扇形
            for cx, cy, a0 in [(w, 0, -90), (w, h, 0), (0, h, 90), (0, 0, 180)]:
                ax.add_patch(Wedge((cx, cy), 2 * r, a0, a0 + 90, fc=HL,
                                   ec=SWEEP_EDGE, lw=1.2, zorder=2))
        if k >= 2:  # 4 条直线部分的长方形
            for xy, ww, hh in [((0, -2 * r), w, 2 * r), ((w, 0), 2 * r, h),
                               ((0, h), w, 2 * r), ((-2 * r, 0), 2 * r, h)]:
                ax.add_patch(Rectangle(xy, ww, hh, fc="#a9dcc2", ec=SWEEP_EDGE,
                                       lw=1.2, zorder=2))
        base(ax)
        cv.text(0.03, 0.96, "(2) 圆通过的部分的面积", size=12, color=NOTE)
        if k >= 1:
            cv.text(0.03, 0.90, f"4个扇形 = 半径{2*r:g}cm的圆 → "
                                f"{2*r:g}×{2*r:g}×3.14", size=11, color=NOTE)
        if k >= 2:
            cv.text(0.03, 0.84,
                    f"+ ({h:g}×2+{w:g}×2)×{2*r:g} = {area:.2f} cm²",
                    size=12, color=NOTE)
        cv.snap(24 if k < 2 else 55)
    return cv.save(name, duration=60)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--w", type=float, default=6.0, help="长方形的横")
    p.add_argument("--h", type=float, default=4.0, help="长方形的縦")
    p.add_argument("--r", type=float, default=1.0, help="圆的半径")
    p.add_argument("--name", default="03_circle_outside.gif")
    a = p.parse_args()
    build(a.w, a.h, a.r, a.name)
