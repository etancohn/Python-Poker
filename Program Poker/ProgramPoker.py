from cmu_112_graphics import *
import random
import copy
import math
import time
 
 
def sortRank(card):        # sort by rank
    return card.rank
 
def sortSuit(card):       # sort by suit
    return card.suit

def sortFirstVal(card):     # sortf"Helvetica {int(self.app.width/40)} by the first value
    return card[0]

 
# crash the program on purpose
def crash():
    crash = "a" + 1
 

class MC(object):       # Monte Carlo
    # 2d deck
    deck = [[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0],[10,0],[11,0],[12,0],[13,0],\
            [1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],\
            [1,2],[2,2],[3,2],[4,2],[5,2],[6,2],[7,2],[8,2],[9,2],[10,2],[11,2],[12,2],[13,2],\
            [1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],[10,3],[11,3],[12,3],[13,3]]

    # found by running MC.prob([],10000000). This is the percent of each kind of hand that were found
    # from 10,000,000 runs of choosing 7 cards from a deck.
    likelihood = {'onePair': '78.9811%', 'twoPair': '26.7656%', 'threeOfKind': '7.6791%', 'straight': '4.3417%', \
                  'flush': '2.2977%', 'fullHouse': '2.6233%', 'fourOfKind': '0.168%', 'straightFlush': '0.0186%'}
    
    # this is the weight of each kind of hand. Straight Flush has the most weight because it beats every other hand
    # and is the least likely. The weights are calculated by finding the inverse of the MC.likelihood
    weight = {'highCard': 0, 'onePair': 1.2661, 'twoPair': 3.7361, 'threeOfKind': 13.0224, 'straight': 23.0325,\
              'flush': 43.5218, 'fullHouse': 38.1199, 'fourOfKind': 595.2381, 'straightFlush': 5376.3441}
    

    def strength(hand):
        if len(hand) == 0 or type(hand[0]) == Card or hand[0][0] not in [1,2,3,4,5,6,7,8,9,10,11,12,13]:
            hand = MC.convert(hand)
        fiveCardHand = TwoDCF.fiveCardHand(hand)
        firstCardRank = fiveCardHand[0][0]
        firstCardWeight = firstCardRank/13
        probs = MC.prob(hand)       # probabilities
        total = 0
        total += (MC.weight['onePair'])*(probs['onePair'])      # the weight of One Pair multiplied by its probability
        total += (MC.weight['twoPair'])*(probs['twoPair'])
        total += (MC.weight['threeOfKind'])*(probs['threeOfKind'])
        total += (MC.weight['straight'])*(probs['straight'])
        total += (MC.weight['flush'])*(probs['flush'])
        total += (MC.weight['fullHouse'])*(probs['fullHouse'])
        total += (MC.weight['fourOfKind'])*(probs['fourOfKind'])
        total += (MC.weight['straightFlush'])*(probs['straightFlush'])
        firstCardFactor = 1/2
        total = total + (firstCardFactor*total*firstCardWeight)     # the strength is increased by an amount based on how high the rank of the first card in the 5-card hand is
        total = round(total,4)
        return total

    # returns the probability of having each kind of hand when all the table cards are out
    @staticmethod
    def prob(hand,runs=3000,percent=False):         # change runs to balance speed/precision
        if len(hand) == 0 or hand[0][0] not in [1,2,3,4,5,6,7,8,9,10,11,12,13]:
            hand = MC.convert(hand)
        prob = dict()
        totalRuns = 0
        onePairS,twoPairS,threeOfKindS,straightS = 0,0,0,0      # successes
        flushS,fullHouseS,fourOfKindS,straightFlushS = 0,0,0,0
        while totalRuns < runs:
            newDeck = MC.deck[:]
            for i in range(len(hand)):
                newDeck.remove(hand[i])
            random.shuffle(newDeck)
            newHand = hand[:]
            cardsLeft = 7 - len(hand)
            for i in range(cardsLeft):      # 5 table cards
                newTableCard = newDeck.pop()
                newHand.append(newTableCard)
            if TwoDCF.isOnePair(newHand):
                onePairS += 1
            if TwoDCF.isTwoPair(newHand):
                twoPairS += 1
            if TwoDCF.isThreeOfKind(newHand):
                threeOfKindS += 1
            if TwoDCF.isStraight(newHand):
                straightS += 1
            if TwoDCF.isFlush(newHand):
                flushS += 1
            if TwoDCF.isFullHouse(newHand):
                fullHouseS += 1
            if TwoDCF.isFourOfKind(newHand):
                fourOfKindS += 1
            if TwoDCF.isStraightFlush(newHand):
                straightFlushS += 1
            totalRuns += 1
        d = 4       # decimal
        if percent == True:
            probOfOnePair = f"{round(((onePairS)/(totalRuns)*100),d)}%"
            probOfTwoPair = f"{round(((twoPairS)/(totalRuns)*100),d)}%"
            probOfThreeOfKind = f"{round(((threeOfKindS)/(totalRuns)*100),d)}%"
            probOfStraight = f"{round(((straightS)/(totalRuns)*100),d)}%"
            probOfFlush = f"{round(((flushS)/(totalRuns)*100),d)}%"
            probOfFullHouse = f"{round(((fullHouseS)/(totalRuns)*100),d)}%"
            probOfFourOfKind = f"{round(((fourOfKindS)/(totalRuns)*100),d)}%"
            probOfStraightFlush = f"{round(((straightFlushS)/(totalRuns)*100),d)}%"
        else:
            probOfOnePair = round(((onePairS)/(totalRuns)),d)
            probOfTwoPair = round(((twoPairS)/(totalRuns)),d)
            probOfThreeOfKind = round(((threeOfKindS)/(totalRuns)),d)
            probOfStraight = round(((straightS)/(totalRuns)),d)
            probOfFlush = round(((flushS)/(totalRuns)),d)
            probOfFullHouse = round(((fullHouseS)/(totalRuns)),d)
            probOfFourOfKind = round(((fourOfKindS)/(totalRuns)),d)
            probOfStraightFlush = round(((straightFlushS)/(totalRuns)),d)
        prob["onePair"] = probOfOnePair
        prob["twoPair"] = probOfTwoPair
        prob["threeOfKind"] = probOfThreeOfKind
        prob["straight"] = probOfStraight
        prob["flush"] = probOfFlush
        prob["fullHouse"] = probOfFullHouse
        prob["fourOfKind"] = probOfFourOfKind
        prob["straightFlush"] = probOfStraightFlush
        return prob
    
    @staticmethod
    def convert(hand):      # convert a hand of card objects into a 2d list in order to do quicker calculations
        newList = []
        for card in hand:
            newList.append([card.rank,card.suit])
        return newList


