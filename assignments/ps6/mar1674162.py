'''
Name : main.py (problem set 6)
Author: Maribel Bustamante
Problem Set 6 Description: Simulating the Spread of Disease and Virus 
Population Dynamics 
'''

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
import random
import pylab as plt



# Begin helper code
class NoChildException(Exception):
    
  """
  NoChildException is raised by the reproduce() method in the SimpleVirus
  and ResistantVirus classes to indicate that a virus particle does not
  reproduce. You can use NoChildException as is, you do not need to
  modify/add any code.
  """

  pass

# End helper code


#
# PROBLEM 1
#
class SimpleVirus(object):
    
  """
  Representation of a simple virus (does not model drug 
  effects/resistance).
  """
  
  def __init__(self, maxBirthProb: float, clearProb: float):
        
    """
    Initializes a SimpleVirus instance, saves all parameters as attributes
    of the instance. 
    maxBirthProb: Maximum reproduction probability (a float between 0-1)       
    clearProb: Maximum clearance probability (a float between 0-1).
    Both parameters use "max() and min()" functions to ensure that the float 
    values of both parameters are limited to the valid range.
    """

    self.maxBirthProb = max(0, min(maxBirthProb, 1))
    self.clearProb = max(0, min(clearProb, 1))
    

  def getMaxBirthProb(self):
        
    """
    Returns the max birth probability.
    """

    return self.maxBirthProb 
          

  def getClearProb(self):
        
    """
    Returns the clear probability
    """

    return self.clearProb       
    
    
  def doesClear(self):
        
    """ 
    Stochastically determines whether this virus particle is cleared from 
    the patient's body at a time step. 
    
    @param step is timeStep, probability in an elapsed set of
    time.
    
    returns: True with probability self.getClearProb and otherwise returns
    False.
    """

    ans = np.random.choice([True, False],1,p=[self.clearProb,1-self.clearProb])
    return ans
    

  def reproduce(self, popDensity: float):
        
    """
    Stochastically determines whether this virus particle reproduces at a
    time step. Called by the update() method in the Patient and
    TreatedPatient classes. The virus particle reproduces with probability
    self.maxBirthProb * (1 - popDensity).
    
    If this virus particle reproduces, then reproduce() creates and returns
    the instance of the offspring SimpleVirus (which has the same
    maxBirthProb and clearProb values as its parent).         
    
    @param popDensity: the population density (a float), defined as the 
    current virus population divided by the maximum population.         
    
    returns: a new instance of the SimpleVirus class representing the
    offspring of this virus particle. The child should have the same
    maxBirthProb and clearProb values as this virus. Raises a
    NoChildException if this virus particle does not reproduce.               
    """

    # Variable for proability of virus reproducing 
    p1 = self.maxBirthProb * (1 - popDensity)
    
    # Generate random number, and check if virus reproduces
    ans = np.random.random() <= p1
    if ans:
      # Virus offspring with a new instance of SimpleVirus.
      return SimpleVirus(self.maxBirthProb, self.clearProb)
    else:
      raise NoChildException ("Virus did not reproduce")
      


class Patient(object):
    
  """
  Representation of a simplified patient. The patient does not take any drugs
  and his/her virus populations have no drug resistance.
  """
  
  
  def __init__(self, viruses, maxPop: int):
        
    """
    Initialization function, saves the viruses and maxPop       
    parameters as attributes.
    
    viruses: the list representing the virus population (a list of
    SimpleVirus instances)
    
    maxPop: the maximum virus population for this patient (an integer)
    """

    self.viruses = viruses
    self.maxPop = maxPop

 
  def getViruses(self):
      
    """
    Returns the viruses in this Patient.
    """

    return self.viruses

 
  def getMaxPop(self):
      
    """
    Returns the max population.
    """

    return self.maxPop

  
  def getTotalPop(self):
      
    """
    Gets the size of the current total virus population. 
    returns: The total virus population (an integer)
    """

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
    
    # Empty list to copy
    self.viruses = []
    # Get popDensity = current virus pop / max virus population
    popDensity = self.getTotalPop() / self.getMaxPop()
    # Determine if virus is deleted or copied.
    # Copy instead of aliasing, to avoid shifting when removing
    for virus in self.viruses[:]:
      # If clears, remove from virusPop at each step
      if virus.doesClear():  
        self.viruses.remove(virus)        
      else:
        # If not clear, and still alive append to new_virus list
        try:
          new_virus = virus.reproduce(popDensity)
          if new_virus:
            self.viruses.append(new_virus) 
        except NoChildException as e:
            print (e)
    return self.getTotalPop()

