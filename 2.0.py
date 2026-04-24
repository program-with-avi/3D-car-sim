from ursina import *
import math
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



app = Ursina()
world =  Entity(enabled=False)

ground = Entity(model='plane', texture='grass',texture_scale=(2,2), scale=(10000,1,10000), collider='box', parent=world)

light = DirectionalLight(parent=world)
light.direction = (1, -1, 1)
scene.brightness = 0.1
camera.clip_plane_far = 100000
Sky(texture='sky_sunset', parent=world)
Entity(model='cube', color=color.cyan, scale=(100,500,100), position=(-100,0,10), parent=world)
car = Entity(model=resource_path('Koenigsegg6.obj'), scale=(2, 2, 2), position=(0, 1, 0),parent=world,collider='box')
velocity = Vec3(0,0,0)
gear = 1
gear_max = 7
acceleration = 0.1
friction = 0.85
steering = 60
angle = 0
max_speed = 400
worlddef = None
enb = True
menu = Entity(parent=camera.ui)
title = Text(text='WORLD SELECTOR', origin=(0,0), y=0.3, scale=3, parent=menu)
def load_world(texture_name: str):
    '''Load world ground texture'''
    global worlddef
    ground.texture = texture_name
    menu.enabled = False
    world.enabled = True
    worlddef = texture_name
    #mouse.locked = True # Lock mouse for driving
btn_grass = Button(text='Grass World', color=color.green, scale=(0.3, 0.1), y=0, parent=menu, text_color=color.black)
btn_grass.on_click = lambda: load_world('grass')

btn_sand = Button(text='Desert World', color=color.yellow, scale=(0.3, 0.1), y=-0.15, parent=menu, text_color=color.black)
btn_sand.on_click = lambda: load_world('sand') # 'shore' looks like sand
def update():
    global angle, velocity, worlddef, enb, speed_text, gear, max_speed, gear_max
    if world.enabled and enb:
        speed_text = Text(text='0 KPH', position=(-0.85, 0.45), scale=2, color=color.white)
        enb= False
    if held_keys['esc']:
        menu.enabled = True
        world.enabled=False
    if not menu.enabled and worlddef == 'grass':
        if world.enabled:speed_text.text = f"{int(velocity.length())} KPH"
        if   held_keys['1']: gear = 1 ; max_speed = 50
        elif held_keys['2']: gear = 2 ; max_speed = 100
        elif held_keys['3']: gear = 3 ; max_speed = 150
        elif held_keys['4']: gear = 4 ; max_speed = 240
        elif held_keys['5']: gear = 5 ; max_speed = 300
        elif held_keys['6']: gear = 6 ; max_speed = 350
        elif held_keys['7']: gear = 7 ; max_speed = 400
        #if held_keys['e']:
        #    max_speed = min(max_speed + 50, gear_max * 50)
        #elif held_keys['q']:
        #    max_speed = max(max_speed - 50, gear_max * -50)
        target_z_rotation = 0
        if held_keys['a'] and velocity.length() > 0.1:
            angle -= steering * time.dt
            target_z_rotation = 5
        if held_keys['d'] and velocity.length() > 0.1:
            angle += steering * time.dt
            target_z_rotation = -5
    
        car.rotation_y = angle
        is_moving_inp = False

        if held_keys['w']:
            velocity += car.forward * acceleration * time.dt * 100
            is_moving_inp = True
        elif held_keys['s']:
            reverse_speed = 400 
            velocity -= car.forward * (acceleration*reverse_speed) * time.dt * 100
            is_moving_inp = True
    
    
        current_speed = velocity.length()
        if current_speed > max_speed:
            velocity = velocity.normalized() * max_speed
            current_speed = max_speed
    
        if is_moving_inp and current_speed > 0.1:
            grip = 0.15
            velocity = lerp(velocity, car.forward * current_speed, grip)
    
        car.rotation_z = lerp(car.rotation_z, target_z_rotation, time.dt * 5)
    
    # Apply friction only when the kart is moving
        if velocity.length() > 0.1:
            actual_friction = math.pow(friction, time.dt * 30)
            velocity *= actual_friction
    
        new_position = car.position + velocity * time.dt
    
        if distance(new_position, car.position) > 0:
            car.position = new_position
    
        target_cam_pos = car.position + (car.back * 70) + (0, 40, 0)
        camera.position = lerp(camera.position, target_cam_pos, time.dt * 3)
        camera.look_at(car)
        camera.rotation_z = 0
        if current_speed>300:
            speed_text.color = color.red
        else:
            speed_text.color = color.white
        
    elif (not menu.enabled) and worlddef == 'sand':
        if world.enabled:speed_text.text = f"{int(velocity.length())} KPH"
        if   held_keys['1']: gear = 1 ; max_speed = 50
        elif held_keys['2']: gear = 2 ; max_speed = 100
        elif held_keys['3']: gear = 3 ; max_speed = 150
        elif held_keys['4']: gear = 4 ; max_speed = 240
        elif held_keys['5']: gear = 5 ; max_speed = 300
        elif held_keys['6']: gear = 6 ; max_speed = 350
        elif held_keys['7']: gear = 7 ; max_speed = 400
    
        target_z_rotation = 0
        if held_keys['a'] and velocity.length() > 0.1:
            angle -= steering * time.dt
            target_z_rotation = 5
        if held_keys['d'] and velocity.length() > 0.1:
            angle += steering * time.dt
            target_z_rotation = -5
    
        car.rotation_y = angle
        is_moving_inp = False

        if held_keys['w']:
            velocity += car.forward * acceleration * time.dt * 100
            is_moving_inp = True
        elif held_keys['s']:
            reverse_speed = 400 
            velocity -= car.forward * (acceleration*reverse_speed) * time.dt * 100
            is_moving_inp = True
    
    
        current_speed = velocity.length()
        if current_speed > max_speed:
            velocity = velocity.normalized() * max_speed
            current_speed = max_speed
    
        if is_moving_inp and current_speed > 0.1:
            grip = 0.15
            velocity = lerp(velocity, car.forward * current_speed, grip)
    
        car.rotation_z = lerp(car.rotation_z, target_z_rotation, time.dt * 5)
    
    # Apply friction only when the kart is moving
        if velocity.length() > 0.1:
            actual_friction = math.pow(friction, time.dt * 30)
            velocity *= actual_friction
    
        new_position = car.position + velocity * time.dt
    
        if distance(new_position, car.position) > 0:
            car.position = new_position
    
        target_cam_pos = car.position + (car.back * 70) + (0, 40, 0)
        camera.position = lerp(camera.position, target_cam_pos, time.dt * 3)
        camera.look_at(car)
        camera.rotation_z = 0
        if current_speed>300:
            speed_text.color = color.red
        else:
            speed_text.color = color.white


app.run()