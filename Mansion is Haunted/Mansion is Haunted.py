
#Art made in pixilart and photoshop, sound effects made in sfxr, music made in FL studio, all by me
#June 19, 2023

from math import *
from random import *
from pygame import *
from json import *

font.init()
mixer.init()
init()

width, height = 1024, 768
screen = display.set_mode((width, height))
display.set_caption("Mansion is Haunted")
display.set_icon(image.load("resources/zombie.png"))

draw.rect(screen, (255, 255, 255), (130, 311, 824, 75), 5)
display.flip()

UIFont = font.Font("resources/retro_computer.ttf", 50)
GUIFont = font.Font("resources/retro_computer.ttf", 40)
DSFont = font.Font("resources./retro_computer.ttf", 20)
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 1 / 10, 71))
display.flip()

#menu assets
sceneBG = transform.scale(image.load("resources/sceneBG.png"), (1024, 768))
button = transform.scale(image.load("resources/button.png"), (400, 100))

#learned json module from pythonexamples.org
saveData = open("resources/saveData.json", "r")
data = loads(saveData.read())
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 2 / 10, 71))
display.flip()

#load settings
def loadSettings(data):
    "loads previous settings from file"
    mixer.music.set_volume(float(data['saveData']['setting'][0]['volume']))
    if data['saveData']['setting'][0]['SFX'] == "false":
        SFX = False
    else:
        SFX = True
    if data['saveData']['setting'][0]['controls'] == "false":
        controls = False #True for WASD, False for Arrow 
    else:
        controls = True
    return [SFX, controls]
settings = loadSettings(data)
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 3 / 10, 71))
display.flip()

mixer.music.load("resources/mainTheme.ogg")
mixer.music.play(-1)
select = mixer.Sound("resources/select.wav")
select.set_volume(0.1)

#load progress
completion = data['saveData']['progress'][0]['complete']
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 4 / 10, 71))
display.flip()
display.flip()
saveData.close()

##################################### MENU #####################################

def menu():
    "menu screen of game. allows user to go to settings, tutorial, or start the game"
    running = True
    clock = time.Clock()
    buttons = [Rect(312, 300 + x * 120, 400, 100) for x in range(3)]

    title = transform.scale(image.load("resources/title.png"), (1024, 768))
    completion = transform.scale(image.load("resources/completion.png"), (100, 100))

    buttonTexts = [UIFont.render(word, True, (0, 0, 0)) for word in ["Play", "Settings", "Tutorial", "Quit"]]
    textPos = [(buttons[i][0] + ((buttons[i][2] - buttonTexts[i].get_width()) / 2), buttons[i][1] + ((buttons[i][3] - buttonTexts[i].get_height()) / 2)) for i in range(len(buttons))]

    BG = transform.scale(image.load("resources/menuBG.png"), (1024, 768))

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        screen.blit(BG, (0, 0))
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        for i in range(len(buttons)):
            screen.blit(button, buttons[i])
            screen.blit(buttonTexts[i], textPos[i])
        screen.blit(title, (0, 0))
        if data['saveData']['progress'][0]['complete'] == "true":
            screen.blit(completion, (200, 300))
        
        if mb[0]:
            if buttons[0].collidepoint(mx, my):
                if settings[0] == True:
                    mixer.Sound.play(select)
                return "level"
            if buttons[1].collidepoint(mx, my):
                if settings[0] == True:
                    mixer.Sound.play(select)
                return "settings"
            if buttons[2].collidepoint(mx, my):
                if settings[0] == True:
                    mixer.Sound.play(select)
                return "instructions"

        display.flip()

##################################### SETTINGS #####################################

def moveSlider(xPos, mx, lock):
    "Changes the slider x position and sets the volume"
    if lock == True:
        if mx <= 300:
            xPos = 300
            mixer.music.set_volume(0)
        elif 300 < mx < 874:
            xPos = mx
            mixer.music.set_volume((xPos - 250) / 624)
        else:
            xPos = 874
            mixer.music.set_volume(1)
    else:
        xPos = mixer.music.get_volume() * 624 + 250
    return Rect(xPos, 145, 50, 30)

def displaySwitch(pos, state):
    "displays what state switches are in"
    if state == True:
        return Rect(width - 140, pos[1], pos[2], pos[3])
    else:
        return Rect(width - 180, pos[1], pos[2], pos[3])

def saveSettings(controls, SFX):
    "writes settings to save data file"
    saveData = open("resources/saveData.json", "w")

    if 'volume' in data['saveData']['setting'][0]:
        del data['saveData']['setting'][0]['volume']
        data['saveData']['setting'][0].update({"volume":dumps(mixer.music.get_volume())})
    if 'controls' in data['saveData']['setting'][0]:
        del data['saveData']['setting'][0]['controls']
        data['saveData']['setting'][0].update({"controls":dumps(controls)})
    if 'SFX' in data['saveData']['setting'][0]:
        del data['saveData']['setting'][0]['SFX']
        data['saveData']['setting'][0].update({"SFX":dumps(SFX)})
    
    saveData.write(f"{dumps(data)}")
    saveData.close()

