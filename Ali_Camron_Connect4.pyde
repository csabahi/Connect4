import pickle


def loadFileInfo(fileName):
    file = open(fileName)
    fileInfo = []
    text = file.readlines()

    for line in text:
        line = line.strip()
        line = line.split(",")
        fileInfo.append(line)

    file.close()

    return fileInfo

def setup():
    global screenWidth, screenHeight, gameControlKeys, gameKey, winScreen, otherScreen, exitted, exitButton, exitX, exitY, exitWidth, exitHeight
    global asciList, whichKey, controlKeys, scrollKeys, bannedUKey, bannedDKey, nameIn, nameIn2, nameLimit, nameCount, nameCount2
    global bg_Menu, Menu_all, Menu_options, Menu_start, Menu_help, Menu_score, backbutton_on, backbutton_off, endFont, Board, currentBoard, Coin, Scores
    global mode, PrevMode, menuWidth, menuHeight, endFont, playAgain, menuPressed, filename, grid_7x6, grid_9x6, options, options_7x6, options_9x6, help
    global dropdown_mainMenu, dropdown_options, dropdown_scoreboard, dropdown_help, dropdown_none, dropdown_all, menuExpand
    global gridBg, checkDirections, x, y, w, h, cols, rows, startX, startY, slotgap, diam, slotSize, value, scoresList, scrollKeys, scoresList
    global yspeed, gameScreenHeight, addCoin, checkWin, noWin, numCols, numRows, gridList, fillColours, player1, colours, newCoinY, inactiveCols
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, newCoinCol, newCoinRow, played, turnCount, names
    global arrow, arrowY, arrowW, arrowH, arrowPointer, drawBoard, bouncingCoin, drawCoins, newCoinX, newCoinY, bounced, slotgap, fileList, gameScreenWidth, startLocY
    global manInfo, manX, manY, manW, manH, showMan, paraBg, screenWidth, screenHeight, xincr, yincr, portal, portalInfo, portalX, portalY, portalW, portalH, portalincrx, landed, Buttons
    global scoresList, fileName, sortScores, placeScore

    size(1000, 700)
   
    #****** -- Pickle -- ******#
   
    fileName = "scoresList.txt"
   
    try:
       # with open(fileName, 'rb') as pickleFile:
        scoresList = pickle.load(open(fileName, "rb"))
           # pickleFile.close
    except Exception:
        scoresList = [ [], [] ]
       
    
    def sortScores(listToSort):
        print(scoresList)
        limitI = len(listToSort[1]) - 1
        limitJ = len(listToSort[1])
        for i in range(limitI):
            itemToMove = i
            for j in range(itemToMove, limitJ):
                if listToSort[1][itemToMove] > listToSort[1][j]:
                    itemToMove = j
            listToSort[0].insert(i, listToSort[0].pop(itemToMove))
            listToSort[1].insert(i, listToSort[1].pop(itemToMove))
   
        return listToSort
   
   
    def placeScore(listToSort, name, score):
        if name in listToSort[0]:
            nameInd = listToSort[0].index(name)
            if score < listToSort[1][nameInd]:
                listToSort[1][nameInd] = score
        else:
            listToSort[1].insert( - 1, score)
            listToSort[0].insert( - 1, name)
        return listToSort

    #****** -- Variables for Exit Game -- ******#
   
    screenWidth = 1000
    screenHeight = 700
   
    paraLeft = loadImage('paragliderLeft.png')
    paraRight  = loadImage('paragliderRight.png')
    paraBg = loadImage('mountain-g8600679b9_1920.png')
    portal = loadImage('portal.png')
    winScreen = loadImage('win.png')
    otherScreen = loadImage('lastScreen.jpeg')
   
    portalX = 0
    portalY = 1
    portalW = 2
    portalH = 3
    portalincrx = 4

    portalInfo = [ screenWidth/2, screenHeight - 50 - 3, 100, 50, 6]

    gameControlKeys = [ LEFT, RIGHT ]
    gameKey = ""
   
    manX = 2
    manY = 3
    manW = 4
    manH = 5
    xincr = 6
    yincr = 7
   
   
    manInfo = [ paraRight, paraRight, screenWidth / 2 - 125/2, 0, 125, 125, 0, 4 ]
    showMan = manInfo[ 1 ]
   
    exitButton = loadImage('exitButton.png')
    exitX = 900
    exitY = 0
    exitWidth = 100
    exitHeight = 40
    exitted = False

   
    landed = False

    frameRate(120)

    # All the setup for the game only ****************************************
    fileList = loadFileInfo('boardInfo.txt')

    for i in range(len(fileList)):
        for j in range(2, len(fileList[0])):
            fileList[i][j] = int(fileList[i][j])

    currentBoard = fileList[ 0 ]

    scoresFile = "scoresList.txt"

    board = 0

    arrowImage = fileList[board][1]

    x = 2
    y = 3
    w = 4
    h = 5
    cols = 6
    rows = 7
    startX = 8
    startY = 9
    slotSize = 10
    diam = 11
    slotgap = 12
   

    gameScreenWidth = 999
    gameScreenHeight = 599

    newCoinY = 100

    turnCount = [0, 0]

    played = False

    newCoinCol = -1
    newCoinRow = -1

    arrow = loadImage(arrowImage)

    arrowY = 82
    arrowW = 75
    arrowH = 45

    gridList = [[''] * currentBoard[ rows ] for i in range( currentBoard[ cols ])]

    noWin = True
    player1 = False

    colours = ['Red', 'Blue']
    fillColours = [(255, 0, 0), (0, 0, 255)]
    Turns = [0, 0]

    checkDirections = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    newCoinX = 0
    newCoinY = arrowY
    yspeed = 0.0
    bounced = 0

    startLocX = currentBoard[ startX ]
    startLocY = arrowY + arrowW

    allBoundaries = []

    for i in range(currentBoard[ cols ]):
        upperLeft = [startLocX, startLocY]
        lowerRight = [ startLocX + currentBoard[ slotSize ], startLocY + currentBoard[ startY ] + currentBoard[ diam ] ]
        clickBoundary = [upperLeft, lowerRight]
        allBoundaries.append(clickBoundary)
        startLocX += currentBoard[ slotSize ]

    whichBoundary = -1
    numBoundaries = len(allBoundaries)
    removeBoundary = False
    activeBoundaries = [True for i in range(numBoundaries)]
    inactiveCols = []

    ##***** Classes for Game *****#
    class Board:
        global x, y, w, h, cols, rows, startX, startY, slotSize, diam

        def __init__(self, fileList, gridList, newCoinCol, newCoinRow, checkDirections, noWin):

            #**** don't need these instance variables because all this information was taken from the file list so only need to pass that *****#
            self.file = fileList
            self.grid = gridList
            self.col = newCoinCol
            self.row = newCoinRow
            self.directions = checkDirections
            self.Xincr = 0
            self.Yincr = 1
            self.win = noWin
            self.connections = 0
        def drawBoard(self):
           
            for i in range( len( self.grid ) ):
                for j in range( len( self.grid[ i ]) ):
                    if self.grid[ i ][ j ] == 'Red':
                        fill(255, 0, 0)
                        circle(self.file[ startX ] + self.file[ slotSize ] * i + self.file[ diam ] / 2, self.file[ startY ] - self.file[ slotSize ] * j - self.file[ slotgap ] * j - self.file[ diam ] / 2, self.file[ diam ])

                    elif self.grid[ i ][ j ] == 'Blue':
                        fill(0, 0, 255)
                        circle(self.file[ startX ] + self.file[ slotSize ] * i + self.file[ diam ] / 2, self.file[ startY ] - self.file[ slotSize ] * j - self.file[ slotgap ] * j - self.file[ diam ] / 2, self.file[ diam ])
               

            image(loadImage(self.file[0]), self.file[ 2 ], self.file[ 3 ], self.file[ 4 ], self.file[ 5 ])

        def checkWin(self):
            global activeBoundaries
            for i in range(len(self.directions)):
                self.connections = 0
                self.col = newCoinCol
                self.row = newCoinRow
                while 0 <= self.col + self.directions[ i ][ self.Xincr ] < self.file[ cols ] and 0 <= self.row + self.directions[ i ][ self.Yincr ] < self.file[ rows ] and self.grid[ self.col ][ self.row ] == self.grid[ self.col + self.directions[ i ][ self.Xincr ] ][ self.row + self.directions[ i ][ self.Yincr ] ]:
                    self.connections += 1

                    if self.connections == 3:
                        break
                    self.col += self.directions[i][self.Xincr]
                    self.row += self.directions[i][self.Yincr]

                if self.connections == 3:
                    self.win = False
                    for i in range(self.file[ cols ]):
                        activeBoundaries[ i ] = False
                        print('connected 4. Game Done')

                    break

            return(self.win)

    x = Board(currentBoard, gridList, newCoinCol, newCoinRow, checkDirections, noWin)

    class Coin:
        global x, y, w, h, cols, rows, startX, startY, ss, diam

        def __init__(self, newCoinCol, inactiveCols, newCoinRow, newCoinX, fileList, gridList, noWin, activeBoundaries, arrowY, colours, player1, bounced, yspeed):
            self.newCoinCol = newCoinCol
            self.inactiveCols = inactiveCols
            self.newCoinRow = newCoinRow
            self.file = fileList
            self.grid = gridList
            self.win = noWin
            self.boundaries = activeBoundaries
            self.newCoinX = newCoinX
            self.newCoinY = newCoinY
            self.colours = colours
            self.player = player1
            self.yspeed = yspeed
            self.bounced = bounced
            self.arrowY = arrowY

        def addCoin(self):
            self.bounced = 0
            for i in range(self.file[ rows ]):
                if self.grid[ self.newCoinCol ][ i ] == '':
                    self.newCoinRow = i
                    if i == self.file[ rows ] - 1 and self.win:
                        self.boundaries[ self.newCoinCol ] = False
                        self.inactiveCols.append(self.newCoinCol)

                    break

            self.newCoinX = self.file[ startX ] + self.newCoinCol * self.file[ slotSize ] + self.file[ diam ] / 2
            return (self.grid, self.boundaries, self.inactiveCols, self.newCoinX, self.newCoinY, self.newCoinRow, self.bounced)
                       
        def bouncing(self):
            if self.newCoinCol != -1:
               
                if (self.newCoinY + self.file[ diam ] / 2 >= self.file[ startY ] - self.file[ slotSize ] * self.newCoinRow - self.file[ diam ] / 3):
                    self.newCoinY = self.file[ startY ] - self.file[ slotSize ] * self.newCoinRow - self.file[ diam ]
                    self.yspeed = -self.yspeed / 2
                    self.bounced = self.bounced + 1
                   
                self.yspeed += 10
                self.newCoinY += self.yspeed

                if self.bounced < 3:

                    fill(fillColours[ player1 ][ 0 ], fillColours[ player1 ][ 1 ], fillColours[ player1 ][ 2 ])
                    circle(self.newCoinX, self.newCoinY, self.file[ diam ])
                    x = Board(currentBoard, gridList, newCoinCol, newCoinRow, checkDirections, noWin)
                    x.drawBoard()
                    for i in range(self.file[ cols ]):
                        self.boundaries[ i ] = False
                else:
                    self.grid[ self.newCoinCol ][ self.newCoinRow ] = self.colours[ self.player ]
                    x = Board(currentBoard, gridList, newCoinCol, newCoinRow, checkDirections, noWin)
                    self.win = x.checkWin()
                    for i in range(self.file[ cols ]):
                        self.boundaries[ i ] = True
                    for i in self.inactiveCols:
                        self.boundaries[ i ] = False

                    self.newCoinCol = -1
                    self.newCoinY = self.arrowY

            return (self.win, self.newCoinCol, self.newCoinY, self.bounced, self.yspeed)
       
       
    class Buttons:
       
        def __init__(self, menuWidth, mode, PrevMode, menuExpand):
            self.Width = menuWidth
            self.mode = mode
            self.menuExpand = menuExpand
            self.x = mouseX
            self.y = mouseY
            self.preMode = PrevMode
       
        def menuButtons(self):
            if self.mode == "Menu":
                if 450 < self.x < 450 + self.Width and 250 < self.y < 325:
                    self.mode = "Start1"
                if 450 < self.x < 450 + self.Width and 325 < self.y < 400:
                    self.mode = "Options"
                if 450 < self.x < 450 + self.Width and 400 < self.y < 475:
                    self.mode = "Score"
                if 450 < self.x < 450 + self.Width and 475 < self.y < 550:
                    self.mode = "Help"
       
            if self.mode == "Menu":
                if 450 < self.x < 450 + self.Width and 250 < self.y < 325:
                    self.mode = "Start1"
                if 450 < self.x < 450 + self.Width and 325 < self.y < 400:
                    self.mode = "Options"
                if 450 < self.x < 450 + self.Width and 400 < self.y < 475:
                    self.mode = "Score"
                if 450 < self.x < 450 + self.Width and 475 < self.y < 550:
                    self.mode = "Help"
       
            if self.mode == "Help":
                if 450 < self.x < 600 and 575 < self.y < 675:
                    if PrevMode == "Play":
                        self.mode = "Play"
                    else:
                        self.mode = "Menu"
       
            if self.mode == "Options":
                print('options')
                if 400 < self.x < 600 and 575 < self.y < 675:
                    self.mode = "Menu"
                elif 120 < self.x < 460 and 180 < self.y < 520:
                    currentBoard, gridList, activeBoundaries, inactiveCols = setUpGame( 0 )
                    x = Board(currentBoard, gridList, newCoinCol, newCoinRow, checkDirections, noWin)
       
                elif 500 < self.x < 875 and 180 < self.y < 520:
                    currentBoard, gridList, activeBoundaries, inactiveCols = setUpGame( 1 )
                    x = Board(currentBoard, gridList, newCoinCol, newCoinRow, checkDirections, noWin)
       
            if self.mode == "Play":
                if 400 < self.x < 600 and 74 <= self.y <= 110 and menuExpand == True:
                    self.mode = "Menu"
                    self.preMode = "Play"
                if 400 < self.x < 600 and 111 <= self.y <= 152 and menuExpand == True:
                    self.mode = "Options"
                    self.preMode = "Play"
                if 400 < self.x < 600 and 153 <= self.y <= 196 and menuExpand == True:
                    self.mode = "Score"
                if 400 < self.x < 600 and 197 <= self.y <= 237 and menuExpand == True:
                    self.mode = "Help"
                    self.preMode = "Play"
       
            if self.mode == "Score":
                if 400 < self.x < 600 and 575 < self.y < 675:
                    value = 0          
                    if PrevMode == "Play":
                        self.mode = "Play"
                    elif PrevMode == "Menu":
                        self.mode = "Menu"
       
            if self.mode == "Start1":
                if 400 < self.x < 600 and 575 < self.y < 675:
                    self.mode = "Menu"
       
            if self.mode == "Start2":
                if 400 < self.x < 600 and 575 < mouseY < 675:
                    self.mode = "Start1"
           
            return (self.mode, self.preMode )

    #****** --  All the setup for the menus -- ******#

    bg_Menu = loadImage("connect4_bg.jpg")
    asciList = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890"
    controlKeys = [ENTER, BACKSPACE]
    scrollKeys = [ UP, DOWN ]
    whichKey = ''
    bannedUKey = ''
    bannedDKey = ''
    nameIn = ""
    nameIn2 = ""
   
    names = []
       
    nameLimit = 10
    nameCount = 0
    nameCount2 = 0

    size(1000, 700)
    screenWidth = 999
    screenHeight = 699

    mode = "Menu"
    PrevMode = "Menu"
    menuWidth = 500
    menuHeight = 300

    playAgain = False
    menuPressed = False

    filename = 'scoreboard'

    Menu_all = loadImage("c4_allMenu.png")
    Menu_options = loadImage("c4_optionsOn.png")
    Menu_score = loadImage("c4_scoreOn.png")
    Menu_start = loadImage("c4_startOn.png")
    Menu_help = loadImage("c4_helpOn.png")

    menuExpand = False

    dropdown_none = loadImage("gameMenu_none.png")
    dropdown_all = loadImage("gameMenu_all.png")
    dropdown_mainMenu = loadImage("gameMenu_mainMenu.png")
    dropdown_options = loadImage("gameMenu_options.png")
    dropdown_scoreboard = loadImage("gameMenu_scoreboard.png")
    dropdown_help = loadImage("gameMenu_help.png")

    backbutton_on = loadImage("backbutton_on.png")
    backbutton_off = loadImage("backbutton_off.png")

    grid_7x6 = loadImage("7x6_grid.png")
    grid_9x6 = loadImage("9x6_grid.png")

    options = loadImage("Options_nonSelected.png")
    options_7x6 = loadImage("Options_7x6.png")
    options_9x6 = loadImage("Options_9x6.png")

    help = loadImage("rules.jpg")
    value = 0

    # scoresList = [ [], [] ]

    #****** --  Functions needed for game -- ******#

