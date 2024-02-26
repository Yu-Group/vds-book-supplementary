import pandas as pd
from functions.impute_feature import impute_feature


def prepare_organ_data(organs_original,
                       impute_method = "average",
                       per_mil_vars = True): 
  
  
  # define a cleaned version of the original organs data
  # rename the original rows
  organs_clean = organs_original.rename(columns={
    'REGION': 'region',
    'COUNTRY': 'country',
    'REPORTYEAR': 'year',
    'POPULATION': 'population',
    'TOTAL Actual DD': 'total_deceased_donors',
    'Actual DBD': 'deceased_donors_brain_death',
    'Actual DCD': 'deceased_donors_circulatory_death',
    'Total Utilized DD': 'total_utilized_deceased_donors',
    'Utilized DBD': 'utilized_deceased_donors_brain_death',
    'Utilized DCD': 'utilized_deceased_donors_circulatory_death',
    'DD Kidney Tx': 'deceased_kidney_tx',
    'LD Kidney Tx': 'living_kidney_tx',
    'TOTAL Kidney Tx': 'total_kidney_tx',
    'DD Liver Tx': 'deceased_liver_tx',
    'LD Liver Tx': 'living_liver_tx',
    'DOMINO Liver Tx': 'domino_liver_tx',
    'TOTAL Liver TX': 'total_liver_tx',
    'Total Heart': 'total_heart_tx',
    'DD Lung Tx': 'deceased_lung_tx',
    'DD Lung Tx': 'living_lung_tx',
    'TOTAL Lung Tx': 'total_lung_tx',
    'Pancreas Tx': 'total_pancreas_tx',
    'Kidney Pancreas Tx': 'total_kidney_pancreas_tx',
    'Small Bowel Tx': 'total_small_bowel_tx'}).copy()

  # add the rows with missing country-year combinations
  country_year_combinations = pd.MultiIndex.from_product([organs_clean[col].unique() for col in ["country", "year"]], 
                                                         names=["country", "year"])
  # put these combinations into a data frame
  country_year_combinations_df = pd.DataFrame(index=country_year_combinations).reset_index()
  organs_clean = country_year_combinations_df.merge(organs_clean, on=["country", "year"], how="left")

  # For newly added rows, fill region with the unique values from the pre-existing rows  
  organs_clean["region"] = organs_clean.groupby("country")["region"].transform(lambda x: x.ffill().bfill())

  # multiply the population variable by 1 million
  organs_clean["population"] = organs_clean["population"] * 1000000
  
  # add imputed features using the specified imputation method
  # impute_feature() is a custom function defined in imputeFeature.R
  # Note that we are only imputing the total_deceased_donors variable and the 
  # population variable (missing values were introduced when we 
  # "completed" the data). You could impute more variables if you wanted to.
  if impute_method in ["average", "previous"]:
    organs_clean["population_imputed"] = impute_feature(organs_clean, 
                                                        feature = "population",
                                                        group = "country",
                                                        impute_method = impute_method)
    organs_clean["total_deceased_donors_imputed"] = impute_feature(organs_clean, 
                                                                  feature = "total_deceased_donors",
                                                                  group = "country",
                                                                  impute_method = impute_method)
  
  
  # rearrange the columns 
  column_order = ['country', 'year', 'region', 'population', 'population_imputed', 
                               'total_deceased_donors', 'total_deceased_donors_imputed'] + list(organs_clean.columns)
  column_order = pd.unique(column_order)
  organs_clean = organs_clean.reindex(columns=column_order)
  
  return organs_clean

