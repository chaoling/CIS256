import random
import matplotlib.pyplot as plt


class NoChildException(Exception):
    """Raised when a virus particle does not reproduce."""
    pass


class SimpleVirus:
    """
    Representation of a simple virus (no drug resistance).
    """

    def __init__(self, maxBirthProb: float, clearProb: float) -> None:
        if not 0.0 <= maxBirthProb <= 1.0:
            raise ValueError("maxBirthProb must be between 0 and 1")
        if not 0.0 <= clearProb <= 1.0:
            raise ValueError("clearProb must be between 0 and 1")
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self) -> float:
        return self.maxBirthProb

    def getClearProb(self) -> float:
        return self.clearProb

    def doesClear(self) -> bool:
        """Return True with probability clearProb."""
        return random.random() < self.clearProb

    def reproduce(self, popDensity: float) -> "SimpleVirus":
        """
        Return a new SimpleVirus instance with probability
        maxBirthProb * (1 - popDensity), else raise NoChildException.
        """
        birth_prob = self.maxBirthProb * (1 - popDensity)
        birth_prob = max(0.0, min(birth_prob, 1.0))
        if random.random() < birth_prob:
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException()


class Patient:
    """
    Representation of a patient with a population of SimpleVirus particles.
    """

    def __init__(self, viruses: list, maxPop: int) -> None:
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self) -> list:
        return self.viruses

    def getMaxPop(self) -> int:
        return self.maxPop

    def getTotalPop(self) -> int:
        return len(self.viruses)

    def update(self) -> int:
        """
        Simulate one time step:
          1) Remove cleared viruses
          2) Compute population density
          3) Survivors reproduce
        Returns updated population size.
        """
        # Remove cleared
        self.viruses = [v for v in self.viruses if not v.doesClear()]
        # Compute density
        popDensity = self.getTotalPop() / self.getMaxPop()
        # Reproduce
        offspring = []
        for v in self.viruses:
            try:
                child = v.reproduce(popDensity)
                offspring.append(child)
            except NoChildException:
                pass
        self.viruses.extend(offspring)
        return self.getTotalPop()


def simulationWithoutDrug(
    numViruses: int,
    maxPop: int,
    maxBirthProb: float,
    clearProb: float,
    numTrials: int,
    timeSteps: int = 300
) -> list:
    """
    Run numTrials of SimpleVirus/Patient simulation without drugs,
    return and plot average population over timeSteps.
    """
    totals = [0] * timeSteps
    for _ in range(numTrials):
        patient = Patient(
            [SimpleVirus(maxBirthProb, clearProb) for _ in range(numViruses)],
            maxPop
        )
        for t in range(timeSteps):
            totals[t] += patient.update()
    avgPop = [count / numTrials for count in totals]
    # Plot
    plt.plot(avgPop, label="Avg Virus (no drug)")
    plt.title("SimpleVirus Simulation (No Drug)")
    plt.xlabel("Time Steps")
    plt.ylabel("Average Population")
    plt.legend(loc="best")
    plt.show()
    return avgPop


class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(
        self,
        maxBirthProb: float,
        clearProb: float,
        resistances: dict,
        mutProb: float
    ) -> None:
        super().__init__(maxBirthProb, clearProb)
        if not 0.0 <= mutProb <= 1.0:
            raise ValueError("mutProb must be between 0 and 1")
        self.resistances = resistances.copy()
        self.mutProb = mutProb

    def getResistances(self) -> dict:
        return self.resistances.copy()

    def getMutProb(self) -> float:
        return self.mutProb

    def isResistantTo(self, drug: str) -> bool:
        return self.resistances.get(drug, False)

    def reproduce(self, popDensity: float, activeDrugs: list) -> "ResistantVirus":
        """
        Reproduce only if resistant to all activeDrugs, with probability
        maxBirthProb * (1 - popDensity). Offspring flips each resistance
        trait with probability mutProb.
        """
        if not all(self.isResistantTo(d) for d in activeDrugs):
            raise NoChildException()
        birth_prob = self.maxBirthProb * (1 - popDensity)
        birth_prob = max(0.0, min(birth_prob, 1.0))
        if random.random() < birth_prob:
            new_res = {}
            for drug, res in self.resistances.items():
                if random.random() < self.mutProb:
                    new_res[drug] = not res
                else:
                    new_res[drug] = res
            return ResistantVirus(
                self.maxBirthProb,
                self.clearProb,
                new_res,
                self.mutProb
            )
        else:
            raise NoChildException()


class TreatedPatient(Patient):
    """
    Representation of a patient that can take drugs and develop resistance.
    """

    def __init__(self, viruses: list, maxPop: int) -> None:
        super().__init__(viruses, maxPop)
        self.drugsAdministered = []

    def addPrescription(self, drug: str) -> None:
        if drug not in self.drugsAdministered:
            self.drugsAdministered.append(drug)

    def getPrescriptions(self) -> list:
        return list(self.drugsAdministered)

    def getResistPop(self, drugResist: list) -> int:
        return sum(
            1 for v in self.viruses
            if all(v.isResistantTo(d) for d in drugResist)
        )

    def update(self) -> int:
        # Remove cleared
        self.viruses = [v for v in self.viruses if not v.doesClear()]
        popDensity = self.getTotalPop() / self.getMaxPop()
        # Reproduce with drug check
        offspring = []
        for v in self.viruses:
            try:
                child = v.reproduce(popDensity, self.getPrescriptions())
                offspring.append(child)
            except NoChildException:
                pass
        self.viruses.extend(offspring)
        return self.getTotalPop()


def simulationWithDrug(
    numViruses: int,
    maxPop: int,
    maxBirthProb: float,
    clearProb: float,
    resistances: dict,
    mutProb: float,
    numTrials: int,
    timeSteps: int = 150
) -> tuple:
    """
    Run numTrials of ResistantVirus/TreatedPatient sim:
      - Phase1 (no drug): timeSteps
      - Add 'guttagonol'
      - Phase2: timeSteps
    Returns avg total & avg resistant populations.
    """
    total_steps = 2 * timeSteps
    totals = [0] * total_steps
    resists = [0] * total_steps
    for _ in range(numTrials):
        patient = TreatedPatient(
            [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
             for _ in range(numViruses)],
            maxPop
        )
        # Phase1
        for t in range(timeSteps):
            totals[t] += patient.update()
            resists[t] += patient.getResistPop(patient.getPrescriptions())
        patient.addPrescription('guttagonol')
        # Phase2
        for t in range(timeSteps):
            idx = t + timeSteps
            totals[idx] += patient.update()
            resists[idx] += patient.getResistPop(patient.getPrescriptions())
    avgTotals = [c / numTrials for c in totals]
    avgResists = [c / numTrials for c in resists]
    # Plot
    plt.plot(avgTotals, label="Avg Total Population")
    plt.plot(avgResists, label="Avg Resistant Population")
    plt.title("ResistantVirus Simulation (With Drug)")
    plt.xlabel("Time Steps")
    plt.ylabel("Average Population")
    plt.legend(loc="best")
    plt.show()
    return avgTotals, avgResists

if __name__ == "__main__":
    random.seed(0)
    print("Running simulation...")
    v1 = SimpleVirus(0.97, 0.28)
    p1 = Patient([v1], 100)
    for _ in range(100):
        p1.update()
    print("Final population (no drug single trial):", p1.getTotalPop())
    simulationWithoutDrug(100, 1000, 0.1, 0.05, 10)
    simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 10)
    print("Simulation complete.")
    print("Check plots for results.")
    print("Done.")