from OpenGL.GL import *
from OpenGL.GLUT import *
import time


class GWindow:
    def __init__(self, window_name, window_width, window_height, i_process, keep_mouse_stay=False):
        self.window_name = window_name
        self.window_width = window_width
        self.window_height = window_height
        self.io_process = i_process
        self.io_process.set_window_size(window_width, window_height)
        self.delta_time = 0.0
        self.last_frame = 0.0
        self.fps_count = 0
        self._fps = 0
        self.NUM_SAMPLES = 10
        self.frameTimes = []
        self.currentFrame = 0
        self.prevTicks = 0
        self._frameTime = None
        self.keep_mouse_stay = keep_mouse_stay

        self.__init_window_context()
        self.__bind_io_process()

    def reshape(self, w, h):
        glViewport(0, 0, w, h)
        self.window_height = h
        self.window_width = w
        self.io_process.set_window_size(w, h)

    def __init_window_context(self):
        glutInit()
        glutInitContextVersion(3, 3)
        glutInitContextProfile(GLUT_CORE_PROFILE)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)
        glutInitWindowSize(self.window_width, self.window_height)
        glutCreateWindow(self.window_name)
        # glutSetCursor(GLUT_CURSOR_NONE)
        print(glGetString(GL_VERSION))

    def __bind_io_process(self):
        glutDisplayFunc(self.draw_function)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.io_process.keys_down)
        glutKeyboardUpFunc(self.io_process.keys_up)
        glutPassiveMotionFunc(self.io_process.mouse_move)
        glutMotionFunc(self.io_process.mouse_move)
        if self.keep_mouse_stay:
            glutEntryFunc(self.io_process.mouse_state)

    def set_render_function(self, render):
        self.render = render

    def draw_function(self):
        current_frame = glutGet(GLUT_ELAPSED_TIME)
        self.render()
        self.last_frame = glutGet(GLUT_ELAPSED_TIME)
        self.delta_time = (self.last_frame - current_frame)
        self.io_process.process_keys_by_frame(self.delta_time / 1000)
        if self.delta_time < 16:
            time.sleep((16 - self.delta_time) / 1000)
        self.calculate_fps()
        if self.fps_count == 100:
            self.fps_count = 0
            print('fps: %.2f' % self._fps)
        self.fps_count += 1
        glutSwapBuffers()
        glutPostRedisplay()

    def calculate_fps(self):
        current_ticks = glutGet(GLUT_ELAPSED_TIME)
        NUM_SAMPLES = self.NUM_SAMPLES
        self._frameTime = current_ticks - self.prevTicks
        self.currentFrame += 1
        if self.currentFrame <= NUM_SAMPLES:
            self.frameTimes.append(self._frameTime)
        else:
            self.frameTimes[(self.currentFrame) % NUM_SAMPLES] = self._frameTime
        if self.currentFrame < NUM_SAMPLES:
            count_ = self.currentFrame
        else:
            count_ = NUM_SAMPLES

        frame_time_average = 0
        for i in range(count_):
            frame_time_average += self.frameTimes[i]

        self.prevTicks = current_ticks

        frame_time_average /= count_
        if frame_time_average > 0:
            self._fps = 1000 / frame_time_average

        else:
            self._fps = 0.00

    def start_window_loop(self):
        glutMainLoop()
