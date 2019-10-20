from solid import *
from solid.utils import *

pi = { 'size': [56,85,2], 
       'boreholes': { 
            'offset': [3.5, 3.5],
            'size': [49,58],
            'diameter': {
                'inner': 2.7,
                'outer': 6.0 } } }

p = { 'outer-offset': 10 }

def outer_pillars(kind = 'middle'):
    pillar = [cylinder(d=10, h=80, segments=100)]
    if kind != 'top':
        pillar = union()(
            pillar,
            translate([0, 0, 79])(cylinder(d=5, h=11, segments=100)))
    if kind != 'bottom':
        pillar = difference()(
            pillar,
            translate([0, 0, -0.5])(cylinder(d=5, h=11, segments=100)))
    return union()(
        [translate([x / 2.0, y / 2.0, 0])(pillar)
         for x in [pi['size'][0] + 2 * p['outer-offset'], -pi['size'][0] - 2 * p['outer-offset']] 
         for y in [pi['size'][1] + 2 * p['outer-offset'], -pi['size'][1] - 2 * p['outer-offset']]])

def inner_pillars():
    pillar_height = 40
    screw_nut_M_2_5 = cylinder(d=5.5, h=0.8 * pillar_height, segments=6)
    pillar_top = cylinder(d=6, h=0.16 * pillar_height, segments=100)
    pillar_bottom = cylinder(d=8, h=0.9 * pillar_height, segments=100)
    pillar = union()(
        translate([0, 0, pillar_height * 0.85])(pillar_top),
        pillar_bottom)
    final_pillar = difference()(
        pillar,
        translate([0, 0, -0.5])(cylinder(d=3, h=pillar_height + 1, segments=100)),
        translate([0, 0, -0.5])(screw_nut_M_2_5))
    return union()(
        [translate([x / 2.0, y / 2.0, 0])(final_pillar)
         for x in [pi['boreholes']['size'][0], -pi['boreholes']['size'][0]] 
         for y in [pi['boreholes']['size'][1], -pi['boreholes']['size'][1]]])

def bridge():
    bridge_thickness = 3
    middle_size = [20, pi['size'][1] + 3 * p['outer-offset'], bridge_thickness]
    middle = cube(size=middle_size, center=True)
    outer_size = [pi['size'][0] + 2 * p['outer-offset'], p['outer-offset'], bridge_thickness]
    outer_left_out = cylinder(h=outer_size[2] * 3, d=outer_size[1] * 0.95, center=True)
    outer = difference()(
        cube(outer_size, center=True),
        translate([outer_size[0] / 2.0, 0, 0])(outer_left_out),
        translate([-outer_size[0] / 2.0, 0, 0])(outer_left_out))
    outer_bridge = union()(
        translate([0, middle_size[1] / 2.0 - outer_size[1] / 2.0, 0])(outer),
        translate([0, -middle_size[1] / 2.0 + outer_size[1] / 2.0, 0])(outer))
    inner_size = [pi['boreholes']['size'][0], 8, bridge_thickness]
    inner_left_out = cylinder(h=inner_size[2] * 3, d=inner_size[1] * 0.95, center=True)
    inner = difference()(
        cube(inner_size, center=True),
        translate([inner_size[0] / 2.0, 0, 0])(inner_left_out),
        translate([-inner_size[0] / 2.0, 0, 0])(inner_left_out))
    inner_bridge = union()(
        translate([0, pi['boreholes']['size'][1] / 2.0, 0])(inner),
        translate([0, -pi['boreholes']['size'][1] / 2.0, 0])(inner))
    return translate([0, 0, bridge_thickness / 2.0])(union()(middle, outer_bridge, inner_bridge))

raspberry_pi_rack = union()(
    bridge(),
    inner_pillars(),
    outer_pillars())

scad_render_to_file(raspberry_pi_rack, "./raspberry-pi-rack.scad")