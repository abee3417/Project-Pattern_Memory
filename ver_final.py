# pygame모듈의 메소드들을 더 편하게 사용하기 위해 불러옴
# 그 외의 필요한 sys, time, random 모듈 사용
import random, sys, time, pygame
from pygame.locals import *

# 블록 색깔 전역변수로 정의 (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (125, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 125, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 125)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (125, 125, 0)
bgColor = BLACK # 일단 기본 배경색을 검정색으로 설정

# 변수 설정
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLASHSPEED = 500
FLASHDELAY = 200
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 5 # 5초동안 아무 버튼도 안누르면 종료

# 버튼을 만들기 위한 여백 크기 변수 -> 좌표를 정해야 하기 때문에 작성
XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# 화면에 띄울 4개의 버튼 구현
# pygame.Rect(왼쪽 상단 모서리 x좌표, 왼쪽 상단 모서리 y좌표, 가로 길이, 세로 길이)
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)


class System:
    def __init__(self):
        self.newBgColor = BLACK
        self.newBgSurf = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT))
        self.origSurf = DISPLAYSURF.copy()
        self.flashSurf = pygame.Surface(DISPLAYSURF.get_size())
        
    def terminate(self): # 게임 종료
        pygame.quit()
        sys.exit()

    def checkForQuit(self):
        for event in pygame.event.get(QUIT): # 모든 QUIT 이벤트를 가져온다
            self.terminate() # QUIT 이벤트가 발생했으면 종료한다.
        for event in pygame.event.get(KEYUP): # 모든 KEYUP 이벤트를 가져온다
            if event.key==K_ESCAPE:
                self.terminate() # KEYUP 이벤트가 Esc 키면 종료한다
            pygame.event.post(event) # 다른 KEYUP 이벤트 객체는 이벤트 큐에 돌려놓는다

    def changeBackgroundAnimation(self, animationSpeed = 40):
        global bgColor
        self.newBgSurf = self.newBgSurf.convert_alpha()
        r,g,b=self.newBgColor
        for alpha in range(0,255,animationSpeed): # 애니메이션 루프
            self.checkForQuit()
            DISPLAYSURF.fill(bgColor) # 이전 배경색으로 채움
            self.newBgSurf.fill((r,g,b,alpha)) # 새로운 배경색으로 채움
            DISPLAYSURF.blit(self.newBgSurf,(0,0)) # 색깔을 섞음

            # 버튼을 다시 그린다
            Button.drawButtons(self)

            # 화면 그리고 잠깐 멈춤
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        bgColor = self.newBgColor

    def gameOverAnimation(self, color = WHITE, animationSpeed = 50):
        #모든 비프음을 한꺼번에 플레이하며 배경색을 반짝거리게 한다
        self.flashSurf = self.flashSurf.convert_alpha()
        BEEP1.play() #모든 비프음을 한꺼번에 플레이한다
        BEEP2.play()
        BEEP3.play()
        BEEP4.play()
        r,g,b = color
        for i in range(3): # 3번 반짝거린다
            for alpha in range(0, 255, animationSpeed):
                # alpha는 투명도를 말한다. 255는 불투명이고, 0은 완전 투명으로 보이지 않는다.
                # alpha값을 0부터 255까지 증가시키면서 밝아짐
                self.checkForQuit() # 사용자가 esc를 누르는 경우를 생각
                self.flashSurf.fill((r,g,b,alpha)) # fill로 flashsurf를 칠함
                DISPLAYSURF.blit(self.origSurf,(0,0)) # blit로 origSurf을 DISPLAYSURF로 복사
                DISPLAYSURF.blit(self.flashSurf,(0,0)) # blit로 flashSurf을 DISPLAYSURF로 복사
                Button.drawButtons(self)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
            for alpha in range(255, 0, -animationSpeed):
                # alpha값을 255부터 0까지 감소시키면서 어두워짐
                self.checkForQuit()
                self.flashSurf.fill((r,g,b,alpha))
                DISPLAYSURF.blit(self.origSurf,(0,0))
                DISPLAYSURF.blit(self.flashSurf,(0,0))
                Button.drawButtons(self)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
        
        
