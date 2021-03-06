#!/usr/bin/env python
# Generate gcode for milling a mcdox keyboard.
# All parts specified for LHS.
# RHS should just be a reflection around X=0.

swmnt_stats = 0
swmnt_plot = 0
swmnt_gcode = 0
base_plot = 1
base_gcode = 1

from math import *
import sys

sys.path.insert(0, '../cncutils')
from math_base import *

# Spacing between centers of cherrymx switches.
spc = 19.0


# Ergonomic column offsets for finger cluster.
c0_Y = 0.0 # 1.5x outer.
c1_Y = 0.0 # Pinky finger.
c2_Y = 3.0 # Ring finger.
c3_Y = 4.5 # Middle finger.
c4_Y = 3.0 # Index finger.
c5_Y = 1.5 # Other index finger.
c6_Y = 1.5 # 1.5x inner.

# Non-ergonomic positions from origin
c0_X = 0.0              # 1.5x outer.
c1_X = c0_X + 1.25*spc  # Pinky finger.
c2_X = c1_X + spc       # Ring finger.
c3_X = c2_X + spc       # Middle finger.
c4_X = c3_X + spc       # Index finger.
c5_X = c4_X + spc       # Other index finger.
c6_X = c5_X + spc       # 1.5x inner.

c0 = [
      (c0_X,             4*spc+c0_Y, 0),
      (c0_X,             3*spc+c0_Y, 0),
      (c0_X,             2*spc+c0_Y, 0),
      (c0_X,             1*spc+c0_Y, 0),
      (c0_X + 0.25*spc,  0*spc+c0_Y, 0),
     ]
top_left = c0[0]
c0.reverse()

c1 = [
      (c1_X,  4*spc+c1_Y, 0),
      (c1_X,  3*spc+c1_Y, 0),
      (c1_X,  2*spc+c1_Y, 0),
      (c1_X,  1*spc+c1_Y, 0),
      (c1_X,  0*spc+c1_Y, 0),
     ]

c2 = [
      (c2_X,  4*spc+c2_Y, 0),
      (c2_X,  3*spc+c2_Y, 0),
      (c2_X,  2*spc+c2_Y, 0),
      (c2_X,  1*spc+c2_Y, 0),
      (c2_X,  0*spc+c2_Y, 0),
     ]
c2.reverse()

c3 = [
      (c3_X,  4*spc+c3_Y, 0),
      (c3_X,  3*spc+c3_Y, 0),
      (c3_X,  2*spc+c3_Y, 0),
      (c3_X,  1*spc+c3_Y, 0),
      (c3_X,  0*spc+c3_Y, 0),
     ]

c4 = [
      (c4_X,  4*spc+c4_Y, 0),
      (c4_X,  3*spc+c4_Y, 0),
      (c4_X,  2*spc+c4_Y, 0),
      (c4_X,  1*spc+c4_Y, 0),
      (c4_X,  0*spc+c4_Y, 0),
     ]
c4.reverse()

c5 = [
      (c5_X,  4*spc+c5_Y, 0),
      (c5_X,  3*spc+c5_Y, 0),
      (c5_X,  2*spc+c5_Y, 0),
      (c5_X,  1*spc+c5_Y, 0),
     ]

c6 = [
      (c6_X,  4*spc+c6_Y,    0),
      (c6_X,  2.75*spc+c6_Y, 1),
      (c6_X,  1.25*spc+c6_Y, 1),
     ]
c6.reverse()

finger_mx_holes = c6 + c5 + c4 + c3 + c2 + c1 + c0
finger_mx_holes = [(p[0], p[1], p[2]*pi/2) for p in finger_mx_holes]


# Ergonomic angle of rotation for thumb cluster.
thumb_rotate = radians(-25)

# Lower left of thumb cluster is taken as the origin.
thumb_pos = [c5_X +0.5*spc, -0.5*spc]

# Centers of switch holes in thumb cluster.
thumb_mx_holes = [
                  (0*spc, 0*spc),
                  (1*spc, 0*spc),
                  (2*spc, -0.5*spc),
                  (2*spc, +0.5*spc),
                  (2*spc, +1.5*spc),
                  (1*spc, +1.5*spc),
                 ]
