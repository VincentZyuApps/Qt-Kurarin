from __future__ import annotations

import math


def _linear(t: float, total: float, minimum: float, maximum: float) -> float:
    return (maximum - minimum) * t / total + minimum


def _quad_in(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total
    return maximum * t * t + minimum


def _quad_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total
    return -maximum * t * (t - 2) + minimum


def _quad_in_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total / 2
    if t < 1:
        return maximum / 2 * t * t + minimum
    t -= 1
    return -maximum / 2 * (t * (t - 2) - 1) + minimum


def _cubic_in(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total
    return maximum * t * t * t + minimum


def _cubic_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t = t / total - 1
    return maximum * (t * t * t + 1) + minimum


def _cubic_in_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total / 2
    if t < 1:
        return maximum / 2 * t * t * t + minimum
    t -= 2
    return maximum / 2 * (t * t * t + 2) + minimum


def _quart_in(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total
    return maximum * t * t * t * t + minimum


def _quart_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t = t / total - 1
    return -maximum * (t * t * t * t - 1) + minimum


def _quart_in_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total / 2
    if t < 1:
        return maximum / 2 * t * t * t * t + minimum
    t -= 2
    return -maximum / 2 * (t * t * t * t - 2) + minimum


def _quint_in(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total
    return maximum * t * t * t * t * t + minimum


def _quint_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t = t / total - 1
    return maximum * (t * t * t * t * t + 1) + minimum


def _quint_in_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total / 2
    if t < 1:
        return maximum / 2 * t * t * t * t * t + minimum
    t -= 2
    return maximum / 2 * (t * t * t * t * t + 2) + minimum


def _sine_in(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    return -maximum * math.cos(t * (math.pi * 90 / 180) / total) + maximum + minimum


def _sine_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    return maximum * math.sin(t * (math.pi * 90 / 180) / total) + minimum


def _sine_in_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    return -maximum / 2 * (math.cos(t * math.pi / total) - 1) + minimum


def _exp_in(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    return minimum if t == 0 else maximum * math.pow(2, 10 * (t / total - 1)) + minimum


def _exp_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    return maximum + minimum if t == total else maximum * (-math.pow(2, -10 * t / total) + 1) + minimum


def _exp_in_out(t: float, total: float, minimum: float, maximum: float) -> float:
    if t == 0:
        return minimum
    if t == total:
        return maximum
    maximum -= minimum
    t /= total / 2
    if t < 1:
        return maximum / 2 * math.pow(2, 10 * (t - 1)) + minimum
    t -= 1
    return maximum / 2 * (-math.pow(2, -10 * t) + 2) + minimum


def _circ_in(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total
    return -maximum * (math.sqrt(1 - t * t) - 1) + minimum


def _circ_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t = t / total - 1
    return maximum * math.sqrt(1 - t * t) + minimum


def _circ_in_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total / 2
    if t < 1:
        return -maximum / 2 * (math.sqrt(1 - t * t) - 1) + minimum
    t -= 2
    return maximum / 2 * (math.sqrt(1 - t * t) + 1) + minimum


def _elastic_in(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total
    s = 1.70158
    p = total * 0.3
    a = maximum
    if t == 0:
        return minimum
    if t == 1:
        return minimum + maximum
    if a < abs(maximum):
        a = maximum
        s = p / 4
    else:
        s = p / (2 * math.pi) * math.asin(maximum / a)
    t -= 1
    return -(a * math.pow(2, 10 * t) * math.sin((t * total - s) * (2 * math.pi) / p)) + minimum


def _elastic_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total
    s = 1.70158
    p = total * 0.3
    a = maximum
    if t == 0:
        return minimum
    if t == 1:
        return minimum + maximum
    if a < abs(maximum):
        a = maximum
        s = p / 4
    else:
        s = p / (2 * math.pi) * math.asin(maximum / a)
    return a * math.pow(2, -10 * t) * math.sin((t * total - s) * (2 * math.pi) / p) + maximum + minimum


def _elastic_in_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total / 2
    s = 1.70158
    p = total * 0.45
    a = maximum
    if t == 0:
        return minimum
    if t == 2:
        return minimum + maximum
    if a < abs(maximum):
        a = maximum
        s = p / 4
    else:
        s = p / (2 * math.pi) * math.asin(maximum / a)
    if t < 1:
        t -= 1
        return -0.5 * (a * math.pow(2, 10 * t) * math.sin((t * total - s) * (2 * math.pi) / p)) + minimum
    t -= 1
    return a * math.pow(2, -10 * t) * math.sin((t * total - s) * (2 * math.pi) / p) * 0.5 + maximum + minimum


def _back_in(t: float, total: float, minimum: float, maximum: float, s: float) -> float:
    maximum -= minimum
    t /= total
    return maximum * t * t * ((s + 1) * t - s) + minimum


def _back_out(t: float, total: float, minimum: float, maximum: float, s: float) -> float:
    maximum -= minimum
    t = t / total - 1
    return maximum * (t * t * ((s + 1) * t + s) + 1) + minimum


def _back_in_out(t: float, total: float, minimum: float, maximum: float, s: float) -> float:
    maximum -= minimum
    s *= 1.525
    t /= total / 2
    if t < 1:
        return maximum / 2 * (t * t * ((s + 1) * t - s)) + minimum
    t -= 2
    return maximum / 2 * (t * t * ((s + 1) * t + s) + 2) + minimum


def _bounce_out(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    t /= total
    if t < 1 / 2.75:
        return maximum * (7.5625 * t * t) + minimum
    if t < 2 / 2.75:
        t -= 1.5 / 2.75
        return maximum * (7.5625 * t * t + 0.75) + minimum
    if t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return maximum * (7.5625 * t * t + 0.9375) + minimum
    t -= 2.625 / 2.75
    return maximum * (7.5625 * t * t + 0.984375) + minimum


def _bounce_in(t: float, total: float, minimum: float, maximum: float) -> float:
    maximum -= minimum
    return maximum - _bounce_out(total - t, total, 0, maximum) + minimum


def _bounce_in_out(t: float, total: float, minimum: float, maximum: float) -> float:
    if t < total / 2:
        return _bounce_in(t * 2, total, 0, maximum - minimum) * 0.5 + minimum
    return _bounce_out(t * 2 - total, total, 0, maximum - minimum) * 0.5 + minimum + (maximum - minimum) * 0.5


def get_easing(easing_type: int, t: float) -> float:
    lookup = {
        0: _linear,
        1: _cubic_out,
        2: _cubic_in,
        3: _quad_in,
        4: _quad_out,
        5: _quad_in_out,
        6: _cubic_in,
        7: _cubic_out,
        8: _cubic_in_out,
        9: _quart_in,
        10: _quart_out,
        11: _quart_in_out,
        12: _quint_in,
        13: _quint_out,
        14: _quint_in_out,
        15: _sine_in,
        16: _sine_out,
        17: _sine_in_out,
        18: _exp_in,
        19: _exp_out,
        20: _exp_in_out,
        21: _circ_in,
        22: _circ_out,
        23: _circ_in_out,
        24: _elastic_in,
        25: _elastic_out,
        26: _elastic_in_out,
        27: lambda time, total, minimum, maximum: _back_in(time, total, minimum, maximum, 1),
        28: lambda time, total, minimum, maximum: _back_out(time, total, minimum, maximum, 1),
        29: lambda time, total, minimum, maximum: _back_in_out(time, total, minimum, maximum, 1),
        30: _bounce_in,
        31: _bounce_out,
        32: _bounce_in_out,
    }
    return lookup.get(easing_type, _linear)(t, 1, 0, 1)
