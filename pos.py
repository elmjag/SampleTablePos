#!/usr/bin/env python
from dataclasses import dataclass
from numpy import matmul, subtract
from transforms3d.euler import euler2quat, euler2mat
from transforms3d.quaternions import rotate_vector
from transforms3d.affines import compose
from transforms3d.utils import vector_norm

XM = [0, -0.175, 0, 1]
YDM = [0, -0.125, 0.175, 1]
YIM = [-0.375, -0.125, -0.175, 1]
YOM = [0.375, -0.125, -0.175, 1]
ZIM = [-0.375, -0.05, -0.275, 1]
ZOM = [0.375, -0.05, -0.275, 1]

XF = [-0.45, -0.175, 0]
YDF = [0, -0.575, 0.175]
YIF = [-0.375, -0.575, -0.175]
YOF = [0.375, -0.575, -0.175]
ZIF = [-0.375, -0.05, -0.725]
ZOF = [0.375, -0.05, -0.725]


@dataclass
class Pos:
    def __init__(self, hvect):
        self.x = hvect[0]
        self.y = hvect[1]
        self.z = hvect[2]

    def as_dict(self):
        return dict(x=self.x, y=self.y, z=self.z)

    x: float
    y: float
    z: float


@dataclass
class MotorPos:
    xm: Pos
    ydm: Pos
    yim: Pos
    yom: Pos
    zim: Pos
    zom: Pos


def get_pos(rot_x, rot_y, rot_z, tx, ty, tz):
    T = [tx, ty, tz]
    R = euler2mat(rot_x, rot_y, rot_z)
    Z = [1, 1, 1]

    A = compose(T, R, Z)

    xm_pos = matmul(A, XM)
    x_len = vector_norm(subtract(xm_pos[:-1], XF))

    ydm_pos = matmul(A, YDM)
    yd_len = vector_norm(subtract(ydm_pos[:-1], YDF))

    yim_pos = matmul(A, YIM)
    yi_len = vector_norm(subtract(yim_pos[:-1], YIF))

    yom_pos = matmul(A, YOM)
    yo_len = vector_norm(subtract(yom_pos[:-1], YOF))

    zim_pos = matmul(A, ZIM)
    zi_len = vector_norm(subtract(zim_pos[:-1], ZIF))

    zom_pos = matmul(A, ZOM)
    zo_len = vector_norm(subtract(zom_pos[:-1], ZOF))

    print(f"X: {x_len}\nYD: {yd_len}\nYI: {yi_len}\nYO: {yo_len}\n"
          f"ZI: {zi_len}\nZO: {zo_len}")

    return MotorPos(
        xm=Pos(xm_pos),
        ydm=Pos(ydm_pos),
        yim=Pos(yim_pos),
        yom=Pos(yom_pos),
        zim=Pos(zim_pos),
        zom=Pos(zom_pos),
    )
