import random
import matplotlib.pyplot as plt

class NoChildException(Exception):
    pass

class SimpleVirus(object):
    def __init__(self, maxBirthProb, clearProb):
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        return self.maxBirthProb

    def getClearProb(self):
        return self.clearProb

    def doesClear(self):
        return random.random() < self.clearProb

    def reproduce(self, popDensity):
        if random.random() < self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException()

class Patient(object):
    def __init__(self, viruses, maxPop):
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        return self.viruses

    def getMaxPop(self):
        return self.maxPop

    def getTotalPop(self):
        return len(self.viruses)

    def update(self):
        virusesCopy = self.viruses[:]
        for virus in virusesCopy:
            if virus.doesClear():
                self.viruses.remove(virus)
        popDensity = len(self.viruses) / self.maxPop
        for virus in self.viruses:
            try:
                child = virus.reproduce(popDensity)
                self.viruses.append(child)
            except NoChildException:
                pass
        return len(self.viruses)

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials):
    finalPopulations = []
    for trial in range(numTrials):
        viruses = [SimpleVirus(maxBirthProb, clearProb) for _ in range(numViruses)]
        patient = Patient(viruses, maxPop)
        populations = []
    results = []
    for i in range(numTrials):
        viruses = []
        for _ in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))

        patient = Patient(viruses, maxPop)
        population = [0] * 300
        for step in range(300):
            population[step] += patient.update()

        results.append(population) #results is of dim [numTrials]x[300]
    averages = []
    for i in range(300):
        sum = 0
        for j in range(numTrials):
            sum += results[j][i]
        average = sum/numTrials
        averages.append(average)
            
    plt.plot(averages, label="SimpleVirus")
    plt.title("Simple Virus simulation")
    plt.xlabel("Time Steps")
    plt.ylabel("Average Virus Population")
    plt.legend(loc="best")
    plt.show()
    '''
        for step in range(300):
            population = patient.update()
            populations.append(population)
        finalPopulations.append(populations[-1])
    plt.plot(range(300), finalPopulations)
    plt.xlabel('Time Steps')
    plt.ylabel('Virus Population')
    plt.title('Virus Population Over Time')
    '''
    plt.show()

if __name__ == "__main__":
    print("Running simulation without drug...")
    simulationWithoutDrug(100, 1000, 0.1, 0.05, 5)