def binarySearch( myList, searchItem ):
    bottom = 0
    top = len(myList) - 1
    middle = (bottom + top)//2
   
    while ( myList[middle] != searchItem ) and ( top != bottom ) :
        if searchItem > list[middle]:
            bottom = middle + 1
        else:
            top = middle - 1
        middle = ( bottom + top ) // 2
       
    if myList[middle] == searchItem:
        return middle
   
    return ( middle )


def mouseReleased():
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, newCoinCol, played
    global x, y, w, h, cols, rows, startX, startY, ss, diam

    validLocation = False

    for i in range(currentBoard[ cols ]):
        if activeBoundaries[i]:
            validXRange = allBoundaries[i][0][0] <= mouseX <= allBoundaries[i][1][0]
            validYRange = allBoundaries[i][0][1] <= mouseY <= allBoundaries[i][1][1]
            validLocation = validXRange and validYRange
            if validLocation:
                played = True
                whichBoundary = i
                newCoinCol = i
                break

#***** add as a method to the board class *****#
def arrowPointer():
    global arrow, arrowY, arrowW, arrowH
    global x, y, w, h, cols, rows, startX, startY, ss, diam

    arrowX = mouseX - arrowW / 2
    if arrowX < currentBoard[ startX ] + currentBoard[ diam ]/2:
        arrowX = currentBoard[ startX ] + currentBoard[ diam ]/2 - arrowW / 2
    elif arrowX > currentBoard[ startX ] + currentBoard[ diam ]/2 + currentBoard[ slotSize ] * (currentBoard[ cols ] - 1) - arrowW / 2:
        arrowX = currentBoard[ startX ] + currentBoard[ diam ]/2 + currentBoard[ slotSize ] * (currentBoard[ cols ] - 1) - arrowW / 2
    image(arrow, arrowX, arrowY, arrowW, arrowH)


