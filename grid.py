import manim
import numpy as np
from PIL import Image


def to_grid(mob: manim.VMobject, cell_size: float = 0.1) -> manim.VMobject:
    stroke_one_px = manim.config.frame_width / manim.config.pixel_width * 100
    stroke_width = 0.01 * mob.get_stroke_width()
    left, right, bottom, top = (
        mob.get_left()[0] - 0.5 * stroke_width,
        mob.get_right()[0] + 0.5 * stroke_width,
        mob.get_bottom()[1] - 0.5 * stroke_width,
        mob.get_top()[1] + 0.5 * stroke_width,
    )
    width, height = right - left, top - bottom
    resolution = (max(int(width / cell_size), 1), max(1, int(height / cell_size)))
    img = np.asarray(Image.fromarray(_to_image(mob)).resize(size=resolution, resample=Image.Resampling.NEAREST))
    c_h, c_w = height / img.shape[0], width / img.shape[1]
    return manim.VGroup(
        manim.Rectangle(
            width=c_h,
            height=c_w,
            stroke_width=stroke_one_px,
            color=manim.ManimColor.from_rgba(pixel),
            fill_opacity=pixel[3] / 255,
            stroke_opacity=pixel[3] / 255,
        ).move_to((left + (x + 0.5) * c_w, top - (y + 0.5) * c_h, 0))
        for y in range(img.shape[0])
        for x in range(img.shape[1])
        if (pixel := img[y, x]) is not None and pixel[3] > 0
    )


def _to_image(mob: manim.VMobject) -> np.ndarray:
    stroke_offset = 0.5 * 0.01 * mob.get_stroke_width()
    width = mob.width + 2 * stroke_offset
    height = mob.height + 2 * stroke_offset
    if not width or not height:
        return np.zeros((0, 0, 4), dtype=np.uint8)
    img = np.asarray(mob.get_image(manim.Camera(frame_center=mob.get_center(), background_opacity=0)))
    width_px = width * manim.config.pixel_width / manim.config.frame_width
    height_px = height * manim.config.pixel_height / manim.config.frame_height
    return img[
        int((img.shape[0] - height_px) / 2) : int((img.shape[0] + height_px) / 2),
        int((img.shape[1] - width_px) / 2) : int((img.shape[1] + width_px) / 2),
    ]
