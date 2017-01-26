import random, Command

class Player(object):
    def __init__(self, id, name):
        self.riskCards = []
        self.freeArmies = 0
        self.id = id
        self.name = name
        self.commandBuilder = Command.CommandBuilder()
        #self.Countries = [] #Might only be a function level variable

    def PlayTurn(self, previousResults):
        #Maybe add newArmies(int) and map(Map) as parameters?
        
        #I'm starting to like the idea of a callback provided by the game class
        #The callback would take a message like the ones below

        #Need to figure out how the player interfaces with the rest of the game
            #Perhaps some sort of message structure.
            #I.e. ATTACK "From Country" "To Country" NumArmies
            #More generally, COMMAND Params
            #Perhaps a command object instead of string?
                #I think that a command string might be more flexible, or at least easier for v1
            #Could also be used to easily log moves

            #PLACE
            #ATTACK
            #MOVE            
            #TRADE
            #END

        #Previous Results could be used to return if an attack was successful, territory captured, etc...
            
        #Maybe instead of a callback, the game object calls PlayTurn repeatedly for the same player
        #The PlayTurn would become "GetMove" and return a message like the ones above.
        #This would keep control in the hands of the Game class, and not allow a rouge AI to issue moves out of turn
        #I think this should simplify flow of control too
        
        #Get new Armies (from param, or req from Game?)
            #Also needs to handle getting more armies from Risk Cards

        #Get Currently Owned Countries

        #Place new Armies

        #Determine which countries (if any) to attack
            #determine which countries are vunerable?

        #Attack

        #Free Move - This will be difficult
        
        pass
    
    #Player Interface

    def GetId(self):
        return self.id

    def GetName(self):
        return self.name
        
    def GetFreeArmies(self):
        return self.freeArmies

    def ChooseCountry(self, gameMap):
        """
        This is to allocate countries at the beginning of the game
        """
        pass

    def UpdateMap(self, gameMap):
        """
        This could be used to update the Player's map for each turn.
        Although, if the player has a reference to the map, maybe it doesn't need updating
        """
        pass

    def AddArmies(self, numberOfArmies):
        """
        Adds Armies to the player
        """
        self.freeArmies += numberOfArmies
        
    def RemoveArmies(self, numberOfArmies):
        """
        Removes Armies from the player
        """
        self.freeArmies -= numberOfArmies

    def AddRiskCard(self, riskCard):
        self.riskCards.append(riskCard)

    def __str__(self):
        return self.name

#TODO - Implement Concrete Class
class HumanPlayer(Player):
    def __init__(self, id, name = "Human Player"):
        Player.__init__(self, id, name)
    """
    The Human Player give a human the ability to interact with the game
    """
    pass

#TODO - Implement Concrete Class
class RandomAI(Player):
    """
    The Random AI decides all actions randomly
    """
    def __init__(self, id, name = "Random AI"):
        Player.__init__(self, id, name)
    def PlayTurn(self, gameMap):
        #If new armies > 0 Place armies:
        if self.GetFreeArmies() > 0:
            countries = gameMap.getPlayerCountries(self.GetId())
            
            country = random.choice(countries)
            armies = random.randrange(1, self.GetFreeArmies() + 1)
            
            return self.commandBuilder.GetPlace(self.GetId(), country.getId(), armies)
        #decide to attack
        #Skip move for now
        #end turn
        
        return self.commandBuilder.GetEnd(self.id) #Default to End for now
        pass    
    def ChooseCountry(self, gameMap):
        #Get unowned countries
        choices = gameMap.getPlayerCountries(None)

        #If there aren't unoccupied countries, add armies to owned countries
        if len(choices) == 0:
            choices = gameMap.getPlayerCountries(self.id)
            
            if len(choices) == 0:
                return None
        
        #choose one at random        
        country = random.choice(choices)#choices[random.randrange(0, len(choices))]
                        
        return country.getId()
    
#TODO - Implement Concrete Class
class SmartAI(Player):
    def __init__(self, id, name = "Smart AI"):
        Player.__init__(self, id, name)
    """
    The Smart AI is specifically programed to win.
    """
    pass

#TODO - Implement Concrete Class
class PassiveAI(Player):
    def __init__(self, id, name = "Passive AI"):
        Player.__init__(self, id, name)
    """
    The Passive AI gets and places new armies each turn, but doesn't attack
    """
    pass

#TODO - Implement Concrete Class
class DavidAI(Player):
    def __init__(self, id, name = "David AI"):
        Player.__init__(self, id, name)
    """
    Only attacks the Largest Player
    """
    pass

#TODO - Implement Concrete Class
class PredatorAI(Player):
    def __init__(self, id, name = "Predator AI"):
        Player.__init__(self, id, name)
    """
    Focuses on attacking the weakest Player
    """

#TODO - Implement Concrete Class
class PluginAI(Player):
    def __init__(self, id, name = "Plugin AI"):
        Player.__init__(self, id, name)
    """
    Create a way for others to devise and use a custom AI
    """
    pass

#TODO - Implement Concrete Class
class AncestralAI(Player):
    def __init__(self, id, name = "Ancestral AI"):
        Player.__init__(self, id, name)
    """
    Tries to keep it's starting territories at all cost.
    """
    pass

#TODO - Implement Concrete Class
class FoolhardyAI(Player):
    def __init__(self, id, name = "Foolhardy AI"):
        Player.__init__(self, id, name)
    """
    Attacks far more than it probably should
    """
    pass

#TODO - Implement Concrete Class
class GengisKhanAI(Player):
    def __init__(self, id, name = "Gengis Khan AI"):
        Player.__init__(self, id, name)
    """
    Tries to conquer Asia at all costs.
    """
    pass

#TODO - Implement Concrete Class
class BadAI(Player):
    def __init__(self, id, name = "Bad AI"):
        Player.__init__(self, id, name)
    """
    Makes bad decisions at every opportunity.
    """
    pass
