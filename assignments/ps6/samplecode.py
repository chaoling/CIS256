import random
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt


class NoChildException(Exception):
    """Raised when a virus particle does not reproduce."""
    pass


class SimpleVirus:
    """
    Representation of a simple virus (no drug resistance).
    """

    def __init__(self, max_birth_prob: float, clear_prob: float):
        if not 0.0 <= max_birth_prob <= 1.0:
            raise ValueError("max_birth_prob must be between 0 and 1")
        if not 0.0 <= clear_prob <= 1.0:
            raise ValueError("clear_prob must be between 0 and 1")

        self.max_birth_prob = max_birth_prob
        self.clear_prob = clear_prob

    def get_max_birth_prob(self) -> float:
        return self.max_birth_prob

    def get_clear_prob(self) -> float:
        return self.clear_prob

    def does_clear(self) -> bool:
        """Return True with probability clear_prob, else False."""
        return random.random() < self.clear_prob

    def reproduce(self, pop_density: float) -> "SimpleVirus":
        """
        Attempt to reproduce this virus with probability:
          max_birth_prob * (1 - pop_density).
        Returns a new SimpleVirus on success, else raises NoChildException.
        """
        birth_prob = self.max_birth_prob * (1 - pop_density)
        birth_prob = max(0.0, min(birth_prob, 1.0))

        if random.random() < birth_prob:
            return SimpleVirus(self.max_birth_prob, self.clear_prob)
        else:
            raise NoChildException()


