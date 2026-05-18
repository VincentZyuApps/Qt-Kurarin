from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen

from .cli import FRAME_STYLE_MAC, FRAME_STYLE_NONE, FRAME_STYLE_WIN11


@dataclass(slots=True)
class FrameLayout:
    outer_rect: QRectF
    content_rect: QRectF
    title_bar_rect: QRectF
    radius: float
    border_width: float


def compute_frame_layout(content_rect: QRectF, frame_style: str) -> FrameLayout:
    if frame_style == FRAME_STYLE_NONE:
        return FrameLayout(
            outer_rect=QRectF(content_rect),
            content_rect=QRectF(content_rect),
            title_bar_rect=QRectF(),
            radius=0.0,
            border_width=0.0,
        )

    if frame_style == FRAME_STYLE_WIN11:
        top_bar = max(21.0, min(31.0, content_rect.height() * 0.072))
        border = max(1.0, min(1.4, min(content_rect.width(), content_rect.height()) * 0.0022))
        radius = 8.0
    else:
        top_bar = max(23.0, min(35.0, content_rect.height() * 0.092))
        border = max(1.2, min(1.8, min(content_rect.width(), content_rect.height()) * 0.0027))
        radius = 12.0

    outer_rect = QRectF(
        content_rect.left() - border,
        content_rect.top() - top_bar - border,
        content_rect.width() + border * 2,
        content_rect.height() + top_bar + border * 2,
    )
    title_bar_rect = QRectF(
        outer_rect.left(),
        outer_rect.top(),
        outer_rect.width(),
        top_bar,
    )
    return FrameLayout(
        outer_rect=outer_rect,
        content_rect=QRectF(
            outer_rect.left() + border,
            outer_rect.top() + top_bar + border,
            content_rect.width(),
            content_rect.height(),
        ),
        title_bar_rect=title_bar_rect,
        radius=radius,
        border_width=border,
    )


def draw_frame(
    painter: QPainter,
    content_rect: QRectF,
    frame_style: str,
    title: str,
    opacity: float,
) -> QRectF:
    if frame_style == FRAME_STYLE_NONE:
        return content_rect

    layout = compute_frame_layout(content_rect, frame_style)
    if frame_style == FRAME_STYLE_WIN11:
        _draw_win11_frame(painter, layout, title, opacity)
    elif frame_style == FRAME_STYLE_MAC:
        _draw_mac_frame(painter, layout, title, opacity)
    return layout.content_rect


def content_clip_path(content_rect: QRectF, frame_style: str) -> QPainterPath | None:
    if frame_style == FRAME_STYLE_NONE:
        return None

    radius = 8.0 if frame_style == FRAME_STYLE_WIN11 else 12.0
    return _bottom_rounded_path(content_rect, radius)


def _rounded_path(rect: QRectF, radius: float) -> QPainterPath:
    path = QPainterPath()
    path.addRoundedRect(rect, radius, radius)
    return path


def _bottom_rounded_path(rect: QRectF, radius: float) -> QPainterPath:
    radius = min(radius, rect.width() / 2.0, rect.height() / 2.0)
    path = QPainterPath()
    path.moveTo(rect.left(), rect.top())
    path.lineTo(rect.right(), rect.top())
    path.lineTo(rect.right(), rect.bottom() - radius)
    path.quadTo(
        rect.right(),
        rect.bottom(),
        rect.right() - radius,
        rect.bottom(),
    )
    path.lineTo(rect.left() + radius, rect.bottom())
    path.quadTo(
        rect.left(),
        rect.bottom(),
        rect.left(),
        rect.bottom() - radius,
    )
    path.lineTo(rect.left(), rect.top())
    path.closeSubpath()
    return path


def _make_frame_band(layout: FrameLayout) -> QPainterPath:
    band = _rounded_path(layout.outer_rect, layout.radius)
    inner = _bottom_rounded_path(
        layout.content_rect.adjusted(
            -layout.border_width * 0.35,
            -layout.border_width * 0.35,
            layout.border_width * 0.35,
            layout.border_width * 0.35,
        ),
        max(0.0, layout.radius - 2.0),
    )
    return band.subtracted(inner)


def _make_shadow_band(layout: FrameLayout, spread: float) -> QPainterPath:
    outer = _rounded_path(
        layout.outer_rect.adjusted(-spread, -spread, spread, spread),
        layout.radius + spread,
    )
    inner = _rounded_path(layout.outer_rect, layout.radius)
    return outer.subtracted(inner)


def _make_title_path(layout: FrameLayout) -> QPainterPath:
    title_path = _rounded_path(layout.title_bar_rect, layout.radius)
    lower_half = QRectF(
        layout.title_bar_rect.left(),
        layout.title_bar_rect.center().y(),
        layout.title_bar_rect.width(),
        layout.title_bar_rect.height() / 2,
    )
    lower_path = QPainterPath()
    lower_path.addRect(lower_half)
    return title_path.united(lower_path)


