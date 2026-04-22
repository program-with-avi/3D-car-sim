from ursina import *
import math

app = Ursina()

ground = Entity(model='plane', texture='grass', scale=(1000,1,1000), collider='box')

light = DirectionalLight()
light.direction = (1, -1, 1)
scene.brightness = 0.1

#for i in range(10):
#    Entity(model='cube', color=color.gray, scale=(10, 0.1, 10), 
#           position=(0, 0.05, i * 10))
car = Entity(model='Koenigsegg2.obj', scale=(5, 5, 5), position=(0, 1, 0))

velocity = Vec3(0,0,0)
acceleration = 1.5
friction = 0.85
steering = 60
angle = 0
max_speed = 120

speed_text = Text(text='0 KPH', position=(-0.85, 0.45), scale=2, color=color.white)
wall = Entity(model='cube', color=color.orange, scale=(1, 2, 1000), 
              position=(500, 5, 0), collider='box')
wall2 = Entity(model='cube',color=color.orange,scale=(1,5,1000),position=(-500,1,0),collider='box'  )

wall3 = Entity(model='cube',color=color.orange,scale=(1000,5,1),position=(1,1,500),collider='box'  )

wall4 = Entity(model='cube',color=color.orange,scale=(1000,5,1),position=(1,1,-500),collider='box'  )

car.collider = 'box'

def update():
    global angle, velocity
    
    speed_text.text = f"{int(velocity.length() * 3.6)} KPH"
    
    target_z_rotation = 0
    if held_keys['a'] and (held_keys['w'] or held_keys['s']):
        angle -= steering * time.dt
        target_z_rotation = 5
    if held_keys['d'] and (held_keys['w'] or held_keys['s']):
        angle += steering * time.dt
        target_z_rotation = -5
    
    car.rotation_y = angle
    is_moving_inp = False

    if held_keys['w']:
        velocity += car.forward * acceleration * time.dt * 100
        is_moving_inp = True
    elif held_keys['s']:
        velocity -= car.forward * (acceleration * 10) * time.dt * 100
        is_moving_inp = True
    
    current_speed = velocity.length()
    if current_speed > max_speed:
        velocity = velocity.normalized() * max_speed
        current_speed = max_speed
    
    if is_moving_inp and current_speed > 0.1:
        grip = 0.15
        velocity = lerp(velocity, car.forward * current_speed, grip)
    
    car.rotation_z = lerp(car.rotation_z, target_z_rotation, time.dt * 5)
    
    current_friction = friction if is_moving_inp else 0.98
    actual_friction = math.pow(current_friction, time.dt * 70)
    velocity *= actual_friction
    
    new_position = car.position + velocity * time.dt
    
    if distance(new_position, car.position) > 0:
        car.position = new_position
    
    target_cam_pos = car.position + (car.back * 70) + (0, 100, 0)
    camera.position = lerp(camera.position, target_cam_pos, time.dt * 3)
    camera.look_at(car)
    camera.rotation_z = 0

app.run()
