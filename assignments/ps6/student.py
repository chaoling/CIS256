# Problem Set 6: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import matplotlib.pyplot as plt

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''


#
# PROBLEM 1
#
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
            raise NoChildException



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

        new_viruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                new_viruses.append(virus)
                try:
                    new_virus = virus.reproduce(len(new_viruses) / self.maxPop)
                    new_viruses.append(new_virus)
                except NoChildException:
                    pass
        self.viruses = new_viruses
        return self.getTotalPop()

#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):


  avgTotalPopulations = [0] * 300

  for _ in range(numTrials):
    viruses = [SimpleVirus(maxBirthProb, clearProb) for _ in range(numViruses)]
    patient = Patient(viruses, maxPop)

    for step in range(300):
      avgTotalPopulations[step] += patient.update()

  avgTotalPopulations = [pop / numTrials for pop in avgTotalPopulations]

  # Plotting the results
  pylab.plot(avgTotalPopulations, label="SimpleVirus")
  pylab.title("SimpleVirus simulation")
  pylab.xlabel("Time Steps")
  pylab.ylabel("Average Virus Population")
  pylab.legend(loc="best")
  pylab.show()

# Set the parameters for the simulation
numViruses = 100
maxPop = 1000
maxBirthProb = 0.1
clearProb = 0.05
numTrials = 100

# Run the simulation
simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials)

#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):


    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):

        return self.resistances

    def getMutProb(self):

        return self.mutProb

    def isResistantTo(self, drug):


        return self.resistances.get(drug, False)


    def reproduce(self, popDensity, activeDrugs):

      if all(self.isResistantTo(drug) for drug in activeDrugs) and random.random() < (self.maxBirthProb * (1 - popDensity)):
        # Create and return the instance of the offspring ResistantVirus
        offspring_resistances = {}
        for drug, is_resistant in self.resistances.items():
            # Mutate the resistance trait with probability mutProb
            if random.random() < self.mutProb:
                offspring_resistances[drug] = not is_resistant
            else:
                offspring_resistances[drug] = is_resistant

        return ResistantVirus(self.maxBirthProb, self.clearProb, offspring_resistances, self.mutProb)
      else:
        # Virus does not reproduce
        raise NoChildException



class TreatedPatient(Patient):


    def __init__(self, viruses, maxPop):

        Patient.__init__(self, viruses, maxPop)
        self.prescriptions = []


    def addPrescription(self, newDrug):

        if newDrug not in self.prescriptions:
            self.prescriptions.append(newDrug)


    def getPrescriptions(self):

        return self.prescriptions


    def getResistPop(self, drugResist):

      resist_pop = 0
      for virus in self.viruses:
        if all(virus.isResistantTo(drug) for drug in drugResist):
          resist_pop += 1
      return resist_pop

    def update(self):

      total_pop = super().update()

      # Check the effect of drugs on virus particles
      for virus in self.viruses:
          if any(virus.isResistantTo(drug) for drug in self.prescriptions):
              # Virus is resistant to at least one drug, so it reproduces normally
              try:
                  offspring = virus.reproduce(self.getTotalPop() / self.getMaxPop(), self.prescriptions)
                  self.viruses.append(offspring)
              except NoChildException:
                  pass

      return total_pop

#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):

    # Initialize lists to store results for plotting
    avgTotalPopulations = [0] * 300
    avgResistPopulations = [0] * 300

    for _ in range(numTrials):
        # Create a list of ResistantVirus instances
        viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for _ in range(numViruses)]
    
        # Create a TreatedPatient instance
        patient = TreatedPatient(viruses, maxPop)
    
        # Run the simulation for 150 time steps without drug
        for step in range(150):
            avgTotalPopulations[step] += patient.update()
            avgResistPopulations[step] += patient.getResistPop(list(resistances.keys()))
    
        # Add guttagonol drug
        patient.addPrescription("guttagonol")

        # Run the simulation for additional 150 time steps with drug
        for step in range(150, 300):
            avgTotalPopulations[step] += patient.update()
            avgResistPopulations[step] += patient.getResistPop(list(resistances.keys()))
    
# Calculate average populations
avgTotalPopulations = [pop / numTrials for pop in avgTotalPopulations]
avgResistPopulations = [pop / numTrials for pop in avgResistPopulations]

# Plotting the results
import pylab
pylab.plot(avgTotalPopulations, label="Total Virus Population")
pylab.plot(avgResistPopulations, label="Resistant Virus Population")
pylab.title("ResistantVirus Simulation With Drug Treatment")
pylab.xlabel("Time Steps")
pylab.ylabel("Average Virus Population")
pylab.legend(loc="best")
pylab.show()

# Set the parameters for the simulation
numViruses = 100
maxPop = 1000
maxBirthProb = 0.1
clearProb = 0.05
resistances = {'guttagonol': False}
mutProb = 0.005
numTrials = 100

# Run the simulation
simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials)