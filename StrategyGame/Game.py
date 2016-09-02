#Risk Game Simulation
import random

import Map, Player
#import Tkinter
#Tkinter._test()

#Constants
ATTACK = "ATTACK"
END = "END"
MOVE = "MOVE"
PLACE = "PLACE"
TRADE = "TRADE" 

#Done
class InputError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

#TODO - Think through Results
class Result(object):
    #Contains the results of the last command
    #Attack Success
    #Attack Fail
    #Gain Card
    #Territory Captured
    #Invalid
    #etc...
    pass

#TODO - ToString
class Command(object):
    def __init__(self, commandId, playerId, commandType, country1, country2, quantity, cards):
        self.commandId = commandId
        self.playerId = playerId
        self.commandType = commandType
        self.country1 = country1
        self.country2 = country2
        self.quantity = quantity
        self.cards = cards
    def GetId(self):
        return self.commandId
    def GetPlayerId(self):
        return self.playerId
    def GetCommandType(self):
        return self.commandType    
    def GetCountry1(self):
        return self.country1
    def GetCountry2(self):
        return self.country2
    def GetQuantity(self):
        return self.quantity
    def GetCards(self):
        return self.cards
    def __str__(self):
        return "Make Better Command String"

#Done
class CommandBuilder(object):    
    def __init__(self):
        self.commandId = 0
    def GetAttack(self, playerId, country1, country2, numberOfArmies):
        self.commandId += 1 # Id unique to player or game?  Does this belong here?
        return Command(self.commandId, playerId, ATTACK, country1, country2, numberOfArmies, None)
    def GetEnd(self, playerId):
        self.commandId += 1
        return Command(self.commandId, playerId, END, None, None, 0, None)
    def GetMove(self, playerId, country1, numberOfArmies):
        return Command(self.commandId, playerId, MOVE, country1, None, numberOfArmies, None)
        self.commandId += 1
    def GetPlace(self, playerId, country, numberOfArmies):
        return Command(self.commandId, playerId, PLACE, country1, None, numberOfArmies, None)
        self.commandId += 1
    def GetTrade(self, playerId, cards):
        self.commandId += 1
        return Command(self.commandId, playerId, TRADE, None, None, 0, Cards)

#TODO - GetAction
class CommandProcessor(object):
    """
    Interface for command processors

    Mostly a strategy pattern type class
    """

    #maybe pass in a save helper?  Or keep that with the game?

    def __init__(self):
        self.commandValidatorFactory = CommandValidatorFactory()        
        pass

    def Validate(self, command):
        #Returns true if command is valid
        validator = self.commandValidatorFactory.GetValidator(command)
        return validator.IsValid(command)

    def GetAction(self, command):
        #Returns a delegate for the game to use, based on the command

        #Maybe add the validation here, and only expose one method? 
        pass
    
    #Need to figure out how to return values.
    #i.e. Successfull attack, and player need a risk card

#Done
class CommandValidatorFactory(object):
    def __init__(self):
        pass
    def GetValidator(command):
        if command == None:
            return InvalidCommandValidator()
        elif command.GetCommandType() == ATTACK:
            return AttackCommandValidator()
        elif command.GetCommandType() == END:
            return EndCommandValidator()
        elif command.GetCommandType() == MOVE:
            return MoveCommandValidator()
        elif command.GetCommandType() == PLACE:
            return PlaceCommandValidator()
        elif command.GetCommandType() == TRADE:
            return TradeCommandValidator()
        else:
            return InvalidCommandValidator()

#Done
class CommandValidator(object):
    def __init__(self):
        pass
    def IsValid(self, command):
        #Maybe return a Validation result object that has the bool and a list of reasons?
        pass
#TODO - Implement Concrete Class
class AttackCommandValidator(CommandValidator):
    def __init__(self):
        self.simpleValidator = SimpleAttackValidator()
        self.complexValidator = ComplexAttackValidator()
        pass
    def IsValid(self, command):
        return (self.simpleValidator.IsValid(command) and self.complexValidator.IsValid(command))
        #Validate the Attack Command

        #Simple Validation
            #Id is > 0
            #PlayerId > 0
            #CommandType is "ATTACK"
            #Country1 is Populated
            #Country2 is Populated
            #NumberOfArmies is > 0
            #Cards is None

        #Complex Validation
            #PlayerId is Valid Player
            #Country1 is Valid Country
            #Country1 is Owned by Player
            #Country2 is Valid Country
            #Country1 is not Owned by Player
            #Country 1 and 2 are neighbors
            #NumberOfArmies is < Number of in Country1
            #Player has placed All Armies

        #These seem like individual rules?
        #Perhaps a Rule Class with individual validations?
        pass
class SimpleAttackValidator(CommandValidator):
    def __init__(command):
        pass
    def IsValid(self, command):
        #Simple Validation
            #Id is > 0
            #PlayerId > 0
            #CommandType is "ATTACK"
            #Country1 is Populated
            #Country2 is Populated
            #NumberOfArmies is > 0
            #Cards is None
        pass

class ComplexAttackValidator(CommandValidator):
    def __init__(self):
        pass
    def IsValid(self, command):
          #Complex Validation
            #PlayerId is Valid Player
            #Country1 is Valid Country
            #Country1 is Owned by Player
            #Country2 is Valid Country
            #Country1 is not Owned by Player
            #Country 1 and 2 are neighbors
            #NumberOfArmies is < Number of in Country1
            #Player has placed All Armies
         pass