#
# PROBLEM 2
#

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                              numTrials):
        
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
    for i in range(numViruses):
      viruses.append(SimpleVirus(maxBirthProb, clearProb))

    patient = Patient(viruses, maxPop)
    population = [0] * 300  # gives all the data points / plots
    for _ in range(numTrials):
      for step in range(300):  #  each file
        patient.update()
        population[step] += patient.getTotalPop()
        
    # take the average of population
    for i in range(300):
      viruses[i] = population[i] / numTrials
        

    # plot code with plotly
    plt.plot(viruses, "-r", label="Total Virus")
    plt.title("Resistant Virus Simulation")
    plt.xlabel("Time Steps")
    plt.ylabel("Average Virus Population")
    plt.legend(loc="best")
    plt.show()


#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    
  """
  Subclass of SimpleVirus. Representation of a virus which can have drug 
  resistance.
  """
  
  
  def __init__(self, maxBirthProb: float, clearProb: float,
               resistances: dict, mutProb: float):
      
    """
    Initialize a ResistantVirus instance, using reproduce() function child 
    resistances. Saves all parameters as attributes
    of the instance.
  
    maxBirthProb: Maximum reproduction probability (a float between 0-1)       
  
    clearProb: Maximum clearance probability (a float between 0-1).
  
    resistances: A dictionary of drug names (strings) mapping to the state
    of this virus particle's resistance (either True or False) to each drug.
    e.g. {'guttagonol':False, 'srinol':False}, means that this virus
    particle is resistant to neither guttagonol nor srinol.
  
    mutProb: Mutation probability for this virus particle (a float). This is
    the probability of the offspring acquiring or losing resistance to a drug.
    """
    # Initialize this instance's attributes             
    self.maxBirthProb = max(0, min(maxBirthProb, 1))
    self.clearProb = max(0, min(clearProb, 1)) 
                 
    # Initialize reproduce function for child instances            
    ResistantVirus.reproduce(self, self.popDensity)
                 
   # Initialize resistances and mutProb attributes                 
    self.resistances = resistances
    self.mutProb = mutProb      
                 
      
  def getResistances(self):
     
    """
    Returns the resistances for this virus.
    """
    
    return self.resistances

  
  def getMutProb(self):
      
    """
    Returns the mutation probability for this virus.
    """

    return self.mutProb


  def isResistantTo(self, drug: str):
          
    """
    Get the state of this virus particle's resistance to a drug. This method
    is called by getResistPop() in TreatedPatient to determine how many virus
    particles have resistance to a drug.       
  
    drug: The drug (a string)
  
    returns: True if this virus instance is resistant to the drug, False
    otherwise.
    """

    return self.resistances.get(drug, False)
      

  def reproduce(self, popDensity: float, activeDrugs: str):
      
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
    # calculate probability of reproduction from parent
    p1 = SimpleVirus.maxBirthProb * (1 - popDensity)

    # check if virus reproduces
    ans = np.random.random() <= p1
    if ans:      
       # check for and add mutations to child resistances
      for drug in ResistantVirus.isResistantTo.keys():      
        if ans <= self.mutProb:
          # Create child virus with mutated resistances
          return ResistantVirus.reproduce(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
        else:
          raise NoChildException
      
    

class TreatedPatient(Patient):
    
  """
  Subclass of Patient. Representation of a patient. The patient is 
  able to take drugs and his/her   virus population can acquire 
  resistance to the drugs he/she takes.
  """
  
  def __init__(self, viruses: list, maxPop: int):
        
    """
    Initialization function, saves the viruses and maxPop parameters as
    attributes. Also initializes the list of drugs being administered
    (which should initially include no drugs).              

    viruses: The list representing the virus population (a list of
    virus instances)

    maxPop: The  maximum virus population for this patient (an integer)
    """
    
    Patient.__init__(self, viruses, maxPop)
    # List of drugs being administered is empty
    self.drugs = []
        
    
  def addPrescription(self, newDrug: str):
        
    """
    Administer a drug to this patient. After a prescription is added,
    the drug acts on the virus population for all subsequent time 
    steps. If the newDrug is already prescribed to this patient, 
    the method has no effect.
  
    newDrug: The name of the drug to administer to the patient 
    (a string).
  
    postcondition: The list of drugs being administered to a 
    patient is updated
    """
    
    if newDrug not in self.drugs:
      self.drugs.append(newDrug)
            

  def getPrescriptions(self)->str:
      
    """
    Returns the drugs that are being administered to this patient.
        
    returns: The list of drug names (strings) being administered to 
    this patient.
    """

    return self.drugs 

        
  def getResistPop(self, drugResist: list)->int:
    
    """
    Get the population of virus particles resistant to the drugs listed
    in drugResist.       
  
    drugResist: Which drug resistances to include in the population 
    (a list of strings - e.g. ['guttagonol'] or ['guttagonol', 
    'srinol'])
  
    returns: The population of viruses (an integer) with resistances 
    to all drugs in the drugResist list.
    """
    # Start numResistant counter
    numResistant = 0
    
    # Check all items in list for virus particle resistant to one drug
    for virus in self.viruses:       
      if all(self.getPrescriptions(self.drugs) for drug in drugResist):
        numResistant += 1
     # Returns number of virus particles that are resistant 
    return numResistant    
      
    

  def update(self):
    
    """
    Update the state of the virus population in this patient for a 
    single time step. update() should execute these actions in order:

    - Determine whether each virus particle survives and update 
      the list of virus particles accordingly
  
    - The current population density is calculated. This population 
      density value is used until the next call to update().
  
    - Based on this value of population density, determine whether          
      each virus particle should reproduce and add offspring virus           
      particles to the list of viruses in this patient.
      
      The list of drugs being administered should be accounted for in        
      the determination of whether each virus particle reproduces.
  
      returns: The total virus population at the end of the update (an
      integer)
    """
    
    # Get popDensity = current virus pop / max virus population
    popDensity = self.getTotalPop() / self.getMaxPop()
    
    # Determine if virus is deleted or copied.
    for virus in self.viruses[:]:
      # If clears, remove from virusPop at each step
      if virus.doesClear():  
        self.viruses.remove(virus)        
      else:
        # If not clear, and still alive append to new_virus list
        try:
          new_virus = virus.reproduce(popDensity)
          if new_virus:
            self.viruses.append(new_virus) 
        except NoChildException as e:
            print (e)
    return self.getTotalPop()



#
# PROBLEM 4
#

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb,
                           resistances, mutProb, numTrials):
                             
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