class TwoDCF(object):       # 2D list card functions
    @staticmethod
    def convert(hand):      # convert a hand of card objects into a 2d list in order to do quicker calculations
        newList = []
        for card in hand:
            newList.append([card.rank,card.suit])
        return newList

    @staticmethod
    def highCardCards(hand):
        handCopy = hand[:]
        cardValues = []
        cardsReturn = []
        for card in hand:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        i = 1
        while i < len(cardValues):
            if cardValues[i] == cardValues[i-1]:
                return False
            for j in hand:
                if cardValues[i-1] == j[0]:
                    cardsReturn.append([cardValues[i-1],j[1]])
                    handCopy.remove([cardValues[i-1],j[1]])
            i += 1
        cardsReturn.append(handCopy[0])
        return cardsReturn[:5]


    @staticmethod
    def isOnePair(hand):
        cardValues = []
        for card in hand:
            for i in cardValues:
                if i == card[0]:
                    return True
            cardValues.append(card[0])
        return False

    @staticmethod
    def onePairCards(hand):
        handCopy = hand[:]
        cardValues = []
        cardsReturn = []
        for card in hand:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        i = 1
        while i <= len(cardValues)-1:
            if cardValues[i] == cardValues[i-1]:
                for j in hand:
                    if j[0] == cardValues[i]:
                        cardsReturn.append([cardValues[i],j[1]])
                        handCopy.remove([cardValues[i],j[1]])
                        if len(cardsReturn) >= 2:
                            handCopy.sort(key = sortFirstVal, reverse = True)
                            return cardsReturn + handCopy[:3]
            i += 1

    @staticmethod
    def onePairCardsOnly(hand):
        cardValues = []
        cardsReturn = []
        for card in hand:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        i = 1
        while i <= len(cardValues)-1:
            if cardValues[i] == cardValues[i-1]:
                for j in hand:
                    if j[0] == cardValues[i]:
                        cardsReturn.append([cardValues[i],j[1]])
                        if len(cardsReturn) == 2:
                            break
                return cardsReturn
            i += 1


    @staticmethod
    def isTwoPair(hand):
        cardValues = []
        numOfPairs = 0
        for card in hand:
            binary = 0
            for i in cardValues:
                if i == card[0]:
                    numOfPairs += 1
                    if numOfPairs == 2:
                        return True
                    cardValues.remove(card[0])
                    binary = 1
            if binary == 0:
                cardValues.append(card[0])
        return False

    @staticmethod
    def twoPairCards(hand):
        handCopy = hand[:]
        cardValues = []
        cardsReturn = []
        for card in hand:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        i = 1
        while i <= len(cardValues)-1:
            if cardValues[i] == cardValues[i-1]:
                for j in hand:
                    if j[0] == cardValues[i]:
                        cardsReturn.append([cardValues[i],j[1]])
                        handCopy.remove([cardValues[i],j[1]])
            i += 1
            handCopy.sort(key = sortFirstVal, reverse = True)
        if len(handCopy) > 0:
            cardsReturn.append(handCopy[0])
        return cardsReturn

    @staticmethod
    def isThreeOfKind(hand):
        cardValues = []
        for card in hand:
            count = 1
            for i in cardValues:
                if i == card[0]:
                    count += 1
                    if count == 3:
                        return True
            cardValues.append(card[0])
        return False

    @staticmethod
    def threeOfKindCards(hand):
        handCopy = hand[:]
        cardValues = []
        cardsReturn = []
        for card in hand:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        value = 2
        while value < len(cardValues):
            if cardValues[value] == cardValues[value-2]:
                k = 1
                while k <= 3:
                    for j in handCopy:
                        if j[0] == cardValues[value]:
                            cardsReturn.append([cardValues[value],j[1]])
                            handCopy.remove([cardValues[value],j[1]])
                            k += 1
                handCopy.sort(key = sortFirstVal, reverse = True)
                return cardsReturn + handCopy[:2]
            value += 1
        return False

    @staticmethod
    def threeOfKindCardsOnly(hand):
        handCopy = hand[:]
        cardValues = []
        cardsReturn = []
        for card in handCopy:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        value = 2
        while value < len(cardValues):
            if cardValues[value] == cardValues[value-2]:
                k = 1
                while k <= 3:
                    for j in handCopy:
                        if j[0] == cardValues[value]:
                            cardsReturn.append([cardValues[value],j[1]])
                            handCopy.remove([cardValues[value],j[1]])
                            k += 1
                handCopy.sort(key = sortFirstVal, reverse = True)
                return cardsReturn
            value += 1
        return False

    @staticmethod
    def threeOfKindCardsComplement(hand):
        handCopy = hand[:]
        cardValues = []
        cardsReturn = []
        for card in handCopy:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        value = 2
        while value < len(cardValues):
            if cardValues[value] == cardValues[value-2]:
                k = 1
                while k <= 3:
                    for j in handCopy:
                        if j[0] == cardValues[value]:
                            cardsReturn.append([cardValues[value],j[1]])
                            handCopy.remove([cardValues[value],j[1]])
                            k += 1
                handCopy.sort(key = sortFirstVal, reverse = True)
                return handCopy
            value += 1
        return False

    @staticmethod
    def isStraight(hand):
        cardValues = []
        count = 1
        for card in hand:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        i = 0
        while count < 5:
            if i == len(cardValues)-1:
                return False
            if cardValues[i+1] == cardValues[i]:
                i += 1
            elif cardValues[i+1] == cardValues[i]-1:
                i += 1
                count += 1
                if count == 5:
                    return True
            elif cardValues[i+1] < cardValues[i]-1:
                count = 1
                i += 1
        return False

    @staticmethod
    def straightCards(hand):
        cardValues = []
        count = 1
        cardsReturn = []
        for card in hand:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        i = 0
        while count < 5:
            if i == len(cardValues)-1:
                return False
            if cardValues[i+1] == cardValues[i]:
                i += 1
            elif cardValues[i+1] == cardValues[i]-1:
                for j in hand:
                    if cardValues[i] == j[0]:
                        cardsReturn.append([cardValues[i],j[1]])
                        break
                i += 1
                count += 1
                if count == 5:
                    for j in hand:
                        if cardValues[i] == j[0]:
                            cardsReturn.append([cardValues[i],j[1]])
                            break
                    return cardsReturn
                elif cardValues[i+1] < cardValues[i]-1:
                    count = 1
                    i += 1
                    cardsReturn = []
        return False

    @staticmethod
    def straightCardsTotal(hand):
        cardValues = []
        count = 1
        cardsReturn = []
        for card in hand:
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        i = 0
        while count < 5:
            if i == len(cardValues)-1:
                return False
            if cardValues[i+1] == cardValues[i]:
                i += 1
            elif cardValues[i+1] == cardValues[i]-1:
                for j in hand:
                    if cardValues[i] == j[0]:
                        cardsReturn.append([cardValues[i],j[1]])
                i += 1
                count += 1
                if count == 5:
                    for j in hand:
                        if cardValues[i] == j[0]:
                            cardsReturn.append([cardValues[i],j[1]])
                    return cardsReturn
            elif cardValues[i+1] < cardValues[i]-1:
                count = 1
                i += 1
                cardsReturn = []
        return False


    @staticmethod
    def isFlush(hand):
        types = []
        for card in hand:
            types.append(card[1])
        return (types.count(1) >= 5) or (types.count(2) >= 5) or (types.count(3) >= 5) or (types.count(4) >= 5)

    @staticmethod
    def flushCards(hand):
        types = []
        cardsReturn = []
        cardValues = []
        for card in hand:
            types.append(card[1])
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        if types.count(1) >= 5:
            for i in hand:
                if i[1] == 1:
                    cardsReturn.append(i)
                cardsReturn.sort(key = sortFirstVal, reverse = True)
            if len(cardsReturn) >= 5:
                return cardsReturn[:5]
        if types.count(2) >= 5:
            for i in hand:
                if i[1] == 2:
                    cardsReturn.append(i)
                cardsReturn.sort(key = sortFirstVal, reverse = True)
            if len(cardsReturn) >= 5:
                return cardsReturn[:5]
        if types.count(3) >= 5:
            for i in hand:
                if i[1] == 3:
                    cardsReturn.append(i)
                cardsReturn.sort(key = sortFirstVal, reverse = True)
            if len(cardsReturn) >= 5:
                return cardsReturn[:5]
        if types.count(4) >= 5:
            for i in hand:
                if i[1] == 4:
                    cardsReturn.append(i)
                cardsReturn.sort(key = sortFirstVal, reverse = True)
            if len(cardsReturn) >= 5:
                return cardsReturn[:5]
        return False

    @staticmethod
    def flushCardsTotal(hand):
        types = []
        cardsReturn = []
        cardValues = []
        for card in hand:
            types.append(card[1])
            cardValues.append(card[0])
        cardValues.sort(reverse = True)
        if types.count(1) >= 5:
            for i in hand:
                if i[1] == 1:
                    cardsReturn.append(i)
                cardsReturn.sort(key = sortFirstVal, reverse = True)
            if len(cardsReturn) >= 5:
                return cardsReturn
        if types.count(2) >= 5:
            for i in hand:
                if i[1] == 2:
                    cardsReturn.append(i)
                cardsReturn.sort(key = sortFirstVal, reverse = True)
            if len(cardsReturn) >= 5:
                return cardsReturn
        if types.count(3) >= 5:
            for i in hand:
                if i[1] == 3:
                    cardsReturn.append(i)
                cardsReturn.sort(key = sortFirstVal, reverse = True)
            if len(cardsReturn) >= 5:
                return cardsReturn
        if types.count(4) >= 5:
            for i in hand:
                if i[1] == 4:
                    cardsReturn.append(i)
                cardsReturn.sort(key = sortFirstVal, reverse = True)
            if len(cardsReturn) >= 5:
                return cardsReturn
        return False


    @staticmethod
    def fourOfKindCards(hand):
        handCopy = hand[:]
        cardValues = []
        cardsReturn = []
        for card in handCopy:
            cardValues.append(card[0])
        cardValues.sort()
        i = 3
        while i <= len(cardValues)-1:
            if cardValues[i] == cardValues[i-3]:
                #Add the four-of-a-kind cards to the hand
                cardsReturn.append([cardValues[i],1])
                cardsReturn.append([cardValues[i],2])
                cardsReturn.append([cardValues[i],3])
                cardsReturn.append([cardValues[i],4])
                #Add high card as fifth card in the hand
                handCopy.remove([cardValues[i],1])
                handCopy.remove([cardValues[i],2])
                handCopy.remove([cardValues[i],3])
                handCopy.remove([cardValues[i],4])
                handCopy.sort(key = sortFirstVal)
                handCopy.sort(key = sortFirstVal, reverse = True)
                return cardsReturn + [handCopy[0]]
            i += 1
        return False

    
    @staticmethod
    def isFullHouse(hand):
        if (TwoDCF.isThreeOfKind(hand)) and (TwoDCF.isOnePair(hand)):
            return TwoDCF.isOnePair(TwoDCF.threeOfKindCardsComplement(hand))
        else:
            return False

    @staticmethod
    def fullHouseCards(hand):
        return TwoDCF.threeOfKindCardsOnly(hand) + TwoDCF.onePairCardsOnly(TwoDCF.threeOfKindCardsComplement(hand))

    @staticmethod
    def isFourOfKind(hand):
        cardValues = []
        for card in hand:
            cardValues.append(card[0])
        cardValues.sort()
        i = 3
        while i <= len(cardValues)-1:
            if cardValues[i] == cardValues[i-3]:
                return True
            i += 1
        return False

    @staticmethod
    def isStraightFlush(hand):
        if TwoDCF.isStraight(hand):
            return TwoDCF.isFlush(TwoDCF.straightCardsTotal(hand))
        return False

    @staticmethod
    def straightFlushCards(hand):
        return TwoDCF.flushCards(TwoDCF.straightCardsTotal(hand))

    @staticmethod
    def pointValuation(hand):
        pointValue = 00000000000
        if TwoDCF.isOnePair(hand):
            pointValue = 10000000000
        if TwoDCF.isTwoPair(hand):
            pointValue = 20000000000
        if TwoDCF.isThreeOfKind(hand):
            pointValue = 30000000000
        if TwoDCF.isStraight(hand):
            pointValue = 40000000000
        if TwoDCF.isFlush(hand):
            pointValue = 50000000000
        if TwoDCF.isFullHouse(hand):
            pointValue = 60000000000
        if TwoDCF.isFourOfKind(hand):
            pointValue = 70000000000
        if TwoDCF.isStraightFlush(hand):
            pointValue = 80000000000
        return pointValue

    @staticmethod
    def fiveCardHand(hand):
        pointValue = TwoDCF.pointValuation(hand)
        if pointValue >= 80000000000:
            return TwoDCF.straightFlushCards(hand)
        if pointValue >= 70000000000:
            return TwoDCF.fourOfKindCards(hand)
        if pointValue >= 60000000000:
            return TwoDCF.fullHouseCards(hand)
        if pointValue >= 50000000000:
            return TwoDCF.flushCards(hand)
        if pointValue >= 40000000000:
            return TwoDCF.straightCards(hand)
        if pointValue >= 30000000000:
            return TwoDCF.threeOfKindCards(hand)
        if pointValue >= 20000000000:
            return TwoDCF.twoPairCards(hand)
        if pointValue >= 10000000000:
            return TwoDCF.onePairCards(hand)
        if pointValue >= 00000000000:
            return TwoDCF.highCardCards(hand)


 
