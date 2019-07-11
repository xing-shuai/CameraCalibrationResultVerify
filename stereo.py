from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from GEngine.shader import ShaderProgram
from GEngine.model import Model, ModelFromExport, generate_grid_mesh
import glm
from GEngine.camera3D import Camera3D
from GEngine.input_process import InputProcess, keys
from GEngine.window import GWindow
import cv2

SCR_WIDTH = int(1920 * 0.5) * 2
SCR_HEIGHT = int(1080 * 0.5)

camera = Camera3D(glm.vec3(0.0, 5.0, 30.0))
window = GWindow(b"demo", SCR_WIDTH, SCR_HEIGHT, InputProcess(camera, SCR_WIDTH, SCR_HEIGHT), keep_mouse_stay=False)

image_size = (1920, 1080)
light_color = (1.0, 1.0, 1.0)
hand_color = (0.9, 0.9, 0.9)
light_position = (-1000, -700, 1000)

model_position = [
    glm.vec3(1.0, 1.0, 1.0),
    [[0, glm.vec3(1.0, 0.0, 0.0)], [0, glm.vec3(0.0, 1.0, 0.0)], [0, glm.vec3(0.0, 0.0, 1.0)]],
    glm.vec3(500, 500.0, 0.0)
]

image_path = "/media/shuai/SHUAI_AHUT/calibration_same_camera/"

left_camera_intrinsic = np.loadtxt(image_path + "left/Intrinsic.txt")

right_camera_intrinsic = np.loadtxt(image_path + "/right/Intrinsic.txt")

# left_camera_extrinsic = np.array([[0.072070, 0.997290, 0.014783, 96.257969],
#                                   [0.914850, -0.072002, 0.397322, -1869.315674],
#                                   [0.397309, -0.015111, -0.917560, 4461.560955],
#                                   [0.000000, 0.000000, 0.000000, 1.000000]])

# right_camera_extrinsic = np.array([[-0.064207, 0.995479, 0.069995, 43.308457],
#                                    [0.941980, 0.083614, -0.325089, 1523.690302],
#                                    [-0.329472, 0.045061, -0.943090, 4255.094080],
#                                    [0.000000, 0.000000, 0.000000, 1.000000]])

stereo_left_index = 14
stereo_right_index = 17

left_camera_extrinsic = np.loadtxt(image_path + "left/ExtrinsicCameraPars.txt")

right_camera_extrinsic = np.loadtxt(image_path + "right/ExtrinsicCameraPars.txt")


