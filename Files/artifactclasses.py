from collections import Counter

class Artifact:
    def __init__(self, piece: str, mainstat: dict, substats: dict) -> None:
        self.piece = piece
        self.mainstat = mainstat
        self.substats = substats
        self.total = self.get_total()

    def __str__(self) -> str:
        return f"Type: {self.piece}\nMainstat: {self.mainstat}\nSubstats: {self.substats}"

    def get_total(self):
        total = {
            "ATK": round(self.mainstat.get("ATK", 0) + self.substats.get("ATK", 0), 2),
            "ATK%": round(self.mainstat.get("ATK%", 0) + self.substats.get("ATK%", 0), 2),
            "CRIT RATE": round(self.mainstat.get("CRIT RATE", 0) + self.substats.get("CRIT RATE", 0), 2),
            "CRIT DMG": round(self.mainstat.get("CRIT DMG", 0) + self.substats.get("CRIT DMG", 0), 2),
            "EM": round(self.mainstat.get("EM", 0) + self.substats.get("EM", 0), 2),
            "ER": round(self.mainstat.get("ER", 0) + self.substats.get("ER", 0), 2),
            "DMG BONUS": round(self.mainstat.get("DMG BONUS", 0), 2),
        }

        return total

class Loadout:
    def __init__(self, artifacts: tuple) -> None:
        self.flower = artifacts[0]
        self.feather = artifacts[1]
        self.sands = artifacts[2]
        self.goblet = artifacts[3]
        self.circlet = artifacts[4]
        self.stats = self.get_stats()

    def __str__(self) -> None:
        return f"{self.flower}\n\n{self.feather}\n\n{self.sands}\n\n{self.goblet}\n\n{self.circlet}"

    def get_stats(self):
        stats = dict(Counter(self.flower.total) +
                     Counter(self.feather.total) +
                     Counter(self.sands.total) +
                     Counter(self.goblet.total) +
                     Counter(self.circlet.total))

        return stats




if __name__ == '__main__':
    a = Artifact("flower", {'HP': 4780}, {'CRIT DMG': 20.2, 'EM': 23.31, 'ER': 18.14, 'ATK%': 9.91})
    b = Artifact('feather', {'ATK': 311}, {'EM': 23.31, 'DEF': 16.2, 'ER': 22.03, 'CRIT RATE': 6.22})
    c = Artifact('sands', {'ER': 51.8}, {'HP': 507.88, 'HP%': 16.32, 'ATK': 13.61, 'CRIT RATE': 7.0})
    d = Artifact('goblet', {'DEF%': 58.3}, {'HP': 507.88, 'ATK': 58.35, 'DEF': 23.15, 'ATK%': 4.66})
    e = Artifact('circlet', {'DEF%': 58.3}, {'ATK%': 4.08, 'ATK': 19.45, 'CRIT DMG': 31.86, 'EM': 18.65})

    test = Loadout((a,b,c,d,e))
    print(test)
    print("===============")
    print(test.stats)
