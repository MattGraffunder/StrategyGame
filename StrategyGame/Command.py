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
