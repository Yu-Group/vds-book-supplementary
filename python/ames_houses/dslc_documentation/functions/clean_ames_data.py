# Cleaning function for the Ames housing data
import numpy as np
import pandas as pd

# Clean the Ames data
def clean_ames_data(ames_data):
  
  ames_data_clean = ames_data.copy() 
  
  # impute missing garage year with house built year
  ames_data_clean["Garage Yr Blt"] = np.where(ames_data_clean["Garage Yr Blt"].isna(), 
                                              ames_data_clean["Garage Yr Blt"],
                                              ames_data_clean["Year Built"])
  
  # replace `Year Remod Add` value of 1950 with the `Year Built` value
  ames_data_clean["Garage Yr Blt"] = np.where(ames_data_clean["Year Remod/Add"] == 1950, 
                                              ames_data_clean["Year Built"],
                                              ames_data_clean["Year Remod/Add"])
  
  # create a date variable
  ames_data_clean["date"] = pd.to_datetime(dict(year=ames_data_clean["Yr Sold"], 
                                                month=ames_data_clean["Mo Sold"], 
                                                day=1))
  
  # clean the column names
  ames_data_clean.columns = ames_data_clean.columns.str.lower() \
                                                    .str.replace(' ', '_') \
                                                    .str.replace('/', '_')
  
  ames_data_clean = ames_data_clean.set_index("pid")
  
  return(ames_data_clean)


