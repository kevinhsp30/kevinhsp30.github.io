import pygame as py

py.init()

screen_width = 1900 /2
screen_height = 1100 /2
screen = py.display.set_mode((screen_width, screen_height))
# background = py.image.load("흰색 이미지.png")


    
class Character:
    character = py.image.load("image\푸앙_사랑_look_right.png")
    size = character.get_rect().size
    width = size[0]
    height = size[1]
    posX = (screen_width/2) - (width/2)
    posY = screen_height - height
    is_sight = "right"
    is_jumping = False
    is_running = True

    def trun_Char(self):
        if self.is_sight == "right":
            self.character = py.image.load("image\푸앙_사랑.png")
            self.is_sight = "left"
        elif self.is_sight == "left":
            self.character = py.image.load("image\푸앙_사랑_look_right.png")
            self.is_sight = "right"
            

class Background:
    def __init__(self, image, posX = 0, upY = 0):
        self.background = image
        self.size = self.background.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.posX = posX                                      # 왼쪽 끝에 맞춤
        self.posY = screen_height - self.height - upY         # 바닥에 맞춤
    # background = py.image.load("image\\68858716_p0.jpg")
    
                           

class Obstacle:
    obstacle = py.image.load("image\장애물_지상.png")
    size = obstacle.get_rect().size
    width = size[0]
    height = size[1]
    posX = screen_width - screen_width/8
    posY = screen_height - height



# 인스턴스 생성
Puang = Character()
Puang.character = py.image.load("image\푸앙_사랑_look_right.png")

bg_space_1 = Background(py.image.load("image\\68858716_p0.jpg"))
bg_space_2 = Background(py.image.load("image\\69526300_p1.jpg"))
bg_asset = Background(py.image.load("image\\Background.png"))




land_obs = Obstacle()
land_obs.obstacle = py.image.load("image\장애물_지상.png")

py.display.set_caption("1st_Stage")
to_x, to_y = 0,0

bg = bg_space_2
clock = py.time.Clock()


init_speed = 1
count = 0


# 이벤트 루프
running = True
while running:

    dt = clock.tick(250)

    # 속도 고정
    # 속도 변화 전처리 or 후처리 결정 필요
    if count < 20:
        temp_speed = init_speed
        temp_speed *= dt
        speed = temp_speed
        count += 1
    
    print("Fps :", str(clock.get_fps()), "speed :", speed,", ", to_x)

    

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                to_x -= speed
                if Puang.is_sight == "right":
                    Puang.trun_Char()

            elif event.key == py.K_RIGHT:
                to_x += speed
                if Puang.is_sight == "left":
                    Puang.trun_Char()

            # elif event.key == py.K_UP:
            #     to_y -= speed
            # elif event.key == py.K_DOWN:
            #     to_y += speed

            elif event.key == py.K_SPACE and Puang.is_running:
                Puang.is_jumping = True
                Puang.is_running = False


        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                to_x = 0
                if py.key.get_pressed()[py.K_LEFT]:
                    to_x -= speed

                if py.key.get_pressed()[py.K_RIGHT]:
                    to_x += speed

            # elif event.key == py.K_UP or event.key == py.K_DOWN:
            #     to_y = 0
            #     if py.key.get_pressed()[py.K_UP]:
            #         to_y -= speed
            #     if py.key.get_pressed()[py.K_DOWN]:
            #         to_y += speed


    # 속도 제한
    if to_x > speed:
        to_x = speed
    if to_x < -speed:
        to_x = -speed



    # 방향 재확인
    if to_x < 0 and Puang.is_sight == "right":
        Puang.trun_Char()
    if to_x > 0 and Puang.is_sight == "left":
        Puang.trun_Char()


    # 점프
    if Puang.is_jumping:
        Puang.posY -= speed
        if Puang.posY < screen_height - Puang.height - 200:
            Puang.is_jumping = False

    # 높이를 지면에 고정
    if not Puang.is_jumping:
        Puang.posY += speed
        if Puang.posY > screen_height - Puang.height:
            Puang.posY = screen_height - Puang.height
            Puang.is_running = True


    # 맵 왼쪽 끝 부분에서의 배경 및 물체 컨트롤
    if bg.posX > 0:
        bg.posX = 0
        Puang.posX += to_x
        
    if Puang.posX < 0:
        Puang.posX = 0
        to_x = 0

    if Puang.posX < (screen_width/2) - (Puang.width/2):
        bg.posX = 0
        Puang.posX += to_x
        land_obs.posX += to_x
    


    







    # 배경과 장해물 이동
    # 원근감 표현
    bg.posX -= to_x/2
    land_obs.posX -= to_x


    # 충돌 확인
    # if land_obs.posX == Puang.posX:


    for i in (1,2,3,4):
        screen.blit(bg.background, (bg.posX + bg.width*i, bg.posY))
        
    screen.blit(bg.background, (bg.posX, bg.posY))


    screen.blit(Puang.character, (Puang.posX, Puang.posY))
    screen.blit(land_obs.obstacle, (land_obs.posX, land_obs.posY))
    
    py.display.update()


py.quit()