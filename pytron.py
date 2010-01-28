from pyglet import window, clock, image
from pyglet.gl import *
from pyglet.window import key
from random import choice

def draw_grid():
  global square_verts, grid, colors, snakes, grid_width, grid_height, square_size
  glBegin(GL_QUADS)  
  for y in range(grid_height):
    for x in range(grid_width):
      state, age = grid[y][x]
      if state != 0:
        snake = snakes[state - 1]
        if snake['reset'] or age > snake['tail']:
          grid[y][x] = (0, 0)
        else:
          grid[y][x] = (state, age + 1)
          #snake['points'] += 1 
          #fade = 1 - (0.04 * age)
          #if fade < 0.2: fade= 0.2
          fade=1
          r, g, b = colors[state]
          glColor3f(r * fade, g * fade, b * fade)
          for vx,vy in square_verts:
            vx += 10 + (x * square_size)
            vy += 10 + (y * square_size)
            glVertex2f(vx, vy)
  glEnd()

def draw_arena():
  global arena_verts
  glBegin(GL_LINES)
  glColor3f(0.5, 0.5, 0.5)
  for i in range(4):
    glVertex2f(*arena_verts[i])
    glVertex2f(*arena_verts[i + 1])
  glEnd()

def draw_header():
  global header_img
  glColor3f(1, 1, 1)
  header_img.blit(10, 520)

screen_width = 720
screen_height = 570
square_size = 10
grid_width = 700 / square_size 
grid_height = 500 / square_size

win = window.Window(visible=False,width=screen_width,height=screen_height)
win.set_visible()
header_img = image.load('header.png').texture
fps_limit = 15
clock.set_fps_limit(fps_limit)
keyboard = key.KeyStateHandler()

arena_verts =  [(9,9),(711,9),(711,511),(9,511),(9,9)]
square_verts = [(0,0),(square_size-1,0),(square_size-1,square_size-1),(0,square_size-1)]

grid = [[(0,0)]*grid_width for i in range(grid_height)]

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
  (  0,   0,   0),
  (  1,   0,   0),
  (  0,   1,   0),
  (  0,   0,   1),
  (  1,   1,   0),
  (  1,   0,   1),
  (  0,   1,   1),
  (  1, 0.5, 0.5),
  (0.5, 0.5,   1),
  (1,     1,   1),
  (1,     1,   1),
  (1,     1,   1),
  (1,     1,   1)        
]

snakes = [
  {'id':  1,'type': 'human','tail':199,'x': 2,'y': 5,'dir': 1,'points': 0,'reset': False,'up': key.UP,'right': key.RIGHT,'down': key.DOWN,'left': key.LEFT},
  {'id':  2,'type': 'cpu','tail':199,'x': 4,'y': 5,'dir': 1,'points': 0,'reset': False,'up': key.W ,'right': key.D    ,'down': key.S   ,'left': key.A},
  {'id':  3,'type': 'off','tail':99,'x': 6,'y': 5,'dir': 1,'points': 0,'reset': False,'up': key.T ,'right': key.H    ,'down': key.G   ,'left': key.F},
  {'id':  4,'type': 'off','tail':99,'x': 8,'y': 5,'dir': 1,'points': 0,'reset': False,'up': key.I ,'right': key.L    ,'down': key.K   ,'left': key.J},
  {'id':  5,'type': 'off','tail':99,'x':10,'y': 5,'dir': 1,'points': 0,'reset': False,'up': 0,'right': 0,'down': 0,'left': 0},
  {'id':  6,'type': 'off','tail':99,'x':12,'y': 5,'dir': 1,'points': 0,'reset': False,'up': 0,'right': 0,'down': 0,'left': 0},
  {'id':  7,'type': 'off','tail':99,'x': 3,'y': 7,'dir': 1,'points': 0,'reset': False,'up': 0,'right': 0,'down': 0,'left': 0},
  {'id':  8,'type': 'off','tail':99,'x': 5,'y': 7,'dir': 1,'points': 0,'reset': False,'up': 0,'right': 0,'down': 0,'left': 0},
  {'id':  9,'type': 'off','tail':99,'x': 7,'y': 7,'dir': 1,'points': 0,'reset': False,'up': 0,'right': 0,'down': 0,'left': 0},
  {'id': 10,'type': 'off','tail':99,'x': 9,'y': 7,'dir': 1,'points': 0,'reset': False,'up': 0,'right': 0,'down': 0,'left': 0},
  {'id': 11,'type': 'off','tail':99,'x':11,'y': 7,'dir': 1,'points': 0,'reset': False,'up': 0,'right': 0,'down': 0,'left': 0},
  {'id': 12,'type': 'off','tail':99,'x':13,'y': 7,'dir': 1,'points': 0,'reset': False,'up': 0,'right': 0,'down': 0,'left': 0}
]

for snake in snakes:
  if snake['type'] != 'off': grid[snake['y']][snake['x']] = (snake['id'], 0)

while not win.has_exit:
  win.dispatch_events()
  win.push_handlers(keyboard)
  
  dt = clock.tick()
  
  #win.set_caption('Pytron v0.2 - 1: %d, 2: %d, 3: %d, 4: %d - (fps: %s)' % (snakes[0]['points'], snakes[1]['points'], snakes[2]['points'], snakes[3]['points'], round(clock.get_fps())))
  win.set_caption('Pytron v0.2 (fps: %s)' % (round(clock.get_fps())))

  glClear(GL_COLOR_BUFFER_BIT)
  glLoadIdentity()
  
  draw_header()
  draw_arena()
  
  for snake in snakes:
    snake['reset'] = False
    if snake['type'] == 'off':
      continue
    elif snake['type'] == 'drone':
      snake['dir'] = choice(cpu_ai[snake['dir']])
    elif snake['type'] == 'cpu':
      avoid_length = choice((2,4,6,8,10))
      if snake['dir'] == 0:
        avoid_y = snake['y'] + avoid_length
        if avoid_y > grid_height - 1 or grid[avoid_y][snake['x']] != (0, 0): snake['dir'] = choice(cpu_avoid[0])
        else:                                                                snake['dir'] = choice(cpu_ai[0])
      elif snake['dir'] == 1:
        avoid_x = snake['x'] + avoid_length
        if avoid_x > grid_width - 1 or grid[snake['y']][avoid_x] != (0, 0):  snake['dir'] = choice(cpu_avoid[1])
        else:                                                                snake['dir'] = choice(cpu_ai[1])
      elif snake['dir'] == 2:
        avoid_y = snake['y'] - avoid_length
        if avoid_y < 0 or grid[avoid_y][snake['x']] != (0, 0):               snake['dir'] = choice(cpu_avoid[2])
        else:                                                                snake['dir'] = choice(cpu_ai[2])
      elif snake['dir'] == 3:
        avoid_x = snake['x'] - avoid_length
        if avoid_x < 0 or grid[snake['y']][avoid_x] != (0, 0):               snake['dir'] = choice(cpu_avoid[3])
        else:                                                                snake['dir'] = choice(cpu_ai[3])
    else:
      if keyboard[snake['up']] and snake['dir'] != 2:      snake['dir'] = 0
      elif keyboard[snake['right']] and snake['dir'] != 3: snake['dir'] = 1
      elif keyboard[snake['down']] and snake['dir'] != 0:  snake['dir'] = 2
      elif keyboard[snake['left']] and snake['dir'] != 1:  snake['dir'] = 3
      
    if snake['dir'] == 0:
      if snake['y'] < grid_height - 1:
        snake['y']+=1
      else:
        snake['y']=0
        #snake['dir'] = 2
        #snake['reset'] = True
    elif snake['dir'] == 1:
      if snake['x'] < grid_width - 1:
        snake['x']+=1
      else:
        snake['x']=0
        #snake['dir'] = 3
        #snake['reset'] = True
    elif snake['dir'] == 2:
      if snake['y'] > 0:
        snake['y']-=1
      else:
        snake['y']=grid_height - 1
        #snake['dir'] = 0
        #snake['reset'] = True
    elif snake['dir'] == 3:
      if snake['x'] > 0:
        snake['x']-=1
      else:
        snake['x']=grid_width - 1
        #snake['dir'] = 1
        #snake['reset'] = True
    
    if not snake['reset']:
      state, age = grid[snake['y']][snake['x']]
      #if state == 0 or (snake['type'] == 'drone' and state == snake['id']):
      if state == 0 or snake['type'] == 'drone':
        grid[snake['y']][snake['x']] = (snake['id'],0)
        snake['points'] += 1
      else:
        snake['reset'] = True
#        if state == snake['id']:
#          if snake['points'] >= 100:
#            snake['points'] -= 100
#          else:
#            snake['points'] = 0  
#        else:
#          snakes[state-1]['points'] += 100  

  draw_grid()

  win.flip()

print "Punteggio\n"
for snake in snakes:
  print snake['id'], ": ", snake['points']
   