def setUpGame(chosenBoard):
    global gridImage, arrowImage, gridWidth, gridHeight, numCols, numRows, startSlotX, gridList
    global startSlotY, slotSize, coinDiameter, slotgap, coinRadius, allBoundaries, gridBg
    global whichBoundary, activeBoundaries, inactiveCols, fileList, gameScreenWidth, startLocY, currentBoard
    global x, y, w, h, cols, rows, startX, startY, slotgap, diam

    currentBoard = fileList[ chosenBoard ]

    gridImage =  currentBoard[0]
    arrowImage = currentBoard[1]
   
    gridList = [[''] * currentBoard[ rows ] for i in range( currentBoard[ cols ])]

    turnCount = [0, 0]
    startLocX = currentBoard[ startX ]
    gridBg = loadImage(gridImage)

    allBoundaries = []

    for i in range(currentBoard[ cols ]):
        upperLeft = [startLocX, startLocY]
        lowerRight = [ startLocX + currentBoard[ slotSize ], startLocY + currentBoard[ startY ] + currentBoard[ diam ] ]
        clickBoundary = [upperLeft, lowerRight]
        allBoundaries.append(clickBoundary)
        startLocX += currentBoard[ slotSize ]

    whichBoundary = -1
    numBoundaries = len(allBoundaries)
    removeBoundary = False
    activeBoundaries = []
    activeBoundaries = [False for i in range(numBoundaries)]
    inactiveCols = []
   
    return( currentBoard, gridList, activeBoundaries, inactiveCols )

    #****** -- Function to run Exit Game -- ******#
   
