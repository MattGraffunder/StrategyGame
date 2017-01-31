import random

class GameDice(object):
    
    def __init__(self):
        pass
        
    def GetWinners(self, numberOfAttackers, numberOfDefenders):
        #if number of attackers is greater than 3, roll three dice
        attackingDiceToRoll = min(numberOfAttackers, 3)
        
        #if the number of defenders in greater than 2, roll two dice
        defendingDiceToRoll = min(numberOfDefenders, 2)       
                
        #Roll Dice
        attackerRoll = self.roll(attackingDiceToRoll)
        defenderRoll = self.roll(defendingDiceToRoll)
        
        chances = min(attackingDiceToRoll, defendingDiceToRoll)
        
        #Check Wins
        attackerWins = 0        
        for chance in xrange(chances):
            #Tie goes to the defender
            if attackerRoll[chance] > defenderRoll[chance]:
                attackerWins += 1
                
        #Return tuple of (# of Attacker Wins, # of Defender Wins)
        return (attackerWins, chances - attackerWins)

    def roll(self, numDie):
        """
        numDie: The number of dice to be rolled
        Returns a list of dice sorted highest to lowest
        """
        rolls = []
        
        for die in xrange(numDie):
            rolls.append(random.randrange(1,7))

        rolls.sort(reverse = True) #Sort Descending Order
        
        return rolls

#Different version of GameDice that can replay prior commands
#~ 
#~ gameDice = GameDice()
#~ 
#~ print gameDice.GetWinners(3,2)