def settingsPage():
    "settings for game"
    running = True
    back = Rect(20, 20, 50, 50) 
    x = GUIFont.render("X", True, (0, 0, 0))

    #load settings
    saveData = open("resources/saveData.json", "r")
    data = loads(saveData.read())

    #volume slider
    lock = False
    VSlider = Rect(300, 150, 624, 20)
    VText = GUIFont.render("Volume", True, (255, 255, 255))
    VTPos = (230 - VText.get_width(), 130)
    VSliderUI = Rect(300, 145, 50, 30)

    #sfx switch
    if data['saveData']['setting'][0]['SFX'] == "false":
        SFX = False
    else:
        SFX = True
    SFXText = GUIFont.render("SFX", True, (255, 255, 255))
    SFXSwitchUI = Rect(width - 180, 210, 40, 40)
    SFXSwitch = Rect(width - 180, 212, 80, 36)

    #controls switch
    if data['saveData']['setting'][0]['controls'] == "false":
        controls = False #True for WASD, False for Arrow 
    else:
        controls = True
    controlText = GUIFont.render("Controls", True, (255, 255, 255))
    controlSwitchUI = Rect(width - 180, 280, 40, 40)
    controlSwitch = Rect(width - 180, 282, 80, 36)

    saveData.close()

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                saveSettings(controls, SFX)
                return "exit"
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 1:
                    if VSliderUI.collidepoint(mx, my):
                        lock = True
                    if SFXSwitch.collidepoint(mx, my) or SFXSwitchUI.collidepoint(mx, my):
                        SFX = not SFX
                    if controlSwitch.collidepoint(mx, my) or controlSwitchUI.collidepoint(mx, my):
                        controls = not controls
            if evt.type == MOUSEBUTTONUP:
                lock = False

        screen.blit(sceneBG, (0, 0))
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        draw.rect(screen, (127, 127, 127), back)
        screen.blit(x, (28, 18))
        if mb[0]:
            if back.collidepoint(mx, my):
                #write to saveData.json
                saveSettings(controls, SFX)
                if SFX == True:
                    mixer.Sound.play(select)
                return "menu"

        #volume slider
        VSliderUI = moveSlider(VSliderUI[0], mx, lock)
        
        draw.rect(screen, (125, 125, 125), VSlider)
        draw.rect(screen, (150, 150, 150), VSliderUI)
        screen.blit(VText, VTPos)

        SFXSwitchUI = displaySwitch(SFXSwitchUI, SFX)
        screen.blit(SFXText, (30, 200))
        if SFX == True:
            draw.rect(screen, (125, 125, 125), SFXSwitch)
            screen.blit(GUIFont.render("ON", True, (255, 255, 255)), (width - 300, 200))
        else:
            draw.rect(screen, (25, 25, 25), SFXSwitch)
            screen.blit(GUIFont.render("OFF", True, (255, 255, 255)), (width - 300, 200))
        draw.rect(screen, (150, 150, 150), SFXSwitchUI)

        controlSwitchUI = displaySwitch(controlSwitchUI, controls)
        screen.blit(controlText, (30, 270))
        if controls == True:
            draw.rect(screen, (125, 125, 125), controlSwitch)
            screen.blit(GUIFont.render("WASD Keys", True, (255, 255, 255)), (width - 510, 270))
        else:
            draw.rect(screen, (25, 25, 25), controlSwitch)
            screen.blit(GUIFont.render("ARROW Keys", True, (255, 255, 255)), (width - 510, 270))
        draw.rect(screen, (150, 150, 150), controlSwitchUI)

        display.flip()

##################################### INSTRUCTIONS #####################################

def instructions():
    "tutorial screen"
    running = True
    back = Rect(20, 20, 50, 50)
    x = GUIFont.render("X", True, (0, 0, 0))
    tutorialImage = transform.scale(image.load("resources/tutorial.png"), (1024, 768))

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        screen.blit(sceneBG, (0, 0))
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        screen.blit(tutorialImage, (0, 0))

        draw.rect(screen, (127, 127, 127), back)
        screen.blit(x, (28, 18))
        if mb[0]:
            if back.collidepoint(mx, my):
                if settings[0] == True:
                    mixer.Sound.play(select)
                return "menu"

        display.flip()

##################################### GAME LOOP #####################################

timerTime = 0
killTimer = 0

player = [width / 2, height / 2, 4, 4, 250, int(data['saveData']['progress'][0]['ammo']), 0, False]
#x offX, y offX, vx, vy, HP, ammo, score, go to next level

enemyRect = []
enemyWeaponSpeed = []
enemyMode = []
#max hp for type
enemyMax = [100, 125, 150, 175, 250, 1500]

walls = []

offX, offY = 0, 0

speed = 15
weaponsList = [["Knife", 15], ["Pistol", 20], ["Shotgun", 40], ["Machine Gun", 5]]
weapons = weaponsList[:int(data['saveData']['progress'][0]['weapons'])]

##### loading resources

levelFile = open("resources/levels.txt")
levelMaps = levelFile.read().split("!")
for i in range(len(levelMaps)):
    levelMaps[i] = levelMaps[i].split()
    for j in range(len(levelMaps[i])):
        levelMaps[i][j] = levelMaps[i][j].split(",")
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 5 / 10, 71))
                                                                                            #0                  1           2               3               4               5               6               7               8              9                 10             11              12              13          14          15
tiles = [transform.scale(image.load(f"resources/{name}.png"), (64, 64)) for name in ["floor_tile_detailed", "wall_top", "wall_side", "wall_cornerTL", "wall_cornerTR", "wall_cornerBL", "wall_cornerBR", "wall_endUp", "wall_endRight", "wall_endDown", "wall_endLeft", "wall_3cDown", "wall_3cLeft", "wall_3cUp", "wall_3cRight", "wall"]]
icons = [transform.scale(image.load(f"resources/{name}.png"), (32, 32)) for name in ["ammo_icon", "healthPot_icon", "key_icon"]]
UI = [transform.scale(image.load(f"resources/{name}.png"), (64, 64)) for name in ["ammo_UI", "ammo_UI", "knife_icon", "pistol_icon", "shotgun_icon", "machineGun_icon"]]
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 6 / 14, 71))
display.flip()

