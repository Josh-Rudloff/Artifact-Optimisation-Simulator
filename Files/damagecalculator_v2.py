class DamageCalculatorV2:

    def __init__(self, base_stats: dict, artifact_set: str) -> None:
        self.base_atk = base_stats["Base ATK"]
        self.ability = base_stats["Ability"]
        self.dmg_bonus = base_stats["DMG BONUS"]
        self.crit_rate = base_stats["CRIT RATE"]
        self.crit_dmg = base_stats["CRIT DMG"]
        self.em = base_stats.get("EM", 0)
        self.react_mult = {"vaporise": 2, "reverse vaporise": 1.5,
                           "melt": 2, "reverse melt": 1.5}
        self.reaction = base_stats["Reaction"]
        self.artifact_set = artifact_set
        self.base_er = base_stats.get("ER", 0)

    def get_dmg_bonus(self, artifact_stats: dict):
        dmg_bonus = self.dmg_bonus + artifact_stats.get("DMG BONUS", 0)

        if self.artifact_set == "emblem of severed fate":
            er = self.base_er + artifact_stats.get("ER", 0) + 100
            dmg_bonus += 0.25 * er      
            
        return (1 + dmg_bonus / 100)

    def get_base_dmg(self, artifact_stats: dict):
        atk_mult = artifact_stats.get("ATK%", 0)
        atk_flat = artifact_stats.get("ATK", 0)
        ability = self.ability

        atk = (self.base_atk * (1 + atk_mult/100)) + atk_flat
        base_damage = (ability / 100) * atk

        return round(base_damage, 2)
    
    def get_def_mult(self, character_lvl: int = 80, enemy_lvl: int = 92):
        def_mult = (character_lvl + 100) / (character_lvl + enemy_lvl + 200)

        return def_mult

    def get_res_mult(self, enemy_res: int = 10):
        return (1 - enemy_res/100)
    
    def get_amp_mult(self, artifact_stats: dict):
        react_mult = self.react_mult[self.reaction]
        em_bonus = self.get_em_bonus(artifact_stats)

        amp_mult = react_mult * (1 + em_bonus)

        return round(amp_mult, 5)
        
    def get_em_bonus(self, artifact_stats: dict):
        em = artifact_stats.get("EM", 0) + self.em
        em_bonus = 2.78 * (em / (em + 1400))

        return em_bonus

    def get_crit_mult(self, artifact_stats: dict):
        crit_mult = 1 + (self.crit_dmg + artifact_stats.get("CRIT DMG", 0)) / 100
        crit_rate = min((self.crit_rate + artifact_stats.get("CRIT RATE", 0)), 100) / 100


        return crit_rate, crit_mult

    def calc_damage(self, artifact_stats: dict):
        base_dmg = self.get_base_dmg(artifact_stats)
        dmg_bonus = self.get_dmg_bonus(artifact_stats)
        def_mult = self.get_def_mult() # Independent of artifacts
        res_mult = self.get_res_mult() # Independent of artifacts
        amp_mult = self.get_amp_mult(artifact_stats)
        crit_rate, crit_mult = self.get_crit_mult(artifact_stats)

        damage = base_dmg * dmg_bonus * def_mult * res_mult
        amp_damage = damage * amp_mult
        critical = amp_damage * crit_mult
        avg_damage = (1 - crit_rate) * amp_damage + crit_rate * critical

        return damage, amp_damage, critical, avg_damage

    def final_stats(self, artifact_stats: dict):
        final_stats = {
            "ATK%": round(artifact_stats.get("ATK%", 0), 2),
            "CRIT RATE": round(artifact_stats.get("CRIT RATE", 0) + self.crit_rate, 2),
            "CRIT DMG": round(artifact_stats.get("CRIT DMG", 0) + self.crit_dmg, 2),
            "EM": round(artifact_stats.get("EM", 0) + self.em, 2),
            "ER": round(artifact_stats.get("ER", 0) + self.base_er + 100, 2)
        }

        return final_stats



if __name__ == '__main__':
    base_stats = {"Base ATK": 900, "Ability": 650, "DMG BONUS": 28.8 + 46.6 + 15,
                  "CRIT RATE": 5 + 22.1, "CRIT DMG": 50 + 20, "Reaction": "vaporise"}
    artifact_stats = {'ATK%': 87.41, 'CRIT RATE': 73.91, 'CRIT DMG': 124.36, 'EM': 209.79, 'ER': 12.96}
    test = DamageCalculatorV2(base_stats, "emblem of severed fate")


    print(test.get_base_dmg(artifact_stats))
    print(test.get_res_mult())
    print(test.get_amp_mult(artifact_stats))
    a, b = test.get_crit_mult(artifact_stats)
    print(a)
    print(b)

    damage, amp_damage, critical, avg_damage = test.calc_damage(artifact_stats)
    print("Damage:", damage)
    print("Amp:", amp_damage)
    print("Crit:", critical)
    print("Avg damage:", avg_damage)