from itertools import combinations, product

class ArtifactCombos:
    def __init__(self) -> None:
        self.possible_substats = list(combinations(["ATK%",
                                                    "EM",
                                                    "ER",
                                                    "CRIT RATE",
                                                    "CRIT DMG"], 4))
        self.sands_mainstats = [("ATK%", 46.6), ("EM", 186.5), ("ER", 51.8)]
        self.circlet_mainstats = [("CRIT RATE", 31.1), ("CRIT DMG", 62.2)]
        self.max_sub = {"ATK": 19.45,
                        "ATK%": 5.83,
                        "EM": 23.31,
                        "ER": 6.48,
                        "CRIT RATE": 3.89,
                        "CRIT DMG": 7.77}
        self.roll_combinations = self.get_roll_combinations()

    def get_roll_combinations(self):
        # Returns possible substat roll allocations e.g. (1,0,3,1,)
        roll_combinations = []

        for roll in product(range(6), repeat = 4):
            if sum(roll) == 5:
                roll_combinations.append(roll)

        return roll_combinations

    def roll_artifact(self):
        # Returns cartesian product of substats and roll possibilities
        rolled_substats = []

        for row in product(self.roll_combinations, self.possible_substats):
            rolled = {}
            for i, stat_name in enumerate(row[1]):
                rolled[stat_name] = round((row[0][i] + 1) * self.max_sub[stat_name], 2)
            rolled_substats.append(rolled)
        
        return rolled_substats

    def crit_value_check(self, substats: dict, floor: int):
        crit_rate = substats.get("CRIT RATE", 0)
        crit_dmg = substats.get("CRIT DMG", 0)
        crit_value = crit_rate * 2 + crit_dmg

        if crit_value > floor:
            return True
        return False

    def filter_artifacts(self, rolled_artifact: list, mainstat: bool = False, floor: int = 40):
        # Removes combinations below given crit floor, considers only substats
        artifact_filtered = []

        for line in rolled_artifact:
            if mainstat:
                substats = line[1]
            else:
                substats = line

            if self.crit_value_check(substats, floor):
                artifact_filtered.append(line)

        return artifact_filtered

    def add_mainstats(self, substats: list, type: str):
        artifact_complete = []

        if type == "sands":
            mainstats = self.sands_mainstats
        else:
            mainstats = self.circlet_mainstats

        for line in product(mainstats, substats):
            if line[0][0] not in line[1]:
                artifact_complete.append(line)
        
        return artifact_complete

    def filtered_combos(self, type: str):
        rolled = self.roll_artifact()

        if type == "sands":
            complete = self.add_mainstats(rolled, type)
            filtered = self.filter_artifacts(complete, True)
        elif type == "circlet":
            complete = self.add_mainstats(rolled, type)
            filtered = self.filter_artifacts(complete, True, 20)
        else:
            filtered = self.filter_artifacts(rolled)

        return filtered


if __name__ == "__main__":
    test = ArtifactCombos()

    flower_test = test.filtered_combos("flower")
    feather_test = test.filtered_combos("feather")
    sands_test = test.filtered_combos("sands")
    goblet_test = test.filtered_combos("goblet")
    circlet_test = test.filtered_combos("circlet")

    print(len(flower_test))
    print(flower_test[0])

    print(len(feather_test))
    print(feather_test[0])

    print(len(sands_test))
    print(sands_test[0])

    print(len(goblet_test))
    print(goblet_test[0])

    print(len(circlet_test))
    print(circlet_test[0])