thumb_mx_holes = pts_rotate(thumb_mx_holes, [thumb_rotate])
thumb_mx_holes = pts_shift(thumb_mx_holes, thumb_pos)
thumb_mx_holes = [list(p) + [thumb_rotate] for p in thumb_mx_holes]
thumb_mx_holes[0][2] += pi/2
thumb_mx_holes[1][2] += pi/2
thumb_mx_holes = [tuple(p) for p in thumb_mx_holes]
bottom_right = thumb_mx_holes[2]


mx_holes = thumb_mx_holes + finger_mx_holes
center = pt_between_pts(top_left[:2], bottom_right[:2])
radius = distance_between_pts(top_left[:2], center) + 0.75*spc
diameter = 2 * radius

# Center whole design about the origin to make zeroing on A4 sheets easier as
#   there is little margin for error.
mx_rotates = [h[2] for h in mx_holes]
mx_points = [(h[0], h[1]) for h in mx_holes]
mx_points = pts_shift(mx_points, [-center[0], -center[1]])
mx_holes = [(mx_points[i][0], mx_points[i][1], mx_rotates[i]) for i in range(len(mx_holes))]
center = (0.0, 0.0)
# A4 dimensions are 297x210 so to fit nicely on cheap sheets of acrylic try to
#   keep dimensions down.

# TODO: In future versions it should be the base holes which have the rotate of
#   11 degrees, although negative.
# This hasn't been changed yet as I've already cut a pair of swmnt plates and
#   need a base plate to match them.
n_fix = 6
base_holes = gen_polygon_pts(n_fix, [radius-0.5*spc])
base_holes = pts_rotate(base_holes, [3*2*pi/n_fix], center)
fix_holes = pts_rotate(base_holes, [radians(11)], center)

# mx_holes is now a list of tuples containing the coordinates and rotations of all switches on LHS.
if swmnt_stats:
    out = []
    out += ['Operations:']
    out += ['\tCherryMX holes:']
    for h in mx_holes:
        out += ['\t\t(%0.2f, %0.2f) rotate=%d' % (h[0], h[1], degrees(h[2]))]
    out += ['\tFixing holes:']
    for h in fix_holes:
        out += ['\t\t(%0.2f, %0.2f)' % (h[0], h[1])]
    out += ['\tLED holes: TODO']
    out += ['\tOuter:']
    out += ['\t\tcenter=(%0.2f, %0.2f)' % center]
    out += ['\t\tradius=%0.2f' % radius]
    out += ['\t\tdiameter=%0.2f' % diameter]
    print('\n'.join(out))

# TODO: Calculate LED holes.
# TODO: Plot LED holes.

if swmnt_plot:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    
    ax = plt.subplot(111, aspect=1)
    # Plot path between centers of switch holes.
    x = [p[0] for p in mx_holes]
    y = [p[1] for p in mx_holes]
    ax.plot(x, y, marker='x', color='r')
    
    # Plot fixing holes.
    x = [p[0] for p in fix_holes]
    y = [p[1] for p in fix_holes]
    ax.plot(x, y, marker='x', color='g')
    
    # Draw circle for outer
    ax.scatter(center[0], center[1])
    c = mpatches.Circle(center, radius, fill=False)
    ax.add_patch(c)
    
    # Plot paths for each switch
    from cherrymx_hole import *
    for h in mx_holes:
        pts = pts_shift(cherrymx_points(rotate=h[2]), [h[0], h[1]])
        x = [p[0] for p in pts] + [pts[0][0]]
        y = [p[1] for p in pts] + [pts[0][1]]
        ax.plot(x, y, color='g')
    plt.show()

