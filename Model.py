from pyglet.gl import *
from CubeHandler import CubeHandler
import os


class Model:
    
    alpha_textures = 'leaves_oak','tall_grass'

    def load_textures(self):
        t = self.texture = {}; self.texture_dir = {}; dirs = ['textures']
        while dirs:
            dir = dirs.pop(0); textures = os.listdir(dir)
            for file in textures:
                if os.path.isdir(dir+'/'+file): dirs+=[dir+'/'+file]
                else:
                    n = file.split('.')[0]; self.texture_dir[n] = dir; image = pyglet.image.load(dir+'/'+file)
                    transparent = n in self.alpha_textures
                    texture = image.texture if transparent else image.get_mipmapped_texture()
                    self.texture[n] = pyglet.graphics.TextureGroup(texture)
                    if not transparent: glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST_MIPMAP_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)

        self.block = {}; self.ids = []; done = []
        items = sorted(self.texture_dir.items(),key=lambda i:i[0])
        for name,dir in items:
            n = name.split(' ')[0]
            if n in done: continue
            done+=[n]
            if dir.startswith('textures/blocks'):
                self.ids+=[n]
                if dir=='textures/blocks': self.block[n] = t[n],t[n],t[n],t[n],t[n],t[n]
                elif dir=='textures/blocks/tbs': self.block[n] = t[n+' s'],t[n+' s'],t[n+' b'],t[n+' t'],t[n+' s'],t[n+' s']
                elif dir=='textures/blocks/ts': self.block[n] = t[n+' s'],t[n+' s'],t[n+' t'],t[n+' t'],t[n+' s'],t[n+' s']

    def draw(self):
        glEnable(GL_ALPHA_TEST); self.opaque.draw(); glDisable(GL_ALPHA_TEST)
        glColorMask(GL_FALSE,GL_FALSE,GL_FALSE,GL_FALSE); self.transparent.draw()
        glColorMask(GL_TRUE,GL_TRUE,GL_TRUE,GL_TRUE); self.transparent.draw()

    def update(self,dt): pass

    def __init__(self):
        self.opaque = pyglet.graphics.Batch()
        self.transparent = pyglet.graphics.Batch()
        self.load_textures()
        self.cubes = CubeHandler(self.opaque,self.block,self.alpha_textures)


        for x in range(64):
            for z in range(64):
                self.cubes.add((x,-1,-z),'grass')
                for y in range(6): self.cubes.add((x,-2-y,-z),'dirt')
        for x in range(32):
            for z in range(32):
                self.cubes.add((x+16,0,-z-16),'sand')
        for x in range(16):
            for z in range(16):
                self.cubes.add((x+24,1,-z-24),'leaves_oak')
        for x in range(20):
            for z in range(20):
                self.cubes.add((x+22,1,-z-22),'log_oak')

        for cube in  self.cubes.cubes.values(): self.cubes.update_cube(cube)