class Patient:
    """
    Representation of a patient with a population of SimpleVirus particles.
    """

    def __init__(self, viruses: List[SimpleVirus], max_pop: int):
        self.viruses = viruses
        self.max_pop = max_pop

    def get_viruses(self) -> List[SimpleVirus]:
        return self.viruses

    def get_max_pop(self) -> int:
        return self.max_pop

    def get_total_pop(self) -> int:
        return len(self.viruses)

    def update(self) -> int:
        """
        Simulate one time step:
          1. Remove cleared viruses in-place
          2. Compute population density
          3. Survivors reproduce and append offspring in-place
        Returns the updated total virus population.
        """
        # 1) Remove cleared viruses by iterating over a copy
        for virus in self.viruses[:]:
            if virus.does_clear():
                self.viruses.remove(virus)

        # 2) Recompute population density
        pop_density = self.get_total_pop() / self.get_max_pop()

        # 3) Survivors reproduce and append offspring
        for virus in self.viruses[:]:
            try:
                child = virus.reproduce(pop_density)
                self.viruses.append(child)
            except NoChildException:
                continue

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
    Runs num_trials of the SimpleVirus/Patient simulation without drugs for time_steps,
    and returns the average virus population at each time step.
    """
    totals = [0] * time_steps

    for _ in range(num_trials):
        viruses = [SimpleVirus(max_birth_prob, clear_prob) for _ in range(num_viruses)]
        patient = Patient(viruses, max_pop)

        for t in range(time_steps):
            patient.update()
            totals[t] += patient.get_total_pop()

    avg_pop = [total / num_trials for total in totals]

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(avg_pop, label="Avg Virus Population")
    ax.set(
        title="SimpleVirus Simulation (no drug)",
        xlabel="Time Steps",
        ylabel="Average Population"
    )
    ax.legend()
    plt.show()

    return avg_pop


class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(
        self,
        max_birth_prob: float,
        clear_prob: float,
        resistances: Dict[str, bool],
        mut_prob: float
    ):
        super().__init__(max_birth_prob, clear_prob)
        if not 0.0 <= mut_prob <= 1.0:
            raise ValueError("mut_prob must be between 0 and 1")

        self.resistances = resistances.copy()
        self.mut_prob = mut_prob

    def get_resistances(self) -> Dict[str, bool]:
        return self.resistances.copy()

    def get_mut_prob(self) -> float:
        return self.mut_prob

    def is_resistant_to(self, drug: str) -> bool:
        return self.resistances.get(drug, False)

    def reproduce(
        self,
        pop_density: float,
        active_drugs: List[str]
    ) -> "ResistantVirus":
        """
        Reproduce only if resistant to all active_drugs, with probability
        max_birth_prob * (1 - pop_density). Offspring resistances flip each trait
        with probability mut_prob.
        """
        # 1) Must be resistant to every active drug
        if not all(self.is_resistant_to(d) for d in active_drugs):
            raise NoChildException()

        # 2) Reproduction probability
        birth_prob = self.max_birth_prob * (1 - pop_density)
        birth_prob = max(0.0, min(birth_prob, 1.0))

        if random.random() >= birth_prob:
            raise NoChildException()

        # 3) Build offspring resistances
        new_resistances: Dict[str, bool] = {}
        for drug, parent_resistant in self.resistances.items():
            if random.random() < self.mut_prob:
                new_resistances[drug] = not parent_resistant
            else:
                new_resistances[drug] = parent_resistant

        return ResistantVirus(
            self.max_birth_prob,
            self.clear_prob,
            new_resistances,
            self.mut_prob
        )


class TreatedPatient(Patient):
    """
    Patient that can take drugs and whose viruses can evolve resistance.
    """

    def __init__(self, viruses: List[ResistantVirus], max_pop: int):
        super().__init__(viruses, max_pop)
        self.drugs_administered: List[str] = []

    def add_prescription(self, drug: str) -> None:
        """Administer a new drug (if not already)."""
        if drug not in self.drugs_administered:
            self.drugs_administered.append(drug)

    def get_prescriptions(self) -> List[str]:
        return list(self.drugs_administered)

    def get_resist_pop(self, drug_resist: List[str]) -> int:
        """
        Count viruses resistant to all drugs in drug_resist.
        """
        return sum(
            1 for v in self.viruses
            if all(v.is_resistant_to(d) for d in drug_resist)
        )

    def update(self) -> int:
        """
        Simulate one time step with drug effects:
          1. Remove cleared viruses in-place
          2. Compute population density
          3. Survivors reproduce (accounting for current prescriptions) and append offspring
        """
        # 1) Remove cleared viruses
        for virus in self.viruses[:]:
            if virus.does_clear():
                self.viruses.remove(virus)

        # 2) Recompute population density
        pop_density = self.get_total_pop() / self.get_max_pop()

        # 3) Survivors reproduce under current prescriptions
        for virus in self.viruses[:]:
            try:
                child = virus.reproduce(pop_density, self.drugs_administered)
                self.viruses.append(child)
            except NoChildException:
                continue

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
    Runs num_trials of the ResistantVirus/TreatedPatient simulation for
    time_steps, then adds 'guttagonol' and runs for another time_steps.
    Returns two lists: average total population and average resistant population.
    """
    total_counts = [0] * (2 * time_steps)
    resist_counts = [0] * (2 * time_steps)

    for _ in range(num_trials):
        viruses = [
            ResistantVirus(max_birth_prob, clear_prob, resistances, mut_prob)
            for _ in range(num_viruses)
        ]
        patient = TreatedPatient(viruses, max_pop)

        # Phase 1: before drug
        for t in range(time_steps):
            patient.update()
            total_counts[t] += patient.get_total_pop()
            resist_counts[t] += patient.get_resist_pop(patient.get_prescriptions())

        # Add drug
        patient.add_prescription('guttagonol')

        # Phase 2: after drug
        for t in range(time_steps):
            patient.update()
            idx = t + time_steps
            total_counts[idx] += patient.get_total_pop()
            resist_counts[idx] += patient.get_resist_pop(patient.get_prescriptions())

    avg_total = [c / num_trials for c in total_counts]
    avg_resist = [c / num_trials for c in resist_counts]

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(avg_total, label="Avg Total Population")
    ax.plot(avg_resist, label="Avg Resistant Population")
    ax.set(
        title="ResistantVirus Simulation (with drug)",
        xlabel="Time Steps",
        ylabel="Average Population"
    )
    ax.legend()
    plt.show()

    return avg_total, avg_resist


if __name__ == "__main__":
    simulation_without_drug(
        num_viruses=100,
        max_pop=1000,
        max_birth_prob=0.1,
        clear_prob=0.05,
        num_trials=100
    )
    simulation_with_drug(
        num_viruses=100,
        max_pop=1000,
        max_birth_prob=0.8,
        clear_prob=0.1,
        resistances={'guttagonol': True},
        mut_prob=0.8,
        num_trials=100
    )