class CF(object):        # Card Functions
    @staticmethod
    def highCardCards(hand):
        handCopy = hand[:]
        cardValues = [ ]
        cardsReturn = [ ]
        handCopy.sort(key = sortRank, reverse = True)
        return handCopy[:5]
            
 
    @staticmethod
    def hasOnePair(hand):
        cardValues = [ ]
        for card in hand:
            for i in cardValues:
                if i == card.rank:
                    return True
            cardValues.append(card.rank)
        return False
 
    @staticmethod
    def onePairCards(hand):
        handCopy = hand[:]
        cardValues = [ ]
        cardsReturn = [ ]
        for card in hand:
            cardValues.append(card.rank)
        cardValues.sort(reverse = True)
        i = 1
        while i <= len(cardValues)-1:
            if cardValues[i] == cardValues[i-1]:
                for card in hand:
                    if card.rank == cardValues[i]:
                        cardsReturn.append(card)
                        handCopy.remove(card)
                        if len(cardsReturn) >= 2:
                            handCopy.sort(key = sortRank,reverse = True)
                            return cardsReturn + handCopy[:3]
            i += 1
 
    @staticmethod
    def onePairCardsOnly(hand):
        cardValues = [ ]
        cardsReturn = [ ]
        for card in hand:
            cardValues.append(card.rank)
        cardValues.sort(reverse = True)
        i = 1
        while i <= len(cardValues)-1:
            if cardValues[i] == cardValues[i-1]:
                for card in hand:
                    if card.rank == cardValues[i]:
                        cardsReturn.append(card)
                        if len(cardsReturn) == 2:
                            break
                return cardsReturn
            i += 1
 
    @staticmethod
    def hasTwoPair(hand):
        cardValues = [ ]
        numOfPairs = 0
        for card in hand:
            foundPair = False
            for i in cardValues:
                if i == card.rank:
                    numOfPairs += 1
                    if numOfPairs == 2:
                        return True
                    cardValues.remove(card.rank)
                    foundPair = True
            if not foundPair:
                cardValues.append(card.rank)
        return False
    
    @staticmethod
    def twoPairCards(hand):
        handCopy = hand.copy()
        cardValues = [ ]
        cardsReturn = [ ]
        for card in hand:
            cardValues.append(card.rank)
        cardValues.sort(reverse = True)
        i = 1
        while i <= len(cardValues)-1:
            if cardValues[i] == cardValues[i-1]:
                for card in hand:
                    if card.rank == cardValues[i]:
                        cardsReturn.append(card)
                        if i == len(cardValues)-1:
                            continue
                        handCopy.remove(card)
            i += 1
            handCopy.sort(key = sortRank, reverse = True)
        cardsReturn.append(handCopy[0])
        return cardsReturn
 
    @staticmethod
    def hasThreeOfAKind(hand):
        cardValues = [ ]
        for card in hand:
            cardValues.append(card.rank)
        cardValues.sort(reverse=True)
        i = 2
        while i < len(cardValues)-1:
            if cardValues[i] == cardValues[i-2]:
                return True
            i += 1
        return False
 
 
    @staticmethod
    def threeOfAKindCards(hand):
        handCopy = hand[:]
        cardValues = []
        cardsReturn = []
        for card in hand:
            cardValues.append(card.rank)
        cardValues.sort(reverse = True)
        value = 2
        while value < len(cardValues):
            if cardValues[value] == cardValues[value-2]:
                k = 1
                while k <= 3:
                    for card in handCopy:
                        if card.rank == cardValues[value]:
                            cardsReturn.append(card)
                            handCopy.remove(card)
                            k += 1
                handCopy.sort(key = sortRank, reverse = True)
                return cardsReturn + handCopy[:2]
            value += 1
        return False
        
 
    @staticmethod
    def threeOfAKindCardsComplement(hand):      # needed for full house
        handCopy = hand[:]
        cardValues = [ ]
        cardsReturn = [ ]
        for card in handCopy:
            cardValues.append(card.rank)
        cardValues.sort(reverse = True)
        value = 2
        while value < len(cardValues):
            if cardValues[value] == cardValues[value-2]:
                k = 1
                while k <= 3:
                    for card in handCopy:
                        if card.rank == cardValues[value]:
                            cardsReturn.append(card)
                            handCopy.remove(card)
                            k += 1
                handCopy.sort(key = sortRank,reverse = True)
                return handCopy
            value += 1
        return False
 
    @staticmethod
    def threeOfAKindCardsOnly(hand):
        handCopy = hand[:]
        cardValues = [ ]
        cardsReturn = [ ]
        for card in handCopy:
            cardValues.append(card.rank)
        cardValues.sort(reverse = True)
        value = 2
        while value < len(cardValues):
            if cardValues[value] == cardValues[value-2]:
                k = 1
                while k <= 3:
                    for card in handCopy:
                        if card.rank == cardValues[value]:
                            cardsReturn.append(card)
                            handCopy.remove(card)
                            k += 1
                handCopy.sort(key = sortRank,reverse = True)
                return cardsReturn
            value += 1
        return False
 
    @staticmethod
    def hasStraight(hand):
        cardValues = [ ]
        count = 1
        for card in hand:
            cardValues.append(card.rank)
            cardValues.sort(reverse = True)
        i = 0
        while count < 5:
            if i == len(cardValues)-1:
                return False
            if cardValues[i+1] == cardValues[i]:
                i += 1
            elif cardValues[i+1] == cardValues[i]-1:
                i += 1
                count += 1
                if count == 5:
                    return True
            else:
                count = 1
                i += 1
        return False
 
    @staticmethod
    def straightCards(hand):
        cardValues = [ ]
        cardsReturn = [ ]
        count = 1
        for card in hand:
            cardValues.append(card.rank)
        cardValues.sort(reverse = True)
        i = 0
        while count < 5:
            if i == len(cardValues)-1:
                return False
            if cardValues[i+1] == cardValues[i]:
                i += 1
            elif cardValues[i+1] == cardValues[i]-1:    # the next card is one less than the current card
                for card in hand:       # I think i can change this to just append the card
                    if cardValues[i] == card.rank:
                        cardsReturn.append(card)
                        break
                i += 1
                count += 1
                if count == 5:
                    for card in hand:
                        if cardValues[i] == card.rank:
                            cardsReturn.append(card)
                            break
                    return cardsReturn
            elif cardValues[i+1] < cardValues[i]-1:
                count = 1
                i += 1
                cardsReturn = [ ]
        return False
 
    @staticmethod
    # take out the break so that multiple of the same card value can be returned
    def straightCardsTotal(hand):
        cardValues = [ ]
        cardsReturn = [ ]
        count = 1
        for card in hand:
            cardValues.append(card.rank)
        cardValues.sort(reverse = True)
        i = 0
        while count < 5:
            if i == len(cardValues)-1:
                return False
            if cardValues[i+1] == cardValues[i]:
                i += 1
            elif cardValues[i+1] == cardValues[i]-1:
                for card in hand:
                    if cardValues[i] == card.rank:
                        cardsReturn.append(card)
                i += 1
                count += 1
                if count == 5:
                    for card in hand:
                        if cardValues[i] == card.rank:
                            cardsReturn.append(card)
                    return cardsReturn
            elif cardValues[i+1] < cardValues[i]-1:
                count = 1
                i += 1
                cardsReturn = [ ]
        return False
 
    @staticmethod
    def hasFlush(hand):
        suits = [ ]
        for card in hand:
            suits.append(card.suit)
        return (suits.count(0) >= 5) or (suits.count(1) >= 5) or \
            (suits.count(2) >= 5) or (suits.count(3) >= 5)
 
    @staticmethod
    def flushCards(hand):
        suits = [ ]
        cardsReturn = [ ]
        handCopy = hand[:]
        handCopy.sort(key=sortSuit)
        for card in hand:
            suits.append(card.suit)
        for i in range(4):
            if suits.count(i) >= 5:
                for card in handCopy:
                    if card.suit == i:
                        cardsReturn.append(card)
                break
        if len(cardsReturn) != 0:
            cardsReturn.sort(key=sortRank,reverse = True)
            return cardsReturn
        return False
 
 
    @staticmethod
    def hasFullHouse(hand):
        if CF.hasThreeOfAKind(hand) and (CF.hasOnePair(hand)):
            return CF.hasOnePair(CF.threeOfAKindCardsComplement(hand))
        else:
            return False
 
    @staticmethod
    def fullHouseCards(hand):
        return CF.threeOfAKindCardsOnly(hand) + \
            CF.onePairCardsOnly(CF.threeOfAKindCardsComplement(hand))
 
    # make card ranks into a list, sort the list, check if the value of each card
    # is the same value as the rank of the card 4 spots further in the list
    @staticmethod
    def hasFourOfAKind(hand):
        cardValues = [ ]
        for card in hand:
            cardValues.append(card.rank)
        cardValues.sort()
        i = 3
        while i <= len(cardValues)-1:
            if cardValues[i] == cardValues[i-3]:
                return True
            i += 1
        return False
    
    # sort cards in a hand copy by rank, higher ranks first. Return the first four of a kind
    @staticmethod
    def fourOfAKindCards(hand):
        handCopy = hand[:]
        cardsReturn = [ ]
        handCopy.sort(key=sortRank,reverse=True)
        for i in range(3,len(handCopy)-1):
            if handCopy[i].rank == handCopy[i-3].rank:
                cardsReturn.append(handCopy[i-3])
                cardsReturn.append(handCopy[i-2])
                cardsReturn.append(handCopy[i-1])
                cardsReturn.append(handCopy[i])
        if len(cardsReturn) != 0:
            return cardsReturn
        return False
 
    @staticmethod
    def hasStraightFlush(hand):
        if CF.hasStraight(hand):
            return CF.hasFlush(CF.straightCardsTotal(hand))
        return False
 
    @staticmethod
    def straightFlushCards(hand):
        return CF.flushCards(CF.straightCardsTotal(hand))
 
    @staticmethod
    def pointValuation(hand):
        if CF.hasStraightFlush(hand):
            return 80000000000
        if CF.hasFourOfAKind(hand):
            return 70000000000
        if CF.hasFullHouse(hand):
            return 60000000000
        if CF.hasFlush(hand):
            return 50000000000
        if CF.hasStraight(hand):
            return 40000000000
        if CF.hasThreeOfAKind(hand):
            return 30000000000
        if CF.hasTwoPair(hand):
            return 20000000000
        if CF.hasOnePair(hand):
            return 10000000000
        return 00000000000
 
 
    # make a point value that is higher depending on the specific five cards that are in your hand to determine how good a hand is
    # after already figuring out its type of hand (example: if we have a two-pair, we want to account for in the point valuation
    # which two cards make up the two pair. A two-pair of aces and kings beats a two-pair of 2s and 3s)
    @staticmethod
    def tieBreaker(hand,pointValue):
        j = 2
        for card in hand:
            if j == 2:
                pointValue += (card.rank+1)*10**(10-j)      # card.rank+1 is because the actual rank is 1 higher than the rank                                              
            else:                                           # assigned in the card class. card.rank*2 double weights the first card
                pointValue += (card.rank+1)*10**(10-j)
            j += 2
        return int(pointValue)
 
    @staticmethod
    def getFiveCardHand(hand,pointValue):
        if pointValue >= 80000000000:
            return CF.straightFlushCards(hand)
        if pointValue >= 70000000000:
            return CF.fourOfAKindCards(hand)
        if pointValue >= 60000000000:
            return CF.fullHouseCards(hand)
        if pointValue >= 50000000000:
            return CF.flushCards(hand)
        if pointValue >= 40000000000:
            return CF.straightCards(hand)
        if pointValue >= 30000000000:
            return CF.threeOfAKindCards(hand)
        if pointValue >= 20000000000:
            return CF.twoPairCards(hand)
        if pointValue >= 10000000000:
            return CF.onePairCards(hand)
        if pointValue >= 00000000000:
            return CF.highCardCards(hand)
 
    @staticmethod
    def getHandName(pointValue):
        if pointValue >= 80000000000:
            return "Straight Flush"
        elif pointValue >= 70000000000:
            return "Four of a Kind"
        elif pointValue >= 60000000000:
            return "Full House"
        elif pointValue >= 50000000000:
            return "Flush"
        elif pointValue >= 40000000000:
            return "Straight"
        elif pointValue >= 30000000000:
            return "Three of a Kind"
        elif pointValue >= 20000000000:
            return "Two Pair"
        elif pointValue >= 10000000000:
            return "Pair"
        elif pointValue >= 00000000000:
            return "High Card"
 
class TitleScreenButton(object):
    def __init__(self,app,text,fontDims,x,y):
        self.app = app
        self.text = text
        self.fontDims = fontDims
        self.font = f"Helvetica {int(self.fontDims)}"
        self.LGurl = "LightGray.png"
        self.DGurl = "DarkGray.png"
        self.LGimage = self.app.loadImage(self.LGurl)
        self.DGimage = self.app.loadImage(self.DGurl)
        self.x,self.y = x,y
        self.w,self.h = self.app.width/2,self.app.height/8
        x1,y1 = 0,0
        x2,y2 = self.w,self.h
        self.image1 = self.LGimage.crop((x1,y1,x2,y2))
        self.image2 = self.DGimage.crop((x1,y1,x2,y2))
        self.image = self.image1
        self.wr,self.hr = self.w/2,self.h/2
        self.spritestrip = [self.image1,self.image2]
        self.location = (self.x-self.wr,self.y-self.hr,self.x+self.wr,self.y+self.hr)
    
 
class TitleScreenMode(Mode):
    def appStarted(self):
        self.background = self.loadImage("InstructionsBackground.png")
        self.background = self.app.scaleImage(self.background, 11/10)     
        self.deck = Deck(self,shuffled=False)
        self.initialize112Cards()
        self.iButton = TitleScreenButton(self.app,"Instructions",self.app.width/20,self.app.width/2,14*self.app.height/20)  #instructions button
        self.gButton = TitleScreenButton(self.app,"Play Game",self.app.width/20,self.app.width/2,11*self.app.height/20)  #play game button
 
 
    def mouseMoved(self,event):
        x1,y1,x2,y2 = self.iButton.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            self.iButton.image = self.iButton.image2
        else:
            self.iButton.image = self.iButton.image1
 
        x1,y1,x2,y2 = self.gButton.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            self.gButton.image = self.gButton.image2
        else:
            self.gButton.image = self.gButton.image1
 
    def initialize112Cards(self):
        self.aces = [self.deck.cards[12],self.deck.cards[25],self.deck.cards[38],self.deck.cards[51]]   # initialize 112 cards
        self.ace1 = self.aces.pop(random.randint(0,3))
        self.ace2 = self.aces.pop(random.randint(0,2))
        x = self.app.width-175      # 3*self.app.width/4
        y = 7*self.app.height/8     # 7*self.app.height/8
        self.distanceBetweenCards = self.app.width/20     
        self.ace1.x,self.ace1.y = x,y
        self.ace2.x,self.ace2.y = x+self.distanceBetweenCards,y
        self.twos = [self.deck.cards[0],self.deck.cards[13],self.deck.cards[26],self.deck.cards[39]]
        self.two = self.twos.pop(random.randint(0,3))
        self.two.x,self.two.y = x+(2*self.distanceBetweenCards),y
        self.cards = [self.ace1,self.ace2,self.two]
 
    def redrawAll(self,canvas):
        width = self.app.width
        height = self.app.height
        # canvas.create_image(width/2, height/2, image=ImageTk.PhotoImage(self.grayBackground))
        canvas.create_image(self.app.width/2,self.app.height/2, image=ImageTk.PhotoImage(self.background))
        self.drawTitle(canvas)
        self.draw112Cards(canvas)
        self.drawButtons(canvas)
 
    def draw112Cards(self,canvas):
        canvas.create_image(self.ace1.x,self.ace1.y,image=ImageTk.PhotoImage(self.ace1.cardImage))
        canvas.create_image(self.ace2.x,self.ace2.y,image=ImageTk.PhotoImage(self.ace2.cardImage)) # cardImage
        canvas.create_image(self.two.x,self.two.y,image=ImageTk.PhotoImage(self.two.cardImage))
 
    def drawButtons(self,canvas):
        canvas.create_image(self.iButton.x,self.iButton.y,image=ImageTk.PhotoImage(self.iButton.image))
        canvas.create_text(self.iButton.x,self.iButton.y,text=self.iButton.text,font=self.iButton.font)
        canvas.create_image(self.gButton.x,self.gButton.y,image=ImageTk.PhotoImage(self.gButton.image))
        canvas.create_text(self.gButton.x,self.gButton.y,text=self.gButton.text,font=self.gButton.font)
 
    def sizeChanged(self):
        #self.fixLocationOf112Cards()
        self.fixLocationOfButtons()
 
    def fixLocationOf112Cards(self):
        w,h = self.width,self.height
        i = -1
        for card in self.cards:
            i += 1
            x = 3*w/4
            y = 7*h/8
            card.x,card.y = x,y
            card.x,card.y = x+i*self.distanceBetweenCards,y
 
    def fixLocationOfButtons(self):
        w,h = self.width,self.height
        self.iButton.x,self.iButton.y = w/2,14*h/20
        self.iButton.w,self.iButton.h = w/2,h/8
        self.iButton.wr,self.iButton.hr = self.iButton.w/2,self.iButton.h/2
        self.iButton.location = (self.iButton.x-self.iButton.wr,self.iButton.y-self.iButton.hr,\
            self.iButton.x+self.iButton.wr,self.iButton.y+self.iButton.hr)
        
        self.gButton.x,self.gButton.y = w/2,11*h/20
        self.gButton.w,self.gButton.h = w/2,h/8
        self.gButton.wr,self.gButton.hr = self.gButton.w/2,self.gButton.h/2
        self.gButton.location = (self.gButton.x-self.gButton.wr,self.gButton.y-self.gButton.hr,\
            self.gButton.x+self.gButton.wr,self.gButton.y+self.gButton.hr)
 
    def mousePressed(self,event):
        if self.iButton.image == self.iButton.image2:
            self.app.setActiveMode(self.app.instructionsMode)
        elif self.gButton.image == self.gButton.image2:
            self.app.setActiveMode(self.app.gameMode)
 
            
    def drawTitle(self,canvas):
        text = "Program Poker"
        x,y,color = self.app.width/2,self.app.height/4,"darkred"       # red4
        font = f"Times {int(self.app.width/7)} bold italic"
        canvas.create_text(x,y,text=text,fill=color,font=font)
        