def _make_ring(outer_rect: QRectF, outer_radius: float, inner_rect: QRectF, inner_radius: float) -> QPainterPath:
    return _rounded_path(outer_rect, outer_radius).subtracted(_bottom_rounded_path(inner_rect, inner_radius))


def _draw_shadow(painter: QPainter, layout: FrameLayout, opacity: float, dy: float) -> None:
    layers = (
        (1.5, 18),
        (3.0, 13),
        (5.0, 9),
        (7.5, 6),
    )
    previous_rect = QRectF(layout.outer_rect)
    previous_radius = layout.radius

    painter.save()
    painter.translate(0.0, dy)
    for spread, alpha in layers:
        expanded_rect = layout.outer_rect.adjusted(-spread, -spread, spread, spread)
        expanded_radius = layout.radius + spread
        ring = _make_ring(expanded_rect, expanded_radius, previous_rect, previous_radius)
        painter.fillPath(ring, QColor(0, 0, 0, int(alpha * opacity)))
        previous_rect = expanded_rect
        previous_radius = expanded_radius
    painter.restore()


def _draw_outline(
    painter: QPainter,
    layout: FrameLayout,
    frame_color: QColor,
    title_color: QColor,
    line_color: QColor,
    opacity: float,
) -> None:
    painter.fillPath(_make_frame_band(layout), frame_color)
    painter.fillPath(_make_title_path(layout), title_color)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(line_color, 1.0))
    painter.drawPath(_rounded_path(layout.outer_rect, layout.radius))

    separator_y = layout.title_bar_rect.bottom()
    painter.drawLine(
        QPointF(layout.outer_rect.left() + 1.5, separator_y),
        QPointF(layout.outer_rect.right() - 1.5, separator_y),
    )


def _draw_win11_frame(painter: QPainter, layout: FrameLayout, title: str, opacity: float) -> None:
    _draw_shadow(painter, layout, opacity, 1.2)
    _draw_outline(
        painter,
        layout,
        QColor(249, 249, 249, int(228 * opacity)),
        QColor(251, 251, 251, int(244 * opacity)),
        QColor(206, 210, 214, int(220 * opacity)),
        opacity,
    )

    painter.setPen(QColor(92, 95, 100, int(220 * opacity)))
    painter.setFont(QFont("Segoe UI", 7))
    painter.drawText(
        QRectF(layout.title_bar_rect.left() + 10, layout.title_bar_rect.top(), max(0.0, layout.title_bar_rect.width() - 126), layout.title_bar_rect.height()),
        Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
        title.replace("_", " "),
    )

    button_center_y = layout.title_bar_rect.center().y() - 0.2
    cluster_right = layout.title_bar_rect.right() - 10.5
    spacing = 22.0
    close_center_x = cluster_right
    max_center_x = close_center_x - spacing
    min_center_x = max_center_x - spacing

    pen = QPen(QColor(98, 102, 108, int(220 * opacity)), 1.15)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    painter.drawLine(
        QPointF(min_center_x - 4.2, button_center_y + 2.1),
        QPointF(min_center_x + 4.2, button_center_y + 2.1),
    )

    painter.drawRect(
        QRectF(
            max_center_x - 4.3,
            button_center_y - 4.3,
            8.6,
            8.6,
        )
    )

    painter.drawLine(
        QPointF(close_center_x - 3.8, button_center_y - 3.8),
        QPointF(close_center_x + 3.8, button_center_y + 3.8),
    )
    painter.drawLine(
        QPointF(close_center_x - 3.8, button_center_y + 3.8),
        QPointF(close_center_x + 3.8, button_center_y - 3.8),
    )


def _draw_mac_frame(painter: QPainter, layout: FrameLayout, title: str, opacity: float) -> None:
    _draw_shadow(painter, layout, opacity, 1.0)
    _draw_outline(
        painter,
        layout,
        QColor(249, 249, 249, int(224 * opacity)),
        QColor(255, 255, 255, int(242 * opacity)),
        QColor(210, 214, 219, int(224 * opacity)),
        opacity,
    )

    circles = [
        (QColor(255, 95, 87), layout.outer_rect.left() + 9),
        (QColor(255, 189, 46), layout.outer_rect.left() + 27),
        (QColor(39, 201, 63), layout.outer_rect.left() + 45),
    ]
    painter.setPen(QPen(QColor(0, 0, 0, int(42 * opacity)), 0.4))
    for color, x in circles:
        painter.setBrush(QColor(color.red(), color.green(), color.blue(), int(242 * opacity)))
        painter.drawEllipse(QRectF(x, layout.title_bar_rect.center().y() - 5.5, 11.0, 11.0))

    painter.setPen(QColor(96, 74, 81, int(228 * opacity)))
    painter.setFont(QFont("SF Pro Text", 8))
    painter.drawText(
        QRectF(layout.title_bar_rect.left() + 58, layout.title_bar_rect.top(), max(0.0, layout.title_bar_rect.width() - 116), layout.title_bar_rect.height()),
        Qt.AlignmentFlag.AlignCenter,
        title.replace("_", " "),
    )
