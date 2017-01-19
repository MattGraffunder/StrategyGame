#Done
class GameMap(object):
    def __init__(self, countries, continents, links):
        self.countries = countries
        self.continents = continents
        self.countryLookup = {}
        self.neighbors = {}

        for country in self.countries:
            self.countryLookup[country.getId()] = country
            self.neighbors[country.getId()] = []
            
            for continent in self.continents:
                if country.getContinentId() == continent.getId():
                    continent.addCountry(country)

        #Build Links
        for link in links:
            self.neighbors[link[0]].append(self.countryLookup[link[1]])
            self.neighbors[link[1]].append(self.countryLookup[link[0]])

        return

    #Probably need somthing to help choose countries in the game setup

    def getAllCountries(self):
        return self.countries

    def getAllContinents(self):
        return self.continents
    
    def getPlayerCountries(self, playerId):
        playerCountries = []
        
        for country in self.countries:
            if country.getOwnerId() == playerId:
                playerCountries.append(country)

        return playerCountries

    def getCountry(self, countryId):
        return self.countryLookup[countryId]

    def getNeighbors(self, countryId):
        return self.neighbors[country.getId()]

#TODO - Add Countries
class StandardMap(GameMap):
    #Build the standard risk map
    
    def __init__(self):
        standardContinents = [
            Continent("NA","North America", 5, []),
            Continent("SA","South America", 2, []),
            Continent("EU","Europe", 5, []),
            Continent("AF","Africa", 3, []),
            Continent("AS","Asia", 7, []),
            Continent("AU","Austrailia", 2, [])]

        standardCountries = []
        standardLinks=[]        
        
        GameMap.__init__(self, standardCountries, standardContinents, standardLinks)

#Done
class SimpleMap(GameMap):
    #Build a simple risk map
    def __init__(self):
        #Link Countries to Continents better
        #Need to build Neighbors

        #Looks something like
        #
        #          [C4]
        #          /  \
        #       [C2]--[C3]
        #          \  /
        #          [C1]
        #          /  \
        #         /    \ 
        # [A3]-[A1] -- [B1]-[B2]
        #  |  /            \  |
        #  | /              \ |
        # [A2]              [B3]
        #
        
        simpleContinents = [
            Continent("A", "Continent A", 3, []),
            Continent("B", "Continent B", 3, []),
            Continent("C", "Continent C", 4, [])]

        simpleCountries = [
            Country("A1", "Alpha One", "A", "Horse", 0),
            Country("A2", "Alpha Two", "A", "Cannon", 0),
            Country("A3", "Alpha Three", "A", "Soldier", 0),
            Country("B1", "Bravo One", "B", "Horse", 0),
            Country("B2", "Bravo Two", "B", "Cannon", 0),
            Country("B3", "Bravo Three", "B", "Soldier", 0),
            Country("C1", "Charlie One", "C", "Horse", 0),
            Country("C2", "Charlie Two", "C", "Cannon", 0),
            Country("C3", "Charlie Three", "C", "Soldier", 0),
            Country("C4", "Charlie Four", "C", "Soldier", 0)
            ]

        #Probably will build a list of links and pass that into the constructor
        simpleLinks = [
            ("A1","A2"),
            ("A1","A3"),
            ("A1","B1"),
            ("A1","C1"),
            ("A3","A2"),
            ("B1","B2"),
            ("B1","B3"),
            ("B1","C1"),
            ("B2","B3"),
            ("C1","C2"),
            ("C1","C3"),
            ("C2","C3"),
            ("C2","C4"),
            ("C3","C4")]
        
        GameMap.__init__(self, simpleCountries, simpleContinents, simpleLinks)

#TODO - Implement Concrete Class
class RandomMap(GameMap):
    """
    Builds a random map
    """
    pass

#TODO - Implement Concrete Class
class UserMap(GameMap):
    """
    Builds a map based on user design (file, direct input, something...)
    """
    pass

#TODO - Implement Concrete Class
class ShiftingMap(GameMap):
    """
    A map that can change during the game.
    That sounds cool
    """
    pass

#Done
class Continent(object):
    #Think about removing add country
    #Should probably only exist as part of a subclass used by ShiftingMap

    #Figure out how to add countries better
    def __init__(self, continentId, name, value, countries):
        self.continentId = continentId
        self.name = name
        self.value = value
        self.countries = countries

    def getId(self):
        return self.continentId

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def addCountry(self, country):
        self.countries.append(country)

    def getCountries(self):
        return self.countries

    def isOwnedBy(self, playerId):
        """
        Returns True if continent is fully owned by the player
        """
        #Check each country        
        for country in self.countries:
            if country.getOwnerId() != playerId:
                return False

        return True

    def __str__(self):
        return self.name + ": " + str(len(self.countries)) + " countries"

    def getOwnerId(self):
        """
        Return Player Id that owns the continent
        Return NoneType if no single owner
        """

        #Set owner to owner of first country to start with
        ownerId = self.countries[0]

        for country in self.countries:
            if country.getOwnerId() != ownerId:
                return None

        return ownerId

#Done
class Country(object):
    def __init__(self, countryId, name, continentId, cardType, cardStars):
        """
        Creates a new Country.
        name: string of Country Name
        owner: string of Owner's Id
        continent: string continent of country belongs to
        """

        self.countryId = countryId
        self.name = name
        self.continentId = continentId
        self.ownerId = None
        self.numberOfArmies = 0
        
        #I added these to keep countries as the source of Truth
        #Someone needed to maintain the data, and it makes as much sense here as elsewhere
        self.cardType = cardType
        self.cardStars = cardStars
        
    def getId(self):
        return self.countryId

    def getName(self):
        return self.name

    def getContinentId(self):
        return self.continentId

    def getOwnerId(self):
        return self.ownerId

       
    def getCardType(self):
        return self.cardType

    def getCardStars(self):
        return self.cardStars
    
    def setOwner(self, newOwnerId):
        self.ownerId = newOwnerId

    def getNumberOfArmies(self):
        return self.NumberOfArmies

    def addArmies(self, armiesToAdd):
        if armiesToAdd < 0:
            raise InputError("Cannot add negative armies")

        self.numberOfArmies += armiesToAdd

    def removeArmies(self, armiesToRemove):
        if armiesToRemove < 0:
            raise InputError("Cannot remove negative armies")
        elif armiesToRemove > self.numberOfArmies:
            raise InputError("Cannot remove " + str(armiesToRemove) + " armies. There are only " + str(self.numberOfArmies) + " in " + self.Name)

        self.numberOfArmies -= armiesToRemove            

    def __str__(self):
        return self.name + ": Owned By Player" + str(self.ownerId) + ", " + str(self.numberOfArmies) + " armies."