# from http://www.cs.cmu.edu/~112/notes/week5-case-studies.html and http://www.cs.cmu.edu/~112/notes/notes-oop-part3.html
class Card(object):
    numberNames = [None, "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K","A"]
    suitNames = ["♣", "♦", "♥", "♠"]
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    def __init__(self,app,rank,suit):
        self.app = app
        self.rank = rank    # from 0 to 12
        self.suit = suit    # from 0 to 3
        self.rank1 = Card.numberNames[rank]
        self.suit1 = Card.suitNames[suit]
        self.spritestrip= [ ]
        self.frontUrl = "FrontOfCards.png"
        self.backUrl = "BackOfCard.png"
        self.image = self.app.loadImage(self.frontUrl)
        self.rbackImage = self.app.loadImage(self.backUrl)  # red back image
        self.bbackImage = self.app.loadImage(self.backUrl)  # blue back image
        x1,y1 = 1+42*(self.rank-1),1+62*(self.suit)
        x2,y2 = x1+41,y1+61
        self.cardImage = self.image.crop((x1,y1,x2,y2))
        self.cardImage = self.app.scaleImage(self.cardImage, 7/4)
        x1,y1 = 938,2
        x2,y2 = 1005,94
        self.rbackImage = self.rbackImage.crop((x1,y1,x2,y2))
        self.rbackImage = self.app.scaleImage(self.rbackImage,9/8)
        x1,y1 = 938,99
        x2,y2 = 1005,191
        self.bbackImage = self.bbackImage.crop((x1,y1,x2,y2))
        self.bbackImage = self.app.scaleImage(self.bbackImage,9/8)
        self.spritestrip = [self.cardImage,self.rbackImage,self.bbackImage]
        self.x = None
        self.y = None
        self.location = (self.x,self.y)
 
    # from http://www.cs.cmu.edu/~112/notes/notes-oop-part3.html
    def __repr__(self):
        return f"{self.rank1}{self.suit1}"
 
    # from http://www.cs.cmu.edu/~112/notes/notes-oop-part3.html
    def getHashables(self):
        return (self.number, self.suit) # return a tuple of hashables
 
    # from http://www.cs.cmu.edu/~112/notes/notes-oop-part3.html
    def __hash__(self):
        return hash(self.getHashables())
 
    # from http://www.cs.cmu.edu/~112/notes/notes-oop-part3.html
    def __eq__(self, other):
        return (isinstance(other, Card) and
                (self.rank == other.rank) and
                (self.suit == other.suit))
 
 
# from http://www.cs.cmu.edu/~112/notes/week5-case-studies.html
class Deck(object):
    numberNames = [None, "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King","Ace"]
    suitNames = ["♣", "♦", "♥", "♠"]
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    def __init__(self,app,shuffled=True):
        self.app = app
        self.cards = [ ]
        self.initializeCards(shuffled)
    def initializeCards(self,shuffled):
        for suit in range(4):
            for number in range(1,14):
                self.cards.append(Card(self.app,number,suit))
        if (shuffled):
            random.shuffle(self.cards)
 
 
 
 
class VDeck(Deck):      # viewable deck
    def __init__(self,app,x,y,color,shuffled=True):
        super().__init__(app)
        self.color = color
        self.x = x
        self.y = y
        self.url = "BackOfCard.png"
        self.image = self.app.loadImage(self.url)
        if color == "red":
            x1,y1 = 938,2
            x2,y2 = 1005,94
            self.image = self.image.crop((x1,y1,x2,y2))
            self.image = self.app.scaleImage(self.image,9/8)
        else:
            x1,y1 = 938,99
            x2,y2 = 1005,190
            self.image = self.image.crop((x1,y1,x2,y2))
            self.image = self.app.scaleImage(self.image,9/8)
 
 
 
    # from from http://www.cs.cmu.edu/~112/notes/week5-case-studies.html
    def dealCard(self):
        return None if (self.cards == [ ]) else self.cards.pop()
 
 
class InstructionsMode(Mode):
    def appStarted(self):
        self.background = self.loadImage("PatternedGrayBackground4.png")
        self.background = self.scaleImage(self.background, 3)



    def redrawAll(self,canvas):
        canvas.create_image(self.app.width/2,self.app.height/2, image=ImageTk.PhotoImage(self.background))
        canvas.create_text(self.app.width/2,self.app.height/10,text="Instructions:",font="Helvetica 60 bold")

        canvas.create_text(13*self.app.width/28,self.app.height/5,text=\
            """
            -The rules are the standard rules of Texas Hold'em poker. 
            
            -Every player starts with 2 cards.

            -Small blind ante of $15, big blind ante of $30,

            -Every player starts with $500. 
            
            -If there is already a bet on the table, you can either call (put in that amount of 
            money into the pot) or fold (leave the round without putting money in). 
            
            -If there is not a bet on the table, you can either bet, fold, or check (neither bet or fold).



            -On the top right of the screen there are two icons. 
            
            -The poker cards icon will take you to a screen that lists the classifications of poker hands and their order by hand strength. 
            
            -The dice icon will take you to a screen that shows you your probabilities with your hand of getting each other kind of hand.
            
            """,anchor="n",font="Helvetica 16 bold")
        canvas.create_text(self.app.width/2,9*self.app.height/10,text="(Click anywhere to go back.)",font="Helvetica 20")
 
    def mousePressed(self,event):
        self.app.setActiveMode(self.app.titleScreenMode)
 
 
class Hand(object):
    def __init__(self):
        self.cards = [ ]
 
class Player(object):
    def __init__(self,app):
        self.app = app
        self.money = 500
        self.isFolded = False
        self.isBankrupt = False
        self.cards = [ ]
        self.name = "You"   # updated in gameMode.doIntroduction()
        self.currentBet = 0
        self.allIn = False
 
    
    def check(self):
        self.app.gameMode.messageBox.q.append(f"{self.name} checks.")  
        self.app.gameMode.cPindex += 1
        self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
        self.app.gameMode.consecNonBets += 1
        self.app.gameMode.doBets()
 

    def bet(self):
        bet = self.app.gameMode.getUserInput("How much would you like to bet?")
        while type(bet) != int:   # converting into an integer
            try:
                bet = int(bet)
                if bet < 0:
                    raise Exception
                if bet > self.money:
                    bet = self.money
                    confirm = self.app.gameMode.getUserInput(f"Would you like to go all in? (yes/no)")
                    if confirm not in ["yes","y"]:
                        raise Exception
            except:     # invalid input
                bet = self.getUserInput(f"Sorry, that is an invalid input. How much would you like to bet? (Please type a number)")
        self.app.gameMode.messageBox.q.append(f"{self.name} bets ${bet}.")
        self.app.gameMode.cPindex += 1
        self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
        self.currentBet = bet
        self.money -= bet
        if self.money == 0:
            self.allIn = True
        self.app.gameMode.pot += bet
        self.app.gameMode.currentBet += bet
        self.app.gameMode.consecNonBets = 1
        self.app.gameMode.doBets()
 
    def fold(self):
        self.app.gameMode.messageBox.q.append(f"{self.name} folds.")
        self.app.gameMode.playersLeft.remove(self)
        self.isFolded = True
        if self == self.app.gameMode.playersLeft[-1]:
            self.app.gameMode.cPindex %= self.app.gameMode.playersLeft
        if self.c1 in self.app.gameMode.cards:
            self.app.gameMode.cards.remove(self.c1)
        if self.c2 in self.app.gameMode.cards:
            self.app.gameMode.cards.remove(self.c2)
        self.cards = [ ]
        self.app.gameMode.doBets()
 
    def raiseBet(self):
        bet = self.app.gameMode.getUserInput("How much would you like to raise?")
        while type(bet) != int:   # converting into an integer
            try:
                bet = int(bet)
                if bet < 0: #or self.money < bet + self.app.gameMode.currentBet - self.currentBet:
                    raise Exception
                if self.money < bet + self.app.gameMode.currentBet - self.currentBet:
                    bet = self.money
                    confirm = self.app.gameMode.getUserInput("Would you like to go all in? (yes/no)")
                    if confirm not in ["yes","y"]:
                        raise Exception
            except:     # invalid input
                bet = self.app.gameMode.getUserInput(f"Sorry, that is an invalid input. How much would you like to raise? (Please type a number)")
        self.app.gameMode.cPindex += 1
        self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
        self.money -= bet
        self.money -= self.app.gameMode.currentBet
        self.money += self.currentBet
        if self.money <= 0:
            self.allIn = True
        self.app.gameMode.pot += bet
        self.app.gameMode.pot += self.app.gameMode.currentBet
        self.app.gameMode.pot -= self.currentBet
        self.currentBet = bet + self.app.gameMode.currentBet
        self.app.gameMode.consecNonBets = 1
        self.app.gameMode.currentBet += bet
        self.app.gameMode.messageBox.q.append(f"{self.name} raises ${bet} to ${self.app.gameMode.currentBet}.")
        self.app.gameMode.doBets()
 
    def call(self):
        bet = self.app.gameMode.currentBet - self.currentBet
        if bet >= self.money:
            bet = self.money
            self.allIn = True
        self.app.gameMode.messageBox.q.append(f"{self.name} calls.")
        self.app.gameMode.cPindex += 1
        self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
        self.app.gameMode.consecNonBets += 1
        self.money -= bet
        self.currentBet += bet
        self.app.gameMode.pot += bet
        self.app.gameMode.doBets()
 
 
    def __repr__(self):
        return f"{self.name}"
 
