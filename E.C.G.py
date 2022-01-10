
# Element Combination Game

import random, time, pygame, sys
from pygame.locals import*

pygame.init()

# 원소사진과 원소리스트
ELEMENTSPICLIST = [
    'H.png','Li.png','Be.png',
    'B.png','C.png','N.png',
    'O.png','F.png','Na.png',
    'Mg.png','Al.png','Si.png',
    'P.png','S.png','Cl.png',
    'K.png','Ca.png'
    ]
ELEMENTSLIST = [
    ['H','H.png'],['LI','Li.png'],['Be','Be.png'],['B','B.png'],['C','C.png'],['N','N.png'],['O','O.png'],['F','F.png'],
    ['Na','Na.png'],['Mg','Mg.png'],['Al','Al.png'],['Si','Si.png'],['P','P.png'],['S','S.png'],['Cl','Cl.png'],['K','K.png'],['Ca','Ca.png']
    ]

ADDNEWELEMENTSRATE = 45


# 미션 리스트
MISSIONLIST =  [{'name':'산소', 'ans':['O.png', 'O.png']  }, {'name':'질소', 'ans':['N.png', 'N.png']},
                {'name':'물', 'ans':['H.png', 'O.png', 'O.png']}, {'name':'이산화탄소', 'ans':['C.png', 'O.png', 'O.png']},
                {'name':'이산화황', 'ans':['S.png', 'O.png', 'O.png']}, {'name':'심플로오로보란', 'ans':['B.png', 'F.png', 'F.png', 'F.png']},
                {'name':'일산화탄', 'ans':['C.png', 'O.png']}, {'name':'시레인', 'ans':['Si.png', 'H.png', 'H.png', 'H.png', 'H.png']},
                {'name':'산화질소', 'ans':['N.png', 'O.png']}, {'name':'플루오로매탄', 'ans':['C.png', 'H.png', 'F.png', 'F.png', 'F.png']},]

###  색깔  ###
#               R    G    B
WHITE       = (255, 255, 255)
LIGHTGRAY   = (230, 230, 230)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
NAVYBLUE    = (  0,   0, 128)

# 스크린 크기
WINDOWWIDTH = 450
WINDOWHEIGHT = 800

# 스크린 설정
GameWindow = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Elements Combination Simulation GAME')
GameWindow.fill(WHITE)# 화면 흰색으로

# 폰트 설정
Scorefont = pygame.font.SysFont('comicsansms', 30)
fpsfont = pygame.font.SysFont('comicsansms', 20)
Pressfont = pygame.font.SysFont('comicsansms',45)
cfont = pygame.font.SysFont('comicsansms', 15)
Missionfont = pygame.font.Font('HoonWhitecatR.ttf', 27)

# 스코어 
Score = 0

##### 이미지 불러오기
# 비커
Beaker = pygame.image.load('Beaker.png')
Beaker_x = WINDOWWIDTH/2
Beaker_y = WINDOWHEIGHT * 0.86 #고정
BeakerRect = Beaker.get_rect()
BeakerRect.center = (Beaker_x, Beaker_y)

# 시간
Time = pygame.image.load('time.png')

# 배경
Startbackground = pygame.image.load('BG.jpg')
instructionBG = pygame.image.load('bgbgbg.jpg')
 
# FPS
FPS = pygame.time.Clock()
fps = 100

# 원소 속도
SPEED = 2

def main():
    global scoreText, Score
    
    # 음악
    pygame.mixer.music.load('bgm.mp3')
    pygame.mixer.music.play(-1, 1.8)

    # 원소
    ELEMENTS = []
    ele_AddCounter = 0
    Answer = []
    AnswerTXT = []

    # 미션
    Mission = Missionfont.render('MISSION: %s을(를) 만들어라!' %(MISSIONLIST[random.randint(0, len(MISSIONLIST)-1)]['name']), True, BLACK)

    pygame.mouse.set_visible(False)
    
    StartScreen()
    instruction()

    GameWindow = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Elements Combination Simulation GAME')
    while True:
        
        KeyEvent()
                
        move_Beaker()# 비커움직임
        
        MakeScore()# 점수그리기

        ### 원소 그리기
        if len(ELEMENTS) < 10:
            ele_AddCounter += 1
        if ele_AddCounter == ADDNEWELEMENTSRATE:
            ele_AddCounter = 0
            ele_Name = ELEMENTSLIST[random.randint(0, len(ELEMENTSPICLIST)-1)]
            ele_Pic = pygame.image.load(ele_Name[1])
            newELE = {'rect':pygame.Rect(random.randint(0, WINDOWWIDTH-47), 0 - 47, 47, 47),
                      'speed': SPEED, 
                      'surface':pygame.transform.scale(ele_Pic, (47, 47)),
                      'name':ele_Name[0],
                      'ansName':ele_Name[1]
                      }

            ELEMENTS.append(newELE)

        for e in ELEMENTS:
            e['rect'].move_ip(0, e['speed'])

        for e in ELEMENTS:
            if BeakerRect.colliderect(e['rect']):
                ELEMENTS.remove(e)
                Answer.append(e['ansName'])
                AnswerTXT.append(e['name'])
            
        for e in ELEMENTS[:]:
            if e['rect'].top > WINDOWHEIGHT:
                ELEMENTS.remove(e)

        AnswerText = Missionfont.render('획득한 원소: %s' %(AnswerTXT), True, BLACK)
        
        FPS.tick(fps)# 게임 속도
        
        GameWindow.fill(WHITE)# 화면 흰색으로
        
        for e in ELEMENTS:
            GameWindow.blit(e['surface'], e['rect'])
            
        GameWindow.blit(Beaker, BeakerRect)# 비커 그리기
        GameWindow.blit(Time, (1,1))
        GameWindow.blit(scoreText,(WINDOWWIDTH - scoreText.get_width() - 10 ,1))# score 그리기
        GameWindow.blit(fpsText,(38 ,4))
        GameWindow.blit(Mission,(1,WINDOWHEIGHT -60))
        GameWindow.blit(AnswerText,(1,WINDOWHEIGHT -35))
        
        pygame.display.update()
        
        
