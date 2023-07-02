from ursina import *

app = Ursina()
window.borderless = False
window.exit_button.visible = False
EditorCamera()

cubes = []
history = []

cubes_left = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
cubes_down = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
cubes_front = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
cubes_back = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
cubes_right = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
cubes_up = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
cubes_m = {Vec3(0, y, z) for y in range(-1, 2) for z in range(-1, 2)}
cubes_e = {Vec3(x, 0, z) for x in range(-1, 2) for z in range(-1, 2)}
cubes_s = {Vec3(x, y, 0) for x in range(-1, 2) for y in range(-1, 2)}

dict_cubes = {
    'l': cubes_left,
    'r': cubes_right,
    'u': cubes_up,
    'd': cubes_down,
    'f': cubes_front,
    'b': cubes_back,
    'm': cubes_m,
    'e': cubes_e,
    's': cubes_s
}

dict_axis = {
    'l': 'rotation_x',
    'r': 'rotation_x',
    'm': 'rotation_x',
    'u': 'rotation_y',
    'd': 'rotation_y',
    'e': 'rotation_y',
    'f': 'rotation_z',
    'b': 'rotation_z',
    's': 'rotation_z'
}

for x in range(-1, 2):
    for y in range(-1, 2):
        for z in range(-1, 2):
            cubes.append(
                Entity(model='models/custom_cube.obj', texture='textures/rubik_texture.png', position=(x, y, z)))

cubes[12].texture = 'textures/front.png'
cubes[4].texture = 'textures/left.png'
cubes[14].texture = 'textures/back.png'
cubes[22].texture = 'textures/right.png'
cubes[10].texture = 'textures/down.png'
cubes[16].texture = 'textures/up.png'

history.append(cubes)


def delete_parent():
    for cube in cubes:
        if cube.parent == cubes[13]:
            world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
            cube.parent = scene
            cube.position, cube.rotation = world_pos, world_rot


def attach_parrent(face):
    buf = dict_cubes[face]

    cubes[13].rotation = 0
    for cube in cubes:
        if cube.position in buf:
            cube.parent = cubes[13]


def cube_rotation(name, angle=0):
    delete_parent()
    attach_parrent(name)
    if held_keys['shift'] and angle == 0:
        angle = -90
    elif angle == 0:
        angle = 90

    H.add_move(name, -angle)

    if name in 'lrm':
        cubes[13].animate(dict_axis[name], cubes[13].rotation_x + angle, duration=.2)
    if name in 'ude':
        cubes[13].animate(dict_axis[name], cubes[13].rotation_y + angle, duration=.2)
    if name in 'fbs':
        cubes[13].animate(dict_axis[name], cubes[13].rotation_z + angle, duration=.2)


class History:
    def __init__(self):
        self.history = []

    def add_move(self, name, angle):
        self.history.append((name, angle))

    def undo(self):
        if len(self.history) > 0:
            cube_rotation(self.history[-1][0], self.history[-1][1])
            self.history.pop()
            self.history.pop()


def input(key):
    if key in ('lrufbdmes'):
        cube_rotation(key)
    if key == 'h':
        H.undo()


H = History()
app.run()
