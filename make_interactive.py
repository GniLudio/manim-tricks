from manim import *
from typing import Literal
import ipywidgets as widgets

config.verbosity = "WARNING"


def make_interactive(
    scene_cls: type[Scene],
    controls: dict[str, widgets.Widget],
    format: Literal["png", "mp4"],
):
    container = widgets.Image() if format == "png" else widgets.Video()

    def render(**kwargs) -> None:
        with tempconfig({"format": format}):
            scene = scene_cls(**kwargs)
            _ = scene.render()
            container.value = (
                scene.renderer.file_writer.image_file_path.read_bytes()
                if format == "png"
                else scene.renderer.file_writer.movie_file_path.read_bytes()
            )

    _ = widgets.interactive_output(render, controls)
    _ = display(widgets.HBox(list(controls.values())), container)