def move_Beaker():
    # 비커의 움직임 함수
    global Beaker_x, Beaker_xMove # 전역변수 설정
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a] or pressed[pygame.K_LEFT]: # 만약 왼쪽 화살표가 눌려졌다면
        if Beaker_x < 0:
            Beaker_x -=0
        else:
            Beaker_x-= 5 
    elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]: # 만약 오른쪽 화살표가 눌려졌다면
        if Beaker_x > WINDOWWIDTH-56:
            Beaker_x +=0
        else:
            Beaker_x +=5

    BeakerRect.centerx = Beaker_x

def MakeScore():
    # 점수 생성 함수
    global scoreText
    scoreText = Scorefont.render('Score: %s' % (Score), True, BLACK)

def beakerHasHitELE(BeakerRect, ELEMENTS):
    for e in ELEMENTS:
        if BeakerRect.colliderect(e['rect']):
            return True

    return False

        
def KeyEvent():
    # 키 이벤트 관련함수
    global fps, fpsText, Score
    h = False
    j = False
    fText = ''
    for event in pygame.event.get(): #게임에서 발생하는 이벤트를 가져옴
        if event.type == QUIT:
            pygame.quit()      #파이게임 라이브러리 종료
            sys.exit()  #시스템 종료
        if event.type == KEYDOWN:
            if event.key == K_UP:
                fps += 50
            elif event.key == K_DOWN:
                fps -= 50
            if event.key == ord('h'):
                h = True
            if event.key == ord('j'):
                j = True


        if h == True and j == True:
            Score += 99999
            print(' ! H I D D E N C O M M A N D !')

        if fps < 50:
            fps = 50
        elif fps > 250:
            fps = 250
        if fps < 100:
            fText = 'Very slow'
        elif fps >= 100 and fps < 150:
            fText = 'Slow'
        elif fps >= 150 and fps < 200:
            fText = 'Fast'
        elif fps >= 200:
            fText = 'Very Fast'

        fpsText = fpsfont.render(fText, True, BLACK)
        
    
def checkForKeyPress():
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def StartScreen():
    GRB = pygame.image.load('GRB_15.svg.png')
    
    GameName = Pressfont.render('Elements Game', True, BLACK)
    GameNameRect = GameName.get_rect()
    GameNameRect.center = (int(WINDOWWIDTH / 2.5), int(WINDOWHEIGHT / 3) - 15)
    
    pressKey = Scorefont.render('Press a key to play', True, LIGHTRED)
    pressKeyRect = pressKey.get_rect()
    pressKeyRect.center = (int(WINDOWWIDTH / 2.5), int(WINDOWHEIGHT / 3) + 35)

    CpressKey = cfont.render('< Copyright(c). 2017. Progresso. All rights reserved. >', True, BLACK)
    CpressKeyRect = CpressKey.get_rect()
    CpressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT * 0.95))

    GameWindow.blit(Startbackground, (0,0))
    
    GameWindow.blit(GRB,(WINDOWWIDTH-55, 20))
    GameWindow.blit(CpressKey, CpressKeyRect)
    GameWindow.blit(pressKey, pressKeyRect)
    GameWindow.blit(GameName, GameNameRect)

    while checkForKeyPress() == None:
        for event in pygame.event.get(): #게임에서 발생하는 이벤트를 가져옴
            if event.type == QUIT:
                pygame.quit()      #파이게임 라이브러리 종료
                sys.exit()   
        pygame.display.update()

def instruction():
    global fps, fpsText
    GameWindow = pygame.display.set_mode((1000, 400))
    pygame.display.set_caption('INSRUCTION')
    GameWindow.fill(WHITE)
    instructionTitle = Pressfont.render('INSTRUCTION', True, LIGHTGREEN)
    instruction0 = Scorefont.render('1. Press the up or down key to make it faster or slower.', True, BLACK)
    instruction1 = Scorefont.render('2. Press the Left or Right key to move the beaker to the left or right.', True, BLACK)
    instruction2 = fpsfont.render('Press the ESC to continue', True, LIGHTRED)

    GameWindow.blit(instructionBG, (0,0))
    GameWindow.blit(instructionTitle, (5, 90))
    GameWindow.blit(instruction0, (5,160))
    GameWindow.blit(instruction1, (5,210))
    GameWindow.blit(instruction2, (700, 300))
    while checkForKeyPress() != K_ESCAPE:
        KeyEvent()
        pygame.display.flip()


main()

