# FrioMACADataAnlysis
this repo is for the python scripts to calculate statistics and visualizing the results of the MACA GCMs at the Frio basin


notes: 
  1) The pyhton scripts were written with Python 3.x 
  2) The zip files at the folder of DataT should be unzipped before running the python scripts.
  3) Main calculations were implemented in a python class, dataanalysis.py. This file will be imported in the Jupyter notebook file
  4) The Jupyter notebook file includes 6 sections:
       
       Section 1: Import the modules
       
       Section 2: Load the class of data analysis customized for the Frio basin 
       
       Section 3: Use the class to load the data for the Frio basin
  
       Section 4:  Calculate annul mean and seasonal mean for precipitation and temperature at different time periods, different RCPs and zones (recharge and contributing)
 
        Section 5: Reformat the 4 data frames for visualizing with Seaborn module
        
        Section 6: Visualizing the results
        
             Section 6.1 Plot the mean precipitation and temperature

             Section 6.2 Plot the relative change for mean precipitation and temperature
