from artifactgeneration import ArtifactGenerator
import random
from artifactclasses import Artifact, Loadout
from heapq import heappush, heappushpop
from damagecalculator_v2 import DamageCalculatorV2
from itertools import product

ag = ArtifactGenerator()

class MonteCarloSim:
    def __init__(self, base_stats: dict, set: str) -> None:
        self.artifact_pool = {
            "flower": [Artifact("flower", {}, {})],
            "feather": [Artifact("feather", {}, {})],
            "sands": [Artifact("sands", {}, {})],
            "goblet": [Artifact("goblet", {}, {})],
            "circlet": [Artifact("circlet", {}, {})]
            }
        self.dc_v2 = DamageCalculatorV2(base_stats, set)

    def calc_the_damage(self, combo: tuple):
        loadout = Loadout(combo)
        damage, amp_damage, critical, avg_damage = self.dc_v2.calc_damage(loadout.stats)

        return (avg_damage, loadout)

    def trim_pools(self, top_10):
        new_artifact_pool = {"flower": [], "feather": [], "sands": [], "goblet": [], "circlet": []}

        for avg_damage, loadout in top_10:
            if loadout.flower not in new_artifact_pool["flower"]:
                new_artifact_pool["flower"].append(loadout.flower)
            if loadout.feather not in new_artifact_pool["feather"]:
                new_artifact_pool["feather"].append(loadout.feather)
            if loadout.sands not in new_artifact_pool["sands"]:
                new_artifact_pool["sands"].append(loadout.sands)
            if loadout.goblet not in new_artifact_pool["goblet"]:
                new_artifact_pool["goblet"].append(loadout.goblet)
            if loadout.circlet not in new_artifact_pool["circlet"]:
                new_artifact_pool["circlet"].append(loadout.circlet)
 
        self.artifact_pool = new_artifact_pool

    def get_top_builds(self):
        top_10 = []

        for combo in product(self.artifact_pool["flower"],
                            self.artifact_pool["feather"],
                            self.artifact_pool["sands"],
                            self.artifact_pool["goblet"],
                            self.artifact_pool["circlet"]):
            avg_damage, loadout = self.calc_the_damage(combo)

            if len(top_10) < 10:
                heappush(top_10, (avg_damage, loadout))
            else:
                heappushpop(top_10, (avg_damage, loadout))
        
        return sorted(top_10)
    
    def run_domain(self):
        changes_made = False
        # 2 or 1 artifacts, 0.065 to 0.935
        extra_artifact = random.choices(population = [2, 1], weights = [0.935, 0.935])[0]
        # Run set number of times
        for i in range(extra_artifact):
            # 50-50 whether correct set
            wrong_set = random.choice([True, False])
            if wrong_set:
                continue

            new_artifact = Artifact(*ag.generate_artifact())

            if ag.artifact_is_dominated(new_artifact, self.artifact_pool[new_artifact.piece]):
                continue
            
            self.artifact_pool[new_artifact.piece] = [a for a in self.artifact_pool[new_artifact.piece]
                                                if not ag.weakly_preferred_to(new_artifact.total, a.total)]
            self.artifact_pool[new_artifact.piece].append(new_artifact)

            changes_made = True
        
        return changes_made
