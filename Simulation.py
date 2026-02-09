import streamlit as st
import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import os  # Added to check for file existence

DEFAULT_FILE_PATH = "D:\\5-Projects\\SciFair26\\InputData\\SciFairDataTables - 2003_SPE_Data.csv"

#Varibles
num_of_100mev = 0.0
dedx = 0.0


def run_spe_simulation(file_path, start_row, end_row, total_particles_input):
    global num_of_100mev
    num_of_100mev = 0.0 
    df = pd.read_csv(file_path)
    selected_data = df.iloc[start_row : end_row + 1].copy()
    energy_bins = [(10, 30), (30, 60), (60, 100)]
    weights = [0.85, 0.10, 0.04]
    all_generated_energies = []

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

def mat_simulation(material,):
    #Material, density, Z/A Ratio, I-value
    material = [("Aluminum",2.7,.481,166), ("Polyethylene",.94,.571,57.4), ("Water",1,.555,75)]
    # create a loop for some tiny step, and calculate the energy loss
    #sum up energy lost, different things depending on organic vs no organic material toggalabe option
    #

def bethe_bloche(kinetic_energy, density, za_Ratio, i_value):
    global dedx
    dedx = 0.0
    rest_mass_proton = 938.27 
    rest_mass_electron = .510998
    k = .307236
    #Calc gamma
    gamma_int = 1 + (kinetic_energy/rest_mass_proton) 
    #Calc beta
    beta_int = math.sqrt(1-(1/(gamma_int^2)))
    # low energy check
    if beta_int^2 < 1e-6:
        return 0
    #Calc Bethe Bloch
    bethe_bloche_t1 = (k * density * za_Ratio)/(beta_int^2)
    bethe_bloche_t2 = math.log ((2 * rest_mass_electron^2 * beta_int^2 * gamma_int^2)/i_value)
    dedx = bethe_bloche_t1 * (bethe_bloche_t2 - beta_int^2)
    return dedx

# Streamlit
st.title("Solar Particle Event (SPE) Simulation")

#File trouble shot
if not os.path.exists(DEFAULT_FILE_PATH):
    st.error(f"FILE NOT FOUND AT: {DEFAULT_FILE_PATH}")
    st.info("**Troubleshooting Tips:**\n"
            "1. Open your folder containing your data as a .csv file"
            "2. Ensure the file path is corrrect by copying the file explorer address bar"
            "3. Ensure the D: drive is plugged in and accessible.")
else:
    #Rest of the code only runs if file is found
    st.success("Connected to SPE Database")
    
    st.sidebar.header("Simulation Settings")
    PARTICLES = st.sidebar.number_input("Number of particles for sim", value=10000, step=1000)

    try:
        temp_df = pd.read_csv(DEFAULT_FILE_PATH)
        max_rows = len(temp_df) - 1
        START, END = st.sidebar.slider("Select Row Range", 0, max_rows, (0, max_rows))

        if st.sidebar.button("Run Simulation"):
            energy_list = run_spe_simulation(DEFAULT_FILE_PATH, START, END, PARTICLES)
            col1, col2 = st.columns(2)
            col1.metric(">10 MeV Generated", len(energy_list))
            col2.metric(">100 MeV Total", math.floor(num_of_100mev))

            st.subheader("Energy Distribution Profile")
            if energy_list:
                fig, ax = plt.subplots()
                ax.hist(energy_list, bins=30, color='skyblue', edgecolor='black')
                ax.set_xlabel("Energy (MeV)")
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Error reading data: {e}")

#streamlit run EnergySim.py
