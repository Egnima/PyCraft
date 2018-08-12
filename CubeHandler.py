from pyglet.gl import *
from Cube import Cube
import Util


class CubeHandler:
    def __init__(self,batch,block,alpha_textures):
        self.batch,self.block,self.alpha_textures = batch,block,alpha_textures
        self.cubes = {}

    def hit_test(self,p,vec,dist=256):
        m = 8; x,y,z = p; dx,dy,dz = vec
        dx/=m; dy/=m; dz/=m; prev = None
        for i in range(dist*m):
            key = Util.normalize((x,y,z))
            if key in self.cubes: return key,prev
            prev = key
            x,y,z = x+dx,y+dy,z+dz
        return None,None

    def show(self,v,t): return self.batch.add(4,GL_QUADS,t,('v3f/static',v),('t2f/static',(0,0, 1,0, 1,1, 0,1)))

    def update_cube(self,cube):
        if not any(cube.shown.values()): return
        v = Util.cube_vertices(cube.p)
        f = 'left','right','bottom','top','back','front'
        for i in (0,1,2,3,4,5):
            if cube.shown[f[i]]:
                if not cube.faces[f[i]]: cube.faces[f[i]] = self.show(v[i],cube.t[i])
            elif cube.faces[f[i]]: cube.faces[f[i]].delete(); cube.faces[f[i]] = None

    def set_adj(self,cube,adj,state):
        x,y,z = cube.p; X,Y,Z = adj; d = X-x,Y-y,Z-z; f = 'left','right','bottom','top','back','front'
        for i in (0,1,2):
            if d[i]:
                j = i+i; a,b = [f[j+1],f[j]][::d[i]]; cube.shown[a] = state
                if not state and cube.faces[a]: cube.faces[a].delete(); cube.faces[a] = None

    def add(self,p,t,now=False):
        if p in self.cubes: return
        cube = self.cubes[p] = Cube(p,self.block[t],t in self.alpha_textures)

        for adj in Util.adjacent(*cube.p):
            if adj in self.cubes:
                if not cube.alpha or self.cubes[adj].alpha: self.set_adj(self.cubes[adj],cube.p,False)
                if self.cubes[adj].alpha: self.set_adj(cube,adj,True)
            else: self.set_adj(cube,adj,True)

        if now: self.update_cube(cube)

    def remove(self,p):
        if p not in self.cubes: return
        cube = self.cubes.pop(p)

        for side,face in cube.faces.items():
            if face: face.delete()

        for adj in Util.adjacent(*cube.p):
            if adj in self.cubes:
                self.set_adj(self.cubes[adj],cube.p,True)
                self.update_cube(self.cubes[adj])