def init():
    grid_vertices, grid_mesh = generate_grid_mesh(-5, 5, step=0.5)

    cube_vertices = np.array([0, 0, 0, 0.0, 0.0,
                              1, 0, 0, 1.0, 0.0,
                              1, 1, 0, 1.0, 1.0,
                              1, 1, 0, 1.0, 1.0,
                              0, 1, 0, 0.0, 1.0,
                              0, 0, 0, 0.0, 0.0,

                              0, 0, 1, 0.0, 0.0,
                              1, 0, 1, 1.0, 0.0,
                              1, 1, 1, 1.0, 1.0,
                              1, 1, 1, 1.0, 1.0,
                              0, 1, 1, 0.0, 1.0,
                              0, 0, 1, 0.0, 0.0,

                              0, 1, 1, 1.0, 0.0,
                              0, 1, 0, 1.0, 1.0,
                              0, 0, 0, 0.0, 1.0,
                              0, 0, 0, 0.0, 1.0,
                              0, 0, 1, 0.0, 0.0,
                              0, 1, 1, 1.0, 0.0,

                              1, 1, 1, 1.0, 0.0,
                              1, 1, 0, 1.0, 1.0,
                              1, 0, 0, 0.0, 1.0,
                              1, 0, 0, 0.0, 1.0,
                              1, 0, 1, 0.0, 0.0,
                              1, 1, 1, 1.0, 0.0,

                              0, 0, 0, 0.0, 1.0,
                              1, 0, 0, 1.0, 1.0,
                              1, 0, 1, 1.0, 0.0,
                              1, 0, 1, 1.0, 0.0,
                              0, 0, 1, 0.0, 0.0,
                              0, 0, 0, 0.0, 1.0,

                              0, 1, 0, 0.0, 1.0,
                              1, 1, 0, 1.0, 1.0,
                              1, 1, 1, 1.0, 0.0,
                              1, 1, 1, 1.0, 0.0,
                              0, 1, 1, 0.0, 0.0,
                              0, 1, 0, 0.0, 1.0
                              ], dtype=np.float32)

    bg = np.array([-1, 1, 0, 0, 1, 1, 1, 0, 1, 1, -1, -1, 0, 0, 0, -1, -1, 0, 0, 0, 1, -1, 0, 1, 0, 1, 1, 0, 1, 1],
                  dtype=np.float32)

    global hand_model
    hand_model = ModelFromExport("resources/models/hand.obj", vertex_format="VN")

    global cube_model
    cube_model = Model([cube_vertices],
                       texture_path=["resources/images/awesomeface.png"])

    global cube_shader_program
    cube_shader_program = ShaderProgram("resources/shaders/hand_shader.vs", "resources/shaders/hand_shader.fg")
    cube_shader_program.init()

    global shader_program
    shader_program = ShaderProgram("resources/shaders/shader.vs", "resources/shaders/shader.fg")
    shader_program.init()

    global grid_model
    grid_model = Model([grid_vertices], indices=[grid_mesh])

    global bg_model_left
    bg_model_left = Model([bg], texture_path=[image_path + "left/left" + str(stereo_left_index + 1) + ".png"])

    global bg_model_right
    bg_model_right = Model([bg], texture_path=[image_path + "right/right" + str(stereo_right_index + 1) + ".png"])

    global bg_shader_program
    bg_shader_program = ShaderProgram("resources/shaders/bg_shader.vs", "resources/shaders/bg_shader.fg")
    bg_shader_program.init()

    glEnable(GL_DEPTH_TEST)


def build_projection_matrix(camera_intrinsic_matrix, width, height):
    d_near = 0.1  # Near clipping distance
    d_far = 1000.0  # Far clipping distance

    # Camera parameters
    fx = camera_intrinsic_matrix[0, 0]  # Focal length in x axis
    fy = camera_intrinsic_matrix[1, 1]  # Focal length in y axis (usually the same?)
    cx = camera_intrinsic_matrix[0, 2]  # Camera primary point x
    cy = camera_intrinsic_matrix[1, 2]  # Camera primary point y

    projection_matrix = np.array([[fx / cx, 0.0, 0.0, 0.0],
                                  [0.0, fy / cy, 0.0, 0.0],
                                  [0, 0, -(d_far + d_near) / (d_far - d_near), -1.0],
                                  [0.0, 0.0, -2.0 * d_far * d_near / (d_far - d_near), 0.0]], dtype=np.float32)

    # projection_matrix = np.array([[2.0 * f_x / image_width, 0.0, 0.0, 0.0],
    #                               [0.0, -2.0 * f_y / image_height, 0.0, 0.0],
    #                               [0, 0,
    #                                -(d_far + d_near) / (d_far - d_near), -1.0],
    #                               [0.0, 0.0, -2.0 * d_far * d_near / (d_far - d_near), 0.0]], dtype=np.float32)

    return projection_matrix


