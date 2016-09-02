#Risk Die Roll Testing

import random

def StandardDeviation(listOfNumbers):
    sumOfList = 0
    mean = 0
    
    #Calculate the Mean
    for num in listOfNumbers:
        sumOfList += num

    mean = float(sumOfList) / len(listOfNumbers)

    #Calculate the Deviations of all numbers
    totalDeviations = 0
    
    for num in listOfNumbers:
        totalDeviations += (num - mean)**2
    
    #Divide by n-1
    standardDeviation = (totalDeviations / (len(listOfNumbers) -1)) ** .5

    return standardDeviation

def Roll(numDie):
    """
    numDie: The number of dice to be rolled
    Returns a sorted list of dice
    """
    rolls = []
    
    for die in xrange(numDie):
        rolls.append(random.randrange(1,7))

    rolls.sort(reverse = True) #Sort Descending Order
    
    return rolls

def Trial(numAttackerDies, numDefenderDies, trialSize):
    """
    Returns the ratio of Attacker Wins to Attacker Losses
    numAttackerDies: The number of dice used by the attacker
    numDefenderDies: The number of dice used by the defender
    trialSize: The number of times to roll
    """
    
    #Get the size of the shortestList
    chances = min(numAttackerDies, numDefenderDies)

    attackerWins = 0

    for trialRound in xrange(trialSize):
        attackerDice = Roll(numAttackerDies);
        defenderDice = Roll(numDefenderDies);

        for chance in xrange(chances):
            #Tie goes to the defender
            if attackerDice[chance] > defenderDice[chance]:
                attackerWins += 1

    return float(attackerWins) / (trialSize * chances)

def RunTrials(numAttackerDies, numDefenderDies, numTrials, trialSize):
    """
    Runs multiple trials, returns the mean of the trials
    Returns Tuple of (Mean, Standard Deviation)
    """

    intermediateRatio = 0
    trialResults = []

    for trial in xrange(numTrials):
        result = Trial(numAttackerDies, numDefenderDies, trialSize)
        trialResults.append(result)
        intermediateRatio += result

    meanOfTrials = intermediateRatio / numTrials
    standardDeviation = StandardDeviation(trialResults)

    return (meanOfTrials, standardDeviation)
    
def GetAllRiskOdds(numberOfTrials, trialSize):
    maxAttackerDies = 3
    maxDefenderDies = 2

    print "Calculating Risk Odds Running",numberOfTrials,"trials of size",trialSize
    print

    for defenders in xrange(1, maxDefenderDies + 1):
        for attackers in xrange(1, maxAttackerDies + 1):
            odds = RunTrials(attackers, defenders, numberOfTrials, trialSize)
            #odds = (0.25, .005)
            print "Attackers:", attackers, "Defenders:", defenders
            print "    Odds of Winning Chance:", odds[0]
            print "    Standard Deviation:", odds[1]
            print ""
