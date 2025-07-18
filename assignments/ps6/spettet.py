# Problem Set 6: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab as plt
import numpy as np
#import plotly (optional, if you want to use plotly)


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

#
# PROBLEM 1
#
class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

      self.maxBirthProb = maxBirthProb
      self.clearProb = clearProb

    def getMaxBirthProb(self):
      return self.maxBirthProb
  

    def getClearProb(self):
      return self.clearProb

    def doesClear(self):
      """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
      """

      ans = np.random.choice([True, False], 1, p=[self.getClearProb(), 1-self.getClearProb()])
      return ans

    
    def reproduce(self, popDensity):
      """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
      """

      if random.random() < self.maxBirthProb * (1 - popDensity):
        return SimpleVirus(self.maxBirthProb, self.clearProb)
      else:
        raise NoChildException


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

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
      """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
      """

    # Calculate current population density
      popDensity = self.getTotalPop() / self.getMaxPop()

    # Determine whether each virus particle should reproduce and add offspring virus particles to the list of viruses in this patient
      for virus in self.viruses[:]: # Creating copy of list to ensure iteration over entire original list
        if virus.doesClear():
          self.viruses.remove(virus)
        else:
          try:
            new_virus = virus.reproduce(popDensity)
            if new_virus:
              self.viruses.append(new_virus)
          except NoChildException as e:
            print(e)

    # Return the total virus population at the end of the update
      return self.getTotalPop()

#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials):
  """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
  """

  viruses = []
  avg_t = [0]*300
    # Create a list to store the virus populations for each trial
  for i in range(numViruses):
      viruses.append(SimpleVirus(maxBirthProb, clearProb))
    
      patient = Patient(viruses, maxPop)
      population = [0] * 300
      for _ in range(numTrials):
        for step in range(300):
          patient.update()
          population[step] += patient.getTotalPop()


    # Calculate the average virus population for each time step across all trials
  for i in range(300):
    avg_t[i] = population[i] / numTrials

    # Plot the graph of the average virus population for each time step
  plt.plot(avg_t, '-r', label="Total Virus")
  plt.title("Resistant Virus Simulation")
  plt.xlabel('Time Steps')
  plt.ylabel('Average and Total Resistant Virus Population')
  plt.legend(loc="best")
  plt.show()


#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
      """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.
      """

      self.maxBirthProb = 0.0
      assert 0.0 <= mutProb <= 1.0


    def getResistances(self):
      return self.resistances

    def getMutProb(self):
      return self.mutProb

    def isResistantTo(self, drug):
      return self.resistances.get(drug, False)


    def reproduce(self, popDensity, activeDrugs):
      """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
      """
      resistant_to_all_drugs = True
      for drug in activeDrugs:
          if not self.isResistantTo(drug):
            resistant_to_all_drugs = False
            break

      if resistant_to_all_drugs:
          if random.random() < self.maxBirthProb * (1 - popDensity):
              child_resistances = {}
              for drug, is_resistant in self.resistances.items():
                if random.random() < 1 - self.mutProb:
                        child_resistances[drug] = is_resistant
                else:
                    child_resistances[drug] = not is_resistant
              return ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances, self.mutProb)
        
      raise NoChildException

            

class TreatedPatient(Patient):

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).             
        """
        super().__init__(viruses, maxPop)
        self.drugs = []


    def addPrescription(self, newDrug):
        """
        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
          self.drugs.append(newDrug)


    def getPrescriptions(self):
        return self.drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        resist_pop = 0
        for virus in self.viruses:
            is_resistant = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    is_resistant = False
                    break
            if is_resistant:
                resist_pop += 1

        return resist_pop


    def update(self):
      """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
      """

     # Calculate current population density
      popDensity = self.getTotalPop() / self.getMaxPop()

    # Determine whether each virus particle should reproduce and add offspring virus particles to the list of viruses in this patient
      for virus in self.viruses[:]: # Creating copy of list to ensure iteration over entire original list
        if virus.doesClear():
          self.viruses.remove(virus)
        else:
          try:
            new_virus = virus.reproduce(popDensity, self.getPrescriptions())
            if new_virus:
              self.viruses.append(new_virus)
          except NoChildException as e:
            print(e)

    # Return the total virus population at the end of the update
      return self.getTotalPop()


#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials):
  """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
  """
  viruses = []
  for i in range(numViruses):
    viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

  patient = TreatedPatient(viruses, maxPop)
  population = [0] * 300
  rpopulation = [0] * 300
  avg_t = population[:]
  avg_r = rpopulation[:]
  for _ in range(numTrials):
    for step in range(150):
      patient.update()
      population[step] += patient.getTotalPop()
      rpopulation[step] += patient.getResistPop(['guttagonol'])

    patient.addPrescription('guttagonol')
    for step in range(150, 300):
      patient.update()
      population[step] += patient.getTotalPop()
      rpopulation[step] += patient.getResistPop(['guttagonol'])
  

# plot the results
  plt.plot(avg_t, '-r', label="total Virus")
  plt.plot(avg_r, '-b', label="Resistant Virus")
  plt.title("Resistant Virus Simulation")
  plt.xlabel("Time Steps")
  plt.ylabel("Average and Total Resistant Virus Population")
  plt.legend(loc="best")
  plt.show()

if __name__ == "__main__":
  print("running simulation......")
  v1 = SimpleVirus(0.97, 0.28)
  p1 = Patient([v1], 100)
  for i in range(100):
    p1.update()
  print(p1.getTotalPop())

  simulationWithoutDrug(10, 100, .8, .2, 1)
  simulationWithDrug(75, 100, .8, 0.1, {'guttagonol': True}, 0.8, 1)