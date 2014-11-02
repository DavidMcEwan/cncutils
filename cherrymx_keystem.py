#!/usr/bin/env python
# Everything is always in millimeters, not stupid imperial!
# Jog machine to desired location then run the output generated by this script.

from gcode_base import *
from gcode_profile_polygon import *
from math_base import *

def cherrymx_keycross_points(
                    height=4.0,
                    width=4.0,
                    height_thk=1.1,
                    width_thk=1.3,
                    endmill=1.0,
                   ): # {{{
    '''Generate points for polygon used for making CherryMX cross holes for keycaps.
    '''

    assert isinstance(width, float) and width > 0.0
    
    # Calculate points to move to.
    inner_x = height_thk/2 - endmill/2
    outer_x = width/2 - endmill/2
    inner_y = width_thk/2 - endmill/2
    outer_y = height/2 - endmill/2
    
    # Points relative to centre listed in CW direction.
    pts = [
           # Up spar
           (-inner_x, +inner_y),
           (-inner_x, +outer_y),
           (+inner_x, +outer_y),
           
           # Right spar
           (+inner_x, +inner_y),
           (+outer_x, +inner_y),
           (+outer_x, -inner_y),
           
           # Down spar
           (+inner_x, -inner_y),
           (+inner_x, -outer_y),
           (-inner_x, -outer_y),
           
           # Left spar
           (-inner_x, -inner_y),
           (-outer_x, -inner_y),
           (-outer_x, +inner_y),
           (-inner_x, +inner_y),
          ]
    
    return pts
# }}}

def cherrymx_keysup_points(
                    height=5.2,
                    width=6.8,
                    endmill=1.0,
                   ): # {{{
    '''Generate points for polygon used for making CherryMX cross support for keycaps.
    '''

    assert isinstance(width, float) and width > 0.0
    
    # Calculate points to move to.
    y = height/2 + endmill/2
    x = width/2 + endmill/2
    
    # Points relative to centre listed in CW direction.
    pts = [
           (-x, +y),
           (+x, +y),
           (+x, -y),
           (-x, -y),
          ]
    
    return pts
# }}}

def array_keystem_points(
                    height=6,
                    width=14,
                    supheight=5.2,
                    supwidth=6.8,
                    space=1.0,
                    endmill=1.0,
                   ): # {{{
    '''Generate points for polygon used for making CherryMX cross support for keycaps.
    '''
    
    # Calculate points to move to.
    xdiff = supwidth + endmill + space + endmill
    ydiff = supheight + endmill + space + endmill
    
    # Move along X row, then up Y column to next row, then back along row.
    pts = []
    yacc = 0.0
    for row in range(height):
        r = [(col*xdiff, yacc) for col in range(width)]
        if not row % 2:
            r.reverse()
        yacc += ydiff
        pts += r
    
    return pts
# }}}

def cherrymx_keystem_profile(
                     crossheight=4.5,
                     crosswidth=4.5,
                     crossheight_thk=1.1,
                     crosswidth_thk=1.3,
                     supheight=5.2,
                     supwidth=6.8,
                     depth=3.3,
                     pitch=1.0,
                     feedrate=100.0,
                     plungerate=100.0,
                     clearance=5.0,
                     endmill=1.0,
                     direction='ccw',
                     ablpd=True,
                    ): # {{{
    '''Generate gcode for a hole at the current position to hold cherry mx keystem.
    '''

    assert isinstance(crosswidth, float) and crosswidth > 0.0
    assert isinstance(crossheight, float) and crossheight > 0.0
    assert isinstance(depth, float) and depth > 0.0
    assert isinstance(pitch, float) and pitch > 0.0
    assert isinstance(feedrate, float) and feedrate > 0.0
    assert isinstance(plungerate, float) and plungerate > 0.0
    assert isinstance(clearance, float) and clearance > 0.0
    # Endmill size > 0 assertion not needed as you may want to just generate a
    #   "dumb" path for a different shape of endmill.
    assert isinstance(endmill, float) and endmill < crosswidth
    assert isinstance(direction, str) and direction in ['cw', 'ccw']
    assert isinstance(ablpd, bool)
    
    pts = cherrymx_keycross_points(crossheight,
                                   crosswidth,
                                   crossheight_thk,
                                   crosswidth_thk,
                                   endmill)
    
    # Initialise gcode lines.
    g = []
    
    # Use relative positioning (as opposed to absolute).
    # Required to make this code callable like a function.
    g.append('G91')
    
    g.append(polygon_profile(
                             pts=pts,
                             depth=depth,
                             pitch=pitch,
                             feedrate=feedrate,
                             plungerate=plungerate,
                             clearance=clearance,
                             ablpd=ablpd,
                            ))
    
    # Now the surrounding support square.
    pts = cherrymx_keysup_points(supheight, supwidth, endmill)
    g.append(polygon_profile(
                             pts=pts,
                             depth=depth,
                             pitch=pitch,
                             feedrate=feedrate,
                             plungerate=plungerate,
                             clearance=clearance,
                             ablpd=ablpd,
                            ))
    
    return '\n'.join(g)
