# Source code released under gpl v3 licence, see COPYING file

from pyglet import window, clock, image
from pyglet.gl import *
from pyglet.window import key
from random import choice, randint

#Bonus
class Bonus:
  def __init__(self, id, type, color, coord):
    global grid
    self.id = id
    self.type = type
    self.x, self.y = coord
    self.color = color

#snake
class Snake:

  def __init__(self, id, type, keys, color, coord):
    global grid
    self.id = id
    self.type = type
    if type == 'drone':
      self.min_tail = 0
      self.max_tail = 0
    else:
      self.min_tail = 9
      self.max_tail = 299
    self.tail = self.min_tail
    self.x, self.y = coord
    self.dir = choice((0,1,2,3))
    self.points = 0
    self.reset = False
    self.up, self.right, self.down, self.left = keys
    self.color = color

  def select_direction(self, grid):
    global cpu_ai, cpu_avoid
    if self.type == 'drone':
      self.dir = choice(cpu_ai[snake.dir])
    elif self.type == 'cpu':
      avoid_length = choice((4,4,4,8,8))
      if self.dir == 0:
        avoid_y = snake.y + avoid_length
        if avoid_y > grid_height - 1 or grid.get_point(self.x,avoid_y) != (0, 0):
          self.dir = choice(cpu_avoid[0])
        else:
          self.dir = choice(cpu_ai[0])
      elif self.dir == 1:
        avoid_x = self.x + avoid_length
        if avoid_x > grid_width - 1 or grid.get_point(avoid_x,self.y) != (0, 0):
          self.dir = choice(cpu_avoid[1])
        else:
          self.dir = choice(cpu_ai[1])
      elif self.dir == 2:
        avoid_y = self.y - avoid_length
        if avoid_y < 0 or grid.get_point(self.x,avoid_y) != (0, 0):
          self.dir = choice(cpu_avoid[2])
        else:
          self.dir = choice(cpu_ai[2])
      elif self.dir == 3:
        avoid_x = self.x - avoid_length
        if avoid_x < 0 or grid.get_point(avoid_x,self.y) != (0, 0):
          self.dir = choice(cpu_avoid[3])
        else:
          self.dir = choice(cpu_ai[3])

  def move(self, grid):
    if self.dir == 0:
      if self.y < grid.height - 1: self.y+=1
      else:                        self.y=0
    elif self.dir == 1:
      if self.x < grid.width - 1:  self.x+=1
      else:                        self.x=0
    elif self.dir == 2:
      if self.y > 0:               self.y-=1
      else:                        self.y=grid.height - 1
    elif self.dir == 3:
      if self.x > 0:               self.x-=1
      else:                        self.x=grid.width - 1

  def check_collision(self, grid):
    global snakesArray
    state, age = grid.get_point(self.x,self.y)
    if state == 0:
      grid.set_point(self.x,self.y,(self.id,0))
    elif state >= 1 and state <= 20:
      if self.type == 'drone':
        grid.set_point(self.x,self.y,(self.id,0))
      else:
        self.reset = True
        self.tail = self.min_tail
        if self.id == self.id:
          if self.points >= 100:
            self.points -= 100
          else:
            self.points = 0  
        else:
            snake = snakesArray[state]
            snake.points += 100
    elif state >= 21 and state <= 40:
      grid.set_point(self.x,self.y,(self.id,0))
      if state == 21:
        self.points += 10
        self.tail += 10
        if self.tail > self.max_tail:
          self.tail = self.max_tail
      elif state == 22:
        self.points += 20
        self.tail -= 10
        if self.tail < self.min_tail:
          self.tail = self.min_tail
    elif state == 255:
      self.reset = True
      self.tail = self.min_tail
      if self.points >= 100:
        self.points -= 100
      else:
        self.points = 0
  

#Grid
class Grid:

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.data = [[(0,0)]*self.width for i in range(self.height)]
    
  def get_point(self, x, y):
    return self.data[y][x]
    
  def set_point(self, x, y, value):
    self.data[y][x] = value
    
  def reset_point(self, x, y):
    self.data[y][x] = (0,0)
    
  def random_point(self):
    bx = randint(0, self.width - 1)
    by = randint(0, self.height - 1)
    for y in range(self.height):
      by = (by + y) % self.height
      for x in range(self.width):
        bx = (bx + x) % self.width
        if self.data[by][bx] == (0, 0):
          return (bx, by)
    return Null, Null
    
  def show_bonus(self):
    global bonus
    b = choice(bonus)  
    if b != 0:
      bx, by = self.random_point()
      self.set_point(bx,by,(b,0))
      
      

