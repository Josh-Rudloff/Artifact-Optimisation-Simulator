from itertools import product

class Pruning:
    def __init__(self, filter_crit: float) -> None:
        self.filter_crit = filter_crit

    def weakly_preferred_to(self, state_a: dict, state_b: dict):
    # Returns True if state_a is weakly preferred to state_b
        better_or_equal = (
            state_a["ATK%"] >= state_b["ATK%"] and
            state_a["CRIT RATE"] >= state_b["CRIT RATE"] and
            state_a["CRIT DMG"] >= state_b["CRIT DMG"] and
            state_a["EM"] >= state_b["EM"] and
            state_a["ER"] >= state_b["ER"]
        )

        return better_or_equal
    
    def is_dominated(self, new_state: dict, combo_list: list):
        for combo in combo_list:
            if self.weakly_preferred_to(combo["state"], new_state):
                return True
        
        return False

    def total_inc_main(self, value: str, stats: tuple):
        total = 0

        if stats[0][0] == value:
            total += stats[0][1]
        total += stats[1].get(value, 0)
        
        return total
    
    def new_state_total(self, old_state: dict, new_values: dict):
        new_state = {
            "ATK%": round(old_state.get("ATK%", 0) + new_values.get("ATK%", 0), 2),
            "CRIT RATE": round(old_state.get("CRIT RATE", 0) + new_values.get("CRIT RATE", 0), 2),
            "CRIT DMG": round(old_state.get("CRIT DMG", 0) + new_values.get("CRIT DMG", 0), 2),
            "EM": round(old_state.get("EM", 0) + new_values.get("EM", 0), 2),
            "ER": round(old_state.get("ER", 0) + new_values.get("ER", 0), 2)
        }

        return new_state
    
    def new_state_total_main(self, old_state: dict, artifact: tuple):
        new_state = {
            "ATK%": round(old_state.get("ATK%", 0) +
                          self.total_inc_main("ATK%", artifact), 2),
            "CRIT RATE": round(old_state.get("CRIT RATE", 0) +
                               self.total_inc_main("CRIT RATE", artifact), 2),
            "CRIT DMG": round(old_state.get("CRIT DMG", 0) +
                              self.total_inc_main("CRIT DMG", artifact), 2),
            "EM": round(old_state.get("EM", 0) +
                        self.total_inc_main("EM", artifact), 2),
            "ER": round(old_state.get("ER", 0) +
                        self.total_inc_main("ER", artifact), 2)
        }

        return new_state
    
    def prune_dp(self, current_dp: list):
        pruned_combos = []

        for line in current_dp:
            state = line["state"]

            if not self.is_dominated(state, pruned_combos):
                pruned_combos.append(line)

        return pruned_combos
    
    def combo_tuple(self, old_combo: tuple, new_values: dict):
        combo = []

        for artifact in old_combo:
            combo.append(artifact)
        combo.append(new_values)        

        return tuple(combo)

    def create_dp(self, new_artifact: dict, pruned: list, mainstat: bool = False):
        new_dp = []

        for line in product(new_artifact, pruned):
            old_state = line[1]["state"]
            new_values = line[0]
            old_combo = line[1]["combo"]
            
            if mainstat:
                state = self.new_state_total_main(old_state, new_values)
            else:
                state = self.new_state_total(old_state, new_values)

            if state["ER"] > 80:
                continue
            if state["CRIT RATE"] > self.filter_crit:
                continue

            new_dp.append({"state": state, "combo": self.combo_tuple(old_combo, new_values)})

        return new_dp
    
    def intial_dp(self, artifact_a: dict, artifact_b: dict):
        initial_dp = []

        for line in product(artifact_a, artifact_b):
            state = self.new_state_total(line[0], line[1])

            initial_dp.append({"state": state, "combo": (line[0], line[1])})
        
        return initial_dp
