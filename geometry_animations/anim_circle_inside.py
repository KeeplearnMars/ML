"""8 辺にそって転がる円 / ステップ4：圆沿正方形的内侧滚一周。

圆通过的部分 = 正方形 − 4 个角上的白色部分 − 中间的白色正方形
  4 个角：每个是 (r×r) 的正方形去掉四分之一圆
  中间  ：边长 L−4r 的正方形
中心O的轨迹是边长 L−2r 的正方形（4 个角是直角，不是弧）。
"""

import argparse

import numpy as np
from matplotlib.patches import Circle, Rectangle, Wedge

from common import (CJK, INK, NOTE, SWEEP, SWEEP_EDGE, TRACE, CIRCLE, Canvas)

HL = "#f6d97a"
HL2 = "#a9dcc2"


def build(side=10.0, r=2.0, name="04_circle_inside.gif"):
    L, c0, c1 = side, r, side - r
    corners = np.array([[c0, c0], [c1, c0], [c1, c1], [c0, c1]])
    seg_len = L - 2 * r
    total = 4 * seg_len

    cv = Canvas((-1.8, L + 1.8), (-3.2, L + 5.4), size=(5.6, 6.6),
                title=f"半径{r:g}cm的圆沿边长{L:g}cm正方形的内侧滚一周")

    def sweep(ax, u, fc=SWEEP):
        """画出走过 u 长度时，圆扫过的区域（长方形 + 拐角圆的并集）。"""
        kw = dict(fc=fc, ec="none", zorder=2)
        ax.add_patch(Circle(corners[0], r, **kw))
        left = u
        for i in range(4):
            d = min(left, seg_len)
            if d <= 0:
                break
            a, b = corners[i], corners[(i + 1) % 4]
            t = (b - a) / seg_len
            p = a + t * d
            lo = np.minimum(a, p) - r * np.abs([t[1], t[0]])
            hi = np.maximum(a, p) + r * np.abs([t[1], t[0]])
            ax.add_patch(Rectangle(lo, *(hi - lo), **kw))
            ax.add_patch(Circle(p, r, **kw))
            left -= d

    def frame_pos(u):
        i = min(int(u // seg_len), 3)
        d = u - i * seg_len
        a, b = corners[i], corners[(i + 1) % 4]
        return a + (b - a) / seg_len * d

    def base(ax):
        ax.add_patch(Rectangle((0, 0), L, L, fc="none", ec=INK, lw=2.0,
                               zorder=5))
        ax.text(L / 2, -0.85, f"{L:g}cm", fontproperties=CJK, fontsize=10,
                color=INK, ha="center", zorder=6)

    frames = 88
    for k in range(frames + 1):
        u = total * k / frames
        ax = cv.begin()
        if k:
            sweep(ax, u)
        base(ax)
        # 中心O的轨迹
        done = np.vstack([corners[:min(int(u // seg_len), 3) + 1],
                          [frame_pos(u)]])
        ax.plot(done[:, 0], done[:, 1], color=TRACE, lw=2.0, zorder=4)
        p = frame_pos(u)
        ax.add_patch(Circle(p, r, fc="none", ec=CIRCLE, lw=2.0, zorder=6))
        sp = -u / r
        ax.plot([p[0], p[0] + r * np.cos(sp)], [p[1], p[1] + r * np.sin(sp)],
                color=CIRCLE, lw=1.4, zorder=6)
        ax.plot([p[0]], [p[1]], "o", ms=4, color=CIRCLE, zorder=7)
        ax.text(p[0] + 0.3, p[1] + 0.3, "O", fontproperties=CJK, fontsize=11,
                color=CIRCLE, zorder=7)
        cv.text(0.03, 0.95, f"中心O已经走了 {u:.1f} cm", size=12, color=NOTE)
        cv.snap(10 if k == 0 else 1)
    cv.snap(16)

    inner = L - 4 * r
    corner_white = 4 * r * r - 3.14 * r * r
    area = L * L - corner_white - inner * inner

    # 面积：整体 − 4 角 − 中间
    for k in range(4):
        ax = cv.begin()
        sweep(ax, total)
        if k >= 1:  # 4 个角上的白色部分
            for i, (cx, cy) in enumerate([(0, 0), (L, 0), (L, L), (0, L)]):
                sx, sy = (1 if cx == 0 else -1), (1 if cy == 0 else -1)
                ax.add_patch(Rectangle((min(cx, cx + sx * r),
                                        min(cy, cy + sy * r)), r, r, fc=HL,
                                       ec=SWEEP_EDGE, lw=1.2, zorder=3))
                a0 = {0: 0, 1: 90, 2: 180, 3: 270}[i]
                ax.add_patch(Wedge(corners[i], r, a0 + 180, a0 + 270,
                                   fc=SWEEP, ec=SWEEP_EDGE, lw=1.0, zorder=4))
        if k >= 2:  # 中间的白色正方形
            ax.add_patch(Rectangle((2 * r, 2 * r), inner, inner, fc=HL2,
                                   ec=SWEEP_EDGE, lw=1.2, zorder=3))
            ax.text(2 * r + inner / 2, 2 * r + inner / 2, f"{inner:g}×{inner:g}",
                    fontproperties=CJK, fontsize=10, color=INK, ha="center",
                    va="center", zorder=6)
        base(ax)
        cv.text(0.03, 0.96, "圆通过的部分的面积", size=12, color=NOTE)
        if k >= 1:
            cv.text(0.03, 0.91, f"4个角：4×({r:g}×{r:g})−{r:g}×{r:g}×3.14"
                                f" = {corner_white:.2f}", size=11, color=NOTE)
        if k >= 2:
            cv.text(0.03, 0.86, f"中间：{inner:g}×{inner:g} = {inner*inner:g}",
                    size=11, color=NOTE)
        if k >= 3:
            cv.text(0.03, 0.03,
                    f"{L:g}×{L:g}−(4×({r:g}×{r:g})−{r:g}×{r:g}×3.14)"
                    f"−{inner:g}×{inner:g} = {area:.2f} cm²", size=12,
                    color=NOTE)
        cv.snap(26 if k < 3 else 60)

    # 中心O的轨迹长度
    ax = cv.begin()
    sweep(ax, total, fc="#fbe4e8")
    base(ax)
    ax.add_patch(Rectangle((c0, c0), seg_len, seg_len, fill=False, ec=TRACE,
                           lw=2.4, zorder=6))
    cv.text(0.03, 0.96, "中心O动过的线：边长 "
                        f"{L:g}−{r:g}×2 = {seg_len:g} 的正方形", size=12,
            color=NOTE)
    cv.text(0.03, 0.91, f"{seg_len:g}×4 = {4*seg_len:g} cm（4个角是直角，"
                        f"没有弧）", size=12, color=NOTE)
    cv.snap(60)
    return cv.save(name, duration=60)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--side", type=float, default=10.0, help="正方形的边长")
    p.add_argument("--r", type=float, default=2.0, help="圆的半径")
    p.add_argument("--name", default="04_circle_inside.gif")
    a = p.parse_args()
    build(a.side, a.r, a.name)
