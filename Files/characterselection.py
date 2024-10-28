from collections import Counter

class CharacterSelection:
    def __init__(self) -> None:
        #self.base_stats = Counter(Character.characters[character]) + Counter(Character.weapons[weapon])
        self.characters = {
        "tartaglia": {"Base ATK": 280.18, "Ability": 681.12, "DMG BONUS": 28.8, "CRIT RATE": 5, "CRIT DMG": 50, "EM": 0},
        "xiangling": {"Base ATK": 209.55, "Ability": 238, "DMG BONUS": 0, "CRIT RATE": 5, "CRIT DMG": 50, "EM": 96}
        }
        self.weapons = {
            "skyward harp": {"Base ATK": 674, "CRIT RATE": 22.1, "CRIT DMG": 20},
            "the catch": {"Base ATK": 510, "ER": 45.9, "DMG BONUS": 32, "CRIT RATE": 12}
        }
        self.artifacts = {
            "heart of depth": {"DMG BONUS": 15},
            "emblem of severed fate": {"ER": 20}
        }


    def get_base_stats(self):
        character = input("Please select a character: ").lower()
        weapon = input("Please select a weapon: ").lower()
        artifact_set = input("Please select an artifact set: ").lower()
        reaction = input("Please select amplifying reaction: ").lower()

        base_stats = dict(Counter(self.characters[character]) + 
                          Counter(self.weapons[weapon]) + 
                          Counter(self.artifacts[artifact_set])) 
        base_stats["Reaction"] = reaction

        return (base_stats, artifact_set)


if __name__ == '__main__':
    test = CharacterSelection()

    stats = test.get_base_stats()

    print(stats)


