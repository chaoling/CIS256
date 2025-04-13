# Problem Set 6: Simulating the Spread of Disease and Virus Population Dynamics

from patient import Patient
from simpleVirus import NoVirusChildException

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
        super().__init__(viruses, maxPop)
        self.prescription = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        self.newDrug = newDrug

        if self.newDrug not in self.prescription:
            self.prescription.append(self.newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescription

    def getVirusPopulationResistant(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        self.drugResist = drugResist

        resist_pop = 0

        for i in self.viruses:
            if all([i.isResistantTo(j) for j in self.drugResist]) == True:
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
        viruses = self.viruses[:]
        for virus in viruses:
            if virus.doesClear() == True:
                self.viruses.remove(virus)

        popDensity = len(self.viruses) / self.maxPop

        viruses = self.viruses[:]
        for virus in viruses:
            try:
                virus.reproduce(popDensity, self.prescription)
                self.viruses.append(virus)
            except NoVirusChildException:
                continue