def boundaryCheck( type, objectX, objectY, objectIncrX, objectWidth, objectHeight, screenWidth, screenHeight, bool ):
    if objectX <= 0:
        objectX = 0
        if type == 'port':
            objectIncrX *= -1
    elif objectX + objectWidth >= screenWidth:
        objectX = screenWidth - objectWidth
        if type == 'port':
            objectIncrX *= -1

    if objectY + objectHeight >= screenHeight:
        objectY = screenHeight - objectHeight
        bool = True
       
    return(objectX, objectY, objectIncrX, bool)


def closingGame():
    global manInfo, manX, manY, manW, manH, showMan, paraBg, screenWidth, screenHeight, xincr, yincr, portal, portalInfo, portalX, portalY, portalW, portalH, portalincrx, landed
    global gameControlKeys, gameKey, controlKeys
   
    manInfo[ manY ] += manInfo[ yincr ]
    manInfo[ manX ] += manInfo[ xincr ]
   
    portalInfo[ portalX ] += portalInfo[ portalincrx ]
   
    portalInfo[ portalX ], portalInfo[ portalY ], portalInfo[ portalincrx], landed = boundaryCheck( 'port', portalInfo[ portalX ], portalInfo[ portalY ], portalInfo[ portalincrx], portalInfo[ portalW ], portalInfo[ portalH ], screenWidth, screenHeight, landed )
    manInfo[ manX ], manInfo[ manY ], manInfo[ xincr ], landed = boundaryCheck( 'man', manInfo[ manX ], manInfo[ manY ], manInfo[ xincr ], manInfo[ manW ], manInfo[ manH ], screenWidth, screenHeight, landed )
   
       
    if gameKey == LEFT:
        manInfo[ xincr ] -= 1
    elif gameKey == RIGHT:
        manInfo[ xincr ] += 1
       
       
    if manInfo[ xincr ] != 0 and gameKey == "":
        manInfo[ xincr ] = manInfo[ xincr ] / 1.1
       
    if -0.2 < manInfo[ xincr ] < 0.2 and gameKey == "":
        manInfo[ xincr ] = 0
       
    image(paraBg, 0, 0, screenWidth + 1, screenHeight + 1)
    image(portal, portalInfo[ portalX ], portalInfo[ portalY ], portalInfo[ portalW ], portalInfo[ portalH ])
    image(showMan, manInfo[ manX ], manInfo[ manY ], manInfo[ manW ], manInfo[ manH ])
   
    if landed:
        manInfo[ xincr ] = manInfo[ yincr ] = portalInfo[ portalincrx ] = 0
        gameControlKeys = []
       
        if portalInfo[ portalX ] < manInfo[ manX ] + manInfo[ manW ] /2 < portalInfo[ portalX ] + portalInfo[ portalW ]:
            imageMode(CENTER)
            background(0)
            image(winScreen, screenWidth / 2, screenHeight / 2, 400, 200)
            controlKeys = [ ESC ]

        else:
            imageMode(CENTER)
            background(0)
            image(otherScreen, screenWidth / 2, screenHeight / 2, 700, 350)
            controlKeys = [ ESC ]



