#!/usr/bin/env python
import math
import argparse
import time
from math import radians
from pos import get_pos
from wscli import WSRemote

#
# pitch  – rotation around global x
# yaw    – rotation around global y
# roll   – rotation around global z
#


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("pitch", type=float)
    parser.add_argument("yaw", type=float)
    parser.add_argument("roll", type=float)
    parser.add_argument("x", type=float)
    parser.add_argument("y", type=float)
    parser.add_argument("z", type=float)

    args = parser.parse_args()

    # convert angles to radians
    args.pitch = math.radians(args.pitch)
    args.yaw = math.radians(args.yaw)
    args.roll = math.radians(args.roll)

    return args


def set_posture(rot_x, rot_y, rot_z, x, y, z):
    marks_pos = get_pos(rot_x, rot_y, rot_z, x, y, z)

    marks = dict(
        xm=marks_pos.xm.as_dict(),
        ydm=marks_pos.ydm.as_dict(),
        yim=marks_pos.yim.as_dict(),
        yom=marks_pos.yom.as_dict(),
        zim=marks_pos.zim.as_dict(),
        zom=marks_pos.zom.as_dict(),
    )

    remote = WSRemote()
    remote.send(
        dict(
            pitch=rot_x,
            yaw=rot_y,
            roll=rot_z,
            x=x,
            y=y,
            z=z,
            marks=marks,
        )
    )


def steps():
    for n in range(-5, 5):
        yield n/100


def from_cli():
    args = parse_args()

    set_posture(args.pitch, args.yaw, args.roll, args.x, args.y, args.z)


def oscillate_trans(rot_x, rot_y, rot_z):
    for x in steps():
        for y in steps():
            for z in steps():
                set_posture(radians(rot_x), radians(rot_y), radians(rot_z), x, y, z)
                time.sleep(0.1)


def oscillate():
    for rot_x in range(-10, 10):
        for rot_y in range(-10, 10):
            for rot_z in range(-10, 10):
                oscillate_trans(rot_x, rot_y, rot_z)


from_cli()
#oscillate()
#print(list(steps()))