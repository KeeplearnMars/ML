"""7 回転する図形 / ステップ1：长方形沿直线滚动一周，顶点画出的轨迹。

顶点的轨迹 = 4 段 90° 的圆弧，半径依次是「顶点到当前支点的距离」。
其中有一次支点就是这个顶点本身（半径 0），所以实际只有 3 段弧。
"""

import argparse

import numpy as np
from matplotlib.patches import Polygon

from common import CJK, FIG_FILL, GHOST, INK, NOTE, TRACE, Canvas, rot


def build(ab=4.0, bc=3.0, track="A", name="01_rect_roll.gif"):
    # B 左下、C 右下、D 右上、A 左上；AB 为竖边，BC 为底边
    labels = ["A", "B", "C", "D"]
    pts = np.array([[0.0, ab], [0.0, 0.0], [bc, 0.0], [bc, ab]])
    ti = labels.index(track)
    diag = float(np.hypot(ab, bc))

    perim = 2 * (ab + bc)
    top = max(np.hypot(*(p - pts[ti])) for p in pts) + 2.8   # 最高的那段弧
    cv = Canvas((-1.6, perim + bc + 1.6), (-2.2, top),
                size=(8.2, 4.6),
                title=f"长方形沿直线ℓ滚动一周：顶点{track}的轨迹")

    start = pts.copy()
    trace = [pts[ti].copy()]
    radii = []

    def draw(cur, pivot, r, running):
        ax = cv.begin()
        ax.axhline(0, color=INK, lw=1.6, zorder=1)
        cv.ax.text(-1.4, -0.55, "ℓ", fontproperties=CJK, fontsize=13, color=INK)
        # 起始虚影
        ax.add_patch(Polygon(start, closed=True, fill=False, ec=GHOST,
                             ls="--", lw=1.2, zorder=2))
        # 轨迹
        t = np.array(trace)
        ax.plot(t[:, 0], t[:, 1], color=TRACE, lw=2.4, zorder=5)
        # 长方形本体
        ax.add_patch(Polygon(cur, closed=True, fc=FIG_FILL, ec=INK, lw=1.8,
                             zorder=3))
        for (x, y), s in zip(cur, labels):
            ax.text(x, y + 0.22, s, fontproperties=CJK, fontsize=11,
                    color=INK, ha="center", zorder=6)
        # 半径（支点 → 被追踪的顶点）
        if r > 1e-9:
            ax.plot([pivot[0], cur[ti][0]], [pivot[1], cur[ti][1]],
                    color=TRACE, ls=":", lw=1.5, zorder=4)
            mid = (pivot + cur[ti]) / 2
            ax.text(mid[0] + 0.15, mid[1] + 0.12, f"{r:g}cm",
                    fontproperties=CJK, fontsize=10, color=TRACE, zorder=6)
        ax.plot([pivot[0]], [pivot[1]], "o", ms=6, color=TRACE, zorder=7)
        cv.text(0.02, 0.93, f"已画出 {running:.2f} cm", size=12, color=NOTE)

    draw(pts, pts[1], 0.0, 0.0)
    cv.snap(12)

    running = 0.0
    for _ in range(4):
        on_line = [i for i in range(4) if abs(pts[i][1]) < 1e-6]
        pivot = pts[max(on_line, key=lambda i: pts[i][0])].copy()
        r = float(np.hypot(*(pts[ti] - pivot)))
        radii.append(r)
        for k in range(1, 19):
            cur = rot(pts, pivot, -np.pi / 2 * k / 18)
            trace.append(cur[ti].copy())
            draw(cur, pivot, r, running + r * np.pi / 2 * k / 18)
            cv.snap()
        running += r * np.pi / 2
        pts = rot(pts, pivot, -np.pi / 2)
        pts = np.round(pts, 9)

    nz = [r for r in radii if r > 1e-9]
    expr = "+".join(f"({r:g}×2)×3.14×90/360" for r in nz)
    total = sum(nz) * 3.14 / 2
    draw(pts, pts[1], 0.0, running)
    cv.text(0.02, 0.09, f"{expr}", size=11, color=NOTE)
    cv.text(0.02, 0.02, f"=({'+'.join(f'{2*r:g}' for r in nz)})×3.14×90/360"
                        f" = {total:.2f} cm", size=12, color=NOTE)
    cv.snap(40)
    return cv.save(name, duration=60)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ab", type=float, default=4.0, help="竖边 AB")
    p.add_argument("--bc", type=float, default=3.0, help="底边 BC")
    p.add_argument("--track", default="A", choices=list("ABCD"))
    p.add_argument("--name", default="01_rect_roll.gif")
    a = p.parse_args()
    build(a.ab, a.bc, a.track, a.name)