#sprites:
playerIcons = [transform.scale(image.load(f"resources/{name}.png"), (64, 64)) for name in ["player"]]
knife_anim = [transform.scale(image.load(f"resources/knife-frame-{i}.png"), (196, 64)) for i in range(6)]
bulletSprites = [transform.scale(image.load(f"resources/{name}.png"), (24, 24)) for name in ["bullet", "enBullet"]]
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 7 / 14, 71))
display.flip()

zombieSprites = [transform.scale(image.load(f"resources/{name}.png"), (64, 64)) for name in ["zombie"]]
bossSprites = [transform.scale(image.load(f"resources/{name}.png"), (196, 196)) for name in ["boss", "base"]]
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 8 / 10, 71))
display.flip()

#sound effects
SFXVolume = 0.1

plShoot = mixer.Sound('resources/plShoot.wav')
plShoot.set_volume(SFXVolume)
enShoot = mixer.Sound('resources/enShoot.wav')
enShoot.set_volume(SFXVolume)
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 9 / 10, 71))
display.flip()

healthGet = mixer.Sound('resources/healthGet.wav')
healthGet.set_volume(SFXVolume)
ammoGet = mixer.Sound('resources/ammoGet.wav')
ammoGet.set_volume(0.5 * SFXVolume)
keyGet = mixer.Sound('resources/keyGet.wav')
keyGet.set_volume(SFXVolume)
bossAppears = mixer.Sound("resources/bossAppears.wav")
bossAppears.set_volume(SFXVolume)
draw.rect(screen, (255, 255, 255), (130, 313, 820 * 9 / 10, 71))
display.flip()

death = mixer.Sound('resources/death.wav')
death.set_volume(SFXVolume)
draw.rect(screen, (255, 255, 255), (130, 313, 820, 71))
display.flip()

def setupLevel(level):
    "run this when loading any level for a list of immovable hitboxes"
    return [Rect(64 * j - offX, 64 * i + offY, 64, 64) for j in range(len(level[i])) for i in range(len(level)) if level[i][j] != "00"]

##### visuals

def displayAmmo(player):
    "displays how much ammo the player has left"
    if player[5] != 0:
        text = GUIFont.render(str(player[5]), True, (255, 255, 255))
    else:
        text = GUIFont.render(str(player[5]), True, (255, 0, 0))
    screen.blit(text, (width - 50 - text.get_width(), height - 150))
    screen.blit(UI[0], (width - 400, height - 150))

def displayHP(player, enemyRect, enemyH, enemyType):
    "displays HP info for play and enemies if they have lost any health"
    #enemy HP if health < max display bar over head
    for i in range(len(enemyH)):
        if enemyH[i] < enemyMax[enemyType[i]]:
            draw.rect(screen, (255 - 255 * enemyH[i] / enemyMax[enemyType[i]], 255 * enemyH[i] / enemyMax[enemyType[i]], 0), (enemyRect[i][0] - 15, enemyRect[i][1] - 25, 80 * enemyH[i] / enemyMax[enemyType[i]], 15))
            draw.rect(screen, (0, 0, 0), (enemyRect[i][0] - 15, enemyRect[i][1] - 25, 80, 15), 2)
    
    #####player HP display bar in corner of screen
    area = Rect(width - 400, height - 75, 350, 50)

    screen.set_clip(area)
    draw.rect(screen, (255, 0, 0), (width - 400 + (350 - 350 * player[4] / 250), height - 75, 350, 50))
    draw.rect(screen, (0, 0, 0), area, 4)
    screen.set_clip(None)

def displaySTexts(scoreT):
    "displays floating text for points and damage dealt that disappear after a while"
    for text in scoreT:
        text[2] += 1/60
        if text[2] <= 1:
            screen.blit(text[0], (text[1][0], text[1][1] - 20 * text[2]))
        else:
            scoreT.remove(text)

def displayScore(score):
    "displays player score"
    screen.blit(GUIFont.render(f"SCORE: {score}", True, (255, 255, 255)), (15, 5))

def displayGuns(index):
    "draws the menu for weapons"
    for i in range(len(weapons)):
        draw.rect(screen, (125, 125, 125), (40 + i * 64, height - 104, 64, 64))
        screen.blit(UI[2 + i], (40 + i * 64, height - 104))
        if i == index:
            draw.rect(screen, (255, 255, 255), (40 + i * 64, height - 104, 64, 64), 3)
        else:
            draw.rect(screen, (25, 25, 25), (40 + i * 64, height - 104, 64, 64), 3)
def renderLevel(level):
    "renders the level from the level file"
    for i in range(len(level)):
        for j in range(len(level[i])):
                screen.blit(tiles[int(level[i][j])], (64 * j - offX, 64 * i + offY))

def drawPlayer(player, kind, krect):
    "draws the player and weapon animations"
    mx, my = mouse.get_pos()
    ang = atan2(player[1] - my, player[0] - mx)

    screen.blit(playerIcons[0], (player[0] - 6, player[1] - 6))

    #knife animation
    if kind != -1:
        rotImg = transform.rotate(knife_anim[int(kind)], -degrees(ang) - 270)
        screen.blit(rotImg, ((player[0] + 32) - cos(ang) * 50 - rotImg.get_width() / 2, (player[1] + 32) - sin(ang) * 50 - rotImg.get_height() / 2))

