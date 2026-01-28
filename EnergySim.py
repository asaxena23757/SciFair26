import streamlit as st
import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt

# Global Varibles
num_of_100mev = 0.0

def run_spe_simulation(file_path, start_row, end_row, total_particles_input):
    global num_of_100mev
    num_of_100mev = 0.0 # Reset for each run

    # 1. Load the data
    df = pd.read_csv(file_path)
    
    # 3. Import specific columns into a 2D array
    data_2d_array = df[['#  Date', '>1 MeV ', '>10 MeV ', '>100 MeV ']].values
    
    # 4. Filter by starting and ending row
    selected_data = df.iloc[start_row : end_row + 1].copy()

    # Energy Range setup
    energy_bins = [(10, 30), (30, 60), (60, 100)]
    weights = [0.85, 0.10, 0.04]
    
    all_generated_energies = []

    # Iterate through each day in the selected range
    for index, row in selected_data.iterrows():
        perc_10mev = float(str(row['% >10 MeV']).strip('%')) / 100.0
        perc_100mev = float(str(row['% >100 MeV']).strip('%')) / 100.0
        
        num_to_simulate = int(total_particles_input * perc_10mev)
        num_of_100mev = (total_particles_input * perc_100mev) + num_of_100mev
        
        for _ in range(num_to_simulate):
            chosen_bin = random.choices(energy_bins, weights=weights, k=1)[0]
            specific_energy = random.uniform(chosen_bin[0], chosen_bin[1])
            all_generated_energies.append(specific_energy)
            
    return all_generated_energies

# --- STREAMLIT IMPLEMENTATION ---

st.title("Solar Particle Event (SPE) Simulation")
st.markdown("""
This simulation models radiation risk by analyzing historical NASA data. 
Adjust the parameters below to see how particle distributions change.
""")

# Sidebar for Configuration
st.sidebar.header("Simulation Settings")

# 1. File Path Input
# Default set to your local path; added a file uploader option for flexibility
CSV_FILE = st.sidebar.text_input("CSV File Path", value="ONLY 2003 SciFairDataTables - 2003_SPE_Data.csv")

# 2. Particle Input
PARTICLES = st.sidebar.number_input("Number of particles for simulation", value=10000, step=1000)

# 3. Row Range Sliders
# We load the dataframe just to find the max length for the slider
try:
    temp_df = pd.read_csv(CSV_FILE)
    max_rows = len(temp_df) - 1
    
    START, END = st.sidebar.slider(
        "Select Range of Rows (Dates)",
        0, max_rows, (0, max_rows)
    )

    # Run Simulation Button
    if st.sidebar.button("🚀 Run Simulation"):
        energy_list = run_spe_simulation(CSV_FILE, START, END, PARTICLES)

        # Output Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows Processed", f"{START+2} to {END+2}")
        with col2:
            st.metric(">10 MeV Count", len(energy_list))
        with col3:
            st.metric(">100 MeV Count", math.floor(num_of_100mev))

        # Data Visualization
        st.subheader("📊 Generated Energy Distribution")
        if energy_list:
            fig, ax = plt.subplots()
            ax.hist(energy_list, bins=20, color='orange', edgecolor='black')
            ax.set_xlabel("Energy (MeV)")
            ax.set_ylabel("Particle Count")
            ax.set_title("Stochastic Energy Distribution (>10 MeV Range)")
            st.pyplot(fig)
            
            # Show Sample Data
            with st.expander("View Raw Energy Sample (First 100)"):
                st.write(energy_list[:100])
        else:
            st.warning("No particles generated for the selected range. Check if the percentage data for these rows is above 0%.")

except FileNotFoundError:
    st.error(f"Could not find the file at: {CSV_FILE}. Please check the path.")
except Exception as e:
    st.error(f"An error occurred: {e}")