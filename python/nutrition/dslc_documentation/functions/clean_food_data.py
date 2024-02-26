# Cleaning function for the food data
import pandas as pd

# Clean the food data
def clean_food_data(nutrient_amount_data,
                    food_name_data,
                    nutrient_name_data,
                    select_data_type="survey_fndds_food"):
  
  select_data_type_options = ["survey_fndds_food", "branded_food", "foundation_food",
                              "sr_legacy_food", "sub_sample_food", "agricultural_acquisition"]
  if select_data_type not in select_data_type_options:
    raise ValueError("Invalid select_data_type. Expected one of: %s" % select_data_type_options)
  
  # filter the nutrient and food ID datasets to the relevant columns and
  nutrient_amount_lite = nutrient_amount_data[["fdc_id", "nutrient_id", "amount"]]
  food_name_lite = food_name_data[["fdc_id", "data_type", "description"]]
  
  # join the tables to create one dataset
  food_clean = nutrient_amount_lite.merge(food_name_lite, on="fdc_id", how="left") \
    .merge(nutrient_name_data, on="nutrient_id", how="left") 
  
  # filter to just fndds foods (default)
  food_clean = food_clean.query("data_type == @select_data_type")
  food_index = food_clean.description.drop_duplicates()

  # convert to wide tidy form
  food_clean = (
    food_clean[["description", "amount", "nutrient_name"]].drop_duplicates() 
      .dropna(subset="nutrient_name") \
      # deal with duplicate description/nutrient_name entries
      .groupby(["description", "nutrient_name"])["amount"].mean() 
      .unstack()
  )
  # remove column index name
  food_clean.columns.name = None
  # remove alphabetical ordering of index
  food_clean = food_clean.reindex(index=food_index)
  
  return food_clean