class Button:
    def __init__(self):
        self.sys = System()
        self.sound = None
        self.flashColor = None
        self.rectangle = None
        self.origSurf = None
        self.FlashSurf = None
        
    def flashButtonAnimation(self, color, animationSpeed = 50):
        # Color 파라메터로 어떤 값을 전달해 주었는지에 따라 sound, flashColor, rectangle이 달라진다
        if color == YELLOW:
            self.sound = BEEP1
            self.flashColor = BRIGHTYELLOW
            self.rectangle = YELLOWRECT
        elif color == BLUE:
            self.sound = BEEP2
            self.flashColor = BRIGHTBLUE
            self.rectangle = BLUERECT
        elif color == RED:
            self.sound = BEEP3
            self.flashColor = BRIGHTRED
            self.rectangle = REDRECT
        elif color == GREEN:
            self.sound = BEEP4
            self.flashColor = BRIGHTGREEN
            self.rectangle = GREENRECT

        # 버튼을 깜빡깜빡하는 애니메이션
        self.origSurf = DISPLAYSURF.copy()
        self.flashSurf = pygame.Surface((BUTTONSIZE,BUTTONSIZE))
        self.flashSurf = self.flashSurf.convert_alpha()
        r,g,b = self.flashColor
        self.sound.play() # 소리를 재생
        for alpha in range(0, 255, animationSpeed):
            # alpha값을 0부터 255까지 증가시키면서 밝아짐
            self.sys.checkForQuit() # 사용자가 esc를 누르는 경우를 생각
            DISPLAYSURF.blit(self.origSurf,(0,0)) # blit로 origSurf을 DISPLAYSURF로 복사
            self.flashSurf.fill((r,g,b,alpha)) # fill로 flashsurf를 칠함
            DISPLAYSURF.blit(self.flashSurf,self.rectangle.topleft) # flashSurf를 DISPLAYSURF로 복사
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        for alpha in range(255, 0, -animationSpeed):
            # alpha값을 255부터 0까지 감소시키면서 어두워짐
            self.sys.checkForQuit()
            DISPLAYSURF.blit(self.origSurf,(0,0))
            self.flashSurf.fill((r,g,b,alpha))
            DISPLAYSURF.blit(self.flashSurf,self.rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        DISPLAYSURF.blit(self.origSurf,(0,0))

    def drawButtons(self): # 버튼 만드는 함수
        pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
        pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
        pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
        pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)

    def getButtonClicked(self, x, y): # 버튼 클릭했을 경우
        if YELLOWRECT.collidepoint((x,y)):
            return YELLOW
        elif BLUERECT.collidepoint((x,y)):
            return BLUE
        elif REDRECT.collidepoint((x,y)):
            return RED
        elif GREENRECT.collidepoint((x,y)):
            return GREEN
    

