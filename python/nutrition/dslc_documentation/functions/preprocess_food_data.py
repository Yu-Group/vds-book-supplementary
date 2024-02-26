# Cleaning function for the food data
import pandas as pd
import numpy as np

# Clean the food data
def preprocess_food_data(food_clean, 
                         log_transform=True,
                         center=True,
                         scale=True,
                         remove_fat=False):
  
  food_pre_processed = food_clean.copy()

  if log_transform:
    food_pre_processed = food_pre_processed.apply(lambda x: np.log10(x + 1) if np.issubdtype(x.dtype, np.number) else x)
  
  
  # perform centering
  if center:
    food_pre_processed = food_pre_processed.apply(lambda x: x - x.mean() if np.issubdtype(x.dtype, np.number) else x)
  
  # perform SD-scaling
  if scale:
    food_pre_processed = food_pre_processed.apply(lambda x: x / x.std() if np.issubdtype(x.dtype, np.number) else x)
  
  if remove_fat:
    food_pre_processed = food_pre_processed.drop(columns="fat")
  
  # do some mean imputation
  food_pre_processed = food_pre_processed.fillna(food_pre_processed.mean())
  
  return food_pre_processed