class ComputerPlayer(Player):
    def __init__(self,app,x,y,playerNum,dBetweenCards):
        super().__init__(app)
        self.app = app
        self.x = x
        self.y = y
        self.playerNum = playerNum
        self.dBetweenCards = dBetweenCards
        dUp = -self.app.height/30
        self.CS1 = CardSilhouette(self.app,x-dBetweenCards,y+self.app.height/50+dUp)    # card silhouette 1
        self.CS2 = CardSilhouette(self.app,x+dBetweenCards,y+dUp)                # card silhouette 2
        self.scale = 1/2
        self.CS1.image = self.app.scaleImage(self.CS1.image,GameMode.scale)
        self.CS2.image = self.app.scaleImage(self.CS2.image,GameMode.scale)
        self.isBigBlind = False
        self.isSmallBlind = False
        self.currentBet = 0
        self.allIn = False
        self.handStrength = 0
        self.totalRoundBet = 0
       
    
    def doTurn(self):
        print(f"player {self.playerNum}'s turn")
        print(f"cPindex = ",self.app.gameMode.cPindex)
        print(f"len(playersLeft) = {len(self.app.gameMode.playersLeft)}")
        if self.allIn:
            print(f"player {self.playerNum} is all in")
            self.app.gameMode.messageBox.q.append(f"Player {self.playerNum} is all in!")
            self.app.gameMode.cPindex += 1
            self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
            self.app.gameMode.consecNonBets += 1
            return
        self.handStrength = MC.strength(self.hand)

        betMax = 1000
        decisionToBet = random.randint(0,betMax)    
        bluffF = 50     # randomly bet sometimes
        indivHandStrength = self.handStrength - (1/4)*self.app.gameMode.tableCardsStrength  
        strengthF = 30*indivHandStrength 
        betting = int(bluffF + strengthF)
        if self.app.gameMode.currentBet == 0:     # betting
            if decisionToBet <= betting:
                self.app.gameMode.noFirstRoundBets = False
                factor = (5/2)
                bet = factor*indivHandStrength
                bluffing = random.randint(0,100)        # bluff every once in a while
                if bluffing <= 5:
                    bet += 15
                    bet *= 2
                variance = random.randint(-50,50)
                variance /= 100
                bet += variance*bet
                bet = int(bet)
                bet += 5-(bet%5)
                print("betting")
                if bet >= self.money:
                    bet = self.money
                    self.allIn = True
                    self.app.gameMode.messageBox.q.append(f"player {self.playerNum} is going all in with ${bet}!")
                else:
                    self.app.gameMode.messageBox.q.append(f"player {self.playerNum} bets ${bet}.")
                self.app.gameMode.cPindex += 1
                self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
                self.money -= bet
                self.app.gameMode.pot += bet
                self.app.gameMode.currentBet += bet
                self.app.gameMode.consecNonBets = 1
                return
            else:
                print("checking1")
                self.app.gameMode.messageBox.q.append(f"player {self.playerNum} checks.")       # checking
                self.app.gameMode.cPindex += 1
                self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
                self.app.gameMode.consecNonBets += 1
                return


        else:           # folding
            if self.currentBet < self.app.gameMode.currentBet: 
                foldMaximum = 1000
                # Round Factor. More likely to fold in earlier rounds. The 3 dilutes the factor. 
                roundF = 3/(self.app.gameMode.bettingRound+3)  
                # Bet Factor. Less likely to fold if the player has already invested a lot of money. 
                betF = self.app.gameMode.currentBet/((self.currentBet+20))  
                # strength of player's hand minus a factor of the table card strength
                indivHandStrength = self.handStrength - (1/4)*self.app.gameMode.tableCardsStrength  
                indivHandStrength *= 8 
                strengthF = 7000/indivHandStrength     # strength factor
                # scalingF = 1000                   # multiply by 1000 to get within the range
                decisionToFold = random.randint(1,foldMaximum)
                # the decision to fold is based on the current round, the player's previous investment in the round,
                # the bet on the table, the strength of the player's hand, and the strength of the table cards
                folding = int(roundF*betF*strengthF)
                if decisionToFold <= folding:           # fold
                    print("folding")
                    self.app.gameMode.messageBox.q.append(f"player {self.playerNum} folds.")
                    self.app.gameMode.playersLeft.remove(self)
                    if self == self.app.gameMode.playersLeft[-1]:
                        self.app.gameMode.cPindex %= self.app.gameMode.playersLeft
                    self.app.gameMode.cards.remove(self.c1)
                    self.app.gameMode.cards.remove(self.c2)
                    self.cards = [ ]
                    return
                else:               # raising
                    raiseMax = 1000
                    decisionToRaise = random.randint(0,raiseMax)
                    raisesAlreadyF = 1/(5*(self.app.gameMode.raisesAlready+1))     
                    bluffF = 15     # randomly sometimes raise
                    indivHandStrength = self.handStrength - (1/4)*self.app.gameMode.tableCardsStrength  
                    strengthF = 100*indivHandStrength     
                    raising = int(bluffF + strengthF*raisesAlreadyF)
                    if decisionToRaise <= raising:     # raise
                        print("raising")
                        self.app.gameMode.raisesAlready += 1
                        factor = (5/2)
                        bet = factor*indivHandStrength
                        variance = random.randint(-50,50)
                        variance /= 100
                        bet += variance*bet
                        bet = int(bet)
                        bet += 5-(bet%5)
                        if bet >= self.money:
                            bet = self.money
                            self.allIn = True
                            self.app.gameMode.cPindex += 1
                            self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
                            self.money -= bet
                            self.app.gameMode.pot += bet
                            self.currentBet = bet 
                            self.totalRoundBet += bet 
                            self.app.gameMode.consecNonBets = 1
                            self.app.gameMode.currentBet = bet
                            self.app.gameMode.messageBox.q.append(f"player {self.playerNum} is going all in with ${bet}!")
                            return
                        self.app.gameMode.cPindex += 1
                        self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
                        self.money -= bet
                        self.money -= self.app.gameMode.currentBet
                        self.money += self.currentBet
                        self.app.gameMode.pot += bet
                        self.app.gameMode.pot += self.app.gameMode.currentBet
                        self.app.gameMode.pot -= self.currentBet
                        self.currentBet = bet + self.app.gameMode.currentBet
                        self.totalRoundBet += bet + self.app.gameMode.currentBet
                        self.app.gameMode.consecNonBets = 1
                        self.app.gameMode.currentBet += bet
                        self.app.gameMode.messageBox.q.append(f"player {self.playerNum} raises ${bet} to ${self.app.gameMode.currentBet}.")
                        return
                    else:               # calling
                        bet = self.app.gameMode.currentBet - self.currentBet
                        if bet >= self.money:
                            bet = self.money
                            self.allIn = True
                        print("calling")
                        self.app.gameMode.messageBox.q.append(f"player {self.playerNum} calls.")
                        self.app.gameMode.cPindex += 1
                        self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
                        self.app.gameMode.consecNonBets += 1
                        self.money -= bet
                        self.app.gameMode.pot += bet
                        self.currentBet += bet
                        self.totalRoundBet += bet
                        return
            else:
                print("checking2")
                self.app.gameMode.messageBox.q.append(f"player {self.playerNum} checks.")       # checking
                self.app.gameMode.cPindex += 1
                self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
                self.app.gameMode.consecNonBets += 1
                return
        print("checking3")
        self.app.gameMode.messageBox.q.append(f"player {self.playerNum} checks.")       # checking
        self.app.gameMode.cPindex += 1
        self.app.gameMode.cPindex %= len(self.app.gameMode.playersLeft)
        self.app.gameMode.consecNonBets += 1
        return

 
    def __repr__(self):
        return f"Player {self.playerNum}"
 
class CardSilhouette(object):
    scale = 38/96
    def __init__(self,app,x,y):
        self.app = app
        self.x = x
        self.y = y
        self.url = "CardSil.png"
        self.image = self.app.loadImage(self.url)
        x1,y1 = 4,11
        x2,y2 = 180,280
        self.image = self.image.crop((x1,y1,x2,y2))
        self.image = self.app.scaleImage(self.image, CardSilhouette.scale)
        self.location = (self.x,self.y)
 
class MessageBox(object):
    def __init__(self,app):
        self.app = app
        self.wr = 84*self.app.width/256      # width of mb
        self.hr = 65*self.app.height/576     # height of mb
        self.cx = self.app.width/2      # x location
        self.cy = 19*self.app.height/48 # y location
        self.color = "white"
        self.dBetween = self.app.height/36      # 70distance between lines
        self.q = ["","","","","","","","","","","","","",""]  # message Queue
 
 
class Button(object):
    def __init__(self,app,text,fontDims,x,y,width,height):
        self.app = app
        self.text = text
        self.fontDims = fontDims
        self.font = f"Helvetica {int(self.fontDims)}"
        self.LGurl = "LightGray.png"
        self.DGurl = "DarkGray.png"
        self.Turl = "TransparentBackground.png"     # transparent url
        self.LGimage = self.app.loadImage(self.LGurl)
        self.DGimage = self.app.loadImage(self.DGurl)
        self.Timage = self.app.loadImage(self.Turl)
        self.x,self.y = x,y
        self.w,self.h = width,height
        x1,y1 = 0,0
        x2,y2 = self.w,self.h
        self.image1 = self.LGimage.crop((x1,y1,x2,y2))
        self.image2 = self.DGimage.crop((x1,y1,x2,y2))
        self.Timage = self.Timage.crop((x1,y1,x2,y2))
        self.image = self.image1
        self.wr,self.hr = self.w/2,self.h/2
        self.spritestrip = [self.image1,self.image2]
        self.location = (self.x-self.wr,self.y-self.hr,self.x+self.wr,self.y+self.hr)
 
class CardsIcon(object):
    def __init__(self,app,x,y):
        self.app = app
        self.x = x
        self.y = y
        self.r = 25     # this affects the area that can be clicked on and hovered over
        self.image1 = self.app.loadImage("CardsIcon.png")
        self.image1 = self.app.scaleImage(self.image1,1/4)
        self.image2 = self.app.loadImage("CardsIcon.png")     # ShadowCards.png
        self.image2 = self.app.scaleImage(self.image2,1/3)
        self.image = self.image1
        self.spritestrip = [self.image1,self.image2]
        self.location = (self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r)


class ProbabilityIcon(object):
    def __init__(self,app,x,y):
        self.app = app
        self.x = x
        self.y = y
        self.r = 25     # this affects the area that can be clicked on and hovered over
        self.image1 = self.app.loadImage("ProbabilityIcon.png")
        self.image1 = self.app.scaleImage(self.image1,1/6)
        self.image2 = self.app.loadImage("ProbabilityIcon.png")
        self.image2 = self.app.scaleImage(self.image2,1/4)
        self.image = self.image1
        self.spritestrip = [self.image1,self.image2]
        self.location = (self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r)



