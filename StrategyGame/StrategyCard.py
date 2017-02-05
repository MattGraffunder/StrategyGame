import random

WILD = "Wild"

#Done
class StrategyCard(object):
    def __init__(self, countryId, countryName, cardType, stars):
        self.countryId = countryId
        self.countryName = countryName #Implement Country
        self.cardType = cardType #Types: Soldier, Horse, Cannon
        self.stars = stars #For New Risk Card Types

    def GetCountryId(self):
        return self.countryId

    def GetCountryName(self):
        return self.countryName

    def GetCardType(self):
        return self.cardType

    def GetStars(self):
        return self.stars

    def __str__(self):
        return "Country: " + self.countryName + ", Type: " + self.cardType + ", Stars: " + str(self.stars)

#Done
class StrategyCardDeck(object):
    def __init__(self):
        self.cards = []
        self.discards = []

    def BuildDeck(self, countries, numWilds):
        """
        Builds the risk deck based on the countries and the number of Wilds needed.
        """
        self.cards = []
        
        for country in countries:
            self.cards.append(StrategyCard(country.getId(), country.getName(), country.getCardType(), country.getCardStars()))

        for wild in xrange(numWilds):
            self.cards.append(StrategyCard("","", "WILD", 0))

        #Shuffle the Deck
        self.ShuffleArray(self.cards)

    def DrawCard(self):
        """
        Removes a Risk card from the deck, and returns it.
        """
        #If deck is empty shuffle discards
        if len(self.cards) == 0:
            self.cards = self.discards
            self.discards = []
            self.ShuffleArray(self.cards)
        
        return self.cards.pop(0)

    def ReturnCard(self, card):
        """
        This adds a risk card back to the discard array.  
        These cards are shuffled back when the draw deck is empty
        """
        self.discards.append(card)

    #Helper Methods
    def ShuffleArray(self, array):
        """
        Shuffles the array by reference using the Fisher-Yates algorithm
        """

        #This could be broken out into its own module, class, etc...

        #From arrayLength -1, to -1, steping by -1 each time
        for i in xrange(len(array) - 1, -1, -1):
            n = random.randint(0, i) #RandInt is inclusive

            tempVar = array[i]
            array[i] = array[n]
            array[n] = tempVar
            
def IsHandValid(cards):
    cardTypes = {}
    for card in cards:
        if card.GetCardType() in cardTypes:
            cardTypes[card.GetCardType()] += 1
        else:
            cardTypes[card.GetCardType()] = 1
               
    #Cards must meet one of two criteria:
    cardType = cardTypes.keys()[0]
    # 1) All Cards must be the same or wild
    if cardTypes[cardType] == 3:
        return True
    # 2) Two cards of the same type, and one wild
    elif WILD in cardTypes and cardTypes[cardType] == 2 and cardTypes[WILD] == 1:
        return True
    # 3) Any one card, and two wilds
    elif WILD in cardTypes and cardTypes[cardType] == 1 and cardTypes[WILD] == 2:
        return True
    # 4) Three cards of different types (Three regular types, or two different types and one wild)
    elif len(cardTypes) == 3:
        return True
    else:
        return False
