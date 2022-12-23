# python scirpt that automates the solving of the game wordle on the new york times website
import random, pyautogui, time, keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By


# importing words and creating an alaphabet list
with open ('wordlewords.txt') as f:
    contents = f.read()
wordsLeft = list(contents.split("\n"))
for word in wordsLeft:
    if len(word) != 5:
        wordsLeft.remove(word)
newList = []
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


# class functions contaning all the functions needed to automate the process
class wordlePlay():
    def __init__(self):
        self.knowledgeBase = ['-', '-', '-', '-', '-']
        self.kindaCorrect = []
        self.wrong = []
        self.tries = 0
        self.index = 0
        self.row = 1

    # updates knowledge based on score and word chosen
    def updateKnowledge(self,score,chosen):
        wordsLeft.remove(chosen)
        for attempt in score:
            if attempt == 'y':
                self.knowledgeBase[self.index] = chosen[self.index]
            elif attempt == 'k':
                self.kindaCorrect.append(chosen[self.index])
            elif attempt == 'n':
                self.wrong.append(chosen[self.index])
            self.index += 1
        self.index = 0
        print(self.knowledgeBase)
        print(self.wrong)
        print(self.kindaCorrect)

    def updateCorrect(self,score):
        while self.index < len(score):
            if str(score[self.index]) == 'y':
                for word in wordsLeft:
                    if str(word[self.index]) == str(self.knowledgeBase[self.index]) and word not in newList:
                        newList.append(word)
            self.index += 1
        self.index = 0
        if len(newList) != 0:
            wordsLeft.clear()
            for word in newList:
                wordsLeft.append(word)
            newList.clear()

    # updating word bank based on knowledge base
    def updateWordsWrong(self):
        for ch in self.wrong:
            if ch in alphabet:
                alphabet.remove(ch)
        put = True
        for word in wordsLeft:
            for letter in word:
                if letter not in alphabet:
                    put = False
            if put == True and word not in newList:
                newList.append(word)
            put = True
        if len(newList) != 0:
            wordsLeft.clear()
            for word in newList:
                wordsLeft.append(word)
            newList.clear()

    # updates word bank to only words containing kinda letters
    def updateMaybeWords(self, score, chosen):    
        put = True
        for word in wordsLeft:
            for ch in self.kindaCorrect:
                if ch not in word:
                    put = False
            if put == True:
                while self.index < len(score):
                    if score[self.index] == 'k':
                        if word[self.index] == chosen[self.index]:
                            put = False
                    self.index += 1
                self.index = 0
            if put == True and word not in newList:
                    newList.append(word)
            put = True
        if len(newList) != 0:
            wordsLeft.clear()
            for word in newList:
                wordsLeft.append(word)
            newList.clear()       

    def updateALL(self,score,chosen):
        self.updateCorrect(score)
        self.updateWordsWrong()
        self.updateMaybeWords(score,chosen)             

    #  pick a random word if there are many choices
    def randomPick (self):
        print(len(wordsLeft))
        word = random.choice(wordsLeft)
        print(word)
        return word

    # checking to see if game is over
    def gameOver(self):
        self.tries += 1

        if self.tries == 6:
            print ("Game over...")
            return True
        return False

    # removing any letters from kinda correct that are in knowledge base
    def dupeCheck(self):
        for ch in self.kindaCorrect:
            if ch in self.knowledgeBase:
                self.kindaCorrect.remove(ch)

    def play(self, word, driver):
        for i in word:
            keyboard.press_and_release(i)
        keyboard.press_and_release('enter')

        time.sleep(5)

        # retriving the score of the word just guessed
        score = []
        rowid = str('//*[@id="wordle-app-game"]/div[1]/div/div[' + str(self.row) + ']/div[')
        for i in range(1,6):
            tile = str(rowid + str(i) + ']/div')
            tileXpath = driver.find_element(By.XPATH, tile)
            score.append(tileXpath.get_attribute("data-state"))
        self.row += 1
        real = []
        # changing it so the functions above can read the score
        for i in score:
            if i == 'correct':
                real.append('y')
            elif i == 'absent':
                real.append('n')
            elif i == 'present':
                real.append('k')
        return real
    

def main():
    play = wordlePlay()
     # opens up wordle webstite
    url = 'https://www.nytimes.com/games/wordle/index.html'
    driver = webdriver.Chrome('/Users/louiscerda/Desktop/chromedriver')
    driver.get(url)

    # clickcs out of first pop up and enters word that was randomly guessed
    time.sleep(5)
    pyautogui.click(100, 300)
    

    # play functions
    while play.gameOver() == False:
        word = play.randomPick()
        score = play.play(word,driver)
        play.updateKnowledge(score,word)
        play.updateALL(score,word)
        # play.dupeCheck()
        time.sleep(5)
        if score == 'yyyyy':
            quit()

main()