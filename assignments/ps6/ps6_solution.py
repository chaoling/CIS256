import random
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt

class NoChildException(Exception):
    """Raised when a virus particle does not reproduce."""
    pass

class SimpleVirus:
    """Representation of a simple virus without drug resistance."""
    def __init__(self, max_birth_prob: float, clear_prob: float) -> None:
        if not 0.0 <= max_birth_prob <= 1.0:
            raise ValueError("max_birth_prob must be between 0 and 1")
        if not 0.0 <= clear_prob <= 1.0:
            raise ValueError("clear_prob must be between 0 and 1")
        self.max_birth_prob = max_birth_prob
        self.clear_prob = clear_prob

    def does_clear(self) -> bool:
        """Return True with probability clear_prob."""
        return random.random() < self.clear_prob

    def reproduce(self, pop_density: float) -> "SimpleVirus":
        """
        Return a new SimpleVirus offspring with probability
        max_birth_prob * (1 - pop_density), else raise NoChildException.
        """
        birth_prob = self.max_birth_prob * (1 - pop_density)
        birth_prob = max(0.0, min(birth_prob, 1.0))
        if random.random() < birth_prob:
            return SimpleVirus(self.max_birth_prob, self.clear_prob)
        else:
            raise NoChildException()

class Patient:
    """Representation of a patient with a population of SimpleVirus particles."""
    def __init__(self, viruses: List[SimpleVirus], max_pop: int) -> None:
        self.viruses = viruses
        self.max_pop = max_pop

    def get_total_pop(self) -> int:
        """Return current virus population size."""
        return len(self.viruses)

    def update(self) -> int:
        """
        Simulate one time step:
          1) Remove cleared viruses
          2) Compute population density
          3) Survivors reproduce
        Returns updated population size.
        """
        # 1) Remove cleared
        self.viruses = [v for v in self.viruses if not v.does_clear()]

        # 2) Density
        pop_density = self.get_total_pop() / self.max_pop

        # 3) Reproduce
        offspring = []
        for v in self.viruses:
            try:
                offspring.append(v.reproduce(pop_density))
            except NoChildException:
                continue
        self.viruses.extend(offspring)

        return self.get_total_pop()

def simulation_without_drug(
    num_viruses: int,
    max_pop: int,
    max_birth_prob: float,
    clear_prob: float,
    num_trials: int,
    time_steps: int = 300
) -> List[float]:
    """
    Run num_trials of the SimpleVirus/Patient simulation without drugs,
    return and plot the average virus population over time_steps.
    """
    totals = [0] * time_steps
    for _ in range(num_trials):
        patient = Patient(
            [SimpleVirus(max_birth_prob, clear_prob) for _ in range(num_viruses)],
            max_pop
        )
        for t in range(time_steps):
            patient.update()
            totals[t] += patient.get_total_pop()

    avg_pop = [count / num_trials for count in totals]

    # Plot
    fig, ax = plt.subplots()
    ax.plot(avg_pop, label="Avg Virus Population (No Drug)")
    ax.set(title="SimpleVirus Simulation (No Drug)",
           xlabel="Time Steps",
           ylabel="Average Population")
    ax.legend()
    plt.show()

    return avg_pop

class ResistantVirus(SimpleVirus):
    """Representation of a virus with drug resistance."""
    def __init__(
        self,
        max_birth_prob: float,
        clear_prob: float,
        resistances: Dict[str, bool],
        mut_prob: float
    ) -> None:
        super().__init__(max_birth_prob, clear_prob)
        if not 0.0 <= mut_prob <= 1.0:
            raise ValueError("mut_prob must be between 0 and 1")
        self.resistances = resistances.copy()
        self.mut_prob = mut_prob

    def is_resistant_to(self, drug: str) -> bool:
        """Return True if resistant to the given drug."""
        return self.resistances.get(drug, False)

    def reproduce(
        self,
        pop_density: float,
        active_drugs: List[str]
    ) -> "ResistantVirus":
        """
        Reproduce only if resistant to all active_drugs, with probability
        max_birth_prob * (1 - pop_density). Offspring flips each resistance
        trait with probability mut_prob.
        """
        if not all(self.is_resistant_to(d) for d in active_drugs):
            raise NoChildException()

        birth_prob = self.max_birth_prob * (1 - pop_density)
        birth_prob = max(0.0, min(birth_prob, 1.0))
        if random.random() < birth_prob:
            new_resistances = {}
            for drug, res in self.resistances.items():
                if random.random() < self.mut_prob:
                    new_resistances[drug] = not res
                else:
                    new_resistances[drug] = res
            return ResistantVirus(
                self.max_birth_prob,
                self.clear_prob,
                new_resistances,
                self.mut_prob
            )
        else:
            raise NoChildException()

