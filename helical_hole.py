#!/usr/bin/env python
# Everything is always in millimeters, not stupid imperial!
# Jog machine to desired location then run the output generated by this script.

def floatf(f=0.0):
    return ('%0.4f' % f).rstrip('0').rstrip('.')

def helical_hole(
               diameter=0.0,
               depth=0.0,
               pitch=0.0,
               feedrate=0.0,
               endmill=0.0,
               direction='',
              ):
    '''Generate gcode for a hole at the current position using a helix.
    '''
    assert isinstance(diameter, float) and diameter > 0.0
    assert isinstance(depth, float) and depth > 0.0
    assert isinstance(pitch, float) and pitch > 0.0
    assert isinstance(feedrate, float) and feedrate > 0.0
    assert isinstance(direction, str) and direction in ['cw', 'ccw']
    # Endmill size > 0 assertion not needed as you may want to just generate a
    #   "dumb" path for a different shape of endmill.
    assert isinstance(endmill, float) and endmill < diameter
    
    # Initialise gcode lines.
    g = []
    
    # Set units as millimeters.
    g.append('G21')
    
    # Select XY plane.
    g.append('G17')
    
    # Use relative positioning (as opposed to absolute).
    g.append('G91')
    
    if direction == 'cw':
        g_dir = 'G2'
    elif direction == 'ccw':
        g_dir = 'G3'
    
    radius = (diameter / 2) - (endmill / 2)
    
    # Offset from centre of hole to start spiral
    g.append('G0 Y-%s' % floatf(radius))
    
    # First shallow loop for remainder.
    # This loop will be less than the specified pitch.
    remainder_pitch = depth % pitch
    g.append('%(dir)s X0 Y0 Z-%(lp)s I0 J%(j)s F%(f)s' % {
                                                          'dir': g_dir,
                                                          'f': floatf(feedrate),
                                                          'lp': floatf(remainder_pitch),
                                                          'j': floatf(radius),
                                                          })
    
    # Main helix.
    for l in range(int(depth / pitch)):
        g.append('%(dir)s X0 Y0 Z-%(lp)s I0 J%(j)s F%(f)s' % {
                                                              'dir': g_dir,
                                                              'f': floatf(feedrate),
                                                              'lp': floatf(pitch),
                                                              'j': floatf(radius),
                                                             })
    
    # Finishing circle.
    # This has no depth and just evens out the bottom.
    g.append('%(dir)s X0 Y0 Z0 I0 J%(j)s F%(f)s' % {
                                                 'dir': g_dir,
                                                 'f': floatf(feedrate),
                                                 'j': floatf(radius),
                                                })
    
    # Go back to original position.
    g.append('G0 Z%s' % floatf(depth))
    g.append('G0 Y%s' % floatf(radius))
    
    print('\n'.join(g))


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--diameter',
                        action='store',
                        default=10.0,
                        type=float,
                        help='hole diameter')
    
    parser.add_argument('--depth',
                        action='store',
                        default=8.0,
                        type=float,
                        help='hole depth')
    
    parser.add_argument('--pitch',
                        action='store',
                        default=2.0,
                        type=float,
                        help='helix pitch')
    
    parser.add_argument('--feedrate',
                        action='store',
                        default=500.0,
                        type=float,
                        help='feedrate (mm/minute)')
    
    parser.add_argument('--endmill',
                        action='store',
                        default=3.0,
                        type=float,
                        help='endmill diameter (cylindrical)')
    
    parser.add_argument('--direction',
                        action='store',
                        default='cw',
                        choices=['cw', 'ccw'],
                        help='helix direction')

    args = parser.parse_args()
    
    helical_hole(
                 diameter=args.diameter,
                 depth=args.depth,
                 pitch=args.pitch,
                 feedrate=args.feedrate,
                 endmill=args.endmill,
                 direction=args.direction,
                )
