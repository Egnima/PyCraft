from pyglet.gl import *
from Window import Window


def main():
    window = Window(800,600,'Minecraft',True)
    # window.model.cubes.add((1, 1, 1), 'sand', True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST); glDepthFunc(GL_LEQUAL); glAlphaFunc(GL_GEQUAL,1)
    glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    pyglet.app.run()


if __name__ == '__main__':
    main()
