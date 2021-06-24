import pygame as pg
import random
import glob
import sys
 

#배경/전역변수 설정
white = (255, 255, 255)
orange = (255, 127, 0)
pad_height = 700
pad_width = int(pad_height * 0.8)
img_ratio = pad_height / 1000

# 물체 움직임 함수
def obj_disp(obj,x,y):
    global gamepad
    gamepad.blit(obj,[x,y])

# 게임 구동 / 이미지 지정
def init_game():
    global gamepad, clock
    global back_1, back_2, plane, plane_left, plane_right, shoot, exp_img
    global ufo_img, ufo_atk_img, ufo_boss_img, fire, fire_boss
    global plane_size, plane_lr_size, shoot_size, fire_size, explosion_size, ufo_size, ufo_boss_size

   # 구동 기본 세팅
    pg.init()
    pg.display.set_caption('Shooting Universe') 
    gamepad = pg.display.set_mode((pad_width, pad_height))
    clock = pg.time.Clock() 

   # 배경화면(back_1, back_2)    
    back_1 = pg.image.load('./image/back.png')
    pg.transform.rotate(back_1, 180)
    back_1 = pg.transform.scale(back_1, (pad_width, pad_height)) 
    back_2 = pg.image.load('./image/back2.png')
    back_2 = pg.transform.scale(back_2, (pad_width, pad_height)) 

   # 비행기(plane, plane_left, plane_right)
    plane = pg.image.load('./image/plane.png')   
    plane_size = [int(plane.get_rect().size[0]/6*img_ratio),int(plane.get_rect().size[1]/6*img_ratio)]
    plane = pg.transform.scale(plane, plane_size)

    plane_left = pg.image.load('./image/plane_left.png')
    plane_lr_size = [int(plane_left.get_rect().size[0]/6*img_ratio),int(plane_left.get_rect().size[1]/6*img_ratio)]
    plane_left = pg.transform.scale(plane_left, plane_lr_size)
    plane_right = pg.transform.scale(pg.image.load('./image/plane_right.png'), plane_lr_size)

   # 미사일(shoot)
    shoot = pg.image.load('./image/shoot.png')
    shoot_size = [int(shoot.get_rect().size[0]/30*img_ratio),int(shoot.get_rect().size[1]/20*img_ratio)]
    shoot = pg.transform.scale(shoot, shoot_size)

   # ufo(ufo, ufo_atk, ufo_boss)
    ufo_img = glob.glob('./image/ufoimg/*.png')
    ufo_atk_img = glob.glob('./image/ufo_atk_img/*.png')
    ufo_boss_img = glob.glob('./image/ufo_boss_img/*.png') 
    ufo_size = [int(pg.image.load(ufo_img[0]).get_rect().size[0]/2*img_ratio)
                ,int(pg.image.load(ufo_img[0]).get_rect().size[1]/2*img_ratio)]
    ufo_boss_size = [int(ufo_size[0]*1.5), int(ufo_size[1]*1.5)]

  
    

   # 적 공격 발사체(fireball)
    fire = pg.image.load('./image/fireball.png')
    fire_size = [int(fire.get_rect().size[0]/30*img_ratio),int(fire.get_rect().size[1]/30*img_ratio)]
    fire_boss = pg.transform.scale(fire, [fire_size[0]*2, fire_size[1]*2])
    fire = pg.transform.scale(fire, fire_size)

   # 폭발 연속 이미지(exp_img)
    exp_img = glob.glob('./image/expimg/*.png')

# 게임 시작 화면
def start_game():
    global back_1, gamepad, clock

    start = False

    start_wait = 0 
    while not start:
        gamepad.fill(white)
        obj_disp(back_1, 0, 0)

        
        start_font = pg.font.SysFont('malgungothic', 30, True, True)
        press_font = pg.font.SysFont('malgungothic', 15, True, False)
        start_text = start_font.render('SHOOTING Universe', True, orange)
        press_text = press_font.render('start to press ''A'' button', True, white)
        start_point = [pad_width/2 - start_text.get_rect().size[0]/2, 
                            pad_height/2 - start_text.get_rect().size[1]/2]
        press_point = [pad_width/2 - press_text.get_rect().size[0]/2, 
                            start_point[1] + 50]   
        if start_wait % 60 <= 30 :
            pg.Surface.set_alpha(press_text, 255)
            start_wait += 1
        elif start_wait % 60 > 30 :
            pg.Surface.set_alpha(press_text, 0)
            start_wait += 1
        gamepad.blit(press_text, press_point)
        gamepad.blit(start_text, start_point)
        if start_wait == 60:
            start_wait = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    start = True

        pg.display.flip()
        clock.tick(60)


