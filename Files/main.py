from artifactcombos import ArtifactCombos
from characterselection import CharacterSelection
from pruningtools import Pruning
from damagecalculator import DamageCalculator
from montecarlosim import MonteCarloSim
import numpy as np
import matplotlib.pyplot as plt

# Create combinations of artifacts --------------------
artifact_combos = ArtifactCombos()

flower = artifact_combos.filtered_combos("flower")
feather = artifact_combos.filtered_combos("feather")
sands = artifact_combos.filtered_combos("sands")
goblet = artifact_combos.filtered_combos("goblet")
circlet = artifact_combos.filtered_combos("circlet")

# Get character stats --------------------
character_selection = CharacterSelection()

base_stats, artifact_set = character_selection.get_base_stats()
print(f"Base stats: {base_stats}\n")

filter_crit = 85 - base_stats.get("CRIT RATE", 0)
print(f"The crit rate filter for combos is: {filter_crit}\n")

# Create and prune possible combos --------------------
pruning = Pruning(filter_crit)

print("Initial iteration:")
current_dp = pruning.intial_dp(flower, feather)
print(f"Number of combos before pruning: {len(current_dp)}")
pruned = pruning.prune_dp(current_dp)
print(f"Number of combos after pruning: {len(pruned)}\n")

print("Second iteration:")
current_dp = pruning.create_dp(goblet, pruned)
print(f"Number of combos before pruning: {len(current_dp)}")
pruned = pruning.prune_dp(current_dp)
print(f"Number of combos after pruning: {len(pruned)}\n")

print("Third iteration:")
current_dp = pruning.create_dp(sands, pruned, True)
print(f"Number of combos before pruning: {len(current_dp)}")
pruned = pruning.prune_dp(current_dp)
print(f"Number of combos after pruning: {len(pruned)}\n")

print("Final iteration:")
current_dp = pruning.create_dp(circlet, pruned, True)
print(f"Number of combos before pruning: {len(current_dp)}")
# Could prune one last time from to <20k but takes two mins, faster to skip
#pruned = pruning.prune_dp(current_dp)
pruned = current_dp
print(f"Number of combos after pruning: {len(pruned)}\n")

# Damage Calculation --------------------
calc = DamageCalculator(base_stats, artifact_set)

best_damage = (0, 0, 0, 0)
best_loadout = {}
equal_builds = 0

for line in pruned:
    artifact_stats = line["state"]
    damage, amp_damage, critical, avg_damage = calc.calc_damage(artifact_stats)
    if avg_damage == best_damage[-1]:
        equal_builds += 1
    if avg_damage > best_damage[-1]:
        best_loadout = line
        best_damage = (damage, amp_damage, critical, avg_damage)
        equal_builds = 0

# Print results --------------------
print("Theoretical Max Results:\n====================")
print("Best loadout:")
for subs in best_loadout["combo"]:
    print(subs)
print("\nFinal stats with this loadout:", calc.final_stats(best_loadout["state"]))
damage, amp_damage, critical, avg_damage = best_damage
print("\nDamage:", damage)
print("Amplified Damage:", amp_damage)
print("Critical Damage:", critical)
print("Average Damage:", avg_damage)
print("Number of Equal Builds:", equal_builds)

# Simulate Artifact Farming --------------------
num_simulations = 50
print("\n====================")
print(f"Simulating {num_simulations} runs of artifact domain farming, with 1350 pulls per run:")
print("====================\n")

complete_sim = []
for i in range(num_simulations):
    mc_sim = MonteCarloSim(base_stats, artifact_set)
    sim_data = []
    highest_damage = 0
    for j in range(1350):
        if mc_sim.run_domain():
            top_10 = mc_sim.get_top_builds()
            highest_damage = top_10[-1][0]
            mc_sim.trim_pools(top_10)

        sim_data.append(round(highest_damage, 2))

    print(f"Best dmg: {highest_damage:.2f} (Simulation number: {i+1})")
    complete_sim.append(sim_data)

print("\nSimulation Complete\n")

# Plot Data --------------------
complete_sim = np.array(complete_sim)
mean_data = np.mean(complete_sim, axis = 0)
std_dev_data = np.std(complete_sim, axis = 0)

std_error_data = std_dev_data / np.sqrt(num_simulations)
ci_lower = mean_data - 1.96 * std_error_data
ci_upper = mean_data + 1.96 * std_error_data

theoretical_max = avg_damage # Average damage from theoretical max run

figure, axis = plt.subplots(2, 1)

for simulation in complete_sim:
    axis[0].plot(simulation, alpha = 0.5)
axis[0].axhline(y = theoretical_max, color = "red", linestyle = "dashed") # Line corresponds to theoretical max

axis[1].plot(mean_data, color = "blue", label = "Avg dmg")
axis[1].fill_between(np.arange(1350), ci_lower, ci_upper, 
                     color = "red", alpha = 0.2, label = "95% confidence interval")
axis[1].legend(loc = "upper left")

plt.show()

# Compute Percentage Growth --------------------
pct_growth = (np.diff(mean_data) / mean_data[:-1]) * 100
moving_avg_growth = np.convolve(pct_growth, np.ones(10)/10, mode = "valid")
threshold = moving_avg_growth[270] * 0.0001

optimal_index = np.where(moving_avg_growth < threshold)
print(f"Possible stopping points: {optimal_index}")