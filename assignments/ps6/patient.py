# Problem Set 6: Simulating the Spread of Disease and Virus Population Dynamics

from simpleVirus import NoVirusChildException


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

    def getVirusPopulationTotal(self):
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

        viruses = self.viruses[:]
        for virus in viruses:
            if virus.doesClear() == True:
                self.viruses.remove(virus)

        popDensity = len(self.viruses) / self.maxPop

        viruses = self.viruses[:]
        for virus in viruses:
            try:
                virus.reproduce(popDensity)
                self.viruses.append(virus)
            except NoVirusChildException:
                continue