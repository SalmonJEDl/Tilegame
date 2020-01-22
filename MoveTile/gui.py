from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
import random
from solver import *
import time

class Tiles():
    def __init__(self, gridlen):
        """Initializes the tiles. Tile order will be represented as
        a single list of numbers as strings and "*" as the empty tile.
        As an example, the initial (and completed) tile order for 3x3 puzzle would be:
        ["1", "2", "3", "4", "5", "6", "7", "8", "*"]
        self.tilelist = list of tiles in a completed state
        self.shufflelist = state of the current game."""
        
        self.tilelist = []
        self.gridlen = gridlen
        self.lastIndex = gridlen**2-1
        self.empty_at = self.lastIndex
        
        for i in range(0, gridlen**2-1):
            self.tilelist.append(str(i))
        self.tilelist.append("*")
        self.shufflelist = self.tilelist.copy()
        
        
    def shuffle(self, shufflenum):
        """Shuffle the tiles"""
        for i in range (shufflenum):
            movelist = self.get_movables()
            moveindex = movelist[random.randint(0, len(movelist)-1)]
            self.swap(moveindex)
            
    def get_movables(self):
        """Gets list indexes for movable tiles"""
        movables = []
        
        """Empty tile not in the top row"""
        if self.empty_at >= self.gridlen:
            movables.append(self.empty_at - self.gridlen)
            
        """Empty tile not in the bottom row"""
        if self.empty_at <= self.lastIndex - self.gridlen:
            movables.append(self.empty_at + self.gridlen)
            
        """Empty tile not in the leftmost column"""
        if self.empty_at % self.gridlen != 0:
            movables.append(self.empty_at - 1)
            
        """Empty tile not in the rightmost column"""
        if (self.empty_at + 1) % self.gridlen != 0:
            movables.append(self.empty_at + 1)
            
        return movables
    
    
    def move(self, index):
        """Moves a tile. Returns the indexes that swapped places
        or (0, 0) if unsuccessful"""
        movables = self.get_movables()
        if index in movables:
            indexes = (self.empty_at, index)
            self.swap(index)
            return indexes
        return (0, 0)
        
        
    def swap(self,index):
        """Swaps the order of two tiles"""
        temp = self.shufflelist[index]
        self.shufflelist[index] = self.shufflelist[self.empty_at]
        self.shufflelist[self.empty_at] = temp
        self.empty_at = index
        
    
    def won(self):
        """Game win condition"""
        if self.shufflelist == self.tilelist:
            return True
        else:
            return False
        
    def __str__(self):
        """For printed testUI only"""
        printtext = ""
        for i in range(0, self.gridlen**2):
            if self.shufflelist[i] == "*":
                printtext += "**"
            elif int(self.shufflelist[i]) < 10:
                printtext += "0" + self.shufflelist[i]
            else:
                printtext += self.shufflelist[i]
            if ((i+1) % self.gridlen == 0):
                printtext += "\n"
        return printtext





