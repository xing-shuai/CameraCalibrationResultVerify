from OpenGL.GL import *
import numpy as np
from GEngine.shader import ShaderProgram
from GEngine.model import Model, ModelFromExport, generate_grid_mesh
import glm
from GEngine.camera3D import Camera3D
from GEngine.input_process import InputProcess
from GEngine.window import GWindow

SCR_WIDTH = 800
SCR_HEIGHT = 800

camera = Camera3D(glm.vec3(0.0, 5.0, 30.0))
window = GWindow(b"demo", SCR_WIDTH, SCR_HEIGHT, InputProcess(camera, SCR_WIDTH, SCR_HEIGHT), keep_mouse_stay=True)

light_color = (1.0, 1.0, 1.0)
hand_color = (0.7, 0.7, 0.7)
light_position = (-10, 6, 10)

grid_position = [
    glm.vec3(1.0, 1.0, 1.0),
    [glm.radians(90), glm.vec3(1.0, 0.0, 0.0)],
    glm.vec3(0, 0.0, 0)
]


def init():
    grid_vertices, grid_mesh = generate_grid_mesh(-10, 10, step=0.5)

    cube_vertices = np.array([-0.5, -0.5, -0.5, 0.0, 0.0,
                              0.5, -0.5, -0.5, 1.0, 0.0,
                              0.5, 0.5, -0.5, 1.0, 1.0,
                              0.5, 0.5, -0.5, 1.0, 1.0,
                              -0.5, 0.5, -0.5, 0.0, 1.0,
                              -0.5, -0.5, -0.5, 0.0, 0.0,

                              -0.5, -0.5, 0.5, 0.0, 0.0,
                              0.5, -0.5, 0.5, 1.0, 0.0,
                              0.5, 0.5, 0.5, 1.0, 1.0,
                              0.5, 0.5, 0.5, 1.0, 1.0,
                              -0.5, 0.5, 0.5, 0.0, 1.0,
                              -0.5, -0.5, 0.5, 0.0, 0.0,

                              -0.5, 0.5, 0.5, 1.0, 0.0,
                              -0.5, 0.5, -0.5, 1.0, 1.0,
                              -0.5, -0.5, -0.5, 0.0, 1.0,
                              -0.5, -0.5, -0.5, 0.0, 1.0,
                              -0.5, -0.5, 0.5, 0.0, 0.0,
                              -0.5, 0.5, 0.5, 1.0, 0.0,

                              0.5, 0.5, 0.5, 1.0, 0.0,
                              0.5, 0.5, -0.5, 1.0, 1.0,
                              0.5, -0.5, -0.5, 0.0, 1.0,
                              0.5, -0.5, -0.5, 0.0, 1.0,
                              0.5, -0.5, 0.5, 0.0, 0.0,
                              0.5, 0.5, 0.5, 1.0, 0.0,

                              -0.5, -0.5, -0.5, 0.0, 1.0,
                              0.5, -0.5, -0.5, 1.0, 1.0,
                              0.5, -0.5, 0.5, 1.0, 0.0,
                              0.5, -0.5, 0.5, 1.0, 0.0,
                              -0.5, -0.5, 0.5, 0.0, 0.0,
                              -0.5, -0.5, -0.5, 0.0, 1.0,

                              -0.5, 0.5, -0.5, 0.0, 1.0,
                              0.5, 0.5, -0.5, 1.0, 1.0,
                              0.5, 0.5, 0.5, 1.0, 0.0,
                              0.5, 0.5, 0.5, 1.0, 0.0,
                              -0.5, 0.5, 0.5, 0.0, 0.0,
                              -0.5, 0.5, -0.5, 0.0, 1.0
                              ], dtype=np.float32)

    global shader_program
    shader_program = ShaderProgram("resources/shaders/shader.vs", "resources/shaders/shader.fg")
    shader_program.init()

    global grid_model
    grid_model = Model([grid_vertices], indices=[grid_mesh])

    global hand_shader_program
    hand_shader_program = ShaderProgram("resources/shaders/hand_shader.vs", "resources/shaders/hand_shader.fg")
    hand_shader_program.init()

    global hand_model
    hand_model = ModelFromExport("/home/shuai/Pictures/calibration/hand.obj", vertex_format="VN")

    global light_shader_program
    light_shader_program = ShaderProgram("resources/shaders/light_shader.vs", "resources/shaders/light_shader.fg")
    light_shader_program.init()

    global light_cube
    light_cube = Model([cube_vertices])

    glEnable(GL_DEPTH_TEST)


def render():
    glClearColor(0, 0, 0, 0.0)
    glClearDepth(1.0)
    glPointSize(5)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    projection = glm.perspective(glm.radians(camera.zoom), SCR_WIDTH * 1.0 / SCR_HEIGHT, 0.1, 1000)
    view = camera.get_view_matrix()

    #
    # draw grid
    shader_program.use()
    shader_program.set_matrix("projection", glm.value_ptr(projection))
    shader_program.set_matrix("view", glm.value_ptr(view))

    m = glm.mat4(1.0)
    m = glm.translate(m, grid_position[2])
    m = glm.rotate(m, glm.radians(90), grid_position[1][1])
    m = glm.scale(m, glm.vec3(5))
    shader_program.set_matrix("model", glm.value_ptr(m))

    shader_program.un_use()
    grid_model.draw(shader_program, draw_type=GL_LINES)

    #
    # draw hand
    hand_shader_program.use()
    hand_shader_program.set_matrix("projection", glm.value_ptr(projection))
    hand_shader_program.set_matrix("view", glm.value_ptr(view))
    m = glm.mat4(1.0)
    m = glm.translate(m, glm.vec3(0, 6, 0))
    m = glm.rotate(m, glm.radians(-90), glm.vec3(1, 0, 0))
    # m = glm.rotate(m, glm.radians(model_position[1][1][0]), model_position[1][1][1])
    # m = glm.rotate(m, glm.radians(model_position[1][2][0]), model_position[1][2][1])
    m = glm.scale(m, glm.vec3(0.02, 0.02, 0.02))
    hand_shader_program.set_matrix("model", glm.value_ptr(m))
    hand_shader_program.set_uniform_3f("lightColor", light_color)
    hand_shader_program.set_uniform_3f("lightPos", light_position)
    hand_shader_program.set_uniform_3f("handColor", hand_color)
    hand_shader_program.un_use()

    hand_model.draw(hand_shader_program, draw_type=GL_TRIANGLES)

    #
    # draw light cube
    light_shader_program.use()
    light_shader_program.set_matrix("projection", glm.value_ptr(projection))
    light_shader_program.set_matrix("view", glm.value_ptr(view))
    m = glm.mat4(1.0)
    m = glm.translate(m, glm.vec3(light_position[0], light_position[1], light_position[2]))
    m = glm.scale(m, glm.vec3(1, 1, 1))
    light_shader_program.set_matrix("model", glm.value_ptr(m))
    light_shader_program.set_uniform_3f("lightColor", light_color)
    light_shader_program.un_use()

    light_cube.draw(light_shader_program, draw_type=GL_TRIANGLES)


def main():
    init()
    window.set_render_function(render)
    window.start_window_loop()


if __name__ == "__main__":
    main()