def draw_grid():
  global snakesArray, grid, squares_verts, colors, bonus_timeout
  verts_coord = []
  verts_color = []
  for y in range(grid.height):
    for x in range(grid.width):
      state, age = grid.get_point(x, y)
      color_index = 0
      fade = 1
      if state >= 1 and state <= 20:
        snake = snakesArray[state - 1]
        if snake.reset or age > snake.tail:
          grid.reset_point(x,y)
        else:
          grid.set_point(x,y,(state, age + 1))
          color_index = snake.color
          fade -= 0.005 * age
          if fade < 0.4: fade= 0.4
      elif state >= 21 and state <= 40:
        if age > bonus_timeout:
          grid.reset_point(x,y)
        else:
          grid.set_point(x,y,(state, age + 1))
          if state == 21:
            color_index = 11
          else:
            color_index = 12
      elif state == 255:
        color_index = 10
      if color_index > 0:
        r, g, b = colors[color_index]
        r *= fade
        g *= fade
        b *= fade
        verts_color.extend([r,g,b,r,g,b,r,g,b,r,g,b])
        verts_coord.extend(squares_verts[y][x])
  verts_coord_size = len(verts_coord)
  verts_color_size = len(verts_color) 
  verts_coord_gl = (GLfloat * verts_coord_size)(*verts_coord)
  verts_color_gl = (GLfloat * verts_color_size)(*verts_color)
  glEnableClientState(GL_VERTEX_ARRAY);
  glEnableClientState(GL_COLOR_ARRAY);
  glColorPointer(3, GL_FLOAT, 0, verts_color_gl)
  glVertexPointer(2, GL_FLOAT, 0, verts_coord_gl);
  glDrawArrays(GL_QUADS, 0, verts_coord_size // 2)
  glDisableClientState(GL_VERTEX_ARRAY);
  glDisableClientState(GL_COLOR_ARRAY);

def draw_arena():
  global arena_verts
  glBegin(GL_LINES)
  glColor3f(0.5, 0.5, 0.5)
  for i in range(4):
    glVertex2f(*arena_verts[i])
    glVertex2f(*arena_verts[i + 1])
  glEnd()

def draw_header():
  global header_img, arena_border, arena_height
  glColor3f(1, 1, 1)
  header_img.blit(arena_border, arena_border + arena_border + arena_height)

def draw_background():
  global background_img, arena_border, arena_height
  glColor3f(1, 1, 1)
  background_img.blit(arena_border, arena_border)

screen_width = 740
screen_height = 550

arena_width = 720
arena_height = 480
arena_border = 10

#2,3,4,5,6,8,10,12,15,16,20,24,30,40
square_size = 8
grid_width = arena_width / square_size 
grid_height = arena_height / square_size

#8 = max 5400 squares

win = window.Window(visible=False,width=screen_width,height=screen_height)
win.set_visible()
header_img = image.load('header.png').texture
background_img = image.load('background.png').texture
fps_limit = 15
clock.set_fps_limit(fps_limit)
#keyboard = key.KeyStateHandler()

@win.event
def on_key_press(symbol, modifiers):
  global snakesArray
  for snake in snakesArray:
    if snake.type == 'human':
      if symbol == snake.up and snake.dir != 2:      snake.dir = 0
      elif symbol == snake.right and snake.dir != 3: snake.dir = 1
      elif symbol == snake.down and snake.dir != 0:  snake.dir = 2
      elif symbol == snake.left and snake.dir != 1:  snake.dir = 3
#win.on_key_press = on_key_press

arena_verts =  [
  (arena_border-1,arena_border-2),
  (arena_border+arena_width+1,arena_border-2),
  (arena_border+arena_width+1,arena_border+arena_height),
  (arena_border-1,arena_border+arena_height),
  (arena_border-1,arena_border-2)
]
square_verts = [
  (0,0),
  (square_size-1,0),
  (square_size-1,square_size-1),
  (0,square_size-1)
]

squares_verts = []
for y in range(grid_height):
  squares_verts.append([])
  for x in range(grid_width):
    squares_verts[y].append([])
    for vx,vy in square_verts:
      squares_verts[y][x].append(vx + arena_border + (x * square_size))
      squares_verts[y][x].append(vy + arena_border + (y * square_size))

#(id, age)
# id = 0          : empty
# id >= 1 e <=20  : snake (human, cpu, drone)
# id >=21 e <=40  : bonus
# id = 255        : wall
grid = Grid(grid_width, grid_height)

#set wall
for y in [10, 11, 48, 49]:
  for x in range(20, 69):
    grid.set_point(x,y,(255,0))

bonus = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,21,22)
cpu_ai = [
  (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,3),
  (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,0),
  (2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,1),
  (3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,2)
]
cpu_avoid = [
  (1,1,1,3),
  (2,2,2,0),
  (3,3,3,1),
  (0,0,0,2)
]
colors = [
  (0,0,0),
  (0,0,1),
  (1,1,0),
  (1,0,1),
  (0,1,1),
  (0.5,0.5,0),
  (0.5,0,0.5),
  (0,0.5,0.5),
  (1,1,1),
  (1,1,1),
  (1,1,1),
  (0,1,0),
  (1,0,0)
]

snakesArray = []
snakesArray.append(Snake(1,'cpu',(key.UP,key.RIGHT,key.DOWN,key.LEFT),1,grid.random_point()))
snakesArray.append(Snake(2,'cpu',(key.W,key.D,key.S,key.A),2,grid.random_point()))
snakesArray.append(Snake(3,'cpu',(key.R,key.G,key.F,key.D),3,grid.random_point()))
snakesArray.append(Snake(4,'cpu',(key.U,key.K,key.J,key.H),4,grid.random_point()))
snakesArray.append(Snake(5,'cpu',(0,0,0,0),5,grid.random_point()))
snakesArray.append(Snake(6,'cpu',(0,0,0,0),6,grid.random_point()))

#bonusArray = [] 
bonus_timeout = 74

for snake in snakesArray:
  grid.set_point(snake.x,snake.y,(snake.id,0))

while not win.has_exit:
  win.dispatch_events()
  dt = clock.tick()
  
  win.set_caption('Pytron v0.3 (fps: %s)' % (round(clock.get_fps())))

  glClear(GL_COLOR_BUFFER_BIT)
  glLoadIdentity()
  
  draw_header()
  draw_background()
  draw_arena()
  
  grid.show_bonus()
  
  for snake in snakesArray:
    snake.reset = False
    snake.select_direction(grid)
    snake.move(grid)
    snake.check_collision(grid)
  
  draw_grid()
  win.flip()

print "Punteggio"
for snake in snakesArray:
  print snake.id, ": ", snake.points
