import random
import copy
import time

class Tik_Tak_Toe:
    
    def __init__(self):
        self.iterations = 100000
        self.alpha = 1.0 #?
        self.epsilon = 0.5
        self.qvalues = {}
        self.chessboard = [[0,0,0],
                           [0,0,0],
                           [0,0,0]]

    
    """Mehtod refer to training"""
    # PLAYER = 1
    def isWinningState(self, player=1):

        _temp = copy.deepcopy(self.chessboard)

        for rowind, row in enumerate(_temp):
            for i in range(len(row)):
                if _temp[rowind][i] != player:
                     _temp[rowind][i] = 0

        win = (sum(_temp[0]) == player*3) or \
              (sum(_temp[1]) == player*3) or \
              (sum(_temp[2]) == player*3) or \
              (sum([row[0] for row in _temp]) == player*3) or \
              (sum([row[1] for row in _temp]) == player*3) or \
              (sum([row[2] for row in _temp]) == player*3) or \
              (sum([row[i] for i, row in enumerate(_temp)]) == player*3) or \
              (sum([row[2-i] for i, row in enumerate(_temp)]) == player*3)
        

        return win



    def train(self):

        for i in range(1, self.iterations+1):

            if i % 10000 == 0:
                print("iteration: ", i)

            self.alpha *= ((self.iterations - i) / self.iterations)**2
            self.resetChessBoard()
            # print("iteration %d", i)
            # Within one round do until some one wins
            while True:

                """Random player's turn"""
                randStep = self.giveRandomStep()

                # print("--random step: ", randStep)

                # A random robert should never find a tie
                if not randStep:
                    assert(1!=1)
                    
                self.setStep(randStep,2)
                
                # print("--after random step: ")
                # self.showChessBoard()

                # Random robert wins
                if self.isWinningState(player=2):
                    # Last step is a terrible step
                    self.updateQValues(stateBeforeAction, step, stateAfterAction, -1)
                    # self.showChessBoard()
                    # print("AI Loses !")
                    break

                
                """AI's turn"""
                # self.showChessBoard()
                # step = self.computeStepFromQValues(self.chessboard)
                step = self.decideStep(self.chessboard, self.epsilon)
                
                # print("---AI step :",step)
                if step != None:
                    stateBeforeAction = copy.deepcopy(self.chessboard)
                    self.setStep(step, 1)
                    stateAfterAction = copy.deepcopy(self.chessboard)

                else:
                    # self.showChessBoard()
                    # print("no action to take")
                    # print("updating: stateBeforeAction",stateBeforeAction)
                    self.updateQValues(stateBeforeAction, None, stateBeforeAction, -0.1)
                    # print("Tie !")
                    break

                # print("--after AI step: ")
                # self.showChessBoard()


                if self.isWinningState(player=1):
                    self.updateQValues(stateBeforeAction, step, stateAfterAction, 1)
                    # self.showChessBoard()
                    # print("AI wins !")
                    break
                else:
                    self.updateQValues(stateBeforeAction, step, stateAfterAction, -0.2)







    def test(self):
        self.alpha = 0

        TEST_EPISODES = 100
        wincounts = 0
        losecounts = 0
        for i in range(TEST_EPISODES):

            self.resetChessBoard()
            # print("iteration %d", i)
            # Within one round do until some one wins
            while True:
                # Random player(2)'s turn
                randStep = self.giveRandomStep()

                # print("--random step: ", randStep)
                
                if not randStep:
                    # self.showChessBoard()
                    # print("Random finds Tie !")
                    break
                self.setStep(randStep,2)
                
                # print("--after random step: ")
                # self.showChessBoard()

                # Random robert wins
                if self.isWinningState(player=2):
                    # Last step is a terrible step
                    # self.showChessBoard()
                    # print("AI Loses !")
                    losecounts += 1
                    break
                
                # AI's turn
                # self.showChessBoard()
                step = self.computeStepFromQValues(self.chessboard)
                
                # print("---AI step :",step)

                if not step:
                    # print(self.chessboard)
                    # self.showChessBoard()
                    # print("AI finds Tie !")
                    break
                self.setStep(step, 1)

                # print("--after AI step: ")
                # self.showChessBoard()


                if self.isWinningState(player=1):
                    # self.showChessBoard()
                    # print("AI wins !")
                    wincounts += 1
                    break

        print("win: ", wincounts)
        print("lose: ", losecounts)
        print("Tie: ", TEST_EPISODES - wincounts - losecounts)


    def testAgainstHuman(self):
        TEST_EPISODES = 100
        wincounts = 0
        losecounts = 0

        for i in range(TEST_EPISODES):
            print("Round: ", i)
            self.resetChessBoard()
            self.showChessBoard()
            while True:
                stepByHuman = input("Choose a postion: 1~9\n")

                postion = ((int(stepByHuman)-1)//3,(int(stepByHuman)-1)%3)
                while postion not in self.getAvailableSteps():
                    print("Are you serious? :(")
                    stepByHuman = input("Choose a postion: 1~9\n")
                    postion = ((int(stepByHuman)-1)//3,(int(stepByHuman)-1)%3)

                self.setStep(postion, 2)
                self.showChessBoard()

                if self.isWinningState(player=2):
                    # Last step is a terrible step
                    # self.showChessBoard()
                    print("AI Loses !")
                    self.showChessBoard()
                    losecounts += 1
                    break
                
                # AI's turn
                # self.showChessBoard()
                step = self.computeStepFromQValues(self.chessboard)
                
                print("---AI step :",step)
                time.sleep(2)
                if not step:
                    # print(self.chessboard)
                    self.showChessBoard()
                    print("AI finds Tie !")
                    break
                self.setStep(step, 1)

                # print("--after AI step: ")
                self.showChessBoard()


                if self.isWinningState(player=1):
                    self.showChessBoard()
                    print("AI wins !")
                    wincounts += 1
                    break

    """Method refer to Q learning"""
    # ACTION should be tuples
    # STATE can be list
    def getQValue(self, state, action):
        state = self._convertToTuple(state)
        if (state,action) in self.qvalues:
            return self.qvalues[(state, action)]
        return 0.0


    def decideStep(self, state, epsilon):
        
        step = None
        if random.random() < epsilon: # Exploration
            if self.getAvailableSteps(state) != []:
                # print(state)
                step = random.choice(self.getAvailableSteps(state))
                self.epsilon *= 0.99
        else: # Exploitation
            
            step = self.computeStepFromQValues(state)
        return step



    def computeStepFromQValues(self, state):
        step = None
        # print("in compute step from q value:")
        # print(self.chessboard)
        # print("out compute step from q value:")

        legalSteps = self.getAvailableSteps(state)
        max_qvalue = -float('inf')
        for s in legalSteps:
            qvalue = self.getQValue(state, s)
            if qvalue > max_qvalue:
                max_qvalue = qvalue
                step = s
            elif qvalue == max_qvalue:
                if step != None:
                    step = random.choice([s, step])

        return step
    
    def computeValueFromQValues(self, state):
        legalSteps = self.getAvailableSteps(state)
        max_value = -float('inf')
        for s in legalSteps:
            qvalue = self.getQValue(state, s)
            if qvalue > max_value:
                max_value = qvalue
        return max_value

    def updateQValues(self, state, action, nextState, reward):
        state = self._convertToTuple(state)
        old_qvalue = self.getQValue(state, action)
        # if (old_qvalue != 0):
        #     print("using old q value")
        #     print(old_qvalue)
        V = self.computeValueFromQValues(nextState)
        # Remove the use of discount
        new_qvalue = (1-self.alpha)*old_qvalue + self.alpha*(reward + 0.9*V)
        self.qvalues[(state, action)] = new_qvalue



    # Convert a 2D list to tuple used in dictionary indexing
    def _convertToTuple(self, _list):
        tupleList = [tuple(_tuple) for _tuple in _list]
        return tuple(tupleList)



    """===========Method refer to chessboard==========="""

    def getAvailableSteps(self, state):
        avaiPos = []
        for rowind, row in enumerate(state):
            for colind, col in enumerate(row):
                if state[rowind][colind] == 0:
                    avaiPos.append((rowind, colind))
        # if avaiPos == []:
        #     print()
        return avaiPos

    # Positon should be of form (row, column)
    def setStep(self, postion, player):
        self.chessboard[postion[0]][postion[1]] = player
        # self.showChessBoard()

    def showChessBoard(self):
        print("+-----------+")
        for i,row in enumerate(self.chessboard):
            line = []
            for grid in row:
                if grid == 1:
                    line.append("O")
                elif grid == 2:
                    line.append("X")
                else:
                    line.append(" ")
            print("|", line[0],"|", line[1],"|", line[2], "|")
            if i!= 2:
                print("+---+---+---+")

        print("+-----------+")

    def resetChessBoard(self):
        self.chessboard = [[0,0,0],
                           [0,0,0],
                           [0,0,0]]

    """===========Method refer to random player==========="""
    def giveRandomStep(self):
        legalSteps = self.getAvailableSteps(self.chessboard)
        if not legalSteps:
            return None
        return random.choice(legalSteps)



def main():
    AI = Tik_Tak_Toe()
    AI.train()
    length = 0
    for a,b in AI.qvalues.items():
        # print(a,b)
        length+=1

    print("qvalues learned: ", length)
    
    # AI.test()
    AI.testAgainstHuman()


if __name__ == '__main__':
    main()