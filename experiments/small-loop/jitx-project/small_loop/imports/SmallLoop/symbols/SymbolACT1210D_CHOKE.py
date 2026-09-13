# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/SymbolACT1210D_CHOKE.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline, Arc, ArcPolyline


class SymbolACT1210D_CHOKE(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((-4, 2), 2, Direction.Left),
        2: Pin((-4, -2), 2, Direction.Left),
        3: Pin((4, -2), 2, Direction.Right),
        4: Pin((4, 2), 2, Direction.Right),
    }
    draws = [
        ArcPolyline(0.2032, [
            Arc((3.19993, -2.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-2.79993, -2.00007), 1.00007, 179.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((3.20007, -2.00007), 1.00007, 179.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((3.19993, 2.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-0.79993, 2.00007), 1.00007, 269.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-0.80007, -2.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((1.20007, -2.00007), 1.00007, 179.99605, -89.99211)]),
        Polyline(0.2032, [(4.2, -0.4), (-3.8, -0.4)]),
        ArcPolyline(0.2032, [
            Arc((1.20007, 2.00007), 1.00007, 269.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-0.79993, -2.00007), 1.00007, 179.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((3.20007, 2.00007), 1.00007, 269.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((1.19993, -2.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((1.19993, 2.00007), 1.00007, 359.99605, -89.99211)]),
        Polyline(0.2032, [(4.2, 0.4), (-3.8, 0.4)]),
        ArcPolyline(0.2032, [
            Arc((-2.80007, 2.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-0.80007, 2.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-2.80007, -2.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.2032, [
            Arc((-2.79993, 2.00007), 1.00007, 269.99605, -89.99211)]),
    ]

