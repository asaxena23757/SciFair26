import pandas as pd
import numpy as np
import random

def run_spe_simulation(file_path, start_row, end_row, total_particles_input):
    # 1. Load the data
    df = pd.read_csv(file_path)
    
    # 2. Verify format (Headers)
    # The columns in your file are: '#  Date', '>1 MeV ', '>10 MeV ', '>100 MeV ', etc.
    
    # 3. Import specific columns into a 2D array
    data_2d_array = df[['#  Date', '>1 MeV ', '>10 MeV ', '>100 MeV ']].values
    
    # 4. Filter by starting and ending row
    # (Using slice to handle range)
    selected_data = df.iloc[start_row : end_row + 1].copy()
    
    # Energy Range setup (Step 6)
    energy_bins = [(10, 30), (30, 60), (60, 100)]
    weights = [0.85, 0.10, 0.04]
    
    all_generated_energies = []

    # Iterate through each day in the selected range
    for index, row in selected_data.iterrows():
        # Get the percentage of particles in the >10 MeV range
        # Clean the string "6.01%" and convert to decimal
        perc_10mev = float(str(row['% >10 MeV']).strip('%')) / 100.0
        perc_100mev = float(str(row['% >100 MeV']).strip('%')) / 100.0
        
        # Calculate number of particles to simulate for this specific day
        num_to_simulate = int(total_particles_input * perc_10mev)
        num_of_100mev = int(total_particles_input * perc_100mev)
        
        for _ in range(num_to_simulate):
            # Choose a bin based on the provided weights
            # random.choices allows for relative weights (sum doesn't have to be 1.0)
            chosen_bin = random.choices(energy_bins, weights=weights, k=1)[0]
            
            # Choose a specific energy value randomly within that bin
            specific_energy = random.uniform(chosen_bin[0], chosen_bin[1])
            all_generated_energies.append(specific_energy)
            
    return all_generated_energies

# --- Configuration ---
CSV_FILE = "D:\\5-Projects\\SciFair26\\InputData\\ONLY 2003 SciFairDataTables - 2003_SPE_Data.csv"
START = 299  # Starting row index (e.g., late October)
END = 300    # Ending row index
PARTICLES = 10000 # Your input variable for number of particles

# Run the simulation
energy_list = run_spe_simulation(CSV_FILE, START, END, PARTICLES)

# Output results
print(f"Simulation complete for rows {START} to {END}.")
print(f"Total particles generated in the >10 MeV category: {len(energy_list)}")
print(f"Sample of generated energies (MeV): {energy_list[:10]}")
print(f"Total particles generated in the >100 MeV category:", num_of_100mev)