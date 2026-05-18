from __future__ import annotations

from threading import Thread
from typing import Callable

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Static

from .animation import PlaybackSnapshot


SnapshotProvider = Callable[[], PlaybackSnapshot]
ShutdownCallback = Callable[[], None]


class PlaybackTui(App[None]):
    CSS = """
    Screen {
        layout: vertical;
        background: #0f1117;
        color: #f3f5f7;
    }

    #summary {
        height: auto;
        padding: 1 2;
        border: round #3a4252;
        background: #171b24;
        margin: 1 1 0 1;
    }

    #progress_bar {
        width: 100%;
        height: 1;
        margin: 1 1 0 1;
    }

    #events {
        height: 1fr;
        padding: 1 2;
        border: round #3a4252;
        background: #131824;
        margin: 1 1 0 1;
    }

    #sprites {
        height: 1fr;
        padding: 1 2;
        border: round #3a4252;
        background: #10141d;
        margin: 1;
    }
    """

    BINDINGS = [
        ("q", "quit_player", "Quit"),
        ("ctrl+c", "quit_player", "Quit"),
    ]

    def __init__(
        self, snapshot_provider: SnapshotProvider, shutdown_callback: ShutdownCallback
    ) -> None:
        super().__init__()
        self._snapshot_provider = snapshot_provider
        self._shutdown_callback = shutdown_callback

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(id="summary")
        yield Static(id="progress_bar")
        with VerticalScroll(id="events"):
            yield Static(id="events_body")
        with VerticalScroll(id="sprites"):
            yield Static(id="sprites_body")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Qt-Kurarin Textual TUI"
        self.sub_title = "Live playback monitor"
        self.set_interval(0.12, self._refresh_snapshot)
        self._refresh_snapshot()

    def action_quit_player(self) -> None:
        self._shutdown_callback()
        self.exit()

    def _refresh_snapshot(self) -> None:
        snapshot = self._snapshot_provider()
        summary = self.query_one("#summary", Static)
        progress_bar = self.query_one("#progress_bar", Static)
        events_body = self.query_one("#events_body", Static)
        sprites_body = self.query_one("#sprites_body", Static)

        def row(key: str, value: str) -> str:
            return f"[b]{key:<12}[/b] : {value}"

        progress = (
            0.0
            if snapshot.total_duration <= 0
            else min(1.0, snapshot.time_ms / snapshot.total_duration)
        )
        filled = int(progress * 20)
        text_bar = "█" * filled + "·" * (20 - filled)
        bar_width = max(progress_bar.size.width - 2, 0)
        bar_filled = int(progress * bar_width)
        bar_widgets = "█" * bar_filled + "░" * max(bar_width - bar_filled, 0)
        progress_bar.update(bar_widgets)

        summary.update(
            "\n".join(
                [
                    "[center]─────── Qt-Kurarin Playback ───────[/center]",
                    row("time", f"{snapshot.time_ms} ms"),
                    row("duration", f"{snapshot.total_duration} ms"),
                    row("progress", f"{text_bar} {progress * 100:.1f}%"),
                    row("frame_style", snapshot.frame_style),
                    row("loudness", f"{snapshot.loudness}%"),
                    row(
                        "visible",
                        f"{len(snapshot.visible_sprites)} / {snapshot.total_sprites}",
                    ),
                    row(
                        "stats",
                        f"holding {snapshot.holding_count}, moving {snapshot.moving_count}, "
                        f"fading {snapshot.fading_count}, scaling {snapshot.scaling_count}",
                    ),
                    row("scene", snapshot.scene_summary),
                ]
            )
        )

        if snapshot.recent_events:
            events_body.update(
                "[center]─────── Recent Events ───────[/center]\n"
                + "\n".join(snapshot.recent_events[-10:])
            )
        else:
            events_body.update(
                "[center]─────── Recent Events ───────[/center]\nNo events yet."
            )

        if not snapshot.visible_sprites:
            sprites_body.update(
                "[center]─────── Visible Sprites ───────[/center]\nNo visible sprites right now."
            )
            return

        lines = ["[center]─────── Visible Sprites ───────[/center]"]
        for frame in snapshot.visible_sprites[:18]:
            lines.append(
                f"{frame.resource_name:<22} "
                f"status={frame.status:<22} "
                f"xy=({frame.x:>7.1f}, {frame.y:>7.1f}) "
                f"opacity={frame.opacity:>5.3f} "
                f"scale={frame.scale:>5.3f}"
            )
        if len(snapshot.visible_sprites) > 18:
            lines.append(
                f"... {len(snapshot.visible_sprites) - 18} more visible sprites"
            )
        sprites_body.update("\n".join(lines))


class TextualTuiHandle:
    def __init__(
        self, snapshot_provider: SnapshotProvider, shutdown_callback: ShutdownCallback
    ) -> None:
        self.app = PlaybackTui(
            snapshot_provider=snapshot_provider, shutdown_callback=shutdown_callback
        )
        self.thread = Thread(
            target=self.app.run, name="qt-kurarin-textual", daemon=True
        )

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        if not self.thread.is_alive():
            return
        try:
            self.app.call_from_thread(self.app.exit)
        except Exception:
            pass
        self.thread.join(timeout=1.0)