def build_model_view_matrix(camera_extrinsic_matrix):
    r, t = camera_extrinsic_matrix[3:], camera_extrinsic_matrix[:3]
    R = cv2.Rodrigues(r)[0]

    inverse = np.array([[1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1]])

    u, _, v = np.linalg.svd(R)
    R = u @ v

    rotation = inverse @ R

    translation = inverse @ t

    # rotation = inverse @ camera_extrinsic_matrix[:3, :3]
    #
    # translation = inverse @ camera_extrinsic_matrix[:3, 3]
    #
    model_view_matrix = np.identity(4, dtype=np.float32)
    model_view_matrix[:3, :3] = rotation
    model_view_matrix[:3, 3] = translation

    model_view_matrix = model_view_matrix.T
    return model_view_matrix
    #
    # INVERSE_MATRIX = np.array([[1.0, 1.0, 1.0, 1.0],
    #                            [-1.0, -1.0, -1.0, -1.0],
    #                            [-1.0, -1.0, -1.0, -1.0],
    #                            [1.0, 1.0, 1.0, 1.0]])

    # view_matrix = np.array([[rmtx[0][0], rmtx[0][1], rmtx[0][2], camera_extrinsic_matrix[1][0]],
    #                         [rmtx[1][0], rmtx[1][1], rmtx[1][2], camera_extrinsic_matrix[1][1]],
    #                         [rmtx[2][0], rmtx[2][1], rmtx[2][2], camera_extrinsic_matrix[1][2]],
    #                         [0.0, 0.0, 0.0, 1.0]])[:3, :]
    #
    # # view_matrix = np.array([[0.072070, 0.997290, 0.014783, 96.257969],
    # #                         [0.914850, -0.072002, 0.397322, -1869.315674],
    # #                         [0.397309, -0.015111, -0.917560, 4461.560955],
    # #                         [0.0, 0.0, 0.0, 1.0]])[:3, :]
    #
    # R = view_matrix[:, :3]
    # U, S, V = np.linalg.svd(R)
    # R = U @ V
    # # R[0, :] = -R[0, :]  # change sign of x-axis
    #
    # # view_matrix = view_matrix * INVERSE_MATRIX
    # #
    # # view_matrix = np.transpose(view_matrix)
    # t = view_matrix[:, 3]
    #
    # # setup 4*4 model view matrixew
    # M = np.eye(4)
    # M[:3, :3] = inverse @ R
    # M[:3, 3] = inverse @ t
    # return M.T


def render_background_image(bg_model):
    glDisable(GL_DEPTH_TEST)
    bg_model.draw(bg_shader_program, draw_type=GL_TRIANGLES)
    glEnable(GL_DEPTH_TEST)


def render_side_view(camera_intrinsic, camera_extrinsic, width, height, stereo_index,
                     hand_color=glm.vec4(0.8, 0.8, 0.8, 0)):
    ##
    # draw grid
    ##
    shader_program.use()
    shader_program.set_matrix("projection", build_projection_matrix(camera_intrinsic, width, height))
    shader_program.set_matrix("view", build_model_view_matrix(camera_extrinsic[stereo_index]))

    m = glm.mat4(1.0)
    m = glm.scale(m, glm.vec3(70))
    shader_program.set_matrix("model", glm.value_ptr(m))
    shader_program.un_use()

    grid_model.draw(shader_program, draw_type=GL_LINES)

    ##
    # draw cube
    ##
    cube_shader_program.use()
    cube_shader_program.set_matrix("projection", build_projection_matrix(camera_intrinsic, width, height))
    cube_shader_program.set_matrix("view", build_model_view_matrix(camera_extrinsic[stereo_index]))
    m = glm.mat4(1.0)
    m = glm.translate(m, model_position[2])
    m = glm.rotate(m, glm.radians(model_position[1][0][0]), model_position[1][0][1])
    m = glm.rotate(m, glm.radians(model_position[1][1][0]), model_position[1][1][1])
    m = glm.rotate(m, glm.radians(model_position[1][2][0]), model_position[1][2][1])
    m = glm.scale(m, model_position[0])
    cube_shader_program.set_matrix("model", glm.value_ptr(m))
    cube_shader_program.set_uniform_3f("handColor", hand_color)
    cube_shader_program.set_uniform_3f("lightColor", light_color)
    cube_shader_program.set_uniform_3f("lightPos", light_position)
    cube_shader_program.un_use()

    hand_model.draw(cube_shader_program, draw_type=GL_TRIANGLES)


