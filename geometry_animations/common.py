"""几何动图公共工具：画布、字体、配色、GIF 输出。

所有动画脚本共用这里的 Canvas / save_gif。
"""

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
GIF_DIR = os.path.join(HERE, "gifs")
FONT_PATH = os.path.join(os.path.dirname(HERE), "ChineseFont.ttf")

if os.path.exists(FONT_PATH):
    font_manager.fontManager.addfont(FONT_PATH)
    CJK = font_manager.FontProperties(fname=FONT_PATH)
    plt.rcParams["font.family"] = CJK.get_name()
else:  # 没有中文字体时退回默认字体，图形部分不受影响
    CJK = font_manager.FontProperties()
plt.rcParams["axes.unicode_minus"] = False

# 配色
INK = "#22303f"        # 图形主线
FIG_FILL = "#dbe6f2"   # 图形本体填充
SWEEP = "#f5b8c0"      # 扫过的区域
SWEEP_EDGE = "#d9455f"
TRACE = "#d9455f"      # 轨迹线
CIRCLE = "#2f7fd1"     # 滚动的圆
GHOST = "#b9c6d4"      # 起始/参考虚影
GRID = "#eef2f6"
NOTE = "#1f6f4a"       # 结论文字


class Canvas:
    """一个固定视野的绘图画布，每帧 clear 后重画。"""

    def __init__(self, xlim, ylim, size=(6.4, 4.8), dpi=100, title=""):
        self.fig, self.ax = plt.subplots(figsize=size, dpi=dpi)
        self.xlim, self.ylim, self.title = xlim, ylim, title
        self.frames = []
        self.holds = []

    def begin(self):
        ax = self.ax
        ax.clear()
        ax.set_xlim(*self.xlim)
        ax.set_ylim(*self.ylim)
        ax.set_aspect("equal")
        ax.axis("off")
        if self.title:
            ax.set_title(self.title, fontproperties=CJK, fontsize=13,
                         color=INK, pad=8)
        return ax

    def text(self, x, y, s, size=11, color=INK, ha="left", va="bottom", **kw):
        self.ax.text(x, y, s, fontproperties=CJK, fontsize=size, color=color,
                     ha=ha, va=va, transform=self.ax.transAxes, **kw)

    def snap(self, repeat=1):
        """把当前画面存成一帧；repeat>1 表示这一帧多停留几帧的时间。"""
        self.fig.canvas.draw()
        buf = np.asarray(self.fig.canvas.buffer_rgba())[:, :, :3]
        self.frames.append(Image.fromarray(buf))
        self.holds.append(repeat)

    def save(self, name, duration=60, loop=0):
        os.makedirs(GIF_DIR, exist_ok=True)
        path = os.path.join(GIF_DIR, name)
        pal = [f.convert("P", palette=Image.ADAPTIVE, colors=64)
               for f in self.frames]
        # 用每帧时长表示停顿，避免重复帧被 GIF 优化掉后节奏丢失
        durs = [duration * h for h in self.holds]
        pal[0].save(path, save_all=True, append_images=pal[1:],
                    duration=durs, loop=loop, optimize=True)
        plt.close(self.fig)
        kb = os.path.getsize(path) / 1024
        print(f"{path}  {len(pal)} 帧  {kb:.0f} KB")
        return path


def rot(points, center, ang):
    """把 points 绕 center 旋转 ang 弧度（逆时针为正）。"""
    p = np.asarray(points, dtype=float)
    c = np.asarray(center, dtype=float)
    m = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    return (p - c) @ m.T + c


def arc(center, radius, a0, a1, n=60):
    """圆弧采样点，a0/a1 为弧度。"""
    t = np.linspace(a0, a1, n)
    return np.stack([center[0] + radius * np.cos(t),
                     center[1] + radius * np.sin(t)], axis=1)


def resample(path, step):
    """按弧长等距重采样折线，返回 (点, 累计弧长)。"""
    path = np.asarray(path, dtype=float)
    seg = np.linalg.norm(np.diff(path, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    total = s[-1]
    q = np.arange(0, total + 1e-9, step)
    x = np.interp(q, s, path[:, 0])
    y = np.interp(q, s, path[:, 1])
    return np.stack([x, y], axis=1), q