class GameMode(Mode):
    scale = 3/4
    def appStarted(self):
        self.doneWithSetUp = False
        x,y = 19*self.app.width/20,self.app.height/12
        self.cardsIcon = CardsIcon(self.app,x,y)
        x,y = 17*self.app.width/20,self.app.height/12
        self.probIcon = ProbabilityIcon(self.app,x,y)
        self.transCall,self.transFold,self.transBet = False,False,False
        self.transRaise,self.transCheck = False,False
        self.showCards = False
        self.playerCards = [ ]
        self.compPlayerCards = [ ]
        self.noFirstRoundBets = True
        self.currentBet = 0
        self.r1,self.r2,self.r3,self.r4 = False,False,False,False       # rounds
        self.messageBox = MessageBox(self.app)
        self.greenBackground = self.loadImage("GreenBackground.png")
        self.pokerChip = self.loadImage("Chip.png")
        x1,y1 = 0,10        # cut off white spot at the top of chip
        x2,y2 = 200,200
        self.pokerChip = self.pokerChip.crop((x1,y1,x2,y2))
        self.pokerChip = self.app.scaleImage(self.pokerChip, 2/3)
        self.setUpButtons()
        self.sils = [ ]                 #silhouettes
        self.gameOver = False
        self.round = 1
        self.raisesAlready = 0      # raises during a round
        self.bettingRound = 0
        self.hand = [ ]             # table cards hand
        self.cs1 = None
        self.setUpCardSilhouettes()
        self.w,self.h = self.app.width,self.app.height
        self.player = Player(self.app)
        self.setUpDeck()
        self.player.totalPointValuation = None
        self.player.hand = [ ]
        self.player.pointValuation = 0
        self.pot = 0
        self.cards = [ ]
        self.player.fiveCardHand = CF.getFiveCardHand(self.player.hand,self.player.pointValuation)
        self.compPlayers = [ ]
        self.totalPlayers = [self.player]
        self.isIntroduction = False
        self.doIntroduction()
        self.isIntroduction = True
        self.cardHeight = (280-11)*GameMode.scale*CardSilhouette.scale
        self.pointValuation = CF.pointValuation(self.player.hand)
        self.fiveCardHand = CF.getFiveCardHand(self.player.hand,self.pointValuation)
        self.totalPointValuation = CF.tieBreaker(self.fiveCardHand,self.pointValuation)
        self.doneWithSetUp = True
        self.r1 = True      # start round 1
        self.doRound1()
 
 
    def setUpButtons(self):
        self.buttons = [ ]
        fontDims = self.app.width/25
        x = self.app.width/2
        yInitial = (36/50)*self.app.height
        dY = (3/50)*self.app.height
        w,h = self.app.width/5,self.app.height/20
        self.foldButton = Button(self.app,"Fold",fontDims,x,yInitial,w,h)
        self.checkButton = Button(self.app,"Check",fontDims,x,yInitial+dY,w,h)
        self.betButton = Button(self.app,"Bet",fontDims,x,yInitial+2*dY,w,h)
        self.raiseButton = Button(self.app,"Raise",fontDims,x,yInitial+3*dY,w,h)
        self.callButton = Button(self.app,"Call",fontDims,x,yInitial+4*dY,w,h)
        self.buttons.append(self.foldButton)
        self.buttons.append(self.checkButton)
        self.buttons.append(self.betButton)
        self.buttons.append(self.raiseButton)
        self.buttons.append(self.callButton)
 
    def setUpDeck(self):
        self.deckColors = ["red","blue"]
        self.pDeckColor = "red"             # primary deck color
        self.sDeckColor = "blue"            # secondary deck color
        self.colorIndex = 0
        self.deckX,self.deckY = 8*self.app.width/9,self.tcsL[1]*self.h
        self.deck = VDeck(self.app,self.deckX,self.deckY,self.deckColors[self.colorIndex%2])
 
    def setUpBlinds(self):
        self.blindUrl = "Blinds.png"
        self.bBimage = self.app.loadImage(self.blindUrl)
        x1,y1,x2,y2 = 0,0,300,300
        self.bBimage = self.bBimage.crop((x1,y1,x2,y2))
        self.bBimage = self.app.scaleImage(self.bBimage, 1/8)
        self.sBimage = self.app.loadImage(self.blindUrl)
        x1,y1,x2,y2 = 500,0,850,350
        self.sBimage = self.sBimage.crop((x1,y1,x2,y2))
        self.sBimage = self.app.scaleImage(self.sBimage, 1/8)
        self.bBindex = random.randint(0,self.playersCount)      # big blind index
        self.sBindex = (self.bBindex+1)%(self.playersCount+1)       # small blind index
    
 
    def doIntroduction(self):
        width,height = self.app.width,self.app.height
        self.playerName = self.getUserInput("What is your name? ")
        self.player.name = self.playerName
        constraints = [2,3,4,5,6,7,8]
        self.playersCount = self.getUserInput(f"How many players would you like to play against? (between 2-{len(constraints)+1})")
        while self.playersCount not in constraints:   # invalid input
            try:
                self.playersCount = int(self.playersCount)
                if self.playersCount not in constraints: 
                    self.playersCount = self.getUserInput(f"Sorry, that number of players is out of range.\n How many players would you like to play against? (between 2-{len(constraints)+1})")
            except:
                self.playersCount = self.getUserInput(f"Sorry, that number of players is out of range.\n How many players would you like to play against? (between 2-{len(constraints)+1})")
        self.isIntroduction = False
        self.setUpCompLocations()
    
    # from writing_session3_practice.py with changes
    def setUpCompLocations(self):
        width,height = self.app.width,self.app.height
        pi = math.pi
        r = 3*width/7
        cx = width/2
        cy = 3*height/7
        playerNum = 0
        dBetweenCompCards = width/75
        for compPlayer in range(self.playersCount):
            playerNum += 1
            theta = compPlayer*pi/self.playersCount+(1/4)
            x = r*math.cos(theta) + cx
            y = -(7/15)*r*math.sin(theta) + cy
            newPlayer = ComputerPlayer(self.app,x,y,playerNum,dBetweenCompCards)
            self.compPlayers.append(newPlayer)
            self.totalPlayers.append(newPlayer)
            self.sils.append(newPlayer.CS1)
            self.sils.append(newPlayer.CS2)
        self.setUpBlinds()
        self.initCards()
        self.messageBox.q.append(f"Welcome, {self.playerName}!")
        self.messageBox.q.append("Thank you for playing Program Poker!")
        self.messageBox.q.append(f"You will be playing against {self.playersCount} players.")
 
    def doBets(self):
        if self.player.money <= 0:
            self.player.allIn = True
        while self.consecNonBets < len(self.playersLeft):
            if type(self.playersLeft[self.cPindex%(len(self.playersLeft))]) != ComputerPlayer:
                if self.player.money > 0:
                    self.player.allIn = False
                if self.player.allIn:
                    self.messageBox.q.append(f"{self.player.name} is all in!")
                    self.cPindex += 1
                    self.cPindex %= len(self.playersLeft)
                    self.consecNonBets += 1
                    continue
                elif self.player.currentBet == self.currentBet:
                    if self.player.allIn != True:
                        self.transCheck,self.transBet = False,False
                        self.transCall,self.transFold,self.transRaise = True,True,True
                        self.checkButton.image, self.betButton.image = self.checkButton.image1, self.betButton.image1
                        self.callButton.image, self.foldButton.image,self.raiseButton.image = self.callButton.Timage,self.foldButton.Timage,self.raiseButton.Timage
                        self.app.gameMode.messageBox.q.append("It is your turn. " +
                            f"The current bet on the table is ${self.app.gameMode.currentBet}. Would you like to check or bet?")
                else:
                    if self.player.currentBet > 0:
                        if self.player.allIn != True:
                            self.transCall,self.transFold,self.transRaise = False,False,False
                            self.transCheck,self.transBet = True,True           
                            self.checkButton.image, self.betButton.image = self.checkButton.Timage, self.betButton.Timage
                            self.callButton.image, self.foldButton.image, self.raiseButton.image = self.callButton.image1,self.foldButton.image, self.raiseButton.image1
                            self.app.gameMode.messageBox.q.append(f"It is your turn. Your bet of ${self.player.currentBet} has been " +
                                f"raised by ${self.currentBet-self.player.currentBet}. Would you like to call, raise, or fold?")
                    else:
                        if self.player.allIn != True:
                            self.transCall,self.transFold,self.transRaise = False,False,False
                            self.transCheck,self.transBet = True,True          
                            self.checkButton.image, self.betButton.image = self.checkButton.Timage, self.betButton.Timage
                            self.callButton.image, self.foldButton.image, self.raiseButton.image = self.callButton.image1,self.foldButton.image1, self.raiseButton.image1
                            self.app.gameMode.messageBox.q.append("It is your turn. " +
                                f"The current bet on the table is ${self.app.gameMode.currentBet}. Would you like to call, fold, or raise?")
                return
            self.playersLeft[self.cPindex%(len(self.playersLeft))].doTurn()
        totalMoney = self.pot
        for player in self.totalPlayers:
            totalMoney += player.money
        self.doNextRound()
    
    def doNextRound(self):
        if self.r1:
            self.r1 = False
            self.r2 = True
            self.doRound2()
        elif self.r2:
            self.r2 = False
            self.r3 = True
            self.doRound3()
        elif self.r3:
            self.r3 = False
            self.r4 = True
            self.doRound4()
        elif self.r4:
            self.r4 = False
            self.winners = True
            self.doWinners()
        elif self.winners:
            self.winners = False
            self.showCards = True

    def setUpPlayerTurn(self):
        print("Your Turn!")
        if self.player.currentBet == self.currentBet:
            if self.player.allIn != True:
                self.transCheck,self.transBet = False,False
                self.transCall,self.transFold,self.transRaise = True,True,True
                self.checkButton.image, self.betButton.image = self.checkButton.image1, self.betButton.image1
                self.callButton.image, self.foldButton.image,self.raiseButton.image = self.callButton.Timage,self.foldButton.Timage,self.raiseButton.Timage
                self.app.gameMode.messageBox.q.append("It is your turn. " +
                    f"The current bet on the table is ${self.app.gameMode.currentBet}. Would you like to check or bet?")
        else:
            if self.player.allIn != True:
                self.transCall,self.transFold,self.transRaise = False,False,False
                self.transCheck,self.transBet = True,True          
                self.checkButton.image, self.betButton.image = self.checkButton.Timage, self.betButton.Timage
                self.callButton.image, self.foldButton.image, self.raiseButton.image = self.callButton.image1,self.foldButton.image, self.raiseButton.image1
                self.app.gameMode.messageBox.q.append("It is your turn. " +
                    f"The current bet on the table is ${self.app.gameMode.currentBet}. Would you like to call, fold, or raise?")


    def doRound1(self):
        self.tableCardsStrength = 0
        self.compPlayerCards = [ ]
        self.noFirstRoundBets = True
        self.raisesAlready = 0
        self.player.isFolded = False
        self.bettingRound = 1
        self.hand = [ ]
        self.pot = 0
        self.ante = 15
        self.currentBet = 2*self.ante
        self.r1 = True      # for updates to the mb
        self.messageBox.q.append("ROUND 1")
        self.initCards()
        for player in self.playersLeft:
            player.allIn = False
        for player in self.playersLeft:
            player.currentBet = 0
        for player in self.playersLeft:
            if type(player)!= ComputerPlayer:
                continue
            else:
                player.currentRoundBet = 0
        ante = 15
        self.totalPlayers[self.bBindex%len(self.totalPlayers)].money -= 2*ante
        self.totalPlayers[self.bBindex%len(self.totalPlayers)].currentBet += 2*ante
        self.totalPlayers[self.sBindex%len(self.totalPlayers)].money -= ante
        self.totalPlayers[self.sBindex%len(self.totalPlayers)].currentBet += ante
        self.pot += 3*ante
        self.consecNonBets = 0
        self.cPindex = 0
        for player in self.playersLeft[self.cPindex%(len(self.playersLeft)):]:
            if type(player) != ComputerPlayer:
                break
            player.doTurn()
        if self.player.isFolded or self.player.allIn:
            print("isFolded or allIn")
            self.doBets()
            return
        elif len(self.playersLeft) == 1:
            print("only one player left")
            self.winners = True
            self.r1 = False
            self.doWinners()
            return
        self.setUpPlayerTurn()


 
    def doRound2(self):
        self.raisesAlready = 0
        self.consecNonBets = 0
        self.currentBet = 0
        self.cPindex = 0
        self.bettingRound = 2
        for player in self.playersLeft:
            player.currentBet = 0
        self.r2 = True
        self.messageBox.q.append("ROUND 2")
        w,h = self.app.width,self.app.height
        for card in range(3):   # generate 3 table cards
            newCard = self.deck.dealCard()
            newCard.x,newCard.y = (self.tcsL[0]*w)+card*self.dBSils,self.tcsL[1]*h
            self.hand.append(newCard)
            for player in self.playersLeft:
                player.hand.append(newCard)
        for player in self.playersLeft:
            player.pointValuation = CF.pointValuation(player.hand)
            player.fiveCardHand = CF.getFiveCardHand(player.hand,player.pointValuation)
            player.totalPointValuation = CF.tieBreaker(player.fiveCardHand,player.pointValuation)
        self.tableCardsStrength = MC.strength(self.hand)
        for player in self.playersLeft[self.cPindex%(len(self.playersLeft)):]:
            if type(player) != ComputerPlayer:
                break
            player.doTurn()
        if self.player.isFolded or self.player.allIn:
            print("isFolded or allIn")
            self.doBets()
            return
        elif len(self.playersLeft) == 1:
            print("only one player left")
            self.winners = True
            self.r2 = False
            self.doWinners()
            return
        self.setUpPlayerTurn()


 
    def doRound3(self):
        self.raisesAlready = 0
        self.consecNonBets = 0
        self.currentBet = 0
        self.cPindex = 0
        self.bettingRound = 3
        for player in self.playersLeft:
            player.currentBet = 0
        self.r3 = True
        self.messageBox.q.append("ROUND 3")
        w,h = self.app.width,self.app.height
        for card in range(3,4):   # generate 1 table card
            newCard = self.deck.dealCard()
            newCard.x,newCard.y = (self.tcsL[0]*w)+card*self.dBSils,self.tcsL[1]*h
            self.hand.append(newCard)
            for player in self.playersLeft:
                player.hand.append(newCard)
        for player in self.playersLeft:
            player.pointValuation = CF.pointValuation(player.hand)
            player.fiveCardHand = CF.getFiveCardHand(player.hand,player.pointValuation)
            player.totalPointValuation = CF.tieBreaker(player.fiveCardHand,player.pointValuation)
        self.tableCardsStrength = MC.strength(self.hand)
 
        for player in self.playersLeft[self.cPindex%(len(self.playersLeft)):]:
            if type(player) != ComputerPlayer:
                break
            print()
            player.doTurn()
        if self.player.isFolded or self.player.allIn:
            print("isFolded or allIn")
            self.doBets()
            return
        elif len(self.playersLeft) == 1:
            print("only one player left")
            self.winners = True
            self.r3 = False
            self.doWinners()
            return
        self.setUpPlayerTurn()
     
 
    def doRound4(self):
        self.raisesAlready = 0
        self.consecNonBets = 0
        self.currentBet = 0
        self.cPindex = 0
        self.bettingRound = 4
        for player in self.playersLeft:
            player.currentBet = 0
        self.r4 = True
        self.messageBox.q.append("ROUND 4")
        w,h = self.app.width,self.app.height
        for card in range(4,5):   # generate 1 table card
            newCard = self.deck.dealCard()
            newCard.x,newCard.y = (self.tcsL[0]*w)+card*self.dBSils,self.tcsL[1]*h
            self.hand.append(newCard)
            for player in self.playersLeft:
                player.hand.append(newCard)
        for player in self.playersLeft:
            player.pointValuation = CF.pointValuation(player.hand)
            player.fiveCardHand = CF.getFiveCardHand(player.hand,player.pointValuation)
            player.totalPointValuation = CF.tieBreaker(player.fiveCardHand,player.pointValuation)
        self.tableCardsStrength = MC.strength(self.hand)        
        for player in self.playersLeft[self.cPindex%(len(self.playersLeft)):]:
            if type(player) != ComputerPlayer:
                break
            player.doTurn()
        if self.player.isFolded:
            self.doBets()
            return
        elif len(self.playersLeft) == 1:
            print("only one player left")
            self.winners = True
            self.r4 = False
            self.doWinners()
            return
            if self.gameOver:
                return
        self.setUpPlayerTurn()
        if self.player.isFolded or self.player.allIn: 
            self.doBets()
            return
 
    def doWinners(self):
        self.winners = True
        winner = self.checkWinner()
        winner.money += self.pot
        self.messageBox.q.append(f"The winner of Game {self.round} is {winner}.")
        if len(self.totalPlayers) == 1 and type(self.totalPlayers[0] != ComputerPlayer):
            self.messageBox.q.append(f"{self.player.name} is the Winner!")
            self.gameOver = True
            return
        for player in self.playersLeft:
            if player.money <= 0:
                self.totalPlayers.remove(player)
                player.isBankrupt = True
                self.messageBox.q.append(f"player {player} is bankrupt!")
                if type(player) != ComputerPlayer:
                    self.messageBox.q.append("Game Over!")
                    self.gameOver = True
                    return
        for player in self.totalPlayers:
            self.allIn = False
        self.round += 1
        self.resetBlinds()
        self.messageBox.q.append("Click anywhere on the screen to continue to a new round.")
        self.messageBox.q.append("")
        self.doNextRound()
        return
 
    def initCards(self):
        self.cards = [ ]
        bBindex = self.bBindex
        firstIndex = (self.sBindex+1)%len(self.totalPlayers)
        self.orderedPlayers = self.totalPlayers[firstIndex:] + self.totalPlayers[:firstIndex]
        self.playersLeft = self.orderedPlayers[:]
        self.colorIndex += 1
        self.deckX,self.deckY = 8*self.app.width/9,self.tcsL[1]*self.h
        self.deck = VDeck(self.app,self.deckX,self.deckY,self.deckColors[self.colorIndex%2])
        self.player.hand = [ ]
        w,h = self.app.width,self.app.height
        for compPlayer in self.compPlayers:
            if compPlayer.isBankrupt:
                continue
            newCard = self.deck.dealCard()
            newCard.cardImage = self.app.scaleImage(newCard.cardImage,GameMode.scale)
            compPlayer.c1 = newCard     # card 1
            dUp = -self.app.height/30
            newCard.x,newCard.y = compPlayer.x-compPlayer.dBetweenCards,compPlayer.y+self.app.height/50+dUp
            self.cards.append(newCard)
            self.compPlayerCards.append(newCard)
            newCard = self.deck.dealCard()
            newCard.cardImage = self.app.scaleImage(newCard.cardImage,GameMode.scale)
            newCard.x,newCard.y = compPlayer.x+compPlayer.dBetweenCards,compPlayer.y+dUp
            compPlayer.c2 = newCard
            self.cards.append(newCard)
            compPlayer.hand = [compPlayer.c1,compPlayer.c2]
 
        newCard = self.deck.dealCard()      # set up your cards
        newCard.x,newCard.y = (self.cs1L[0]*w) + 0*self.dBSils,self.cs1L[1]*h
        self.playerCards = [ ]
        self.playerCards.append(newCard)
        self.player.hand.append(newCard)
        self.player.c1 = newCard
        newCard = self.deck.dealCard()      # your second card
        newCard.x,newCard.y = (self.cs1L[0]*w) + 1*self.dBSils,self.cs1L[1]*h
        self.playerCards.append(newCard)
        self.player.hand.append(newCard)
        self.player.c2 = newCard
        
        self.player.pointValuation = CF.pointValuation(self.player.hand)
        self.player.fiveCardHand = CF.getFiveCardHand(self.player.hand,self.player.pointValuation)
        self.player.totalPointValuation = CF.tieBreaker(self.player.fiveCardHand,self.player.pointValuation)
    
    def resetBlinds(self):
        self.bBindex += 1
        self.bBindex = self.bBindex%(self.playersCount+1)      # big blind index
        self.sBindex = (self.bBindex+1)%(self.playersCount+1)       # small blind index
 
    def checkWinner(self):
        bestPV = 0       # best point value
        bestPlayer = None
        for player in self.playersLeft:
            if player.totalPointValuation > bestPV:
                bestPV = player.totalPointValuation
                bestPlayer = player
        return bestPlayer
        
 
    def setUpCardSilhouettes(self):
        width,height = self.app.width,self.app.height
        self.dBSils = width/7          # distance between sils
        self.cs1L = 3/4,7/8     #cs1 location  
        self.cs1 = CardSilhouette(self.app,self.cs1L[0]*width,self.cs1L[1]*height)                # card silhouette 1  
        self.cs2 = CardSilhouette(self.app,(self.cs1L[0]*width)+self.dBSils,self.cs1L[1]*height) 
        self.sils.append(self.cs1) 
        self.sils.append(self.cs2) 
        self.tcsL = 1/6,3/5            # location of first of the five table card silhouettes at the center of the screen
        self.cs3 = CardSilhouette(self.app,self.tcsL[0]*width,self.tcsL[1]*height)
        self.cs4 = CardSilhouette(self.app,(self.tcsL[0]*width)+self.dBSils,self.tcsL[1]*height)  
        self.cs5 = CardSilhouette(self.app,(self.tcsL[0]*width)+2*self.dBSils,self.tcsL[1]*height)  
        self.cs6 = CardSilhouette(self.app,(self.tcsL[0]*width)+3*self.dBSils,self.tcsL[1]*height)  
        self.cs7 = CardSilhouette(self.app,(self.tcsL[0]*width)+4*self.dBSils,self.tcsL[1]*height)  
        self.sils.append(self.cs3) 
        self.sils.append(self.cs4) 
        self.sils.append(self.cs5) 
        self.sils.append(self.cs6) 
        self.sils.append(self.cs7) 
          
 
    def fixLocationOfSils(self,w,h):
        self.cs1.x,self.cs1.y = self.cs1L[0]*w,self.cs1L[1]*h
        self.cs2.x,self.cs2.y = (self.cs1L[0]*w)+self.dBSils,self.cs1L[1]*h
 
 
    def sizeChanged(self):
        w,h = self.width,self.height    # size changed to w,h
        self.fixLocationOfSils(w,h)
        self.w,self.h = w,h
 
 
    def keyPressed(self,event):
        if event.key == "a":
            newProbMode = ProbMode(self.app,self.player.hand)
            self.app.setActiveMode(newProbMode)

 
 
    def redrawAll(self,canvas):
        width,height = self.app.width,self.app.height
        canvas.create_image(width/2, height/2, image=ImageTk.PhotoImage(self.greenBackground))
        self.chipW,self.chipH = width/10,91*height/100
        canvas.create_image(self.chipW,self.chipH,image=ImageTk.PhotoImage(self.pokerChip))
        canvas.create_image(self.cardsIcon.x,self.cardsIcon.y,image=ImageTk.PhotoImage(self.cardsIcon.image))
        canvas.create_image(self.probIcon.x,self.probIcon.y,image=ImageTk.PhotoImage(self.probIcon.image))
        self.printSilhouettes(canvas)
        self.printGameInfo(canvas)
        self.drawMessageBox(canvas)
        self.printGameDeck(canvas)
        self.drawCards(canvas)
        self.printCompMoneyAndHand(canvas)
        if self.doneWithSetUp == False:
            return
        self.drawBlinds(canvas)
        self.drawButtons(canvas)
 
 
    def drawButtons(self,canvas):
        for button in self.buttons:
            canvas.create_image(button.x,button.y,image=ImageTk.PhotoImage(button.image))
            canvas.create_text(button.x,button.y,text=button.text,font=button.font)

    
    def drawBlinds(self,canvas):
        if self.gameOver:
            return
        if self.bBindex == 0:
            canvas.create_image(13*self.app.width/16,29*self.app.height/40,image=ImageTk.PhotoImage(self.bBimage))    # you are the big blind
            sB = self.totalPlayers[self.sBindex%len(self.totalPlayers)]    
            canvas.create_image(sB.x,sB.y+60,image=ImageTk.PhotoImage(self.sBimage))
            return
        elif self.sBindex == 0:
            canvas.create_image(13*self.app.width/16,29*self.app.height/40,image=ImageTk.PhotoImage(self.sBimage))    # you are the small blind
            bB = self.totalPlayers[self.bBindex%len(self.totalPlayers)]
            if type(bB) != ComputerPlayer:
                if len(self.totalPlayers) == 1:
                    pass
                else:
                    bB = self.totalPlayers[(self.bBindex+1)%len(self.totalPlayers)]
            if len(self.totalPlayers) == 1:
                self.gameOver = True
                self.messageBox.q.append("You Won! Congratulations!!!")
                return
            canvas.create_image(bB.x,bB.y+60,image=ImageTk.PhotoImage(self.bBimage))
            return
        if type(self.totalPlayers[self.bBindex%len(self.totalPlayers)]) == ComputerPlayer:
            bB = self.totalPlayers[self.bBindex%len(self.totalPlayers)]
        else:
            bB = self.totalPlayers[(self.bBindex+1)%len(self.totalPlayers)]
        if type(self.totalPlayers[self.sBindex%len(self.totalPlayers)]) == ComputerPlayer:
            sB = self.totalPlayers[self.sBindex%len(self.totalPlayers)]
        else:
            sB = self.totalPlayers[(self.sBindex+1)%len(self.totalPlayers)]
        if type(sB) != ComputerPlayer:
            if len(self.totalPlayers) == 1:     # you are the only player left
                pass
            else:
                sB = self.totalPlayers[(self.sBindex+1)%len(self.totalPlayers)]
        if len(self.totalPlayers) == 1:
                self.gameOver = True
                self.messageBox.q.append("You Won! Congratulations!!!")
                return
        canvas.create_image(bB.x,bB.y+60,image=ImageTk.PhotoImage(self.bBimage))
        canvas.create_image(sB.x,sB.y+60,image=ImageTk.PhotoImage(self.sBimage))
 
 
 
    def drawMessageBox(self,canvas):
        mb = self.messageBox
        canvas.create_rectangle(mb.cx-mb.wr,mb.cy-mb.hr,mb.cx+mb.wr,mb.cy+mb.hr,fill=mb.color)
        i = self.app.height/75    # 75    
        for message in mb.q[len(mb.q)-8:len(mb.q)]:     # last 8 messages of mb queue
            canvas.create_text(mb.cx,mb.cy-mb.hr+i,text=message,font="Helvetica 16")
            i += mb.dBetween
 
    def drawCards(self,canvas):
        for card in self.hand:
            canvas.create_image(card.x, card.y, image=ImageTk.PhotoImage(card.cardImage))
        for card in self.playerCards:
            canvas.create_image(card.x, card.y, image=ImageTk.PhotoImage(card.cardImage))
        for card in self.cards:
            if self.colorIndex%2 == 0:
                card.image = card.rbackImage
            elif self.colorIndex%2 == 1:
                card.image = card.bbackImage
            if self.showCards:
                card.image  = card.cardImage
            canvas.create_image(card.x, card.y, image=ImageTk.PhotoImage(card.image))
            
            
    def printGameDeck(self,canvas):
        canvas.create_image(self.deck.x, self.deck.y, image=ImageTk.PhotoImage(self.deck.image))
 
    def printGameInfo(self,canvas):
        a = "w"         #anchor
        x,y = self.chipW-self.app.width/35,self.chipH-self.app.height/70
        canvas.create_text(x,y,text=f"${self.player.money}",anchor=a,font="Helvetica 18 bold")
        x = self.app.width/30
        y = 14*self.app.height/20
        canvas.create_text(x,y,text=f"current bet: {self.currentBet}",anchor=a)
        y = 15*self.app.height/20
        canvas.create_text(x,y,text=f"pot: {self.pot}",anchor=a)
        y = 16*self.app.height/20
        canvas.create_text(x,y,text=f"your hand: {CF.getHandName(self.player.pointValuation)}",anchor=a)
 
        
    
    def printSilhouettes(self,canvas):
        for sil in self.sils:
            canvas.create_image(sil.x, sil.y, image=ImageTk.PhotoImage(sil.image))
 
    def printCompMoneyAndHand(self,canvas):
        for cPlayer in self.compPlayers:
            x = cPlayer.x
            dy = self.app.height/15
            y = cPlayer.y-(self.cardHeight/2)
            playerNum = cPlayer.playerNum
            canvas.create_text(x,y-dy,text=f"P {playerNum}'s money: ${cPlayer.money}")
            cPlayer.pointValuation = CF.pointValuation(cPlayer.hand)
            cPlayer.fiveCardHand = CF.getFiveCardHand(cPlayer.hand,cPlayer.pointValuation)
            cPlayer.totalPointValuation = CF.tieBreaker(cPlayer.fiveCardHand,cPlayer.pointValuation)
            # canvas.create_text(x-self.app.width/60,y-2*dy,text=f"P {playerNum}'s cards: {CF.getFiveCardHand(cPlayer.hand,cPlayer.pointValuation)}")
            if self.showCards and cPlayer in self.playersLeft:
                canvas.create_text(x-self.app.width/60,y-(11*dy/8),text=f"P {playerNum}'s hand: {CF.getHandName(cPlayer.pointValuation)}")
            # canvas.create_text(x-self.app.width/60,y-4*dy,text=f"P {playerNum}'s strength: {cPlayer.handStrength}")


 
    def mouseMoved(self,event):
        x1,y1,x2,y2 = self.cardsIcon.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            self.cardsIcon.image = self.cardsIcon.image2
        else:
            self.cardsIcon.image = self.cardsIcon.image1
        x1,y1,x2,y2 = self.probIcon.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            self.probIcon.image = self.probIcon.image2
        else:
            self.probIcon.image = self.probIcon.image1

        if self.transCall == True:
            pass
        else:
            x1,y1,x2,y2 = self.callButton.location
            if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
                self.callButton.image = self.callButton.image2
            else:
                self.callButton.image = self.callButton.image1   
        if self.transFold == True:
            pass
        else:
            x1,y1,x2,y2 = self.foldButton.location
            if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
                self.foldButton.image = self.foldButton.image2
            else:
                self.foldButton.image = self.foldButton.image1   
        if self.transRaise == True:
            pass
        else:
            x1,y1,x2,y2 = self.raiseButton.location
            if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
                self.raiseButton.image = self.raiseButton.image2
            else:
                self.raiseButton.image = self.raiseButton.image1   
        if self.transCheck == True:
            pass
        else:
            x1,y1,x2,y2 = self.checkButton.location
            if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
                self.checkButton.image = self.checkButton.image2
            else:
                self.checkButton.image = self.checkButton.image1   
        if self.transBet == True:
            pass
        else:
            x1,y1,x2,y2 = self.betButton.location
            if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
                self.betButton.image = self.betButton.image2
            else:
                self.betButton.image = self.betButton.image1   
 
    def mousePressed(self,event):
        x1,y1,x2,y2 = self.cardsIcon.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            newHandGuide = HandGuide(self.app,self.player.hand)
            self.app.setActiveMode(newHandGuide)
        x1,y1,x2,y2 = self.probIcon.location
        if event.x < x2 and event.x > x1 and event.y < y2 and event.y > y1:
            newProbMode = ProbMode(self.app,self.player.hand)
            self.app.setActiveMode(newProbMode)


        if self.showCards:
            self.showCards = False
            self.r1 = True
            self.doRound1()
        if self.player.currentBet == self.currentBet:
            x1,y1,x2,y2 = self.betButton.location
            if event.x <= x2 and event.x >= x1 and event.y <= y2 and event.y >= y1:
                self.player.bet()
        if self.player.currentBet == self.currentBet: 
            x1,y1,x2,y2 = self.checkButton.location  
            if event.x <= x2 and event.x >= x1 and event.y <= y2 and event.y >= y1:
                self.player.check()
        else:
            pass        
        if self.currentBet > 0:
            x1,y1,x2,y2 = self.callButton.location 
            if event.x <= x2 and event.x >= x1 and event.y <= y2 and event.y >= y1:
                self.player.call()
        if self.currentBet > 0:
            x1,y1,x2,y2 = self.foldButton.location
            if event.x <= x2 and event.x >= x1 and event.y <= y2 and event.y >= y1:
                self.player.fold()
        if self.currentBet > 0:
            x1,y1,x2,y2 = self.raiseButton.location
            if event.x <= x2 and event.x >= x1 and event.y <= y2 and event.y >= y1:
                self.player.raiseBet()
 

