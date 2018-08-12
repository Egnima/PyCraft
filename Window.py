from pyglet.gl import *
from pyglet.window import key,mouse
from Model import Model
from Player import Player
from APIHandler import APIHandlerThread
import Util, queue


class Window(pyglet.window.Window):
    
    def set2d(self): glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluOrtho2D(0,self.width,0,self.height)
    def set3d(self): glLoadIdentity(); gluPerspective(65,self.width/self.height,0.1,320); glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    def on_resize(self,w,h): glViewport(0,0,w,h); self.load_reticle(w/2,h/2)
    def setLock(self,state): self.set_exclusive_mouse(state); self.mouseLock = state
    mouseLock = False; mouse_lock = property(lambda self:self.mouseLock,setLock)

    def __init__(self, *args):
        super().__init__(*args)
        pyglet.clock.schedule(self.update)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.model = Model()
        self.player = Player(self.model.cubes.cubes)
        self.mouse_lock = True
        self.fps = pyglet.clock.ClockDisplay()
        self.reticle = None
        self.block = 6

        # API Handler
        self.msg_queue = queue.Queue()
        self.api_handler_thread = APIHandlerThread(self.msg_queue)
        self.api_handler_thread.daemon = True
        self.api_handler_thread.start()


    def load_reticle(self,x,y,m=10):
        if self.reticle: self.reticle.delete()
        self.reticle = pyglet.graphics.vertex_list(4,('v2f',(x-m,y, x+m,y, x,y-m, x,y+m)),('c3f',(0,0,0, 0,0,0, 0,0,0, 0,0,0)))

    def update(self,dt):
        self.player.update(dt,self.keys)
        self.model.update(dt)
        # api handling

        try:
            last_api_call = self.msg_queue.get_nowait()
            x, y, z = [int(n) for n in last_api_call.split()]
            self.model.cubes.add((x, y, z), 'sand', True)

        except queue.Empty: # queue.Empty
            pass


    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_mouse_press(self,x,y,button,MOD):
        if button == mouse.LEFT:
            block = self.model.cubes.hit_test(self.player.pos,self.player.get_sight_vector())[0]
            if block: self.model.cubes.remove(block)
        elif button == mouse.RIGHT:
            block = self.model.cubes.hit_test(self.player.pos,self.player.get_sight_vector())[1]
            if block: self.model.cubes.add(block,self.model.ids[self.block],True)

    def on_key_press(self,KEY,MOD):
        if KEY == key.ESCAPE: self.dispatch_event('on_close')
        elif KEY == key.E: self.mouse_lock = not self.mouse_lock
        elif KEY == key.F: self.player.flying = not self.player.flying; self.player.dy = 0; self.player.noclip = True
        elif KEY == key.C: self.player.noclip = not self.player.noclip
        elif KEY == key.UP: self.block = (self.block-1)%len(self.model.ids)
        elif KEY == key.DOWN: self.block = (self.block+1)%len(self.model.ids)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.player.push()
        self.model.draw()

        block = self.model.cubes.hit_test(self.player.pos,self.player.get_sight_vector())[0]
        if block:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE); glColor3d(0,0,0)
            pyglet.graphics.draw(24,GL_QUADS,('v3f/static',Util.flatten(Util.cube_vertices(block,0.52))))
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL); glColor3d(1,1,1)

        glPopMatrix()
        self.set2d()
        self.fps.draw()
        self.reticle.draw(GL_LINES)