class Ui_GameWindow(object):
    def setupUi(self, GameWindow):
        GameWindow.setObjectName("GameWindow")
        GameWindow.setFixedSize(500, 610)
        GameWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(GameWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        
        self.gameWidget3 = GameWidget(self.centralwidget,3)
        self.gameWidget3.setGeometry(QtCore.QRect(10, 10, 480, 510))
        self.gameWidget3.setBaseSize(QtCore.QSize(480, 510))
        self.gameWidget3.setMouseTracking(True)
        self.gameWidget3.setAutoFillBackground(False)
        self.gameWidget3.setObjectName("GameWidget")
        self.gameWidget3.setHidden(True)
        
        self.gameWidget4 = GameWidget(self.centralwidget,4)
        self.gameWidget4.setGeometry(QtCore.QRect(10, 10, 480, 510))
        self.gameWidget4.setBaseSize(QtCore.QSize(480, 510))
        self.gameWidget4.setMouseTracking(True)
        self.gameWidget4.setAutoFillBackground(False)
        self.gameWidget4.setObjectName("GameWidget")
        
        self.gameWidget5 = GameWidget(self.centralwidget,5)
        self.gameWidget5.setGeometry(QtCore.QRect(10, 10, 480, 510))
        self.gameWidget5.setBaseSize(QtCore.QSize(480, 510))
        self.gameWidget5.setMouseTracking(True)
        self.gameWidget5.setAutoFillBackground(False)
        self.gameWidget5.setObjectName("GameWidget")
        self.gameWidget5.setHidden(True)
    
        self.QuitButton = QtWidgets.QPushButton(self.centralwidget)
        self.QuitButton.setGeometry(350, 570, 100, 30)
        self.QuitButton.setObjectName("QuitButton")
        self.ShuffleButton = QtWidgets.QPushButton(self.centralwidget)
        self.ShuffleButton.setGeometry(QtCore.QRect(200, 570, 100, 30))
        self.ShuffleButton.setObjectName("ShuffleButton")
        self.TriButton = QtWidgets.QPushButton(self.centralwidget)
        self.TriButton.setGeometry(QtCore.QRect(50, 530, 100, 30))
        self.TriButton.setObjectName("TriButton")
        self.QuadButton = QtWidgets.QPushButton(self.centralwidget)
        self.QuadButton.setGeometry(QtCore.QRect(200, 530, 100, 30))
        self.QuadButton.setObjectName("QuadButton")
        self.FiveButton = QtWidgets.QPushButton(self.centralwidget)
        self.FiveButton.setGeometry(QtCore.QRect(350, 530, 100, 30))
        self.FiveButton.setObjectName("FiveButton")
        self.SolveButton = QtWidgets.QPushButton(self.centralwidget)
        self.SolveButton.setGeometry(QtCore.QRect(50, 570, 100, 30))
        GameWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(GameWindow)
        QtCore.QMetaObject.connectSlotsByName(GameWindow)
        
        self.ShuffleButton.clicked.connect(self.shuffle)
        self.TriButton.clicked.connect(self.change_size_to3)
        self.QuadButton.clicked.connect(self.change_size_to4)
        self.FiveButton.clicked.connect(self.change_size_to5)
        self.QuitButton.clicked.connect(self.endgame)
        self.SolveButton.clicked.connect(self.solve)

    def retranslateUi(self, GameWindow):
        _translate = QtCore.QCoreApplication.translate
        GameWindow.setWindowTitle(_translate("GameWindow", "Tile Game"))
        self.ShuffleButton.setText(_translate("GameWindow", "Shuffle"))
        self.TriButton.setText(_translate("GameWindow", "Size: 3x3"))
        self.QuadButton.setText(_translate("GameWindow", "Size: 4x4"))
        self.FiveButton.setText(_translate("GameWindow", "Size: 5x5"))
        self.QuitButton.setText(_translate("GameWindow", "Quit"))
        self.SolveButton.setText(_translate("GameWindow", "Solve"))

    
    """These three functions handle the changing between different board sizes"""
    def change_size_to3(self):
        self.gameWidget3.setHidden(False)
        self.gameWidget4.setHidden(True)
        self.gameWidget5.setHidden(True)
        
    def change_size_to4(self):
        self.gameWidget3.setHidden(True)
        self.gameWidget4.setHidden(False)
        self.gameWidget5.setHidden(True)
        
    def change_size_to5(self):
        self.gameWidget3.setHidden(True)
        self.gameWidget4.setHidden(True)
        self.gameWidget5.setHidden(False)
        
        
    def endgame(self):
        sys.exit()
        
    
    def shuffle(self):
        """Shuffles the currently visible board"""
        if self.gameWidget3.isHidden() == False:
            self.gameWidget3.shuffle()
        elif self.gameWidget4.isHidden() == False:
            self.gameWidget4.shuffle()
        elif self.gameWidget5.isHidden() == False:
            self.gameWidget5.shuffle()
            
    def solve(self):
        if self.gameWidget3.isHidden() == False:
            self.gameWidget3.solve()
        elif self.gameWidget4.isHidden() == False:
            self.gameWidget4.solve()
        elif self.gameWidget5.isHidden() == False:
            self.gameWidget5.solve()
        
        
class GameWidget(QtWidgets.QWidget):
    
    
    def __init__(self, parent=None, value=4):
        QtWidgets.QWidget.__init__(self, parent)
        self.level = value
        self.tiles = Tiles(self.level)
        self.tiles.shuffle(10*(self.level**2))
        
        self.solverlabel = QtWidgets.QLabel(self)
        self.solverlabel.setGeometry(0,480,480,30)
        self.solverlabel.hide()
        self.path = []
        self.moves = []
        
        self.winlabel = QtWidgets.QLabel(self)
        self.winlabel.setGeometry(0,480,480,30)
        pixmap = QPixmap("images/youwin.png")
        self.winlabel.setPixmap(pixmap)
        self.winlabel.hide()
        self.setup_board()
        
    def setup_board(self):
        
        self.labels = []
        pixpath = "images/tile"
        increment = 480 / self.tiles.gridlen
        
        """This loop creates a QLabel for each tile picture"""
        for i in range(0, self.tiles.gridlen**2):
            label = QtWidgets.QLabel(self)
            x, y = self.get_picloc(i)
            label.setGeometry(x,y, increment, increment)
            if self.tiles.shufflelist[i] == "*":
                pixmap = QPixmap("images/browntile.png")
            else:
                tilenum = int(self.tiles.shufflelist[i])+1
                pixmap = QPixmap(pixpath + str(tilenum) + ".png")
            label.setPixmap(pixmap.scaled(increment, increment, QtCore.Qt.KeepAspectRatio))
            self.labels.append(label)
        
    
    def get_picloc(self, index):
        """Returns the position for the tile picture 
        based on its index in the tile picture list"""
        columncount = index % self.tiles.gridlen
        rowcount = index // self.tiles.gridlen
        increment = int(480 / self.tiles.gridlen)
        return (columncount*increment, rowcount*increment)
    
    
    def swap_tilepics(self, x, y):
        """Swaps the position of two tiles in the visualisation"""
        temp = self.labels[x]
        self.labels[x] = self.labels[y]
        self.labels[y] = temp
        temppos = self.labels[x].pos()
        self.labels[x].move(self.labels[y].pos())
        self.labels[y].move(temppos)
        
        
    def shuffle(self):
        """Shuffles the board by calling swap functions for both the tile list
        and the tile picture list, and undoes the winning screen"""
        if self.isEnabled() == False:
            self.setEnabled(True)
        if self.winlabel.isHidden() == False:
            self.winlabel.hide()
        for i in range (10*(self.level**2)):
            movelist = self.tiles.get_movables()
            moveindex = movelist[random.randint(0, len(movelist)-1)]
            self.swap_tilepics(self.tiles.empty_at, moveindex)
            self.tiles.swap(moveindex)
        
    def solve(self):
        #self.solvelist == []:
        if self.solverlabel.isHidden():
            self.solverlabel.show()
            self.path = AStar(self.tiles.shufflelist, self.tiles.tilelist).solve()
            for i in self.path:
                move = str(i//self.level+1) + "-" + str(i%self.level+1)
                self.moves.append(move)
            print(self.moves)
            self.solverlabel.setText(self.moves[0])
            self.moves.pop(0)
        else:
            self.solverlabel.setText("")
            self.solverlabel.hide()
            self.moves = []
            self.path = []
           
            
    def move(self, gridindex):
        """Tries to move given tile"""
        x, y = self.tiles.move(gridindex)
        if x == 0 and y == 0:
            return
        else:
            self.swap_tilepics(x, y)
        
        if len(self.path)>0:
            if gridindex == self.path[0]:
                self.path.pop(0)
                try:
                    self.solverlabel.setText(self.moves.pop(0))
                except:
                    self.solverlabel.setText("")
            else:
                self.path = []
                self.moves = []
                self.solverlabel.hide()
                
        if self.tiles.won():
            self.won()
            

        
    def mousePressEvent(self, event):
        """Calculates which tile was clicked"""
        x = event.x()
        y = event.y()
        increment = int(480 / self.tiles.gridlen)
        rowcount = y // increment * self.tiles.gridlen
        columncount = x // increment
        gridindex = (rowcount + columncount)
        self.move(gridindex)
            
          
    def won(self):
        """Simple winning screen"""
        self.solverlabel.hide()
        self.winlabel.show()
        self.setDisabled(True)
        
        
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GameWindow = QtWidgets.QMainWindow()
    ui = Ui_GameWindow()
    ui.setupUi(GameWindow)
    GameWindow.show()
    sys.exit(app.exec_())