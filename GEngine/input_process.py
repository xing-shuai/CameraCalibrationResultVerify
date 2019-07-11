from OpenGL.GL import *
from OpenGL.GLUT import *

keys = {
    "escape": False,
    "w": False,
    "s": False,
    "a": False,
    "d": False,
    "g": False,
    "r": False,
    "z": False,
    "j": False,
    "l": False,
    "c": False
}


class InputProcess:
    def __init__(self, camera, window_width, window_height):
        self.camera = camera
        self.window_width = window_width
        self.window_height = window_height

        self.last_x = window_width / 2.0
        self.last_y = window_height / 2.0
        self.first_mouse = True
        self.mouse_leave = True

    def keys_down(self, key, x, y):
        if ord(key) == 27:
            keys["escape"] = True
        # sd = ord(key)
        if ord(key) == 114:
            keys["r"] = True
            keys["g"] = False
            keys["z"] = False
            keys["c"] = False

        if ord(key) == 103:
            keys["g"] = True
            keys["r"] = False
            keys["z"] = False
            keys["c"] = False

        if ord(key) == 122:
            keys["z"] = True
            keys["r"] = False
            keys["g"] = False
            keys["c"] = False

        if ord(key) == 99:
            keys["c"] = True
            keys["r"] = False
            keys["g"] = False
            keys["z"] = False

        if ord(key) == 119:
            keys["w"] = True

        if ord(key) == 115:
            keys["s"] = True

        if ord(key) == 97:
            keys["a"] = True

        if ord(key) == 100:
            keys["d"] = True

        if ord(key) == 106:
            keys["j"] = True

        if ord(key) == 108:
            keys["l"] = True

    def keys_up(self, key, x, y):
        if ord(key) == 27:
            keys["escape"] = False

        if ord(key) == 119:
            keys["w"] = False

        if ord(key) == 115:
            keys["s"] = False

        if ord(key) == 97:
            keys["a"] = False

        if ord(key) == 100:
            keys["d"] = False

        if ord(key) == 106:
            keys["j"] = False

        if ord(key) == 108:
            keys["l"] = False

    def reshape(self, w, h):
        glViewport(0, 0, w, h)

    def process_keys_by_frame(self, delta_time):
        if self.camera.camera_keep_static is False:
            self.camera.process_keyboard(delta_time)

    def mouse_move(self, x, y):

        if self.mouse_leave:
            self.last_x = x
            self.last_y = y
            self.mouse_leave = False

        if self.first_mouse:
            self.last_x = x
            self.last_y = y
            self.first_mouse = False

        x_offset = x - self.last_x

        y_offset = self.last_y - y

        self.last_x = x
        self.last_y = y

        # print(x, y)
        if self.camera.camera_keep_static is False:
            self.camera.process_mouse_movement(x_offset, y_offset)

    def mouse_state(self, state):
        glutWarpPointer(int(self.window_width / 2), int(self.window_height / 2))
        if state == 1:
            self.mouse_leave = True
            pass
