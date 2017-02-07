#Risk Game Simulation


import Map, Player, Command, StrategyCard, Dice
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
        self.gameDice = Dice.GameDice()

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
        while len(self.gameMap.getPlayerCountries(None)) > 0 or self.GetTotalFreeArmies() > 0:
            for player in self.players:
                choiceId = player.ChooseCountry(self.gameMap)
                
                #Check if there weren't any more countries to choose
                if choiceId == None:
                    break
                
                chosenCountry = self.gameMap.getCountry(choiceId)
                #print chosenCountry
                #Check that country isn't already owned
                if chosenCountry.getOwnerId() == None:
                    chosenCountry.setOwner(player.GetId()) 
                    chosenCountry.addArmies(1)
                    player.RemoveArmies(1)
                elif chosenCountry.getOwnerId() == player.GetId():
                    chosenCountry.addArmies(1)
                    player.RemoveArmies(1)
        
    def PlayRound(self):

        #Long run, if open more widely, will need to add move validation at the Game level.
        #Currently, the Player class could manipulate it's number of armies, risk cards, or even the map.
        
        #for each active player
        for player in self.players:
            if not self.IsActivePlayer(player.GetId()):
                #Player is out of game, skip them
                print "Player: " + str(player.GetId())
                continue
            
            #Determine new armies
                #Count Player's Countries and Integer Divide by three
                #Take the greater of three or countries divided by three
                #Add any Continent Bonus
                
            totalNewArmies = 0
            conqueredTerritory = False
                                
            #Calculate countries
            playerCountries = self.gameMap.getPlayerCountries(player.GetId())
            totalNewArmies = max(len(playerCountries) / 3, 3) #Players get atleast three armies
            
            #Calculate continent bonus
            for continent in self.gameMap.getPlayerContinents(player.GetId()):
                totalNewArmies += continent.getValue()
            
            print player, " New Armies: " + str(totalNewArmies), " Total Armies: " + str(player.GetFreeArmies())
            
            #Give armies to player
            player.AddArmies(totalNewArmies)

            #Give Player Turn
                #Don't need to send anything to the player, player should just work off the new state
                
            player.SetHasMoved(False)
            
            while True:
                command = player.PlayTurn(self.gameMap)
                print command
                
                #Place Command
                if command.GetCommandType() == Command.PLACE:                    
                    placeCountry = self.gameMap.getCountry(command.GetCountry1())
                    placeCountry.addArmies(command.GetQuantity())
                    
                    player.RemoveArmies(command.GetQuantity())
                    
                #Attack Command                    
                elif command.GetCommandType() == Command.ATTACK:   
                    #Validate Command
                    if self.isAttackCommandValid(player, command):
                        attackerCountry = self.gameMap.getCountry(command.GetCountry1())
                        defenderCountry = self.gameMap.getCountry(command.GetCountry2())
                        
                        #Execute Command
                        attackers = command.GetQuantity
                        
                        #Get Roll Results
                        #Tuple (attacker wins, defender wins)
                        wins = self.gameDice.GetWinners(command.GetQuantity(), defenderCountry.getNumberOfArmies())
                                     
                        attackerWins = wins[0]
                        defenderWins = wins[1]
                                     
                        #Update number of Armies
                        attackerCountry.removeArmies(defenderWins)
                        defenderCountry.removeArmies(attackerWins)
                        
                        #Check if defender country changes hands
                        if defenderCountry.getNumberOfArmies() == 0:
                            #Assign the country to the attacker
                            defenderCountry.setOwner(player.GetId())
                            
                            #Get Number of armies to move into the conqured country
                            movingArmies = command.GetQuantity() - defenderWins
                            
                            defenderCountry.addArmies(movingArmies)  
                            
                            #Set conqueredTerritory to true so player gets a risk card.
                            conqueredTerritory = True      
                            
                #Trade Command            
                elif command.GetCommandType() == Command.TRADE:
                    if self.isTradeCommandValid(player, command):
                        #Execute command
                        
                        #Add armies to player
                        player.AddArmies(self.GetCardSetValue())
                        
                        #Return card to deck
                        for card in command.GetCards():
                            if not card.GetCardType() == "WILD":
                                #Check if player owns country, if they do add two armies to country
                                cardCountry = self.gameMap.getCountry(card.GetCountryId())
                                if cardCountry.getOwnerId() == player.GetId():
                                    cardCountry.addArmies(2)
                            
                            player.RemoveRiskCard(card)
                            self.strategyCardDeck.ReturnCard(card)
                
                #Move Command
                elif command.GetCommandType() == Command.MOVE:
                    if self.isMoveCommandValid(player, command):
                        Country1 = self.gameMap.getCountry(command.GetCountry1())
                        Country2 = self.gameMap.getCountry(command.GetCountry2())
                        
                        Country1.removeArmies(command.GetQuantity())
                        Country2.addArmies(command.GetQuantity())
                        
                        player.SetHasMoved(True)
                                        
                #End Turn
                elif command.GetCommandType() == Command.END:         
                    #If Player conqured a country, give risk card
                    if conqueredTerritory:
                        player.AddRiskCard(self.strategyCardDeck.DrawCard())
                    break
                
                ##Validate
                #if commandValidatorFactory.IsValid(command):
                    #action = commandProcessor.GetAction(command)
                    ##Action needs to modify hasEnded somehow
                #else:
                    #break                   
                

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

        #Testing
        #return

        counter = 0

        #While there are 2 or more active players play rounds
        while len(self.GetActivePlayers()) > 1:
            self.PlayRound()
            
            counter += 1
            
            #testing
            if counter > 10000:
                break

        #declare winner
        winner = self.GetActivePlayers()[0]
        print str(winner) + " wins!"

    def ProcessCommand(self, command):
        #Switch statement
        # if commandType == Attack
        # elif commandTYpe == Place
        # etc...
        pass

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
        if len(self.gameMap.getPlayerCountries(playerId)) > 0:
            return True
        else:
            return False
    
    def DrawGame(self):
        #Used to Display the game
        pass

    def GetTotalFreeArmies(self):
        armies = 0
        
        for player in self.players:
            armies += player.GetFreeArmies()
            
        return armies

    def GetStartingNumberOfArmies(self, numPlayers):
        #Could be refactored to dictionary
        #Probably doesn't matter since it gets call once per game.
        
        return 12
        
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
            
    def GetCardSetValue(self):
        return 5

    def isAttackCommandValid(self, player, attackCommand):
        errors = []
        #Simple Validations
        if attackCommand.GetId() <= 0:
            errors.append("Command Id Must be Greater than 0.")
        
        if attackCommand.GetPlayerId() <= 0:
            errors.append("Player Id Must be Greater than 0.")
            
        if len(attackCommand.GetCountry1().strip()) == 0:
            errors.append("Attacking country must be specified.")
        
        if len(attackCommand.GetCountry1().strip()) == 0:
            errors.append("Attacked country must be specified.")
            
        if attackCommand.GetQuantity() < 1:
            errors.append("Must specify one or more attacking armies")
        
        if len(errors) > 0:
            raise ValidationError(errors)
        
        #Complex Validations
        attackingCountry = self.gameMap.getCountry(attackCommand.GetCountry1())
        attackedCountry = self.gameMap.getCountry(attackCommand.GetCountry2())
                
        if attackingCountry.getOwnerId() != player.GetId():
            errors.append("Attacking Country must be owned by Player")
            
        if attackedCountry.getOwnerId() == player.GetId():
            errors.append("Attacked Country must not be owned by Player")
            
        if attackedCountry not in self.gameMap.getNeighbors(attackingCountry.getId()):
            errors.append("Attacked Country (" + attackedCountry.getId() + ") and Attacking Country (" + attackingCountry.getId() + ") must be neighbors")
                
        if attackCommand.GetQuantity() > attackingCountry.getNumberOfArmies():
            errors.append("Attacking Country must attack with fewer armies than are stationed there")
        
        if player.GetHasMoved():
            errors.append("Player cannot attack after moving in the same turn.")
        
        if player.GetFreeArmies() > 0:
            errors.append("Player cannot have unplaced armies when attacking")
        
        if len(errors) > 0:
            raise ValidationError(errors)
            
        return True
        
    def isTradeCommandValid(self, player, tradeCommand):
        errors = []
        
        #Simple Validations
        if tradeCommand.GetId() <= 0:
            errors.append("Command Id Must be Greater than 0.")
        
        if tradeCommand.GetPlayerId() <= 0:
            errors.append("Player Id Must be Greater than 0.")
        
        if not len(tradeCommand.GetCards()) == 3:
            errors.append("Must trade exactly 3 cards.")
        
        if player.GetHasMoved():
            errors.append("Player cannot attack after moving in the same turn.")
            
        if len(errors) > 0:
            raise ValidationError(errors)
        
        #Complex Validations
        if StrategyCard.IsHandValid(tradeCommand.GetCards()):
            return True
        else:
            errors.append("Hand is invalid")
            raise ValidationError(errors)
        
    def isMoveCommandValid(self, player, moveCommand):
        errors = []
        
        #Simple Validations
        if moveCommand.GetId() <= 0:
            errors.append("Command Id Must be Greater than 0.")
        
        if moveCommand.GetPlayerId() <= 0:
            errors.append("Player Id Must be Greater than 0.")
        
        if len(moveCommand.GetCountry1().strip()) == 0:
            errors.append("Attacking country must be specified.")
        
        if len(moveCommand.GetCountry1().strip()) == 0:
            errors.append("Attacked country must be specified.")
            
        if moveCommand.GetQuantity() < 1:
            errors.append("Must specify one or more attacking armies")
        
        if len(errors) > 0:
            raise ValidationError(errors)
            
        #Complex Validations
        country1 = self.gameMap.getCountry(moveCommand.GetCountry1())
        country2 = self.gameMap.getCountry(moveCommand.GetCountry2())
        
        if country1.getOwnerId() != player.GetId():
            errors.append("First Country must be owned by Player")
            
        if country2.getOwnerId() != player.GetId():
            errors.append("Second Country must be owned by Player")

        if country1 not in self.gameMap.getNeighbors(country2.getId()):
            errors.append("Country 1 (" + attackedCountry.getId() + ") and Country 2 (" + attackingCountry.getId() + ") must be neighbors")
          
        if moveCommand.GetQuantity() >= country1.getNumberOfArmies():
            errors.append("Must leave atleast one army in Move Country")

        if player.GetHasMoved():
            errors.append("Player cannot attack after moving in the same turn.")
            
        if len(errors) > 0:
            raise ValidationError(errors)
        
        return True
        
class ValidationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

#Idea: Time Machine Game - Game(Players?) can go back in time and the game will reset.

#Maintains Game Variables

#Could keep list of actions taken by players
#This would allow a game to be reviewed or stepped through move-by-move
#Could also be used to rebuild state and test AI by changing variables