if __name__ == "__main__":
    print("running simulation......")
    v1 = SimpleVirus(0.97, 0.28)
    p1 = Patient([v1], 100)
    for i in range(100):
        p1.update()
    print(p1.getTotalPop())

    simulationWithoutDrug(10, 100, .8, .2, 1)
    simulationWithDrug(75, 100, .8, 0.1, {'guttagonol': True}, 0.8, 1)
    '''
    viruses = [
        SimpleVirus(0.01, 0.9400000000000001),
        SimpleVirus(0.85, 0.73),
        SimpleVirus(0.61, 0.86)
    ]
    P1 = Patient(viruses, 6)
    for i in range(3):
        P1.update()
    print(P1.getTotalPop())
    
    
    viruses = [
        SimpleVirus(0.27, 0.37),
        SimpleVirus(0.26, 0.85),
        SimpleVirus(0.66, 0.29),
        SimpleVirus(0.83, 0.09),
        SimpleVirus(0.22, 0.93),
        SimpleVirus(0.58, 0.93)
    ]
    P1 = Patient(viruses, 7)
    print(P1.getTotalPop())
    virus = SimpleVirus(1.0, 0.0)
    patient = Patient([virus], 100)
    for i in range(100):
        patient.update()
    print(patient.getTotalPop())
    '''