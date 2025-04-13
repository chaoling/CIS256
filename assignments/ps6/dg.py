
# Problem Set 6: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab as plt
#import plotly (optional, if you want to use plotly)

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
class SimpleVirus:
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        return random.random() < self.clearProb

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
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

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
        virusesCopy = self.viruses[:] # Make a copy of the list of viruses to iterate over.
        for virus in virusesCopy:
            if virus.doesClear():
                self.viruses.remove(virus)

        popDensity = self.getTotalPop() / float(self.getMaxPop())

        virusesCopy = self.viruses[:] # Make another copy of the list of viruses to iterate over.
        for virus in virusesCopy:
            try:
                childVirus = virus.reproduce(popDensity)
                self.viruses.append(childVirus)
            except NoChildException:
                pass

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

    # Define the data structure to hold the virus population for each time step and trial
    virus_populations = []

    # Create numTrials number of patients and run simulation for each patient
    for trial in range(numTrials):
        # Create a list of viruses
        viruses = [SimpleVirus(maxBirthProb, clearProb) for v in range(numViruses)]

        # Create a patient with the list of viruses and maximum population size
        patient = Patient(viruses, maxPop)

        # Run the simulation for 300 time steps
        virus_counts = []
        for i in range(300):
            virus_counts.append(patient.update())

        # Append the virus population data for this trial to the list of all virus populations
        virus_populations.append(virus_counts)

    # Calculate the average virus population for each time step
    avg_populations = [sum(step) / float(len(step)) for step in zip(*virus_populations)]

    # Plot the average virus population as a function of time
    plt.plot(avg_populations)
    plt.title("SimpleVirus simulation")
    plt.xlabel("Time Steps")
    plt.ylabel("Average Virus Population")
    plt.legend("Virus Population")
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

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances.copy()
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances.copy()

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
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

        # Determine whether the virus reproduces
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()
        if random.random() <= self.maxBirthProb * (1 - popDensity):
            # Inherit resistance from parent
            child_resistances = {}
            for drug in self.resistances:
                if random.random() < 1 - self.mutProb:
                    child_resistances[drug] = self.resistances[drug]
                else:
                    child_resistances[drug] = not self.resistances[drug]
            return ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances, self.mutProb)
        else:
            raise NoChildException()
            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.drugsList = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if newDrug not in self.drugsList:
            self.drugsList.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugsList

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        resistPop = 0
        for virus in self.viruses:
            isResistant = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    isResistant = False
                    break
            if isResistant:
                resistPop += 1
        return resistPop

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

        for virus in self.viruses[:]:
            if virus.doesClear():
                self.viruses.remove(virus)

        popDensity = len(self.viruses) / self.getMaxPop()

        for virus in self.viruses[:]:
            try:
                childVirus = virus.reproduce(popDensity, self.getPrescriptions())
                self.viruses.append(childVirus)
            except NoChildException:
                pass

        return len(self.viruses)


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

    virus_populations = []
    resistant_populations = []
    for trial in range(numTrials):
        # initialize viruses
        viruses = []
        for i in range(numViruses):
            virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            viruses.append(virus)

        # initialize patient
        patient = TreatedPatient(viruses, maxPop)

        # simulate 150 time steps without drugs
        for i in range(150):
            virus_populations.append(patient.update())
            resistant_populations.append(patient.getResistPop(['guttagonol']))

        # add guttagonol to the treatment
        patient.addPrescription('guttagonol')

        # simulate another 150 time steps with drugs
        for i in range(150):
            virus_populations.append(patient.update())
            resistant_populations.append(patient.getResistPop(['guttagonol']))

    # calculate the average virus populations over all trials
    avg_virus_populations = []
    avg_resistant_populations = []
    for i in range(300):
        avg_virus_populations.append(sum(virus_populations[i::300]) / float(numTrials))
        avg_resistant_populations.append(sum(resistant_populations[i::300]) / float(numTrials))

    # plot the results
    plt.figure(1)
    plt.plot(avg_virus_populations, label="Total")
    plt.plot(avg_resistant_populations, label="Resistant")
    plt.title("ResistantVirus simulation")
    plt.xlabel("Time Steps")
    plt.ylabel("Average Virus Population")
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