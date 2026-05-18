from __future__ import annotations

import json
import sys
from threading import Lock, Thread
from typing import Callable

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Static

from .animation import PlaybackSnapshot, SpriteFrame


SnapshotProvider = Callable[[], PlaybackSnapshot]
ShutdownCallback = Callable[[], None]


def snapshot_to_json(snapshot: PlaybackSnapshot) -> str:
    payload = {
        "time_ms": snapshot.time_ms,
        "total_duration": snapshot.total_duration,
        "frame_style": snapshot.frame_style,
        "loudness": snapshot.loudness,
        "recent_events": snapshot.recent_events,
        "scene_summary": snapshot.scene_summary,
        "total_sprites": snapshot.total_sprites,
        "moving_count": snapshot.moving_count,
        "fading_count": snapshot.fading_count,
        "scaling_count": snapshot.scaling_count,
        "holding_count": snapshot.holding_count,
        "visible_sprites": [
            {
                "resource_name": frame.resource_name,
                "time_ms": frame.time_ms,
                "x": frame.x,
                "y": frame.y,
                "width": frame.width,
                "height": frame.height,
                "opacity": frame.opacity,
                "scale": frame.scale,
                "visible": frame.visible,
                "status": frame.status,
            }
            for frame in snapshot.visible_sprites
        ],
    }
    return json.dumps(payload, ensure_ascii=False)


def snapshot_from_json(line: str) -> PlaybackSnapshot:
    data = json.loads(line)
    return PlaybackSnapshot(
        time_ms=int(data["time_ms"]),
        total_duration=int(data["total_duration"]),
        frame_style=str(data["frame_style"]),
        loudness=int(data["loudness"]),
        visible_sprites=[
            SpriteFrame(
                resource_name=str(frame["resource_name"]),
                time_ms=int(frame["time_ms"]),
                x=float(frame["x"]),
                y=float(frame["y"]),
                width=float(frame["width"]),
                height=float(frame["height"]),
                opacity=float(frame["opacity"]),
                scale=float(frame["scale"]),
                visible=bool(frame["visible"]),
                status=str(frame["status"]),
            )
            for frame in data.get("visible_sprites", [])
        ],
        recent_events=[str(event) for event in data.get("recent_events", [])],
        scene_summary=str(data.get("scene_summary", "")),
        total_sprites=int(data.get("total_sprites", 0)),
        moving_count=int(data.get("moving_count", 0)),
        fading_count=int(data.get("fading_count", 0)),
        scaling_count=int(data.get("scaling_count", 0)),
        holding_count=int(data.get("holding_count", 0)),
    )


class StdioSnapshotFeed:
    def __init__(self) -> None:
        self._lock = Lock()
        self._snapshot = PlaybackSnapshot(
            time_ms=0,
            total_duration=0,
            frame_style="none",
            loudness=100,
        )

    def get_snapshot(self) -> PlaybackSnapshot:
        with self._lock:
            return PlaybackSnapshot(
                time_ms=self._snapshot.time_ms,
                total_duration=self._snapshot.total_duration,
                frame_style=self._snapshot.frame_style,
                loudness=self._snapshot.loudness,
                visible_sprites=[
                    SpriteFrame(
                        resource_name=frame.resource_name,
                        time_ms=frame.time_ms,
                        x=frame.x,
                        y=frame.y,
                        width=frame.width,
                        height=frame.height,
                        opacity=frame.opacity,
                        scale=frame.scale,
                        visible=frame.visible,
                        status=frame.status,
                    )
                    for frame in self._snapshot.visible_sprites
                ],
                recent_events=list(self._snapshot.recent_events),
                scene_summary=self._snapshot.scene_summary,
                total_sprites=self._snapshot.total_sprites,
                moving_count=self._snapshot.moving_count,
                fading_count=self._snapshot.fading_count,
                scaling_count=self._snapshot.scaling_count,
                holding_count=self._snapshot.holding_count,
            )

    def set_snapshot(self, snapshot: PlaybackSnapshot) -> None:
        with self._lock:
            self._snapshot = snapshot

    def start_reader(self, app: "PlaybackTui") -> Thread:
        def run() -> None:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                try:
                    snapshot = snapshot_from_json(line)
                except json.JSONDecodeError:
                    continue
                self.set_snapshot(snapshot)
            try:
                app.call_from_thread(app.exit)
            except Exception:
                pass

        thread = Thread(target=run, name="qt-kurarin-tui-stdin", daemon=True)
        thread.start()
        return thread


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
        self,
        snapshot_provider: SnapshotProvider,
        shutdown_callback: ShutdownCallback,
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

        progress = 0.0 if snapshot.total_duration <= 0 else min(1.0, snapshot.time_ms / snapshot.total_duration)
        filled = int(progress * 20)
        text_bar = "█" * filled + "·" * (20 - filled)
        bar_width = max(progress_bar.size.width, 0)
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
                    row("visible", f"{len(snapshot.visible_sprites)} / {snapshot.total_sprites}"),
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
            lines.append(f"... {len(snapshot.visible_sprites) - 18} more visible sprites")
        sprites_body.update("\n".join(lines))


def run_stdio_tui() -> int:
    feed = StdioSnapshotFeed()
    app = PlaybackTui(
        snapshot_provider=feed.get_snapshot,
        shutdown_callback=lambda: None,
    )
    feed.start_reader(app)
    app.run()
    return 0