# 게임 실행 함수
def run_game():
    global gamepad, clock
    global back_1, back_2, plane, plane_left, plane_right, shoot, exp_img
    global ufo_img, ufo_atk_img, ufo_boss_img, fire, fire_boss
    global plane_size, plane_lr_size, shoot_size, fire_size, explosion_size, ufo_size, ufo_boss_size

  # 초기 설정
   ## 기본 초기값  
    back_1_y = 0
    back_2_y = -pad_height
    text_update = 0 # gameover text 표기 초기값
    isgameover = 0 # gameover flag
    isatk = 0 # 적이 공격 받았을 때 flag
    point = 0 # 점수 초기값
    exp_t = 0 # 폭발 초기값
    exp_t_repeat = 3 # 폭발 반복 횟수
    gameover_wait = 600 # continue 시작시간(600부터 빼기) / gameover 표시시간(0부터 시작)
    continue_wait = 0 # continue flag
    continue_time = 10 # continue 시간
    plane_dead = 180 # 비행기 무적 시간
    ufo_boss_count = 0 # 고민중
    ufo_t = [] # UFO 이미지 순서
    ufo_boss_t = [] # UFO 대장 이미지 순서
    ufo_boss_fire_t = []
    

   ## 초기 속도/시간 변수
    frame_t = 0 #프레임 수/sec
    shoot_t = 0 #공격 텀 초기값 
    ufo_make_t = 0 #UFO 발생텀 초기값
    ufo_speed = 2 # UFO 이동속도
    fire_speed = 3 # UFO 공격속도
    shoot_speed = 20 # 공격속도
    stage_play_time = 0 #게임 플레이 시간
    fire_boss_count = 0

   ## 비행기 초기 좌표
    plane_x = pad_width * 0.5 - plane_size[0]/2
    plane_y = pad_height * 0.95 - plane_size[1]
    plane_lr_x = plane_x + plane_size[0]/2 - plane_lr_size[0]/2
    plane_lr_y = plane_y + plane_size[1] - plane_lr_size[1]

   ## 비행물체 좌표 리스트
    shoot_xy = []
    ufo_xyz = []
    ufo_boss_xyz = []
    fire_boss_xyz = []
    fire_left_xy = []
    fire_down_xy = []
    fire_right_xy = []
    explosion_enemy_xyz = []

   ## 방향키 변수 초기 설정
    up_change = 0
    down_change = 0
    left_change = 0
    right_change = 0
    left_move = 0
    right_move = 0

  # 게임중 루프    
    crashed = False
    while not crashed:     

       # 게임 기본 표출 화면(배경)
        gamepad.fill(white)
        obj_disp(back_1, 0, back_1_y)
        obj_disp(back_2, 0,back_2_y)
             
    
       # 이벤트 타입별 설정 - 비행기 움직임/미사일 발사
        for event in pg.event.get():

            # 창 닫을 때
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            #비행기 방향키 뗐을 때
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    up_change = 0
                elif event.key == pg.K_DOWN:
                    down_change = 0
                elif event.key == pg.K_RIGHT:
                    right_change = 0
                    right_move = 0
                elif event.key == pg.K_LEFT:
                    left_change = 0
                    left_move = 0
                elif event.key == pg.K_SPACE:
                    shoot_t = shoot_t % shoot_speed

        # 미사일 발사 
        if shoot_t < shoot_speed:
            shoot_t += 1
        else:
            pass

        if shoot_t >= shoot_speed:
            shoot_t = shoot_speed
        elif shoot_t < shoot_speed:
            shoot_t += 1

        key_press = pg.key.get_pressed()
        if key_press[pg.K_SPACE]:
            if isgameover == 0:
                if shoot_t >= shoot_speed : ## 변경 방식 여부 확인
                    shoot_xy.append([plane_x + (plane_size[0]-shoot_size[0])/2, plane_y])
                    shoot_t = 0
            if isgameover == 1:
                shoot_t = 0

        # 방향키
        if key_press[pg.K_UP]:
            if isgameover == 0:
                up_change = -5
            if isgameover == 1:
                up_change = 0
        if key_press[pg.K_DOWN]:
            if isgameover == 0:
                down_change = 5
            if isgameover == 1:
                down_change = 0
        if key_press[pg.K_RIGHT]:
            if isgameover == 0:
                right_change = 5
                right_move = 1
            if isgameover == 1:
                right_change = 0
        if key_press[pg.K_LEFT]:
            if isgameover == 0:
                left_change = -5
                left_move = 1
            if isgameover == 1:
                left_change = 0

       # 배경 이동       
        if back_1_y == pad_height:
            back_1_y = -pad_height
        if back_2_y == pad_height:
            back_2_y = -pad_height
        back_1_y += 1 #배경 속도_1
        back_2_y += 1 #배경 속도_2
   

       # 최종 비행기 이동 좌표       
        plane_y += up_change
        plane_y += down_change
        plane_x += left_change
        plane_x += right_change
        plane_lr_y += up_change
        plane_lr_y += down_change
        plane_lr_x += left_change
        plane_lr_x += right_change

       # 비행기 이동 범위 지정
        if plane_x <= 0:
            plane_x = 0
            plane_lr_x = plane_size[0]/2 - plane_lr_size[0]/2 
        elif (plane_x + plane_size[0]) // pad_width == 1:
            plane_x = pad_width - plane_size[0]
            plane_lr_x = pad_width - (plane_size[0]/2 + plane_lr_size[0]/2) 
        if (plane_y + plane_size[1]) >= pad_height * 0.98:
            plane_y = pad_height * 0.98 - plane_size[1]
            plane_lr_y = pad_height * 0.98 - plane_size[1]
        elif plane_y <= pad_height * 0.3:
            plane_y = pad_height * 0.3
            plane_lr_y = pad_height * 0.3

       # UFO 추가
        #일반 UFO
        if ufo_make_t >= 30:
            ufo_make = [1]
            ufo_make_percent = 3
            ufo_dead_point = 2
            for i in range(ufo_make_percent):
                ufo_make.append(0)
            random.shuffle(ufo_make)
            if ufo_make[0] == 1:
                ufo_make_point = random.randint(1, int((pad_width-ufo_size[0]-10)*2/ufo_size[0]))*ufo_size[0]/2
                ufo_xyz.append([ufo_make_point, 0-ufo_size[1], 0, ufo_dead_point, 0])
                ufo_t.append([0]) 
                # x, y, 발사체 생성, 목숨, 번쩍임효과
                ufo_make_t = 0
            else:
                ufo_make_t = 0
        else:
            ufo_make_t += 1

        # UFO 대장
        if stage_play_time % 20 == 19 and frame_t == 0:
            ufo_boss_dead_point = 20
            ufo_make_point_1 = random.randrange(int(pad_width*0.1), int(pad_width*0.9-ufo_size[0]),20)
            #ufo_make_point_2 = random.randrange(int(pad_width*0.5), int(pad_width*0.9-ufo_size[0]),20)
            ufo_boss_xyz.append([ufo_make_point_1, 0-ufo_size[1], ufo_boss_dead_point, 0])# x, y, 목숨, 번쩍임효과
            ufo_boss_fire_t.append([200])
            ufo_boss_t.append([0])


       # UFO 이동/발사체 생성
        ufo_xyz_remove = ufo_xyz.remove
        ufo_t_remove = ufo_t.remove
        if len(ufo_xyz) != 0 :
            for i, xyz in enumerate(ufo_xyz):
                ufo_xyz[i][1] += ufo_speed
                if xyz[4] > 0:
                    ufo_xyz[i][4] -= 1
                if xyz[4] == 0:
                    ufo_xyz[i][4] = 0
                if xyz[1] >= pad_height + ufo_size[1]:
                    ufo_xyz_remove(xyz)
                    ufo_t_remove(ufo_t[i])
                    
                    
               # 발사체 생성
                if xyz[2] == 0:
                    ufo_xyz[i][2] = random.randint(int(pad_height*0.1), int(pad_height*0.7))
                else:
                    if xyz[1] >= xyz[2] and xyz[1] < xyz[2]+ufo_speed:
                        fire_left_xy.append([xyz[0], xyz[1]+ufo_size[1]/2])
                        fire_down_xy.append([xyz[0]+ufo_size[0]/2 - fire_size[0]/2, xyz[1]+ufo_size[1]/2])
                        fire_right_xy.append([xyz[0]+ufo_size[0]-fire_size[0], xyz[1]+ufo_size[1]/2]) 

                                    
       # UFO 대장 이동/발사체 생성
        fire_boss_xyz_append = fire_boss_xyz.append
        if len(ufo_boss_xyz) != 0 :
            for i, xyz in enumerate(ufo_boss_xyz):
                if xyz[1] <= pad_height * 0.3:
                    ufo_boss_xyz[i][1] += ufo_speed
                if xyz[3] > 0:
                    ufo_boss_xyz[i][3] -= 1
                if xyz[3] == 0:
                    ufo_boss_xyz[i][3] = 0
                if xyz[1] > pad_height * 0.3 and xyz[1] < pad_height:
                    xyz[1] = pad_height * 0.3 
                    #발사체 생성
                    if ufo_boss_fire_t[i][0] % 20 == 0 and ufo_boss_fire_t[i][0] >= 120:
                        fire_boss_xyz_append([xyz[0]+ufo_boss_size[0]/2 - fire_size[0], 
                                        xyz[1]+ufo_boss_size[1]/2, 0])
                        fire_boss_xyz_append([xyz[0]+ufo_boss_size[0]/2 - fire_size[0], 
                                        xyz[1]+ufo_boss_size[1]/2, 1])
                        fire_boss_xyz_append([xyz[0]+ufo_boss_size[0]/2 - fire_size[0], 
                                        xyz[1]+ufo_boss_size[1]/2, 2])
                        fire_boss_xyz_append([xyz[0]+ufo_boss_size[0]/2 - fire_size[0], 
                                        xyz[1]+ufo_boss_size[1]/2, 3])
                        fire_boss_xyz_append([xyz[0]+ufo_boss_size[0]/2 - fire_size[0], 
                                        xyz[1]+ufo_boss_size[1]/2, 4])
                        #fire_boss_xyz.append([xyz[0]+ufo_boss_size[0]/2 - fire_size[0], xyz[1],2])
                        # x, y, 발사체 방향, 발사 UFO 순서...(수정 필요)
                        ufo_boss_fire_t[i][0] -= 1
                    elif (ufo_boss_fire_t[i][0] % 20 != 0 and ufo_boss_fire_t[i][0] >= 120
                        or ufo_boss_fire_t[i][0] < 120 and ufo_boss_fire_t[i][0] > 0):
                        ufo_boss_fire_t[i][0] -= 1
                    elif ufo_boss_fire_t[i][0] == 0:
                        ufo_boss_fire_t[i][0] = 200
      

       # UFO 폭발 시 효과
        scale_transform = pg.transform.scale
        image_load = pg.image.load
        ufo_exp = 0
        ufo_boss_exp = 1         
        if len(explosion_enemy_xyz) != 0:
            for i, xyz in enumerate(explosion_enemy_xyz):
                if xyz[2] == ufo_exp:
                    if xyz[3] <= 18:
                        exp_img_x = int(image_load(exp_img[xyz[3]]).get_rect().size[0]/2*img_ratio)
                        exp_img_y = int(image_load(exp_img[xyz[3]]).get_rect().size[1]/2*img_ratio)
                        obj_disp(scale_transform(image_load(exp_img[xyz[3]]), [exp_img_x, exp_img_y]), 
                            xyz[0] + ufo_size[0]/2 - exp_img_x/2 , xyz[1] + ufo_size[0]/2 - exp_img_y/2)
                        explosion_enemy_xyz[i][3] += 1
                    else:
                        explosion_enemy_xyz.remove(xyz)
                
                if xyz[2] == ufo_boss_exp:
                    if xyz[3] <= 18:
                        exp_img_boss_x = int(image_load(exp_img[xyz[3]]).get_rect().size[0]/1*img_ratio)
                        exp_img_boss_y = int(image_load(exp_img[xyz[3]]).get_rect().size[1]/1*img_ratio)
                        obj_disp(scale_transform(image_load(exp_img[xyz[3]]), [exp_img_boss_x, exp_img_boss_y]), 
                            xyz[0] + int(ufo_size[0]*1.5)/2 - exp_img_boss_x/2 , 
                            xyz[1] + int(ufo_size[0]*1.5)/2 - exp_img_boss_y/2)
                        explosion_enemy_xyz[i][3] += 1
                    else:
                        explosion_enemy_xyz.remove(xyz)

       #발사체 화면 표출
        # 왼쪽 이동 UFO발사체 화면 표출
        fire_left_xy_remove = fire_left_xy.remove
        if len(fire_left_xy) != 0 :
            for i, xy in enumerate(fire_left_xy):
                xy[0] -= fire_speed/2
                xy[1] += fire_speed*0.866
                fire_left_xy[i][0] = xy[0]
                fire_left_xy[i][1] = xy[1]
                if xy[1] >= pad_height + fire_size[1] or xy[0] <= -fire_size[0] or xy[0] >= pad_width + fire_size[0]:
                    fire_left_xy_remove(xy)
        
        if len(fire_left_xy) != 0:
            for x, y in fire_left_xy:
                try:
                    obj_disp(fire, x, y)
                except:
                    pass            

        # 아래 이동 UFO발사체 화면 표출
        fire_down_xy_remove = fire_down_xy.remove
        if len(fire_down_xy) != 0 :
            for i, xy in enumerate(fire_down_xy):
                xy[1] += fire_speed
                fire_down_xy[i][1] = xy[1]
                if xy[1] >= pad_height + fire_size[1]:
                    fire_down_xy_remove(xy)

        if len(fire_down_xy) != 0:
            for x, y in fire_down_xy:
                try:
                    obj_disp(fire, x, y)
                except:
                    pass             

        # 오른쪽 이동 UFO발사체 화면 표출
        fire_right_xy_remove = fire_right_xy.remove 
        if len(fire_right_xy) != 0 :
            for i, xy in enumerate(fire_right_xy):
                xy[0] += fire_speed/2
                xy[1] += fire_speed*0.866
                fire_right_xy[i][0] = xy[0]
                fire_right_xy[i][1] = xy[1]
                if xy[1] >= pad_height + fire_size[1] or xy[0] <= -fire_size[0] or xy[0] >= pad_width + fire_size[0]:
                   fire_right_xy_remove(xy) 
           
        if len(fire_right_xy) != 0:
            for x, y in fire_right_xy:
                try:
                    obj_disp(fire, x, y)
                except:
                    pass   

       # UFO 대장 발사체 화면
        fire_boss_speed = 3
        fire_boss_remove = fire_boss_xyz.remove
        if len(fire_boss_xyz) != 0 :
            for i, xyz in enumerate(fire_boss_xyz):
                if xyz[2] == 0:
                    fire_boss_xyz[i][0] -= fire_boss_speed*0.707
                    fire_boss_xyz[i][1] += fire_boss_speed*0.707
                    if (xyz[1] >= pad_height + fire_size[1]*2 or xyz[0] <= -fire_size[0]*2 or 
                        xyz[0] >= pad_width + fire_size[0]*2):
                        fire_boss_remove(xyz)
                if xyz[2] == 1:
                    fire_boss_xyz[i][0] -= fire_boss_speed*0.5
                    fire_boss_xyz[i][1] += fire_boss_speed*0.866
                    if (xyz[1] >= pad_height + fire_size[1]*2 or xyz[0] <= -fire_size[0]*2 or 
                        xyz[0] >= pad_width + fire_size[0]*2):
                        fire_boss_remove(xyz)
                if xyz[2] == 2:
                    fire_boss_xyz[i][1] += fire_boss_speed
                    if xyz[1] >= pad_height + fire_size[1]*2:
                        fire_boss_remove(xyz)       
                if xyz[2] == 3:
                    fire_boss_xyz[i][0] += fire_boss_speed*0.5
                    fire_boss_xyz[i][1] += fire_boss_speed*0.866
                    if (xyz[1] >= pad_height + fire_size[1]*2 or xyz[0] <= -fire_size[0]*2 or 
                        xyz[0] >= pad_width + fire_size[0]*2):
                        fire_boss_remove(xyz)
                if xyz[2] == 4:
                    fire_boss_xyz[i][0] += fire_boss_speed*0.707
                    fire_boss_xyz[i][1] += fire_boss_speed*0.707
                    if (xyz[1] >= pad_height + fire_size[1]*2 or xyz[0] <= -fire_size[0]*2 or 
                        xyz[0] >= pad_width + fire_size[0]*2):
                        fire_boss_remove(xyz)
                    

        if len(fire_boss_xyz) != 0:
            for x, y, z in fire_boss_xyz:
                try:
                    obj_disp(fire_boss, x, y)
                except:
                    pass     

       # UFO 화면 표출
        #scale_transform = pg.transform.scale
        #image_load = pg.image.load    
        if len(ufo_xyz) != 0:
            for i, xyz in enumerate(ufo_xyz):
                if xyz[4] > 0:
                    if ufo_t[i][0] <= 14:
                        obj_disp(scale_transform(image_load(ufo_atk_img[int(ufo_t[i][0])]), 
                        [ufo_size[0], ufo_size[1]]), 
                        xyz[0], xyz[1])
                        ufo_t[i][0] += 1/5
                    else:
                        ufo_t[i][0] = 0
                        obj_disp(scale_transform(image_load(ufo_atk_img[0]), 
                        [ufo_size[0], ufo_size[1]]), 
                        xyz[0], xyz[1])
                if xyz[4] == 0 :
                    if ufo_t[i][0] <= 14:
                        obj_disp(scale_transform(image_load(ufo_img[int(ufo_t[i][0])]), 
                        [ufo_size[0], ufo_size[1]]), 
                        xyz[0], xyz[1])
                        ufo_t[i][0] += 1/5
                    else:
                        ufo_t[i][0] = 0
                        obj_disp(scale_transform(image_load(ufo_img[0]), 
                        [ufo_size[0], ufo_size[1]]), 
                        xyz[0], xyz[1])

        
       # UFO 대장 화면 표출    
        #scale_transform = pg.transform.scale
        #image_load = pg.image.load
        if len(ufo_boss_xyz) != 0:
            for i, xyz in enumerate(ufo_boss_xyz):
                if xyz[3] > 0:
                    if ufo_boss_t[i][0] <= 14:
                        obj_disp(scale_transform(image_load(ufo_atk_img[int(ufo_boss_t[i][0])]), 
                        [ufo_boss_size[0], ufo_boss_size[1]]), 
                        xyz[0], xyz[1])
                        ufo_boss_t[i][0] += 1/5
                    else:
                        ufo_boss_t[i][0] = 0
                        obj_disp(scale_transform(image_load(ufo_atk_img[0]), 
                        [ufo_boss_size[0], ufo_boss_size[1]]), 
                        xyz[0], xyz[1])
                if xyz[3] == 0 :
                    if ufo_boss_t[i][0] <= 14:
                        obj_disp(scale_transform(image_load(ufo_boss_img[int(ufo_boss_t[i][0])]), 
                        [ufo_boss_size[0], ufo_boss_size[1]]), 
                        xyz[0], xyz[1])
                        ufo_boss_t[i][0] += 1/5
                    else:
                        ufo_boss_t[i][0] = 0
                        obj_disp(scale_transform(image_load(ufo_boss_img[0]), 
                        [ufo_boss_size[0], ufo_boss_size[1]]), 
                        xyz[0], xyz[1])

        
       # UFO 격추
        shoot_xy_remove = shoot_xy.remove
        explosion_enemy_xyz_append = explosion_enemy_xyz.append
        #ufo_xyz_remove = ufo_xyz.remove
        #ufo_t_remove = ufo_t.remove
        if len(ufo_xyz) != 0 :
            for i, xyz in enumerate(ufo_xyz):
                if len(shoot_xy) != 0:
                    for j, xy in enumerate(shoot_xy):
                        if (xyz[0] <= xy[0] + shoot_size[0]
                            and xyz[0] + ufo_size[0] >= xy[0]
                            and xyz[1] + ufo_size[1]*0.7 >= xy[1]) :
                            xyz[3] -= 1
                            ufo_xyz[i][3] = xyz[3]
                            if xyz[3] > 0:
                                shoot_xy_remove(xy)
                                ufo_xyz[i][4] = 3
                            elif xyz[3] == 0:
                                explosion_enemy_xyz_append([xyz[0], xyz[1], ufo_exp, 0])
                                ufo_xyz_remove(xyz)
                                ufo_t_remove(ufo_t[i])
                                shoot_xy_remove(xy)
                                point += 10

  
       # UFO 대장 격추
        #shoot_xy_remove = shoot_xy.remove
        #explosion_enemy_xyz_append = explosion_enemy_xyz.append
        ufo_boss_xyz_remove = ufo_boss_xyz.remove
        ufo_boss_t_remove = ufo_boss_t.remove
        ufo_boss_fire_t_remove = ufo_boss_fire_t.remove
        if len(ufo_boss_xyz) != 0 :
            for i, xyz in enumerate(ufo_boss_xyz):
                if len(shoot_xy) != 0:
                    for j, xy in enumerate(shoot_xy):
                        if (xyz[0] + int(ufo_boss_size[0]*0.2) <= xy[0] + shoot_size[0]
                            and xyz[0] + int(ufo_boss_size[0]*0.8) >= xy[0]
                            and xyz[1] + int(ufo_boss_size[1]*0.6) >= xy[1]) :
                            ufo_boss_xyz[i][2] -= 1
                            shoot_xy.remove(xy)
                            ufo_boss_xyz[i][3] = 3
                if xyz[2] <= 0:
                    explosion_enemy_xyz_append([xyz[0], xyz[1], ufo_boss_exp, 0])
                    ufo_boss_xyz_remove(xyz)
                    ufo_boss_t_remove(ufo_boss_t[i])
                    ufo_boss_fire_t_remove(ufo_boss_fire_t[i])
                    point += 100

       # 미사일 움직임 표출
        # 발사했을 때
        #shoot_xy_remove = shoot_xy.remove        
        if len(shoot_xy) != 0:
            for i, xy in enumerate(shoot_xy):
                xy[1] -= 10
                shoot_xy[i][1] = xy[1]
                # 화면 끝까지 이동했을 때 
                if xy[1] <= 0:
                    shoot_xy_remove(xy)                  

           
        if len(shoot_xy) != 0:
            for x, y in shoot_xy:
                try:
                    obj_disp(shoot, x, y)
                except:
                    pass

       # 비행기 화면 표출
        if plane_dead > 0 :
            blink_speed = 20
            plane_dead -= 1
            if plane_dead % blink_speed <= blink_speed/2 :
                    pg.Surface.set_alpha(plane, 255)
                    pg.Surface.set_alpha(plane_left, 255)
                    pg.Surface.set_alpha(plane_right, 255)
            elif plane_dead % blink_speed > blink_speed/2 :
                    pg.Surface.set_alpha(plane, 0)
                    pg.Surface.set_alpha(plane_left, 0)
                    pg.Surface.set_alpha(plane_right, 0)

            if left_move == 0 and right_move == 0:
                obj_disp(plane, plane_x, plane_y)

            elif left_move == 1 and right_move == 0:
                obj_disp(plane_left, plane_lr_x, plane_lr_y)

            elif left_move == 0 and right_move == 1:
                obj_disp(plane_right, plane_lr_x, plane_lr_y)

            elif left_move == 1 and right_move == 1:
                obj_disp(plane, plane_x, plane_y)
      
        
        if plane_dead == 0 :
            if isgameover == 0:
                if left_move == 0 and right_move == 0:
                    obj_disp(plane, plane_x, plane_y)
                    exp_plane = 0
                elif left_move == 1 and right_move == 0:
                    obj_disp(plane_left, plane_lr_x, plane_lr_y)
                    exp_plane = 1
                elif left_move == 0 and right_move == 1:
                    obj_disp(plane_right, plane_lr_x, plane_lr_y)
                    exp_plane = 2
                elif left_move == 1 and right_move == 1:
                    obj_disp(plane, plane_x, plane_y)
                    exp_plane = 0

    
       # 폭발
        #scale_transform = pg.transform.scale
        #image_load = pg.image.load
        if isgameover == 1:
            if exp_t_repeat > 0:
                if exp_t <= 18:
                    exp_img_x = int(image_load(exp_img[exp_t]).get_rect().size[0]/1*img_ratio)
                    exp_img_y = int(image_load(exp_img[exp_t]).get_rect().size[1]/1*img_ratio)
                    obj_disp(scale_transform(image_load(exp_img[exp_t]), [exp_img_x, exp_img_y]), 
                        plane_x + plane_size[0]/2 - exp_img_x/2 , plane_y + plane_size[0]/2 - exp_img_y/2)
                    exp_t += 1
                else:
                    exp_t_repeat -= 1
                    exp_t = 0
            else:
                pass

         
       # 점수 표기
        font = pg.font.SysFont( 'malgungothic', 15, True, False)
        point_text = font.render('Point:' + str(point), True, white)
        point_point = [pad_width*0.05, pad_height*0.02] 
        gamepad.blit(point_text, point_point)

       # Game Over
        # Game over 조건
        #ufo_xyz_remove = ufo_xyz.remove
        if isgameover == 0 and plane_dead == 0:
            if len(ufo_xyz) != 0 :
                for i, xyz in enumerate(ufo_xyz) :
                    if ( xyz[0] <= plane_lr_x + plane_lr_size[0]*3/4 
                        and xyz[0] + ufo_size[0] >= plane_lr_x + plane_lr_size[0]/4 
                        and xyz[1] <= plane_y + plane_size[1]*3/4
                        and xyz[1] + ufo_size[1] >= plane_y + plane_lr_size[1]/4) :
                        ufo_xyz_remove(xyz)
                        isgameover = 1

            #fire_down_xy_remove = fire_down_xy.remove
            if len(fire_down_xy) != 0 and plane_dead == 0:
                for i, xy in enumerate(fire_down_xy) :
                    if ( xy[0] <= plane_lr_x + plane_lr_size[0]*3/4  
                        and xy[0] + fire_size[0] >= plane_lr_x + plane_lr_size[0]/4 
                        and xy[1] <= plane_y + plane_size[1]*3/4 
                        and xy[1] + fire_size[1] >= plane_y + plane_lr_size[1]/4) :
                        fire_down_xy_remove(xy)
                        isgameover = 1

            #fire_left_xy_remove = fire_left_xy.remove
            if len(fire_left_xy) != 0 and plane_dead == 0:
                for i, xy in enumerate(fire_left_xy) :
                    if ( xy[0] <= plane_lr_x + plane_lr_size[0]*3/4  
                        and xy[0] + fire_size[0] >= plane_lr_x + plane_lr_size[0]/4 
                        and xy[1] <= plane_y + plane_size[1]*3/4 
                        and xy[1] + fire_size[1] >= plane_y + plane_lr_size[1]/4) :
                        fire_left_xy_remove(xy)
                        isgameover = 1              

            #fire_right_xy_remove = fire_right_xy.remove
            if len(fire_right_xy) != 0 and plane_dead == 0:
                for i, xy in enumerate(fire_right_xy) :
                    if ( xy[0] <= plane_lr_x + plane_lr_size[0]*3/4  
                        and xy[0] + fire_size[0] >= plane_lr_x + plane_lr_size[0]/4 
                        and xy[1] <= plane_y + plane_size[1]*3/4 
                        and xy[1] + fire_size[1] >= plane_y + plane_lr_size[1]/4) :
                        fire_right_xy_remove(xy)
                        isgameover = 1 
            
            if len(fire_boss_xyz) != 0 and plane_dead == 0:
                for i, xyz in enumerate(fire_boss_xyz) :
                    if ( xyz[0] <= plane_lr_x + plane_lr_size[0]*3/4  
                        and xyz[0] + fire_size[0]*2 >= plane_lr_x + plane_lr_size[0]/4 
                        and xyz[1] <= plane_y + plane_size[1]*3/4 
                        and xyz[1] + fire_size[1]*2 >= plane_y + plane_lr_size[1]/4) :
                        isgameover = 1 


        # gameover/continue 실행
        font = pg.font.SysFont('malgungothic', 40, True, False)
        continue_font = pg.font.SysFont('malgungothic', 30, True, True)
        gameover_text = font.render('Game Over', True, white)
        continue_text = continue_font.render('Continue?  ' + str(continue_time), True, white)
        continue_point = [pad_width/2 - continue_text.get_rect().size[0]/2, 
                            pad_height/2 - continue_text.get_rect().size[1]/2]
        gameover_point = [pad_width/2 - gameover_text.get_rect().size[0]/2, 
                            pad_height/2 - gameover_text.get_rect().size[1]/2]
        if isgameover == 1:
           # continue 표출
            if continue_wait == 0 and gameover_wait > 0:
                if gameover_wait / 60 > continue_time:
                    gamepad.blit(continue_text, continue_point)
                    gameover_wait -= 1
                    if key_press[pg.K_a]:
                            isgameover = 0
                            gameover_wait = 600 # continue 시작시간(600부터 빼기) / gameover 표시시간(0부터 시작)
                            continue_wait = 0 # continue flag
                            continue_time = 10 # continue 시간
                            plane_dead = 180
                            plane_x = pad_width * 0.5 - plane_size[0]/2
                            plane_y = pad_height * 0.95 - plane_size[1]
                            plane_lr_x = plane_x + plane_size[0]/2 - plane_lr_size[0]/2
                            plane_lr_y = plane_y + plane_size[1] - plane_lr_size[1]
                            exp_t_repeat = 3

                elif gameover_wait / 60 <= continue_time:
                    gamepad.blit(continue_text, continue_point)
                    continue_time -= 1

           # gameover 표출
            elif continue_wait == 0 and gameover_wait == 0:
                    continue_wait += 1
            elif continue_wait == 1:
                if gameover_wait % 60 <= 30 :
                    pg.Surface.set_alpha(gameover_text, 255)
                    gameover_wait += 1
                elif gameover_wait % 60 > 30 :
                    pg.Surface.set_alpha(gameover_text, 0)
                    gameover_wait += 1
                gamepad.blit(gameover_text, gameover_point)
                if gameover_wait > 300:
                    crashed = True           


       # frame clock 설정   
        frame_t += 1
        if frame_t >= 60:
            frame_t = 0
            stage_play_time += 1  

       # 화면 업데이트
        pg.display.flip()
        clock.tick(60) 


# 실제 동작 ----------------------------
init_game()                
start_game()
run_game()

while True:
    init_game()  
    for event in pg.event.get():
  #비행기 방향키 뗐을 때
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                run_game()
            else:
                pass

