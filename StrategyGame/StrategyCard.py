import random

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
        return self.cards.pop(0)

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
