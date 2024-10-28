from itertools import product
import numpy as np
import random
from artifactclasses import Artifact

#random.seed(1)
#np.random.seed(1)

class ArtifactGenerator:
    def __init__(self) -> None:
        self.roll_combos = {
            4: self.get_roll_combinations(4),
            5: self.get_roll_combinations(5)
        }
        self.roll_multipliers = [1, 0.9, 0.8, 0.7]
        self.max_rolls = {
            "HP": 298.75,
            "ATK": 19.45,
            "DEF": 23.15,
            "HP%": 5.83,
            "ATK%": 5.83,
            "DEF%": 7.29,
            "EM": 23.31,
            "ER": 6.48,
            "CRIT RATE": 3.89,
            "CRIT DMG": 7.77
            }
        self.substat_weights = {
            "HP": 6,
            "ATK": 6,
            "DEF": 6,
            "HP%": 4,
            "ATK%": 4,
            "DEF%": 4,
            "ER": 4,
            "EM": 4,
            "CRIT RATE": 3,
            "CRIT DMG": 3
            }
        self.mainstat_probabilities = {
            "flower" : {"HP": 1},
            "feather": {"ATK": 1},
            "sands": {"HP%": 26.68,
                      "ATK%": 26.66,
                      "DEF%": 26.66,
                      "ER": 10.00,
                      "EM": 10.00},
            "goblet": {"HP%": 19.25,
                       "ATK%": 19.25,
                       "DEF%": 19.00,
                       "DMG BONUS": 5.00,
                       "WRONG BONUS": 35.00,
                       "EM": 2.50},
            "circlet": {"HP%": 22,
                        "ATK%": 22,
                        "DEF%": 22,
                        "CRIT RATE": 10,
                        "CRIT DMG": 10,
                        "HEAL BONUS": 10,
                        "EM": 4}
        }
        self.mainstat_values = {
            "HP": 4780,
            "ATK": 311,
            "HP%": 46.6,
            "ATK%": 46.6,
            "DEF%": 58.3,
            "EM": 186.5,
            "ER": 51.8,
            "DMG BONUS": 46.6,
            "CRIT RATE": 31.1,
            "CRIT DMG": 62.2,
            "HEAL BONUS": 35.9,
            "WRONG BONUS": 0
        }

    def get_roll_combinations(self, num_rolls: int):
            # Returns possible substat roll allocations e.g. (1,0,3,1,)
            roll_combinations = []

            for roll in product(range(6), repeat = 4):
                if sum(roll) == num_rolls:
                    roll_combinations.append(roll)

            return roll_combinations

    def num_of_rolls(self):
        return random.choices(population = [4, 5], weights = [80, 20], k = 1)[0]

    def get_substat_mult(self):
        num_of_rolls = self.num_of_rolls()
        roll_combo = np.array(random.choice(self.roll_combos[num_of_rolls]))
        #print(roll_combo)

        substat_mult = [
            sum(np.random.choice(self.roll_multipliers, size = roll + 1))
            for roll in roll_combo
        ]
        
        return np.array(substat_mult)
    
    def get_substat_probabilities(self, available_substats):
        total_weight = sum(self.substat_weights[substat] for substat in available_substats)

        substat_probabilites = {
            substat: (self.substat_weights[substat] / total_weight) for substat in available_substats
        }

        return substat_probabilites
    
    def choose_new_substat(self, mainstat: str, current_substats: list):
        available_substats = [
            substat for substat in self.substat_weights
            if substat not in current_substats and substat != mainstat
        ]

        substat_probabilities = self.get_substat_probabilities(available_substats)
        new_substat = random.choices(population = available_substats, weights = substat_probabilities.values(), k = 1)

        return new_substat[0]

    def generate_substats(self, mainstat: str):
        substats = []

        for i in range(4):
            new_substat = self.choose_new_substat(mainstat, substats)
            substats.append(new_substat)

        return substats

    def roll_substats(self, substats: list, substat_mult: np.array):
        rolled_substats = {}

        for index, substat in enumerate(substats):
            rolled_substats[substat] = round(substat_mult[index] * self.max_rolls[substat], 2)

        return rolled_substats

    def choose_artifact(self):
        artifact = random.choice(["flower", "feather", "sands", "goblet", "circlet"])

        return artifact

    def generate_mainstat(self, artifact: str):
        available_mainstats = list(self.mainstat_probabilities[artifact].keys())
        mainstat_weights = list(self.mainstat_probabilities[artifact].values())

        mainstat = random.choices(population = available_mainstats, weights = mainstat_weights, k = 1)

        return mainstat[0]

    def generate_artifact(self):
        piece = self.choose_artifact()
        #print(piece)
        mainstat = self.generate_mainstat(piece)
        #print(mainstat)
        substats = self.generate_substats(mainstat)
        #print(substats)
        substat_mult = self.get_substat_mult()
        #print(substat_mult)
        rolled_substats = self.roll_substats(substats, substat_mult)
        #print(rolled_substats)
        mainstat_value = self.mainstat_values[mainstat]
        
        return (piece, {mainstat: mainstat_value}, rolled_substats)

    def weakly_preferred_to(self, artifact_a: dict, artifact_b: dict):
    # Returns True if state_a is weakly preferred to state_b
        better_or_equal = (
            artifact_a.get("ATK", 0) >= artifact_b.get("ATK", 0) and
            artifact_a.get("ATK%", 0) >= artifact_b.get("ATK%", 0) and
            artifact_a.get("CRIT RATE", 0) >= artifact_b.get("CRIT RATE", 0) and
            artifact_a.get("CRIT DMG", 0) >= artifact_b.get("CRIT DMG", 0) and
            artifact_a.get("EM", 0) >= artifact_b.get("EM", 0) and
            artifact_a.get("ER", 0) >= artifact_b.get("ER", 0) and
            artifact_a.get("DMG BONUS", 0) >= artifact_b.get("DMG BONUS", 0)
        )

        return better_or_equal
    
    def artifact_is_dominated(self, new_artifact: Artifact, artifact_list: list):
        for artifact in artifact_list:
            if self.weakly_preferred_to(artifact.total, new_artifact.total):
                return True
        
        return False



if __name__ == "__main__":
    ag = ArtifactGenerator()

    """rolls_5 = ag.get_roll_combinations(5)
    rolls_4 = ag.get_roll_combinations(4)

    substat_mult = ag.get_substat_mult()
    print(substat_mult)

    substats = ag.generate_substats("ATK")
    print(substats)

    rolled_substats = ag.roll_substats(substats, substat_mult)
    print(rolled_substats)

    piece = ag.choose_artifact()
    print(piece)

    mainstat = ag.generate_mainstat(piece)
    print(mainstat)"""

    print(ag.generate_artifact())