class ProbMode(Mode):
    def __init__(self,app,hand,**kwargs):
        self.app = app
        self.hand = hand
        self.greenBackground = self.loadImage("GreenBackground.png")
        self.background = self.loadImage("PatternedGrayBackground4.png")
        self.background = self.scaleImage(self.background, 3)
        self.handList = MC.convert(hand)
        self.d = MC.prob(self.handList,8000,True)      # change variable for speed
        super().__init__(**kwargs)


    def redrawAll(self,canvas):
        canvas.create_image(self.app.width/2,self.app.height/2, image=ImageTk.PhotoImage(self.background))
        canvas.create_text(self.app.width/2,self.app.height/15,text="Probabilities:",font="Helvetica 50 bold")
        canvas.create_text(self.app.width/2,self.app.height/7,text=f"hand: {self.hand}",font="Helvetica 20 bold")
        x1 = 3*self.app.width/20
        x2 = 13*self.app.width/20
        y = self.app.height/4
        dy = self.app.height/5      # distance between
        a = "w"     # anchor
        f = "helvetica 20 bold"         # font
        d = self.d      # dictionary
        r = 4       # rounding
        probOfOnePair = d["onePair"]
        probOfTwoPair = d["twoPair"]
        probOfThreeOfKind = d["threeOfKind"]
        probOfStraight = d["straight"]
        probOfFlush = d["flush"]
        probOfFullHouse = d["fullHouse"]
        probOfFourOfKind = d["fourOfKind"]
        probOfStraightFlush = d["straightFlush"]
        canvas.create_text(x1,y+(0*dy),text=f"One Pair: {probOfOnePair}",anchor=a,font=f)
        canvas.create_text(x1,y+(1*dy),text=f"Two Pair: {probOfTwoPair}",anchor=a,font=f)
        canvas.create_text(x1,y+(2*dy),text=f"Three of a Kind: {probOfThreeOfKind}",anchor=a,font=f)
        canvas.create_text(x1,y+(3*dy),text=f"Straight: {probOfStraight}",anchor=a,font=f)
        canvas.create_text(x2,y+(0*dy),text=f"Flush: {probOfFlush}",anchor=a,font=f)
        canvas.create_text(x2,y+(1*dy),text=f"Full House: {probOfFullHouse}",anchor=a,font=f)
        canvas.create_text(x2,y+(2*dy),text=f"Four of a Kind: {probOfFourOfKind}",anchor=a,font=f)
        canvas.create_text(x2,y+(3*dy),text=f"Straight Flush: {probOfStraightFlush}",anchor=a,font=f)
        canvas.create_text(self.app.width/2,19*self.app.height/20,text="(click anywhere to continue)")
 
    def mousePressed(self,event):
        self.app.setActiveMode(self.app.gameMode)

