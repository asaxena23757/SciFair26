1. interpret some data table from .xlsx or .csv
2. Read and check if in this format: #  Date,>1 MeV Proton Fluence,>10 MeV Proton Fluence,>100 MeV Proton Fluence,>0.6 MeV Electron Fluence,>2 MeV Electron Fluence,% of bkgd Neutron Monitor
3. import columns #  Date,>1 MeV Proton Fluence,>10 MeV Proton Fluence,>100 MeV Proton Fluence in a 2d array
4. add up the total of >1 MeV Proton Fluence,>10 MeV Proton Fluence,>100 MeV Proton Fluence and find which columns have a certain percentage of particles in each given set

Energy Range (MeV),Probability (Weight)
10 – 30,0.85
30 – 60,0.10
60 – 100,0.04
100 – 500+,0.01