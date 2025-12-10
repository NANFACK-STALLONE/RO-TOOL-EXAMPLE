from ortools.linear_solver import pywraplp

# Création du solveur (GLOP = solveur de programmation linéaire)
solver = pywraplp.Solver.CreateSolver('GLOP')

if not solver:
    raise Exception("Le solveur GLOP n'a pas pu être créé.")

# 1) Définition des variables de décision
# x : quantité du produit A
# y : quantité du produit B
x = solver.NumVar(0, solver.infinity(), "x")
y = solver.NumVar(0, solver.infinity(), "y")

print("Nombre de variables :", solver.NumVariables())

# 2) Ajout des contraintes

# Contraite de temps machine : 2x + y <= 100
constraint_machine = solver.Add(2 * x + y <= 100)

# Contrainte de main-d'œuvre : x + 2y <= 80
constraint_labor = solver.Add(x + 2 * y <= 80)

print("Nombre de contraintes :", solver.NumConstraints())

# 3) Définition de la fonction objectif
# Maximiser Z = 40x + 30y
objective = solver.Objective()
objective.SetCoefficient(x, 40)
objective.SetCoefficient(y, 30)
objective.SetMaximization()

# 4) Lancement de la résolution
status = solver.Solve()

# 5) Analyse et affichage des résultats
if status == pywraplp.Solver.OPTIMAL:
    print("Solution optimale trouvée :")
    print(" - x (quantité de produit A) =", x.solution_value())
    print(" - y (quantité de produit B) =", y.solution_value())
    print("Bénéfice maximal =", objective.Value())
else:
    print("Le solveur n'a pas trouvé de solution optimale.")