# }}}


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--arrayheight',
                        action='store',
                        default=6,
                        type=int,
                        help='array height (number)')
    
    parser.add_argument('--arraywidth',
                        action='store',
                        default=14,
                        type=int,
                        help='array width (number)')
    
    parser.add_argument('--arrayspace',
                        action='store',
                        default=1.0,
                        type=float,
                        help='array spacing (mm)')
    
    parser.add_argument('--crossheight',
                        action='store',
                        default=4.5,
                        type=float,
                        help='cross height (mm)')
    
    parser.add_argument('--crosswidth',
                        action='store',
                        default=4.5,
                        type=float,
                        help='cross width (mm)')
    
    parser.add_argument('--crossheight_thk',
                        action='store',
                        default=1.05,
                        type=float,
                        help='Thickness of up/down spars (mm)')
    
    parser.add_argument('--crosswidth_thk',
                        action='store',
                        default=1.2,
                        type=float,
                        help='Thickness of left/right spars (mm)')
    
    parser.add_argument('--supheight',
                        action='store',
                        default=5.2,
                        type=float,
                        help='support square height (mm)')
    
    parser.add_argument('--supwidth',
                        action='store',
                        default=6.8,
                        type=float,
                        help='support square width (mm)')
    
    parser.add_argument('--depth',
                        action='store',
                        default=3.5,
                        type=float,
                        help='cross depth (mm)')
    
    parser.add_argument('--pitch',
                        action='store',
                        default=1.0,
                        type=float,
                        help='cutting pitch (mm)')
    
    parser.add_argument('--feedrate',
                        action='store',
                        default=200.0,
                        type=float,
                        help='feedrate (mm/minute)')
    
    parser.add_argument('--plungerate',
                        action='store',
                        default=100.0,
                        type=float,
                        help='plungerate (mm/minute)')
    
    parser.add_argument('--clearance',
                        action='store',
                        default=5.0,
                        type=float,
                        help='clearance (mm)')
    
    parser.add_argument('--endmill',
                        action='store',
                        default=1.0,
                        type=float,
                        help='endmill diameter (cylindrical)')
    
    parser.add_argument('--direction',
                        action='store',
                        default='cw',
                        choices=['cw', 'ccw'],
                        help='cutting direction')
    
    parser.add_argument('--ablpd',
                        action='store',
                        default=0,
                        type=int,
                        choices=[0, 1],
                        help='Anti Backlash Point Drilling')

    args = parser.parse_args()
    
    # Initialise gcode lines.
    g = []
    
    # Select XY plane.
    g.append('G17')
    
    # Set units as millimeters.
    g.append('G21')
    
    # Assume spindle starts at zero.
    g.append('G0 Z%s' % floatf(args.clearance))
    
    array_pts = array_keystem_points(
                                     height=args.arrayheight,
                                     width=args.arraywidth,
                                     supheight=args.supheight,
                                     supwidth=args.supwidth,
                                     space=args.arrayspace,
                                     endmill=args.endmill,
                                    )
    for pt in array_pts:
        g.append('G0 X%s Y%s' % (floatf(pt[0]), floatf(pt[1])))
        # Cherry profile function should assume spindle at clearance.
        g.append(cherrymx_keystem_profile(
                                          crossheight=args.crossheight,
                                          crosswidth=args.crosswidth,
                                          crossheight_thk=args.crossheight_thk,
                                          crosswidth_thk=args.crosswidth_thk,
                                          supheight=args.supheight,
                                          supwidth=args.supwidth,
                                          depth=args.depth,
                                          pitch=args.pitch,
                                          feedrate=args.feedrate,
                                          plungerate=args.plungerate,
                                          clearance=args.clearance,
                                          endmill=args.endmill,
                                          direction=args.direction,
                                          ablpd=bool(args.ablpd),
                                         ))
    # Cherry profile function should leave spindle at clearance.
        g.append('G90')


    # Put gcode onto STDOUT to let caller do any file redirect.
    print('\n'.join(g))