def draw():
    global screenWidth, screenHeight, gameControlKeys, gameKey, winScreen, otherScreen, exitted, exitButton, exitX, exitY, exitWidth, exitHeight
    global asciList, whichKey, controlKeys, scrollKeys, bannedUKey, bannedDKey, nameIn, nameIn2, nameLimit, nameCount, nameCount2
    global bg_Menu, Menu_all, Menu_options, Menu_start, Menu_help, Menu_score, backbutton_on, backbutton_off, endFont, Board, currentBoard, Coin, Scores
    global mode, PrevMode, menuWidth, menuHeight, endFont, playAgain, menuPressed, filename, grid_7x6, grid_9x6, options, options_7x6, options_9x6, help
    global dropdown_mainMenu, dropdown_options, dropdown_scoreboard, dropdown_help, dropdown_none, dropdown_all, menuExpand, scoresList
    global gridBg, checkDirections, x, y, w, h, cols, rows, startX, startY, slotgap, diam, slotSize, value, scoresList, scrollKeys
    global yspeed, gameScreenHeight, addCoin, checkWin, noWin, numCols, numRows, gridList, fillColours, player1, colours, newCoinY, inactiveCols
    global allBoundaries, whichBoundary, removeBoundary, activeBoundaries, numBoundaries, validLocation, newCoinCol, newCoinRow, played, turnCount, names
    global arrow, arrowY, arrowW, arrowH, arrowPointer, drawBoard, bouncingCoin, drawCoins, newCoinX, newCoinY, bounced, slotgap, fileList, gameScreenWidth, startLocY
    global manInfo, manX, manY, manW, manH, showMan, paraBg, screenWidth, screenHeight, xincr, yincr, portal, portalInfo, portalX, portalY, portalW, portalH, portalincrx, landed
    global scoresList, fileName, sortScores, placeScore




    if mode != 'Play':
        for i in range(currentBoard[ cols ]):
            activeBoundaries[i] = False

    if mode == "Menu":
        nameIn = ''
        nameIn2 = ''
        background(bg_Menu)
        image(Menu_all, 450, 250, menuWidth, menuHeight)
        if 450 < mouseX < 450 + menuWidth and 250 < mouseY < 325:
            image(Menu_start, 450, 250, menuWidth, menuHeight)
        elif 450 < mouseX < 450 + menuWidth and 325 < mouseY < 400:
            image(Menu_options, 450, 250, menuWidth, menuHeight)
        elif 450 < mouseX < 450 + menuWidth and 400 < mouseY < 475:
            image(Menu_score, 450, 250, menuWidth, menuHeight)
        elif 450 < mouseX < 450 + menuWidth and 475 < mouseY < 550:
            image(Menu_help, 450, 250, menuWidth, menuHeight)

    if mode == "Start1":
        nameCount = 0
        background(255)
        textSize(40)
        fill(0)
        text("Player 1 Enter Your Name > ", 200, 100)
        text("Press ENTER to Continue", 280, 400)
        if 400 < mouseX < 600 and 575 < mouseY < 675:
            image(backbutton_on, 400, 575, 200, 100)
        else:
            image(backbutton_off, 400, 575, 200, 100)
        if (whichKey == ENTER) or (nameCount >= nameLimit):
            names = [ nameIn ]
            mode = "Start2"
        elif whichKey == BACKSPACE:
            nameIn = nameIn[:-1]
            nameCount -= 1
        else:
            if whichKey != "":
                nameIn += whichKey.upper()
                nameCount += 1
        text(nameIn, 420, 200)

        whichKey = ""

    if mode == "Start2":
        nameCount = 0
        background(255)
        textSize(40)
        fill(0)
        text("Player 2 Enter Your Name > ", 200, 100)
        text("Press ENTER to Continue", 280, 450)
        if 400 < mouseX < 600 and 575 < mouseY < 675:
            image(backbutton_on, 400, 575, 200, 100)
        else:
            image(backbutton_off, 400, 575, 200, 100)
        if (whichKey == ENTER) or (nameCount >= nameLimit):
            names.append(nameIn2)
            mode = "Play"
            noWin = True
            turnCount = [ 0, 0 ]
            player1 = False
        elif whichKey == BACKSPACE:
            nameIn2 = nameIn2[:-1]
            nameCount -= 1
        else:
            if whichKey != "":
                nameIn2 += whichKey.upper()
                nameCount2 += 1
        text(nameIn2, 420, 200)
        whichKey = ""

    if mode == "Options":
        background(255)
        image(options, 100, 100, 800, 500)
        if 120 < mouseX < 460 and 180 < mouseY < 520:
            image(options_7x6, 100, 100, 800, 500)
        elif 500 < mouseX < 875 and 180 < mouseY < 520:
            image(options_9x6, 100, 100, 800, 500)

        if 400 < mouseX < 600 and 575 < mouseY < 675:
            image(backbutton_on, 400, 575, 200, 100)
        else:
            image(backbutton_off, 400, 575, 200, 100)
        fill(0, 0, 255)
        textSize(70)
        text("Options", 350, 100)
   

    if mode == "Score":

        background(255)
        fill(150)
        rect(100, 140, 800, 410)
        fill(255)
        rect(105, 145, 790, 400)
        if 400 < mouseX < 600 and 575 < mouseY < 675:
            image(backbutton_on, 400, 575, 200, 100)
        else:
            image(backbutton_off, 400, 575, 200, 100)
        fill(0, 0, 255)
        textSize(70)
        text("Scoreboard", 300, 100)
       
        for i in range(len(scoresList[0])):
            textY = 200 + (100 * i) + value
            if i == 0 and textY >= 200:
                bannedUKey = UP
            elif i == 0 and textY <= 200:
                bannedUKey = ''
            if i == (len(scoresList) - 1) and textY <= 500 and len(scoresList) >= 4:
                bannedDKey = DOWN
            elif i == (len(scoresList) - 1) and textY >= 500 and len(scoresList) >= 4:
                bannedDKey = ''
       
            print(whichKey)
            if textY > 545 or textY < 180:
                pass
            else:
                fill(0)
                textSize(30)
                text(scoresList[0][i], 300, textY)
                text(scoresList[1][i], 600, textY)
 

    if mode == "Play":
        background(255)
        arrowPointer()
        x = Board(currentBoard, gridList, newCoinCol, newCoinRow, checkDirections, noWin)
        x.drawBoard()

        image(dropdown_none, 400, 10, 200, 64)
        if 400 < mouseX < 600 and 10 < mouseY < 74:
            image(dropdown_all, 400, 10, 200, 227)
            menuExpand = True

        if mouseX < 400 or mouseX > 600 or mouseY < 10 or mouseY > 237:
            menuExpand = False

        if menuExpand == True:
            if 400 < mouseX < 600 and 74 <= mouseY <= 110:
                image(dropdown_mainMenu, 400, 10, 200, 227)
            if 400 < mouseX < 600 and 111 <= mouseY <= 152:
                image(dropdown_options, 400, 10, 200, 227)
            if 400 < mouseX < 600 and 153 <= mouseY <= 196:
                image(dropdown_scoreboard, 400, 10, 200, 227)
            if 400 < mouseX < 600 and 197 <= mouseY <= 237:
                image(dropdown_help, 400, 10, 200, 227)

        for i in range(currentBoard[ cols ]):
            activeBoundaries[i] = True
        for i in range(len(inactiveCols)):
            activeBoundaries[inactiveCols[i]] = False

        if noWin == True:

            if whichBoundary != -1:
                player1 = not player1
                turnCount[player1] += 1
                newCoinCol = whichBoundary

                y = Coin(newCoinCol, inactiveCols, newCoinRow, newCoinX, currentBoard, gridList, noWin, activeBoundaries, arrowY, colours, player1, bounced, yspeed)
                gridList, activeBoundaries, inactiveCols, newCoinX, newCoinY, newCoinRow, bounced = y.addCoin()
                whichBoundary = -1

            y = Coin(newCoinCol, inactiveCols, newCoinRow, newCoinX, currentBoard, gridList, noWin, activeBoundaries, arrowY, colours, player1, bounced, yspeed)
            noWin, newCoinCol, newCoinY, bounced, yspeed = y.bouncing()
       
       
        else:
       
            newName = names[ not player1 ]
            newScore = turnCount[ player1 ]
            if scoresList[0] == []:
                scoresList[0].append(newName)
                scoresList[1].append(newScore)
           
            scoresList = placeScore(scoresList, newName, newScore)
            scoresList = sortScores(scoresList)
           
                   
            with open( fileName, 'wb') as f:
                pickle.dump(scoresList, f)
           


    if mode == 'Menu' or mode == 'Options':
        gridList = [[''] * currentBoard[ rows ] for i in range( currentBoard[ cols ] )]
       
    if exitted:
        closingGame()
    else:
        image(exitButton, exitX, exitY, exitWidth, exitHeight)
       

def keyPressed():
    global gameControlKeys, gameKey
    if key == CODED:
        if keyCode in gameControlKeys:
            gameKey = keyCode
        else:
            gameKey = ""

def keyReleased():
    global whichKey, asciList, controlKeys, scrollKeys, exitted, gameKey, value
   
    if exitted:
        gameKey = ""
        if keyCode == ESC:
            exit()
   
    if key == CODED:
        if keyCode in scrollKeys:
            whichKey = keyCode
    elif key in controlKeys:
        whichKey = key
    elif key in asciList:
        whichKey = key
    else:
        whichKey = ''
   
    if whichKey == bannedUKey:
        whichKey = ''
       
    elif whichKey == bannedDKey:
        whichKey = ''

    if whichKey == DOWN:
        value -= 10
        whichKey = ''
    if whichKey == UP:
        value += 10
        whichKey = ''


def mousePressed():
    global exitted, Buttons, mode, PrevMode, menuExpand
   
    if exitX < mouseX < exitX + exitWidth and exitY < mouseY < exitY + exitHeight:
        exitted = True

    buttons = Buttons( menuWidth, mode, PrevMode, menuExpand )
    mode, PrevMode = buttons.menuButtons()
