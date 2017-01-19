#Risk Game Simulation


import Map, Player, Command, StrategyCard
#import Tkinter
#Tkinter._test()

#TODO - GetAction
class CommandProcessor(object):
    """
    Interface for command processors

    Mostly a strategy pattern type class
    """

    #Need to figure out how to return values.
    #i.e. Successfull attack, and player need a risk card

    #maybe pass in a save helper?  Or keep that with the game?

    def __init__(self):
        self.commandValidatorFactory = Command.CommandValidatorFactory()        
        pass

    def Validate(self, command):
        #Returns true if command is valid
        validator = self.commandValidatorFactory.GetValidator(command)
        return validator.IsValid(command)

    def GetAction(self, command):
        #Returns a delegate for the game to use, based on the command

        #Maybe add the validation here, and only expose one method? 
        pass
    
#TODO - Implement Rest of Game
class Game(object):
    def __init__(self):
        self.gameMap = {}
        self.strategyCardDeck = [] 
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
        self.strategyCardDeck = StrategyCard.StrategyCardDeck()
        self.strategyCardDeck.BuildDeck(gameMap.getAllCountries(), numWilds)
        
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
        players = [Player.RandomAI(1, "RandomOne"), Player.RandomAI(2, "RandomTwo")]

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