class Game:
    def __init__(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4
        pygame.init()
        # 게임 설정
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption("Pattern Memory Game")
        BASICFONT = pygame.font.Font("freesansbold.ttf", 16) # 폰트 설정
        self.infoSurf = BASICFONT.render("Match the pattern by clicking on the button or using the Q, W, A, S keys.", 1, WHITE)
        self.infoRect = self.infoSurf.get_rect() # 안내를 담을 사각형
        self.infoRect.topleft = (10, WINDOWHEIGHT - 25)
        # Sound 객체를 반환 -> 사운드 파일을 로드함
        BEEP1 = pygame.mixer.Sound("beep1.ogg")
        BEEP2 = pygame.mixer.Sound("beep2.ogg")
        BEEP3 = pygame.mixer.Sound("beep3.ogg")
        BEEP4 = pygame.mixer.Sound("beep4.ogg")
        # 새 게임에서 사용할 변수를 초기화한다.
        self.pattern = []
        self.currentStep = 8
        self.lastClickTime = 0
        self.score = 0
        # False면 패턴을 보여주고 있는 상태, True면 패턴 맞추는걸 기다리고 있는 상태
        self.waitingForInput = False
        # 버튼 클래스와 게임 시스템 클래스를 불러옴
        self.button = Button()
        self.system = System()
       
        
    def main(self):
        while True: # 게임을 계속해서 진행하기 위한 무한 루프
            clickedButton = None # 클릭한 버튼을 나타내는 변수
            DISPLAYSURF.fill(bgColor) # 배경을 검정색으로 칠함
            self.button.drawButtons()
            # 점수판 만들기
            scoreSurf = BASICFONT.render("Score : " + str(self.score), 1, WHITE)
            scoreRect = scoreSurf.get_rect()
            scoreRect.topleft = (WINDOWWIDTH - 100, 10)
            DISPLAYSURF.blit(scoreSurf, scoreRect)
            DISPLAYSURF.blit(self.infoSurf, self.infoRect)
            self.system.checkForQuit() # QUIT이벤트 검사
            # 이벤트 처리 루프
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP: # 마우스를 클릭하면
                    mousex, mousey = event.pos # 마우스의 x, y좌표를 각각 mousex, mousey에 저장
                    clickedButton = self.button.getButtonClicked(mousex, mousey) # 어떤 버튼을 클릭했는지에 따라 Color 객체를 반환
                elif event.type == KEYDOWN:
                    if event.key == K_q: # Q를 눌렀을 때
                        clickedButton = YELLOW # 노란색 버튼
                    elif event.key == K_w: # W를 눌렀을 때
                        clickedButton = BLUE # 파란색 버튼
                    elif event.key == K_a: # A를 눌렀을 때
                        clickedButton = RED # 빨간색 버튼
                    elif event.key == K_s: # S를 눌렀을 때
                        clickedButton = GREEN # 초록색 버튼

                if not self.waitingForInput: # 1. 패턴을 보여주는 단계 구현
                    pygame.display.update()
                    pygame.time.wait(1000)
                    self.pattern.append(random.choice((YELLOW, BLUE, RED, GREEN))) # 시간이 지날수록 패턴의 길이를 늘림
                    for button in self.pattern: # 패턴에 해당하는 버튼을 순서대로 밝게 보여줌
                        self.button.flashButtonAnimation(button)
                        pygame.time.wait(FLASHDELAY)
                    self.waitingForInput = True # 패턴을 맞추는 상태로 바꿈

                else: # 2. 패턴을 맞추는 단계 구현
                    if clickedButton and clickedButton == self.pattern[self.currentStep]: # 누른 버튼이랑 패턴이랑 일치할 때
                        # 맞는 버튼을 눌렀을 경우
                        self.button.flashButtonAnimation(clickedButton) # 버튼을 반짝거리게 하여 맞췄다는것을 보여줌
                        self.currentStep += 1 # 플레이어가 다음에 눌러야 하는 패턴의 순서를 기록
                        self.lastClickTime = time.time() # 시간 기록

                        if self.currentStep == len(self.pattern): # 맨 마지막 패턴일 경우
                            self.system.changeBackgroundAnimation() # 다 클리어했으므로 배경색을 바꿔 클리어했다는 것을 알려줌
                            self.score += 1 # 점수를 1점 증가시킴
                            self.waitingForInput = False
                            self.currentStep = 0 # 게임의 턴이 종료되고 맨 처음으로 리셋한다

                    # 게임오버의 처리    
                    elif (clickedButton and clickedButton != self.pattern[self.currentStep]) or (self.currentStep != 0 and time.time() - TIMEOUT > self.lastClickTime):
                        # 버튼이 틀렸을 경우 or 타임오버가 됬을 경우
                        self.system.gameOverAnimation() # 게임오버 애니메이션 처리
                        # 새 게임용으로 변수를 처음으로 리셋
                        self.pattern = []
                        self.currentStep = 0
                        self.waitingForInput = False
                        self.score = 0
                        pygame.time.wait(1000)
                        self.system.changeBackgroundAnimation() # 다시 배경색을 바꿈

                # 게임판 다시 그리기
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                        

# 게임 시작
if __name__ == "__main__":
    game = Game()
    game.main()


    
