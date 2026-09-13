# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolL_US_SRP1265.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Arc, ArcPolyline


class SymbolL_US_SRP1265(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((0, 4), 2, Direction.Up),
        2: Pin((0, -4), 2, Direction.Down),
    }
    draws = [
        ArcPolyline(0.254, [
            Arc((-7.0e-05, -1.00007), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, -2.99993), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, -0.99993), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, 0.99993), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, 1.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, 2.99993), 1.00007, 89.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, 3.00007), 1.00007, 359.99605, -89.99211)]),
        ArcPolyline(0.254, [
            Arc((-7.0e-05, -3.00007), 1.00007, 89.99605, -89.99211)]),
    ]