#TODO - Implement Concrete Class
class EndCommandValidator(CommandValidator):
    def __init__(self):
        pass
    def IsValid(self, command):
        #Validate the End Command
        pass

#TODO - Implement Concrete Class
class MoveCommandValidator(CommandValidator):
    def __init__(self):
        pass
    def IsValid(self, command):
        #Validate the Move Command
        pass

#TODO - Implement Concrete Class
class PlaceCommandValidator(CommandValidator):
    def __init__(self):
        pass
    def IsValid(self, command):
        #Validate the Place Command
        #Need some way to validate begining of game places
        pass
#TODO - Implement Concrete Class    
class TradeCommandValidator(CommandValidator):
    def __init__(self):
        pass
    def IsValid(self, command):
        #Validate the Trade Command
        pass
#TODO - Implement Concrete Class
class InvalidCommandValidator(CommandValidator):
    def __init__(self):
        pass
    def IsValid(self, command):
        return False

#Done
class RiskCard(object):
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
class RiskCardDeck(object):
    def __init__(self):
        self.cards = []

    def BuildDeck(self, countries, numWilds):
        """
        Builds the risk deck based on the countries and the number of Wilds needed.
        """
        self.cards = []
        
        for country in countries:
            self.cards.append(RiskCard(country.getId(), country.getName(), country.getCardType(), country.getCardStars()))

        for wild in xrange(numWilds):
            self.cards.append(RiskCard("","", "WILD", 0))

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

#TODO - Implement Rest of Game
class Game(object):
    def __init__(self):
        self.gameMap = {}
        self.riskCardDeck = [] 
        self.players = [] # Build Player List
        self.commandProcessor = CommandProcessor()

    def StartGame(self, gameMap, players):        
        #Setup Game
        self.gameMap = gameMap
        self.players = players

        #Check number of player, must be between 2-6
        if len(players) < 2:
            raise InputError("Too Few Players")
        elif len(players) > 6:
            raise InputError("Too Many Players")

        #Build Risk Card Deck
        numWilds = 2 # Need to find a better place for this
        self.riskCardDeck = RiskCardDeck()
        self.riskCardDeck.BuildDeck(gameMap.getAllCountries(), numWilds)
        
        #Give starting Armies
        startingArmies = self.GetStartingNumberOfArmies(len(self.players))

        for player in self.players:
            player.AddArmies(startingArmies)

        #Divide up countries
            #While there are available countries
            #Have players choose next country
        while self.gameMap.getPlayerCountries(None) > 0:
            for player in self.players:
                choice = player.ChooseCountry(self.gameMap)
                #Do something with choice
                    #Probably Validate it
                    #Definitely Assign it to player
        pass

    def PlayRound(self):

        #Long run, if open more widely, will need to add move validation at the Game level.
        #Currently, the Player class could manipulate it's number of armies, risk cards, or even the map.
        
        #for each active player
        for player in self.players:
            if not self.IsActivePlayer(player):
                #Player is out of game, skip them
                continue
            
            #Determine new armies
                #Count Player's Countries and Integer Divide by three
                #Take the greater of three or countries divided by three
                #Add any Continent Bonus

            #Give Player Turn
                #Somehow communicate with the Player.
                #Options are expose Methods, create callback functions, or create message structure
            hasEnded = false
            while hasEnded == True:
                command = player.PlayTurn(None)
                if commandProcessor.IsValid(command):
                    action = commandProcessor.GetAction(command)
                    #Action needs to modify hasEnded somehow
                else:
                    break

            #Hand out one risk card if player conquers one or more territories

            #Perform any end of turn logic
        
        #Perform end of round logic
        
        pass

    def PlayGame(self):
        #Manages all phases of the game
        #probably need to figure out how to determine Players and the Map
        #Maybe input from the user?

        #Get Players
        players = [Player.RandomAI(), Player.RandomAI()]

        #Get Map
        gameMap = Map.SimpleMap()

        #Start Game
        self.StartGame(gameMap, players)

        #While there are 2 or more active players play rounds
        while len(self.GetActivePlayers()) > 1:
            self.PlayRound()

        #declare winner
        winner = self.GetActivePlayers()[0]
        print str(winner) + " wins!"

    def GetActivePlayers(self):
        #Get the players who are currently in the game
        #Used to determine if there is a winner
        #And who needs a turn
        activePlayers = []
        
        for player in self.players:
            if self.IsActivePlayer(player.GetId()):
                activePlayers.append(player)

        return activePlayers

    def IsActivePlayer(self, playerId):
        #Checks if a player is still active before their turn
        if self.map.getPlayerCountries(playerId) > 0:
            return True
        else:
            return False
    
    def DrawGame(self):
        #Used to Display the game
        pass

    def GetStartingNumberOfArmies(self, numPlayers):
        #Could be refactored to dictionary
        #Probably doesn't matter since it gets call once per game.
        if numPlayers == 2:
            return 50
        elif numPlayers == 3:
            return 35
        elif numPlayers == 4:
            return 30
        elif numPlayers == 5:
            return 25
        elif numPlayers == 6:
            return 20        

#Idea: Time Machine Game - Game(Players?) can go back in time and the game will reset.

#Maintains Game Variables

#Could keep list of actions taken by players
#This would allow a game to be reviewed or stepped through move-by-move
#Could also be used to rebuild state and test AI by changing variables