class TreatedPatient(Patient):
    """Representation of a patient that can take drugs."""
    def __init__(self, viruses: List[ResistantVirus], max_pop: int) -> None:
        super().__init__(viruses, max_pop)
        self.drugs_administered: List[str] = []

    def add_prescription(self, drug: str) -> None:
        """Administer a drug to the patient."""
        if drug not in self.drugs_administered:
            self.drugs_administered.append(drug)

    def get_prescriptions(self) -> List[str]:
        """Return current list of administered drugs."""
        return list(self.drugs_administered)

    def get_resist_pop(self, drug_resist: List[str]) -> int:
        """Count viruses resistant to all drugs in drug_resist."""
        return sum(1 for v in self.viruses
                   if all(v.is_resistant_to(d) for d in drug_resist))

    def update(self) -> int:
        """
        Simulate one time step with drugs:
          1) Remove cleared viruses
          2) Compute pop density
          3) Survivors reproduce with resistance check
        """
        self.viruses = [v for v in self.viruses if not v.does_clear()]
        pop_density = self.get_total_pop() / self.max_pop

        offspring = []
        for v in self.viruses:
            try:
                offspring.append(v.reproduce(pop_density,
                    self.drugs_administered))
            except NoChildException:
                continue
        self.viruses.extend(offspring)
        return self.get_total_pop()

def simulation_with_drug(
    num_viruses: int,
    max_pop: int,
    max_birth_prob: float,
    clear_prob: float,
    resistances: Dict[str, bool],
    mut_prob: float,
    num_trials: int,
    time_steps: int = 150
) -> Tuple[List[float], List[float]]:
    """
    Run num_trials of ResistantVirus/TreatedPatient simulation:
    - phase 1 (no drug): time_steps
    - add 'guttagonol'
    - phase 2: time_steps
    Returns and plots avg total & avg resistant populations.
    """
    total_counts = [0] * (2 * time_steps)
    resist_counts = [0] * (2 * time_steps)

    for _ in range(num_trials):
        patient = TreatedPatient(
            [ResistantVirus(max_birth_prob, clear_prob,
                            resistances, mut_prob)
             for _ in range(num_viruses)],
            max_pop
        )
        # phase 1
        for t in range(time_steps):
            patient.update()
            total_counts[t] += patient.get_total_pop()
            resist_counts[t] += patient.get_resist_pop(
                patient.get_prescriptions())
        # add drug
        patient.add_prescription('guttagonol')
        # phase 2
        for t in range(time_steps):
            idx = t + time_steps
            patient.update()
            total_counts[idx] += patient.get_total_pop()
            resist_counts[idx] += patient.get_resist_pop(
                patient.get_prescriptions())

    avg_total = [c / num_trials for c in total_counts]
    avg_resist = [c / num_trials for c in resist_counts]

    # Plot
    fig, ax = plt.subplots()
    ax.plot(avg_total, label="Avg Total Population")
    ax.plot(avg_resist, label="Avg Resistant Population")
    ax.set(title="ResistantVirus Simulation (with drug)",
           xlabel="Time Steps", ylabel="Average Population")
    ax.legend()
    plt.show()

    return avg_total, avg_resist

if __name__ == "__main__":
    random.seed(0)
    simulation_without_drug(100, 1000, 0.1, 0.05, 100)
    simulation_with_drug(100, 1000, 0.8, 0.1,
                         {'guttagonol': False}, 0.005, 100)
