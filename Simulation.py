import numpy as np
import pandas as pd
import random
import math

# 1. PHYSICAL CONSTANTS
K = 0.3072      # MeV*cm^2/mol
ME = 0.511     # Electron rest mass (MeV)
MP = 938.27    # Proton rest mass (MeV)

# 2. CHOOSE MATERIAL COMPOSITION PROPERTIES
# You can change these variables depending on which material you want to run
MATERIAL_NAME = "Water"
Z_A_RATIO = 0.55506     # Electron Density Ratio (Z/A)
I_POTENTIAL = 75.0 / 1e6 # Mean Excitation Potential (Converted to MeV)
DENSITY = 1.0           # Physical Density (g/cm^3)

# 3. STOCHASTIC BINNING GENERATOR (NOAA Data Simulation)
# Bins represent proton energies: [10-30 MeV, 30-60 MeV, 60-100 MeV]
BINS = [(10, 30), (30, 60), (60, 100)]
WEIGHTS = [0.85, 0.10, 0.05] 

def generate_incoming_storm(total_particles=10000):
    """Filters out low-energy particles and applies stochastic weights"""
    harmful_particles = []
    # Around 15% of the total event particles are potentially harmful (>10 MeV)
    harmful_count = int(total_particles * 0.15)
    
    for _ in range(harmful_count):
        selected_bin = random.choices(BINS, weights=WEIGHTS)[0]
        initial_energy = random.uniform(selected_bin[0], selected_bin[1])
        harmful_particles.append(initial_energy)
    return harmful_particles

# 4. SIMPLIFIED BETHE-BLOCH ENGINE (-dE/dx)
def calculate_stopping_power(energy, za_ratio, i_pot):
    """Calculates electronic stopping power in MeV * cm^2 / g"""
    if energy <= 0.01: 
        return 0
    gamma = 1 + (energy / MP)
    beta_sq = 1 - (1 / (gamma**2))
    if beta_sq <= 0: 
        return 0
    
    # Core Formula Implementation
    front_term = K * (1**2) * za_ratio / beta_sq
    log_argument = (2 * ME * beta_sq * (gamma**2)) / i_pot
    
    if log_argument <= 1: 
        return 0
    bracket_term = math.log(log_argument) - beta_sq
    return front_term * bracket_term

# 5. STEP FUNCTION LOOP USING MATCHED AREAL DENSITIES
def execute_simulation(initial_energies, areal_densities):
    """Iteratively reduces particle energy across specified slices"""
    all_rows = []
    
    for e_init in initial_energies:
        row_data = [e_init]
        current_energy = e_init
        prev_x = 0
        
        for idx, target_x in enumerate(areal_densities):
            dx = target_x - prev_x
            
            # Sub-stepping loop for numerical integration stability
            sub_steps = 10
            sub_dx = dx / sub_steps
            for _ in range(sub_steps):
                if current_energy > 0.05:
                    loss = calculate_stopping_power(current_energy, Z_A_RATIO, I_POTENTIAL) * sub_dx
                    current_energy -= loss
                else:
                    current_energy = 0
            
            row_data.append(target_x)
            row_data.append(max(0.0, current_energy))
            prev_x = target_x
            
        all_rows.append(row_data)
    return all_rows

# 6. RUN AND EXPORT DATA
if __name__ == "__main__":
    # Areal Densities (g/cm^2) matched to your standard experimental parameters
    experimental_areal_densities = [0.27, 1.35, 2.7, 5.4, 9.45, 13.5, 20.25]
    
    # Seed generation to hold environmental control parameters constant
    random.seed(42)
    incoming_spectrum = generate_incoming_storm(10000)
    
    print(f"Simulating {len(incoming_spectrum)} protons through {MATERIAL_NAME}...")
    sim_data = execute_simulation(incoming_spectrum, experimental_areal_densities)
    
    # Constructing DataFrame columns dynamically
    columns = ['Initial_Energy_MeV']
    for i in range(len(experimental_areal_densities)):
        columns.append(f'Areal_Density_{i+1}')
        columns.append(f'Final_Energy_{i+1}')
        
    df = pd.DataFrame(sim_data, columns=columns)
    output_filename = f"2000_{MATERIAL_NAME}_Density_Simulation_Results.csv"
    df.to_csv(output_filename, index=False)
    print(f"Success! Complete simulation dataset saved as: '{output_filename}' ({len(df)} rows generated).")
