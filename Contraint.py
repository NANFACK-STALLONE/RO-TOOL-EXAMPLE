from ortools.sat.python import cp_model

# Création du modèle CP-SAT
model = cp_model.CpModel()

# Données du problème
durations = [3, 2, 4]  # Durées des tâches 1, 2, 3
num_tasks = len(durations)
horizon = 15  # Horizon de planification (borne supérieure sur les dates)

# 1) Variables de décision
starts = []
ends = []
intervals = []

for i in range(num_tasks):
    # Date de début de la tâche i
    start = model.NewIntVar(0, horizon, f"start_{i+1}")
    # Date de fin de la tâche i
    end = model.NewIntVar(0, horizon, f"end_{i+1}")
    # Intervalle (start, durée, end) pour la contrainte NoOverlap
    interval = model.NewIntervalVar(start, durations[i], end, f"interval_{i+1}")

    starts.append(start)
    ends.append(end)
    intervals.append(interval)

# 2) Contrainte de machine unique : pas de chevauchement des tâches
model.AddNoOverlap(intervals)

# 3) Contrainte de précédence : la tâche 1 doit finir avant le début de la tâche 3
# Tâche 1 = index 0, Tâche 3 = index 2
model.Add(ends[0] <= starts[2])

# 4) Variable pour le makespan (date de fin de toutes les tâches)
cmax = model.NewIntVar(0, horizon, "Cmax")
for e in ends:
    model.Add(e <= cmax)

# 5) Objectif : minimiser le makespan
model.Minimize(cmax)

# 6) Résolution
solver = cp_model.CpSolver()
status = solver.Solve(model)

# 7) Affichage des résultats
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("Solution trouvée :")
    for i in range(num_tasks):
        print(f"Tâche {i+1} :")
        print("  Début =", solver.Value(starts[i]))
        print("  Fin   =", solver.Value(ends[i]))
    print("Makespan (Cmax) =", solver.Value(cmax))
else:
    print("Aucune solution réalisable trouvée.")
