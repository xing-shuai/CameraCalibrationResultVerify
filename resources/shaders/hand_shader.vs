#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNom;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
out vec3 Normal;
out vec3 FragPos;
void main()
{
    //gl_Position = projection * view  * model * vec4(aPos, 1.0f);
    vec4 ss = projection * view  *model* vec4(aPos, 1.0f);
	gl_Position = vec4(ss.x,ss.y,ss.z-1,ss.w);
	//gl_Position = projection * view  *model* vec4(aPos, 1.0f);

	FragPos = vec3(model * vec4(aPos, 1.0));
    Normal = mat3(transpose(inverse(model))) * aNom;
}