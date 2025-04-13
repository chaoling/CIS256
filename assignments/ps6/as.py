# Problem Set 6: Simulating the Spread of Disease and Virus Population Dynamics

import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import numpy as np
import pylab

from patient import Patient
from treatedPatient import TreatedPatient
from simpleVirus import SimpleVirus
from resistantVirus import ResistantVirus

TIMESTEPS = 300
PRESCRIPTION = 'guttagonol'
XLABEL = 'Number of steps'
YLABEL = 'Virus Population'
TITLE_WOD = 'Simple Virus Simulation in Patient'
TITLE_WD = 'Virus Simulation in Patient'


def simulationWithoutDrug(numViruses, maxVirusPopulation, maxBirthProbability,
                          maxClearProbability, numTrials):
    """
    Run the simulation and plot the graph.
    No drugs are used and viruses do not have any drug resistance.
    For each trial, instantiate a patient, run a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxVirusPopulation: maximum virus population for patient (an integer)
    maxBirthProbability: Maximum reproduction probability (a float between 0-1)        
    maxClearProbability: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    data = np.zeros(TIMESTEPS)

    for i in range(numTrials):
        virus = SimpleVirus(maxBirthProbability, maxClearProbability)
        viruses = [virus] * numViruses
        patient = Patient(viruses, maxVirusPopulation)
        virus_count = []
        for j in range(TIMESTEPS):
            patient.update()
            virus_count.append(patient.getVirusPopulationTotal())
        data = data + virus_count

    data_avg = data / numTrials

    pylab.plot(list(data_avg), label='Average SimpleVirus Population')
    pylab.xlabel(XLABEL)
    pylab.ylabel(YLABEL)
    pylab.title(TITLE_WOD)
    pylab.legend()
    pylab.show()


def simulationWithDrug(numResistantViruses, maxVirusPopulation,
                       maxBirthProbability, maxClearanceProbability,
                       drugResistances, mutationProbability, numTrials):
    """
    Runs simulations and plots graphs.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxVirusPopulation: maximum virus population for patient (an integer)
    maxBirthProbability: Maximum reproduction probability (a float between 0-1)        
    maxClearProbability: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutationProbability: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)

    """
    halfTimesteps = int(TIMESTEPS / 2)

    data1 = np.zeros(TIMESTEPS)
    data2 = np.zeros(TIMESTEPS)

    for i in range(numTrials):
        virus = ResistantVirus(maxBirthProbability, maxClearanceProbability,
                               drugResistances, mutationProbability)
        viruses = [virus] * numResistantViruses
        patient = TreatedPatient(viruses, maxVirusPopulation)
        virus_count = []
        virus_count_resistant = []

        for j in range(halfTimesteps):
            patient.update()
            virus_count.append(patient.getVirusPopulationTotal())
            virus_count_resistant.append(
                patient.getVirusPopulationResistant([PRESCRIPTION]))

        # Add prescription
        patient.addPrescription(PRESCRIPTION)

        for k in range(halfTimesteps):
            patient.update()
            virus_count.append(patient.getVirusPopulationTotal())
            virus_count_resistant.append(
                patient.getVirusPopulationResistant([PRESCRIPTION]))
        data1 = data1 + virus_count
        data2 = data2 + virus_count_resistant

    data1_avg = data1 / numTrials
    data2_avg = data2 / numTrials

    # Plot
    pylab.figure('Non-Resistant')
    pylab.plot(list([float('{0:.1f}'.format(i)) for i in data1_avg]),
               label='Non-resistant population')
    pylab.xlabel(XLABEL)
    pylab.ylabel(YLABEL)
    pylab.title(TITLE_WD)
    pylab.legend()

    pylab.figure('Resistant')
    pylab.plot(list([float('{0:.1f}'.format(j)) for j in data2_avg]),
               label='Guttagonol Resistant population')
    pylab.xlabel(XLABEL)
    pylab.ylabel(YLABEL)
    pylab.title(TITLE_WD)
    pylab.legend()

    pylab.show()


if __name__ == "__main__":
    # Simulations
    simulationWithoutDrug(10, 500, .75, .2, 5)
    simulationWithoutDrug(100, 1000, 0.99, 0.05, 2)  # viruses grow
    simulationWithoutDrug(100, 1000, 0.1, 0.99, 2)  # viruses die

    simulationWithDrug(100, 1000, 0.2, 0.05, {PRESCRIPTION: False}, 0.005, 5)
    simulationWithDrug(80, 100, .8, 0.1, {PRESCRIPTION: True}, 0.7, 1)
    simulationWithDrug(10, 30, 1.0, 0.0, {PRESCRIPTION: True}, 1.0, 10)
    simulationWithDrug(10, 20, 1.0, 0.0, {}, 1.0, 10)