def drawScene(level, player, bullets, enemyRect, enemyH, enemyType, enemyBullets, irect, itype, krect, scoreTemp, wInd, kind):
    "draws each frame of level, in the order of level -> bullets -> enemies -> player -> items -> user interface"
    renderLevel(level)

    #bullets
    for b in bullets:
        screen.blit(transform.rotate(bulletSprites[0], -degrees(b[4])), (int(b[0]) - offX, int(b[1]) + offY, 10, 10))
    for b in enemyBullets: 
        screen.blit(transform.rotate(bulletSprites[1], -degrees(b[4])), (int(b[0]) - offX, int(b[1]) + offY, 10, 10))

    #enemies
    for e in enemyRect:
        if enemyType[enemyRect.index(e)] != 5:
            rotatedImg = transform.rotate(zombieSprites[0], -degrees(atan2(e[1] - player[1], e[0] - player[0])))
            screen.blit(rotatedImg, (e[0] + 25 - rotatedImg.get_width() // 2, e[1] + 25 - rotatedImg.get_height() // 2))
        else:
            screen.blit(bossSprites[1], e)
            rotatedImg = transform.rotate(bossSprites[0], -degrees(atan2(e[1] - player[1], e[0] - player[0])))
            screen.blit(rotatedImg, (e[0] + 75 - rotatedImg.get_width() // 2, e[1] + 75 - rotatedImg.get_height() // 2))

    #player
    drawPlayer(player, kind, krect)

    #items
    for i in range(len(irect)):
        if itype[i] < 3:
            screen.blit(icons[itype[i]], irect[i])
        else:
            if len(weapons) < 4:
                screen.blit(UI[len(weapons) + 2], irect[i])

    #display UI
    displaySTexts(scoreTemp)
    displayScore(player[6])
    displayGuns(wInd)
    displayAmmo(player)
    displayHP(player, enemyRect, enemyH, enemyType)

    display.flip()

##### collision

def checkWallCollision(x, y, walls, length):
    "checks if an object collides with any wall"
    rectObj = Rect(x, y, length, length)
    return rectObj.collidelist(walls)

def checkEnCollision(x, y, enemyRect, index):
    "check collision of enemies with other enemies"
    rectObj = Rect(x, y, 50, 50)
    ER_no_E = enemyRect[:]; del ER_no_E[index]
    return rectObj.collidelist(ER_no_E)

def moveCam(player, level, dirX, dirY):
    "moves the map screen and changes the hitboxes of the walls for when the player moves to a different screen"
    #player for changing x pos, walls for changing wall pos, direction (1 for right or down, -1 for left or up) for moving screen
    global walls; walls = []
    if dirX != 0:
        if dirX == 1:
            player[0] = 0
        else:
            player[0] = width - 50
        global offX; offX += dirX * width
    if dirY != 0:
        if dirY == 1:
            player[1] = height - 50
        else:
            player[1] = 50
        global offY; offY += dirY * height
    walls = setupLevel(level)

def dropAmmo(rect, etype, irect, itype):
    "calculates how much ammo enemies should drop upon death, based on their type and rng"
    if etype == 0 and randint(1, 4) == 1:
        for i in range(randint(1, 2)):
            irect.append(Rect(rect[0] + randint(-50, 50), rect[1] + randint(-50, 50), 32, 32)); itype.append(0)
    if etype == 1 and randint(1, 2) == 1:
        for i in range(randint(2, 6)):
            irect.append(Rect(rect[0] + randint(-50, 50), rect[1] + randint(-50, 50), 32, 32)); itype.append(0)
    elif etype == 1:
        irect.append(Rect(rect[0] + randint(-50, 50), rect[1] + randint(-50, 50), 32, 32)); itype.append(0)
    if etype == 2:
        for i in range(2, 10):
            irect.append(Rect(rect[0] + randint(-50, 50), rect[1] + randint(-50, 50), 32, 32)); itype.append(0)
    if etype == 3:
        for i in range(4, 15):
            irect.append(Rect(rect[0] + randint(-50, 50), rect[1] + randint(-50, 50), 32, 32)); itype.append(0)
    if etype == 4:
        for i in range(10, 20):
            irect.append(Rect(rect[0] + randint(-50, 50), rect[1] + randint(-50, 50), 32, 32)); itype.append(0)

def checkColl(bullets, walls, player, level, enemyRect, enemyH, enemyType, enemyBullets, enemyWeaponSpeed, enemyMode, iRect, iType, krect, scoreT):
    "checks collision between all collidable objects in the game"
    ### bullets
    for b in bullets:
        brect = Rect(int(b[0]) - offX, int(b[1]) + offY, 10, 10)
        if checkWallCollision(b[0] - offX, b[1] + offY, walls, 10) != -1:
            bullets.remove(b)

        elif brect.collidelist(enemyRect) != -1:
            hitInd = brect.collidelist(enemyRect)
            enemyH[hitInd] -= randint(25, 35)
            if enemyH[hitInd] <= 0:
                dropAmmo(enemyRect[hitInd], enemyType[hitInd], iRect, iType)
                player[6] += 100 + 50 * enemyType[hitInd]
                scoreT.append([DSFont.render(f"+{100 + 50 * enemyType[hitInd]}", True, (255, 255, 255)), (enemyRect[hitInd][0], enemyRect[hitInd][1]), 0])
                del enemyRect[hitInd]; del enemyH[hitInd]; del enemyType[hitInd]; del enemyWeaponSpeed[hitInd]; del enemyMode[hitInd]
            bullets.remove(b)

    for b in enemyBullets:
        brect = Rect(int(b[0]) - offX, int(b[1]) + offY, 10, 10)
        if checkWallCollision(b[0] - offX, b[1] + offY, walls, 10) != -1:
            enemyBullets.remove(b)
        elif brect.colliderect(Rect(player[0], player[1], 50, 50)):
            player[4] -= randint(15, 25)
            enemyBullets.remove(b)

    #knife
    if krect != -1:
        if krect.collidelist(enemyRect) != -1:
            hitInd = krect.collidelist(enemyRect)
            enemyH[hitInd] -= randint(15, 20)
            if enemyH[hitInd] <= 0:
                dropAmmo(enemyRect[hitInd], enemyType[hitInd], iRect, iType)
                player[6] += 100 + 50 * enemyType[hitInd]
                scoreT.append([DSFont.render(f"+{100 + 50 * enemyType[hitInd]}", True, (255, 255, 255)), (enemyRect[hitInd][0], enemyRect[hitInd][1]), 0])
                del enemyRect[hitInd]; del enemyH[hitInd]; del enemyType[hitInd]; del enemyWeaponSpeed[hitInd]; del enemyMode[hitInd]

    #player and enemies
    if Rect(player[0], player[1], 50, 50).collidelistall(enemyRect) != []:
        player[4] -= 0.5 * len(Rect(player[0], player[1], 50, 50).collidelistall(enemyRect))

    #item collision    
    checkItemColl(player, iRect, iType)

    ###player and screen boundaries
    if player[0] > width - 50:
        moveCam(player, level, 1, 0)
        for e in enemyRect:
            e[0] -= 1024
        for item in iRect:
            item[0] -= 1024
    elif player[0] < 0:
        moveCam(player, level, -1, 0)
        for e in enemyRect:
            e[0] += 1024
        for item in iRect:
            item[0] += 1024
    if player[1] + 50 > height:
        moveCam(player, level, 0, -1)
        for e in enemyRect:
            e[1] -= 768
        for item in iRect:
            item[1] -= 768
    elif player[1] < 0:
        moveCam(player, level, 0, 1)
        for e in enemyRect:
            e[1] += 768
        for item in iRect:
            item[1] += 768

def checkItemColl(p, irect, itype):
    "checks for collision between player and items, and gives player the effects of those items"
    prect = Rect(p[0], p[1], 50, 50)
    collIndex = prect.collidelist(irect)

    if collIndex != -1:
        if itype[collIndex] == 0:
            player[5] += 1
            if settings[0] == True:
                mixer.Sound.play(ammoGet)
            player[6] += 25
        if itype[collIndex] == 1:
            if p[4] + 30 <= 250:
                p[4] += 30
            else:
                p[4] = 250
            if settings[0] == True:
                mixer.Sound.play(healthGet)
            player[6] += 250
        if itype[collIndex] == 2:
            player[7] = True
            if settings[0] == True:
                mixer.Sound.play(keyGet)
        if itype[collIndex] == 3:
            if len(weapons) < 4:
                saveData = open("resources/saveData.json", "r")
                data = loads(saveData.read())
                saveData.close()
                saveData = open("resources/saveData.json", "w")
                length = int(data['saveData']['progress'][0]['weapons'])
                #update
                del data['saveData']['progress'][0]['weapons']
                data['saveData']['progress'][0].update({'weapons':dumps(len(weapons) + 1)})
                saveData.write(dumps(data))
                saveData.close()
        del irect[collIndex]; del itype[collIndex]

##### movement

def moveBullets(bullets):
    "moves the bullet postions"
    for b in bullets[:]: #bullets[:] is a copy of the bullets list
        b[0] += b[2]
        b[1] += b[3]
        if b[0] > width + offX or b[0] < offX or b[1] > height - offY or b[1] < offY: #off screen
            bullets.remove(b)

def moveEnemy(enemyR, p, walls, index):
    "moves enemies based on player positions for moving type enemies"
    if 0 < enemyR[0] < 1024 and 0 < enemyR[1] < 768:
        if player[0] > enemyR[0] and checkWallCollision(enemyR[0] + 1, enemyR[1], walls, 50) == -1 and checkEnCollision(enemyR[0] + 1, enemyR[1], enemyRect, index) == -1:
            enemyR[0] += 1
        if player[0] < enemyR[0] and checkWallCollision(enemyR[0] - 1, enemyR[1], walls, 50) == -1 and checkEnCollision(enemyR[0] - 1, enemyR[1], enemyRect, index) == -1:
            enemyR[0] -= 1
        if player[1] < enemyR[1] and checkWallCollision(enemyR[0], enemyR[1] - 1, walls, 50) == -1 and checkEnCollision(enemyR[0], enemyR[1] - 1, enemyRect, index) == -1:
            enemyR[1] -= 1
        if player[1] > enemyR[1] and checkWallCollision(enemyR[0], enemyR[1] + 1, walls, 50) == -1 and checkEnCollision(enemyR[0], enemyR[1] + 1, enemyRect, index) == -1:
            enemyR[1] += 1

def enemyFireRate(enemyBullets, enemyType, enemyMode):
    "calculates whether a shooting enemy can shoot in the current frame"
    global enemyWeaponSpeed
    for i in range(len(enemyWeaponSpeed)):
        if enemyWeaponSpeed[i] != -1:
            if enemyWeaponSpeed[i] == 4 * weaponsList[enemyType[i]][1] and enemyWeaponSpeed[i] != -1 and enemyMode[i] == 1:
                if enemyType[i] != 2:
                    enemyBullets.append(shoot(0, 0, enemyRect[i], -1, player, True))
                else:
                    for j in range(3):
                        enemyBullets.append(shoot(0, 0, enemyRect[i], j, player, True))
                enemyWeaponSpeed[i] = 0
            elif enemyWeaponSpeed[i] != -1 and enemyWeaponSpeed[i] < 4 * weaponsList[enemyType[i]][1]:
                enemyWeaponSpeed[i] += 1

def move(player, walls, bullets, enemyRect, enemyType, enemyBullets, enemyMode, enemyHealth, enemyWeaponSpeed):
    "allows player to move, calls bullet moving functions, and tells enemies what to do"
    #player movement
    keys = key.get_pressed()
    if keys[K_LSHIFT] or keys[K_SPACE] or keys[K_RSHIFT]:
        player[2] = player[3] = 8
    else:
        player[2] = player[3] = 4

    if settings[1] == True:
        if keys[K_d] and checkWallCollision(player[0] + player[2], player[1], walls, 50) == -1:
            player[0] += player[2]
        if keys[K_a] and checkWallCollision(player[0] - player[2], player[1], walls, 50) == -1:
            player[0] -= player[2]
        if keys[K_s] and checkWallCollision(player[0], player[1] + player[3], walls, 50) == -1:
            player[1] += player[3]
        if keys[K_w] and checkWallCollision(player[0], player[1] - player[3], walls, 50) == -1:
            player[1] -= player[3]
    else:
        if keys[K_RIGHT] and checkWallCollision(player[0] + player[2], player[1], walls, 50) == -1:
            player[0] += player[2]
        if keys[K_LEFT] and checkWallCollision(player[0] - player[2], player[1], walls, 50) == -1:
            player[0] -= player[2]
        if keys[K_DOWN] and checkWallCollision(player[0], player[1] + player[3], walls, 50) == -1:
            player[1] += player[3]
        if keys[K_UP] and checkWallCollision(player[0], player[1] - player[3], walls, 50) == -1:
            player[1] -= player[3]

    #bullet movement
    moveBullets(bullets)
    moveBullets(enemyBullets)

    #enemies
    for i in range(len(enemyRect)):
        if enemyType[i] == 0 or enemyType[i] == 4:
            moveEnemy(enemyRect[i], player, walls, i)
        if enemyType[i] == 5:
            bossAttack(enemyRect[i], enemyMode[i], enemyRect, enemyType, enemyMode, enemyHealth, enemyBullets, enemyWeaponSpeed)
        elif enemyType[i] != 0 and enemyMode[i] == 1:
            enemyFireRate(enemyBullets, enemyType, enemyMode)

def bossAttack(rect, mode, enemyRect, enemyType, enemyMode, enemyHealth, enemyBullets, enemyWeaponSpeed):
    "either fires a laser attack or spawns more enemies based on mode, rng, and how many enemies are currently spawned"
    if mode == 1 and randint(1, 4) == 1: #laser attack
        enemyBullets.append(shoot(0, 0, rect, -1, player, True))
    elif mode == 0 and len(enemyRect) == 1 and randint(1,3) == 1: #spawn more enemies
        for i in range(4):
            enemyRect.append(Rect([(2204 - offX, 128, 50, 50), (2204 - offX, 640, 50, 50), (2904 - offX, 640, 50, 50), (2904 - offX, 128, 50, 50)][len(enemyRect) - 2]))
            types = randint(0,1)
            enemyType.append(types)
            enemyMode +=  [randint(0, 1) if types != 0 else -1]
            enemyHealth += [enemyMax[types]]
            enemyWeaponSpeed += [4 * weaponsList[types][1] if types != 0 and types < 4 else -1]

def shoot(mx, my, pos, i, player, en):
    "creates bullet list for player and enemy shooting"
    if en == False: #player shooting
        if settings[0] == True:
            mixer.Sound.play(plShoot)
        player[5] -= 1
        ang = atan2(my - (pos[1] + 25), mx - (pos[0] + 25))
        if i == -1:
            vx = cos(ang) * speed + radians(randint(-15, 15))
            vy = sin(ang) * speed + radians(randint(-15, 15))
        else:
            vx = cos(ang - 0.1745 + 0.1745 * i) * speed
            vy = sin(ang - 0.1745 + 0.1745 * i) * speed
    else: #enemy shooting
        #check if on screen
        if 0 < pos[0] < 1024 and 0 < pos[1] < 768:
            if settings[0] == True:
                mixer.Sound.play(enShoot)
        ang = atan2(player[1] - pos[1], player[0] - pos[0])
        if i == -1:
            vx = cos(ang) * speed / 2  + radians(randint(-25, 25))
            vy = sin(ang) * speed / 2  + radians(randint(-25, 25))
        else:
            #0.1745 is an approximation of 10 degrees in radians
            vx = cos(ang - 0.1745 + 0.1745 * i) * speed / 2
            vy = sin(ang - 0.1745 + 0.1745 * i) * speed / 2
    return [pos[0] + offX, pos[1] - offY, vx, vy, ang]

def knife(p, mx, my):
    "calculates the knife hitbox"
    ang = atan2(my - p[1], mx - p[0])
    x = 50 * cos(ang)
    y = 50 * sin(ang)
    return Rect(p[0] + x, p[1] + y, 50, 50)

def timer(mode):
    "switches enemy modes based on a global 3 second timer"
    rl = []
    global timerTime
    
    timerTime += 1/60
    
    if timerTime >= 3:
        timerTime = 0

        for i in range(len(mode)):
            if mode[i] == -1: 
                rl.append(-1)
            elif mode[i] == 0:
                rl.append(1)
            elif mode[i] == 1:
                rl.append(0)
        return rl
    return mode

def level():
    "main game loop, runs for all levels changing the map and enemy placements using the levelData file and level index"
    running = True
    saveData = open("resources/saveData.json", "r")
    data = loads(saveData.read())

    levelIndex = int(data['saveData']['progress'][0]['level'])
    startWeapons = data['saveData']['progress'][0]['weapons']

    #reset camera offsets
    global offX; offX = 0
    global offY; offY = 0
    try:
        global walls; walls = setupLevel(levelMaps[levelIndex])
    except:
        lol = mixer.Sound("resources/error.mp3")
        mixer.Sound.play(lol)
    
    #load ammo and score from previous level or session
    player[6] = int(data['saveData']['progress'][0]['score'])
    player[5] = int(data['saveData']['progress'][0]['ammo'])
    global weapons
    wInd = int(data['saveData']['progress'][0]['wInd']) #weapon list index
    weaponSpeed = 0

    saveData.close()

    bullets = []
    krect = -1
    kind = -1

    #change to True when in boss room
    bossTrigger = False

    #load level specific data from file
    levelDataFile = open("resources/levelData.json", "r")
    levelData = loads(levelDataFile.read())

    #loads the positions of the items from the levelData file
    itemRect = [item.split(",") for item in [levelData['levelData'][str(levelIndex)][0]['itemRect'][0][str(i)] for i in range(len(levelData['levelData'][str(levelIndex)][0]['itemRect'][0]))]]
    for i in range(len(itemRect)):
        for j in range(len(itemRect[i])):
            itemRect[i][j] = int(itemRect[i][j])

    itemRect = [Rect(item) for item in itemRect]
    #loads the types of the items from the levelData file
    itemType = [int(item) for item in [levelData['levelData'][str(levelIndex)][0]['itemType'][0][str(i)] for i in range(len(levelData['levelData'][str(levelIndex)][0]['itemType'][0]))]]

    enemyBullets = []
    #loads the positions of the enemies from the levelData file
    global enemyRect
    enemyRect = [item.split(",") for item in [levelData['levelData'][str(levelIndex)][0]['enemyRect'][0][str(i)] for i in range(len(levelData['levelData'][str(levelIndex)][0]['enemyRect'][0]))]]
    for i in range(len(enemyRect)):
        for j in range(len(enemyRect[i])):
            enemyRect[i][j] = int(enemyRect[i][j])

    enemyRect = [Rect(enemy) for enemy in enemyRect]
    #loads the types of the enemies from the levelData file
    enemyType = [int(item) for item in [levelData['levelData'][str(levelIndex)][0]['enemyType'][0][str(i)] for i in range(len(levelData['levelData'][str(levelIndex)][0]['enemyType'][0]))]]

    #calculates health, weapon speed, and mode based on type
    enemyH = [enemyMax[i] for i in enemyType]
    global enemyWeaponSpeed; enemyWeaponSpeed = [4 * weaponsList[i][1] if i != 0 and i < 4 else -1 for i in enemyType]
    global enemyMode; enemyMode = [randint(0, 1) if i != 0 else -1 for i in enemyType]

    levelDataFile.close()

    #temporary score text pop-up objects
    scoreTemp = []

    #play game music
    mixer.music.stop()
    mixer.music.load("resources/gameTheme.ogg")
    mixer.music.play(-1)

    clock = time.Clock()
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                if startWeapons != data['saveData']['progress'][0]['weapons']:
                    saveData = open("resources/saveData.json", "w")
                    del data['saveData']['progress'][0]['weapons']
                    data['saveData']['progress'][0].update({'weapons':dumps(int(startWeapons))})
                    saveData.write(dumps(data))
                    saveData.close()
                return "exit"
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 5:
                    wInd = (wInd + 1) % len(weapons)
                    weaponSpeed = 0
                if evt.button == 4:
                    wInd = (wInd - 1 + len(weapons)) % len(weapons)
                    weaponSpeed = 0

        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        if weaponSpeed < weapons[wInd][1]:
            weaponSpeed += 1
            krect = -1
        if mb[0] and weaponSpeed == weapons[wInd][1] and player[5] > 0 and wInd != 0:
            weaponSpeed = 0
            if wInd != 2:
                bullets.append(shoot(mx, my, player, -1, player, False))
            elif wInd == 2 and player[5] >= 3:
                for i in range(3):
                    bullets.append(shoot(mx, my, player, i, player, False))
        elif mb[0] and wInd == 0 and weaponSpeed == weapons[wInd][1]:
            krect = knife(player, mx, my)
            weaponSpeed = 0
            kind = 0

        if 0 <= kind < 5:
            kind += 0.5
        elif kind <= 5:
            kind = -1

        drawScene(levelMaps[levelIndex], player, bullets, enemyRect, enemyH, enemyType, enemyBullets, itemRect, itemType, krect, scoreTemp, wInd, kind)
        enemyMode = timer(enemyMode)
        move(player, walls, bullets, enemyRect, enemyType, enemyBullets, enemyMode, enemyH, enemyWeaponSpeed)
        checkColl(bullets, walls, player, levelMaps[levelIndex], enemyRect, enemyH, enemyType, enemyBullets, enemyWeaponSpeed, enemyMode, itemRect, itemType, krect, scoreTemp)

        saveData = open("resources/saveData.json", "r")
        data = loads(saveData.read())
        weapons = weaponsList[:int(data['saveData']['progress'][0]['weapons'])]
    
        if levelIndex == 6:
            if player[0] + offX >= 2112 and bossTrigger == False:
                mixer.music.stop()
                mixer.music.load("resources/finalBossTheme.ogg")
                mixer.music.play(-1)
                mixer.Sound.play(bossAppears)
                levelIndex += 1
                walls = setupLevel(levelMaps[levelIndex])
                bossTrigger = True
        if player[4] <= 0:
            if settings[0] == True:
                mixer.Sound.play(death)
            if startWeapons != data['saveData']['progress'][0]['weapons']:
                saveData.close()
                saveData = open("resources/saveData.json", "w")
                del data['saveData']['progress'][0]['weapons']
                data['saveData']['progress'][0].update({'weapons':dumps(int(startWeapons))})
                saveData.write(dumps(data))
                saveData.close()
            return "gameover"
        if enemyRect == []:
            #add win item to list
            itemRect.append(Rect(width / 2, height / 2, 32, 32))
            itemType.append(2)
        if player[7] == True:
            player[7] = not player[7]
            saveData.close()
            saveData = open("resources/saveData.json", "w")
            #save progress
            #level index
            if levelIndex != 7:
                del data['saveData']['progress'][0]['level']
                data['saveData']['progress'][0].update({'level':dumps(levelIndex + 1)})
            else:
                del data['saveData']['progress'][0]['level']
                data['saveData']['progress'][0].update({'level':dumps(1)})
                del data['saveData']['progress'][0]['complete']
                data['saveData']['progress'][0].update({'complete':dumps(True)})
            #weapon index
            del data['saveData']['progress'][0]['wInd']
            data['saveData']['progress'][0].update({'wInd':dumps(wInd)})
            #score
            del data['saveData']['progress'][0]['score']
            data['saveData']['progress'][0].update({'score':dumps(player[6])})
            #ammo
            del data['saveData']['progress'][0]['ammo']
            data['saveData']['progress'][0].update({'ammo':dumps(player[5])})
            saveData.write(dumps(data))
            saveData.close()
            return "win"
        saveData.close()
        clock.tick(60)

######################################### WIN SCREEN #########################################

def winScreen():
    #allow user to go to next level or menu
    running = True
    buttons = [Rect(312, 420 + x * 120, 400, 100) for x in range(2)]

    saveData = open("resources/saveData.json", "r")
    data = loads(saveData.read())
    saveData.close()

    winText = UIFont.render("You Win!", True, (255, 255, 255))
    thank = UIFont.render("Thanks For Playing", True, (255, 255, 255))
    ggText = UIFont.render(f"Level {int(data['saveData']['progress'][0]['level']) - 1} Cleared", True, (255, 255, 255))

    buttonTexts = [UIFont.render(word, True, (0, 0, 0)) for word in ["Next", "Menu"]]
    textPos = [(buttons[i][0] + ((buttons[i][2] - buttonTexts[i].get_width()) / 2), buttons[i][1] + ((buttons[i][3] - buttonTexts[i].get_height()) / 2)) for i in range(len(buttons))]

    player[0] = width / 2; player[1] = height / 2

    mixer.music.stop()
    mixer.music.load("resources/mainTheme.ogg")
    mixer.music.play(-1)

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        screen.blit(sceneBG, (0, 0))
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        for i in range(len(buttons)):
            screen.blit(button, buttons[i])
            screen.blit(buttonTexts[i], textPos[i])
        if data['saveData']['progress'][0]['complete'] == "true":
            screen.blit(winText, (335, 100))
            screen.blit(thank, (150, 200))
        else:
            screen.blit(ggText, (210, 100))
        if mb[0]:
            if buttons[0].collidepoint(mx, my):
                if settings[0] == True:
                    mixer.Sound.play(select)
                return "level"
            if buttons[1].collidepoint(mx, my):
                if settings[0] == True:
                    mixer.Sound.play(select)
                return "menu"

        display.flip()

######################################### GAME OVER SCREEN #########################################

def gameOver():
    running = True
    buttons = [Rect(312, 420 + x * 120, 400, 100) for x in range(2)]

    buttonTexts = [UIFont.render(word, True, (0, 0, 0)) for word in ["Retry", "Menu"]]
    textPos = [(buttons[i][0] + ((buttons[i][2] - buttonTexts[i].get_width()) / 2), buttons[i][1] + ((buttons[i][3] - buttonTexts[i].get_height()) / 2)) for i in range(len(buttons))]

    ltext = UIFont.render("You Died", True, (255, 255, 255))
    player[4] = 250; player[0] = width / 2; player[1] = height / 2

    mixer.music.stop()
    mixer.music.load("resources/mainTheme.ogg")
    mixer.music.play(-1)

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "exit"

        screen.blit(sceneBG, (0, 0))
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        screen.blit(ltext, (340, 100))
        for i in range(len(buttons)):
            screen.blit(button, buttons[i])
            screen.blit(buttonTexts[i], textPos[i])
        if mb[0]:
            if buttons[0].collidepoint(mx, my):
                if settings[0] == True:
                    mixer.Sound.play(select)
                return "level"
            if buttons[1].collidepoint(mx, my):
                if settings[0] == True:
                    mixer.Sound.play(select)
                return "menu"

        display.flip()

page = "menu"

while page != "exit":
    if page == "level":
        page = level()
    if page == "win":
        page = winScreen()
    if page == "gameover":
        page = gameOver()
    if page == "settings":
        page = settingsPage()
        settings = loadSettings(data)
    if page == "instructions":
        page = instructions()
    if page == "menu":
        page = menu()

levelFile.close()
quit()