def render_first_person_view():
    ##
    # draw grid
    ##
    projection = glm.perspective(glm.radians(camera.zoom), SCR_WIDTH * 1.0 / SCR_HEIGHT, 0.1, 1000)
    view = camera.get_view_matrix()
    shader_program.use()
    shader_program.set_matrix("projection", glm.value_ptr(projection))

    shader_program.set_matrix("view", glm.value_ptr(view))

    m = glm.mat4(1.0)
    m = glm.scale(m, glm.vec3(10))
    shader_program.set_matrix("model", glm.value_ptr(m))
    shader_program.un_use()

    grid_model.draw(shader_program, draw_type=GL_LINES)

    ##
    # draw cube
    ##
    cube_shader_program.use()
    cube_shader_program.set_matrix("projection", glm.value_ptr(projection))
    cube_shader_program.set_matrix("view", glm.value_ptr(view))
    m = glm.mat4(1.0)
    m = glm.translate(m, model_position[2])
    m = glm.rotate(m, glm.radians(model_position[1][0][0]), model_position[1][0][1])
    m = glm.rotate(m, glm.radians(model_position[1][1][0]), model_position[1][1][1])
    m = glm.rotate(m, glm.radians(model_position[1][2][0]), model_position[1][2][1])
    m = glm.scale(m, model_position[0])
    cube_shader_program.set_matrix("model", glm.value_ptr(m))
    cube_shader_program.un_use()

    hand_model.draw(cube_shader_program, draw_type=GL_TRIANGLES)


def render():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClearDepth(1.0)
    glPointSize(5)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glViewport(0, 0, int(SCR_WIDTH / 2), SCR_HEIGHT)
    render_background_image(bg_model_left)
    render_side_view(left_camera_intrinsic, left_camera_extrinsic, SCR_WIDTH / 2, SCR_HEIGHT, stereo_left_index)

    glViewport(int(SCR_WIDTH / 2), 0, int(SCR_WIDTH / 2), SCR_HEIGHT)
    render_background_image(bg_model_right)
    render_side_view(right_camera_intrinsic, right_camera_extrinsic, SCR_WIDTH / 2, SCR_HEIGHT, stereo_right_index)

    # glViewport(int(SCR_WIDTH / 2), 0, 200, 200)
    # render_first_person_view()


def process_keyboard(delta_time):
    if keys["escape"]:
        glutLeaveMainLoop()

    global camera
    if keys["c"]:
        camera.process_keyboard(delta_time)
        return

    global model_position

    if keys["w"]:
        if keys["g"]:
            model_position[2] -= glm.vec3(delta_time * 200, 0, 0)

        if keys["r"]:
            model_position[1][1][0] -= delta_time * 100

        if keys["z"]:
            model_position[0] += glm.vec3(delta_time * 1, delta_time * 1, delta_time * 1)

    if keys["s"]:
        if keys["g"]:
            model_position[2] += glm.vec3(delta_time * 200, 0, 0)

        if keys["r"]:
            model_position[1][1][0] += delta_time * 100

        if keys["z"]:
            model_position[0] -= glm.vec3(delta_time * 1, delta_time * 1, delta_time * 1)

    if keys["a"]:
        if keys["g"]:
            model_position[2] += glm.vec3(0, -delta_time * 200, 0)

        if keys["r"]:
            model_position[1][0][0] -= delta_time * 100

    if keys["d"]:
        if keys["g"]:
            model_position[2] += glm.vec3(0, delta_time * 200, 0)

        if keys["r"]:
            model_position[1][0][0] += delta_time * 100

    if keys["j"]:
        if keys["g"]:
            model_position[2] += glm.vec3(0, 0, delta_time * 200)

        if keys["r"]:
            model_position[1][2][0] += delta_time * 100

    if keys["l"]:
        if keys["g"]:
            model_position[2] += glm.vec3(0, 0, -delta_time * 200)

        if keys["r"]:
            model_position[1][2][0] -= delta_time * 100


def main():
    init()
    window.set_render_function(render)
    window.io_process.process_keys_by_frame = process_keyboard
    window.start_window_loop()


if __name__ == "__main__":
    main()
