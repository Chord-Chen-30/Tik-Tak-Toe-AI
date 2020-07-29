import random
import copy
import time

class Tik_Tak_Toe:
    
    def __init__(self):
        self.iterations = 12000
        self.gamma = 0.9
        self.alpha = 0.3
        self.epslion = 0.2
        self.qvalues = {}
        self.chessboard = [[0,0,0],
                           [0,0,0],
                           [0,0,0]]

    
    """Mehtod refer to training"""
    # PLAYER = 1
    def isWinningState(self, player):

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
        train_win_counts = 0
        # stateBeforeAction1=[]
        # step1=None 
        # stateAfterAction1=[]

        for i in range(1, self.iterations+1):

            if i % 10000 == 0:
                # print("\rI'm learning... :", int(i/self.iterations*100),"%\t", end="")
                print("I'm learning... :", int(i/self.iterations*100), '%', "("+ str(train_win_counts)+ "/"+ "10000"+")")
                print("alpha: ",self.alpha)
                print("epslion: ", self.epslion)
                train_win_counts = 0

            # self.alpha *= ((self.iterations - i) / self.iterations)**0.5
            self.resetChessBoard()
            if i > self.iterations -4:
                self.showChessBoard()
                time.sleep(1)
            # Within one round do until some one wins
            while True:
                # """Random player's turn"""
                # randStep = self.giveRandomStep()

                # # print("--random step: ", randStep)

                # # A random robert should never find a tie
                # if not randStep:
                #     assert(1!=1)
                    
                # self.setStep(randStep,2)

                # if i > self.iterations -4:
                #     self.showChessBoard()
                #     time.sleep(2)

                # # print("--after random step: ")
                # # self.showChessBoard()

                # # Random robert wins
                # if self.isWinningState(player=2):
                #     # Last step is a terrible step
                #     self.updateQValues(stateBeforeAction1, step1, stateAfterAction1, -1)
                #     # self.showChessBoard()
                #     # print("AI Loses !")
                #     break
                

                """AI 2's turn"""
                # self.showChessBoard()
                # step = self.computeStepFromQValues(self.chessboard)
                step2 = self.decideStep(self.chessboard)

                # print("---AI step :",step)
                if step2 != None:
                    stateBeforeAction2 = copy.deepcopy(self.chessboard)
                    self.setStep(step2, 2)
                    stateAfterAction2 = copy.deepcopy(self.chessboard)

                else: # Tie
                    # self.showChessBoard()
                    # print("no action to take")
                    # print("updating: stateBeforeAction2",stateBeforeAction2)
                    self.updateQValues(stateBeforeAction1, last_step1, stateAfterAction1, 0.5)
                    self.updateQValues(stateBeforeAction2, last_step2, stateAfterAction2, 0.5)
                    # print("Tie !")
                    break

                # print("--after AI step: ")
                if i > self.iterations -4:
                    self.showChessBoard()
                    time.sleep(2)

                if self.isWinningState(player=2):
                    self.updateQValues(stateBeforeAction1, step1, stateAfterAction1, -1.0)
                    self.updateQValues(stateBeforeAction2, step2, stateAfterAction2, 1.0)
                    # self.showChessBoard()
                    # print("AI wins !")
                    break
                else:
                    self.updateQValues(stateBeforeAction2, step2, stateAfterAction2, 0.0)

                last_step2 = step2



                """AI 1's turn"""
                # self.showChessBoard()
                # step = self.computeStepFromQValues(self.chessboard)
                step1 = self.decideStep(self.chessboard)

                # print("---AI step :",step)
                if step1 != None:
                    stateBeforeAction1 = copy.deepcopy(self.chessboard)
                    self.setStep(step1, 1)
                    stateAfterAction1 = copy.deepcopy(self.chessboard)
                
                # Tie!
                else: 
                    # self.showChessBoard()
                    # print("no action to take")
                    # print("updating: stateBeforeAction1",stateBeforeAction1)
                    self.updateQValues(stateBeforeAction1, last_step1, stateAfterAction1, 0.5)
                    self.updateQValues(stateBeforeAction2, last_step2, stateAfterAction2, 0.5)
                    # print("Tie !")
                    break

                # print("--after AI step: ")
                if i > self.iterations -4:
                    self.showChessBoard()
                    time.sleep(2)

                if self.isWinningState(player=1):
                    self.updateQValues(stateBeforeAction1, step1, stateAfterAction1, 1.0)
                    self.updateQValues(stateBeforeAction2, step2, stateAfterAction2, -1.0)
                    train_win_counts += 1
                    # self.showChessBoard()
                    # print("AI wins !")
                    break
                else:
                    self.updateQValues(stateBeforeAction1, step1, stateAfterAction1, 0.0)

                last_step1 = step1
                

        init_state = ((0,0,0),(0,0,0),(0,0,0))
        first_actions = []
        for rowid in range(3):
            for colid in range(3):
                first_actions.append((rowid, colid))

        for fisrt_action in first_actions:
            print('\n')
            print((init_state, fisrt_action))
            print(self.qvalues[(init_state, fisrt_action)])



    """Method for testing"""
    # AI plays against a random player
    def test(self):
        # Make sure each round AI make some step
        def check():
            ones = 0
            twos = 0
            for row in self.chessboard:
                for grid in row:
                    if grid == 1:
                        ones+=1
                    elif grid == 2:
                        twos += 1
            assert(ones==twos)


        self.alpha = 0

        TEST_EPISODES = 100
        wincounts = 0
        losecounts = 0
        tiecounts = 0
        for i in range(TEST_EPISODES):

            self.resetChessBoard()
            # print("iteration %d", i)
            # Within one round do until some one wins
            while True:
                # Random player(2)'s turn
                check()
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
                    tiecounts += 1
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
        print("Tie: ", tiecounts)
        print("No-failing Rate:", (wincounts+tiecounts)/TEST_EPISODES)
        

    def testAgainstHuman(self):
        TEST_EPISODES = 100
        wincounts = 0
        losecounts = 0

        for i in range(TEST_EPISODES):
            print("Round: ", i+1)
            self.resetChessBoard()
            self.showChessBoard()
            while True:
                stepByHuman = input("Choose a postion: 1~9\n")

                postion = ((int(stepByHuman)-1)//3,(int(stepByHuman)-1)%3)
                while postion not in self.getAvailableSteps(self.chessboard):
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
                time.sleep(1)
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
                    time.sleep(1)
                    wincounts += 1
                    break


    """Method refer to Q learning"""
    # ACTION should be tuples
    # STATE can be list
    def getQValue(self, state, action):
        state = self._convertToTuple(state)
        if (state,action) in self.qvalues:
            return self.qvalues[(state, action)]
        else:
            self.qvalues[(state, action)] = 0.0
            return 0.0


    def decideStep(self, state):
        
        step = None
        # self.epslionDecay()
        if random.random() < self.epslion: # Exploration
            available_steps = self.getAvailableSteps(state)
            if available_steps != []:
                # print(state)
                step = random.choice(available_steps)

        else: # Exploitation
            step = self.computeStepFromQValues(state)
        return step



    def computeStepFromQValues(self, state):
        step = None
        # print("in compute step from q value:")
        # print(self.chessboard)
        # print("out compute step from q value:")
        legalSteps = self.getAvailableSteps(state)
        random.shuffle(legalSteps)
        # print(legalSteps)
        max_qvalue = -float('inf')
        for s in legalSteps:
            qvalue = self.getQValue(state, s)
            if qvalue > max_qvalue:
                max_qvalue = qvalue
                step = s
            elif qvalue == max_qvalue:
                if step != None:
                    step = random.choice([s, step])
                else:
                    step = s

        return step
    
    def computeValueFromQValues(self, state):
        legalSteps = self.getAvailableSteps(state)
        max_value = -float('inf')
        for s in legalSteps:
            qvalue = self.getQValue(state, s)
            if qvalue > max_value:
                max_value = qvalue
        if legalSteps == []:
            max_value = 0.0
        return max_value

    def updateQValues(self, state, action, nextState, reward):
        
        # print(state == self._convertToTuple(state))
        old_qvalue = self.getQValue(state, action)
        # if (old_qvalue != 0):
        #     print("using old q value")
        #     print(old_qvalue)
        V = self.computeValueFromQValues(nextState)
        # Remove the use of discount
        new_qvalue = (1.0-self.alpha)*old_qvalue + self.alpha*(reward + self.gamma*V)
        # self.alphaDecay()
        state = self._convertToTuple(state)
        self.qvalues[(state, action)] = new_qvalue



    # Convert a 2D list to tuple used in dictionary indexing
    def _convertToTuple(self, _list):
        _tupleList = [tuple(_tuple) for _tuple in _list]
        return tuple(_tupleList)

    def alphaDecay(self):
        self.alpha *= 0.999998

    def epslionDecay(self):
        self.epslion *= 0.999995

    """===========Method refer to chessboard==========="""

    def getAvailableSteps(self, state):
        avaiPos = []
        for rowind, row in enumerate(state):
            for colind, grid in enumerate(row):
                if grid == 0:
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
    # length = 0
    # for a,b in AI.qvalues.items():
    #     length+=1

    print("\nqvalues learned: ", len(AI.qvalues))
    
    AI.test()
    # AI.testAgainstHuman()


if __name__ == '__main__':
    main()