if swmnt_gcode:
    from gcode_base import *
    from gcode_profile_circle import *
    from cherrymx_hole import *
    clearance = 5.0
    depth = 3.8
    
    # Acrlic 400 just on the slow side, 500 definitely too fast.
    # MDF 660 seems about right.
    feedrate = 480.0
    
    g = []
    # Set units to mm.
    g.append('G21')
    
    # Move to X0Y0, Zclearance
    g.append('G90')
    g.append('G0 Z%s' % floatf(clearance))
    g.append('G0 X0 Y0')
    
    # Cut switch holes.
    for h in mx_holes:
        g.append('G0 X%s Y%s' % (floatf(h[0]), floatf(h[1])))
        g.append(cherrymx_profile(
                                  rotate=h[2],
                                  clearance=clearance,
                                  depth=depth,
                                  pitch=0.8, # MDF=1.0, Acrylic=0.8
                                  width=13.25,
                                  feedrate=feedrate,
                                  ablpd=False,
                                 ))
        g.append('G90')
    
    # Drill fixing holes.
    g.append(points_drill_abs(fix_holes, depth=depth))
    
    # Finally cut out boundary.
    g.append(profile_circle_abs(
                                center,
                                diameter,
                                depth=depth,
                                pitch=1.0,
                                feedrate=feedrate,
                               ))
    
    with open('mcdox_swmnt.nc', 'w') as fd:
        fd.write('\n'.join(g))


# The base is composed of 2 circles with a thinner section in the middle, made
#   from the arcs of other circles.
# Centers of circles are:
# A - left hand
# B - bottom arc
# C - right hand
# D - top arc
# Start stop points of the arcs are:
# E - Between A and D
# F - Between A and B
# G - Between C and D
# H - Between C and B
# The size of the arcs is controlled by 3 parameters:
# hand_sep - separation between hand plates
# r_top - radius of top arc
# r_bot - radius of bottom arc
r_hand = radius
hand_sep = 20.0
r_top = sqrt(2)*r_hand
r_bot = r_hand/sqrt(2)/sqrt(2)

sep = hand_sep + 2*r_hand
baseA = (r_hand, r_hand)
baseB = (baseA[0] + sep/2, baseA[1] - sqrt((r_hand + r_bot)**2 - (sep/2)**2))
baseC = (baseA[0] + sep, baseA[1])
baseD = (baseB[0], baseA[1] + sqrt((r_hand + r_top)**2 - (sep/2)**2))
baseE = pt_between_pts(baseA, baseD, r_hand/(r_hand+r_top))
baseF = pt_between_pts(baseA, baseB, r_hand/(r_hand+r_bot))
baseG = pt_between_pts(baseC, baseD, r_hand/(r_hand+r_top))
baseH = pt_between_pts(baseC, baseB, r_hand/(r_hand+r_bot))

if base_plot:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    
    ax = plt.subplot(111, aspect=1)
    ax.scatter(baseA[0], baseA[1])
    a = mpatches.Circle(baseA, r_hand, fill=False)
    ax.add_patch(a)
    
    ax.scatter(baseB[0], baseB[1])
    b = mpatches.Arc(
                     xy=baseB,
                     width=2*r_bot,
                     height=2*r_bot,
                     theta1=degrees(dir_between_pts(baseB, baseC)[0]),
                     theta2=degrees(dir_between_pts(baseB, baseA)[0]),
                     )
    ax.add_patch(b)
    
    ax.scatter(baseC[0], baseC[1])
    c = mpatches.Circle(baseC, r_hand, fill=False)
    ax.add_patch(c)
    
    ax.scatter(baseD[0], baseD[1])
    d = mpatches.Arc(
                     xy=baseD,
                     width=2*r_top,
                     height=2*r_top,
                     theta1=degrees(dir_between_pts(baseD, baseA)[0]),
                     theta2=degrees(dir_between_pts(baseD, baseC)[0]),
                     )
    ax.add_patch(d)
    
    ax.scatter(baseE[0], baseE[1])
    ax.scatter(baseF[0], baseF[1])
    ax.scatter(baseG[0], baseG[1])
    ax.scatter(baseH[0], baseH[1])
    
    plt.show()

# Because the shapeoko2 is quite small, the base must be cut in 3 parts which
#   should be easy to line up.
# Part0 is for under the left hand plate, includes outline and base holes.
# Part1 is for the middle where the controller will be mounted.
# Part2 is for under the right hand plate, includes outline and base holes.
if base_gcode:
    pass