class HandGuide(Mode):
    def __init__(self,app,hand,**kwargs):
        self.app = app
        self.hand = hand
        self.handList = MC.convert(hand)
        super().__init__(**kwargs)

    def appStarted(self):
        self.image = self.app.loadImage("HandGuide.png")
        x1,y1 = 0,170
        x2,y2 = 550,770
        self.image = self.image.crop((x1,y1,x2,y2))
        self.image = self.app.scaleImage(self.image,19/20)


    def redrawAll(self,canvas):
        canvas.create_text(self.app.width/2,self.app.height/15,text="Hand Guide:",font="Helvetica 50 bold")
        canvas.create_text(self.app.width/2,self.app.height/7,text=f"hand: {self.hand}",font="Helvetica 20 bold")
        canvas.create_image(self.app.width/2,11*self.app.height/20,image=ImageTk.PhotoImage(self.image))
        canvas.create_text(self.app.width/2,19*self.app.height/20,text="(click anywhere to continue)")
 
    def mousePressed(self,event):
        self.app.setActiveMode(self.app.gameMode)
 
 
# from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.titleScreenMode = TitleScreenMode()
        app.instructionsMode = InstructionsMode()
        app.gameMode = GameMode()
        app.setActiveMode(app.titleScreenMode)
 
 
app = MyModalApp(width=1100, height=850)     # size of window can be changed here
 
 
# Citations:
 
 
# front of cards: http://www.davesilvermanart.com/
# back of cards: https://kibernetik.pro/forum/viewtopic.php?t=2064
# blinds: https://www.ebay.com/itm/Big-Little-Blind-and-Dealer-Button-Poker-Game-Chips-Texas-Holdem-Prop-/273406760699
# poker chip: http://www.dice702.com/dicepokerchips.htm
# poker cards icon: https://texaspokersupply.com/store/marion-pro-poker-cards/
# poker hand guide: https://medium.com/@bitstars.io/poker-hand-rankings-3d39129f2c01
# Microsoft PowerPoint used for simple images, edits, and backgrounds
# dice icon: https://icon-library.net/icon/probability-icon-6.html
# title screen background: https://www.vectorstock.com/royalty-free-vector/luxury-casino-gambling-poker-background-with-card-vector-8412200
 
 