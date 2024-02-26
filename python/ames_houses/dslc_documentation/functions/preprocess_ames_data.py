import pandas as pd
import numpy as np

def preprocess_ames_data(ames_data_clean,
                         column_selection=[],
                         max_identical_thresh=0.8,
                         max_missing_thresh=0.5,
                         neighborhood_levels=[],
                         n_neighborhoods=10,
                         neighborhood_dummy=True,
                         impute_missing_categorical="other",
                         simplify_vars=True,
                         log_transform_predictors=None,
                         transform_response="none",
                         cor_feature_selection_threshold=None,
                         convert_categorical="numeric"):
  

  impute_missing_categorical_options = ["other", "mode"]
  if impute_missing_categorical not in impute_missing_categorical_options:
    raise ValueError("Invalid impute_missing_categorical. Expected one of: %s" % impute_missing_categorical_options)

  transform_response_options = ["none", "log", "sqrt"]
  if transform_response not in transform_response_options:
    raise ValueError("Invalid transform_response. Expected one of: %s" % transform_response_options)

  convert_categorical_options = ["numeric", "simplified_dummy", "dummy", "none"]
  if convert_categorical not in convert_categorical_options:
    raise ValueError("Invalid convert_categorical. Expected one of: %s" % convert_categorical_options)
  
  ames_data_preprocessed = ames_data_clean.copy()
  
  
  #------------------------- Handle missing values ---------------------------#
  
  if len(column_selection) == 0:
    # if we have not specified which columns to keep
    # remove variables with more than max_missing_thresh missing proportion
    
    # identify the proportion of missing values for each column
    prop_missing = pd.isna(ames_data_preprocessed).sum() / len(ames_data_preprocessed.index)
    vars_to_keep = prop_missing < max_missing_thresh
    
    # remove the variables above the threshold
    ames_data_preprocessed = ames_data_preprocessed.loc[:,vars_to_keep]

  
  
  # assume that missing basement bathrooms and mas_vnr_area is 0
  # impute lot frontage with median lot frontage
  ames_data_preprocessed = ames_data_preprocessed.fillna(
      {"bsmt_full_bath": 0, 
       "bsmt_half_bath": 0, 
       "full_bath": 0,
       "half_bath": 0,
       "mas_vnr_area": 0, 
       "lot_frontage": ames_data_preprocessed.lot_frontage.median()}
  )


  # impute categorical values per `impute_missing_categorical` argument
  str_columns = ames_data_preprocessed.select_dtypes(include="object").columns
  if impute_missing_categorical == "other":
      ames_data_preprocessed.loc[:,str_columns] = ames_data_preprocessed.loc[:,str_columns].fillna("other")
  elif impute_missing_categorical == "mode":
      # compute the mode for all character type colums
      ames_mode = ames_data_preprocessed.loc[:,str_columns].mode().iloc[0,:]
      # fill each missing value with the mode for the column
      ames_data_preprocessed.loc[:,str_columns] = ames_data_preprocessed.loc[:,str_columns].fillna(ames_mode)
  
  
  #--------------------- Neighborhood levels ---------------------------------#
  
  # if cleaning validation or testing data, you want the levels to match
  # the training data
  if len(neighborhood_levels) == 0:
      # identify the proportion of houses in each neighborhood
      neighborhood_prop = ames_data_preprocessed.value_counts("neighborhood") / len(ames_data_preprocessed.index)
      # identify the number of neighborhoods that will be converted to other
      total_neighborhoods = len(ames_data_preprocessed.neighborhood.unique()) - n_neighborhoods
      # identify the names of the neighborhoods that will be converted to other
      neighborhoods_other = neighborhood_prop.tail(total_neighborhoods).index
      # identify the rows where the neighborhood needs to be replaced with "other"
      neighborhood_other_index = ames_data_preprocessed["neighborhood"].isin(neighborhoods_other)
      # convert the smaller neighborhoods to other
      ames_data_preprocessed.loc[neighborhood_other_index, "neighborhood"] = "other"
  else:  
    # convert all nhbd levels not provided in neighborhood_levels to "other"
    # this is helpful for ensuring that the validation and test sets have the 
    # same neighborhood levels as the training set
    
    # identify which neighborhoods are being excluded
    excluded_neighborhoods_index = ~ames_data_preprocessed["neighborhood"].isin(neighborhood_levels)
    # convert excluded neighborhoods to other
    ames_data_preprocessed.loc[excluded_neighborhoods_index, "neighborhood"] = "other"
  
  
  #------------------------ Simplify variables -------------------------------#
  
  # manually simplify several variables with rare levels
  if simplify_vars == True:
    # if simplify_vars == True, simplify more
    # manually simplify variables with many levels
    ames_data_preprocessed["gable_roof"] = np.where(ames_data_preprocessed["roof_style"] == "Gable", 1, 0)
    ames_data_preprocessed["masonry_veneer_brick"] = np.where(ames_data_preprocessed["mas_vnr_type"].isin(["BrkFace", "BrkCmn"]), 1, 0)
    ames_data_preprocessed["foundation_cinder"] = np.where(ames_data_preprocessed["foundation"] == "CBlock", 1, 0)
    ames_data_preprocessed["foundation_concrete"] = np.where(ames_data_preprocessed["foundation"] == "PConc", 1, 0)
    ames_data_preprocessed["electrical_standard"] = np.where(ames_data_preprocessed["electrical"] == "SBrkr", 1, 0)
    ames_data_preprocessed["garage_attached"] = np.where(ames_data_preprocessed["garage_type"].isin(["Attchd", "BuiltIn", "2Types", "Basement"]), 1, 0)
    ames_data_preprocessed["lot_inside"] = np.where(ames_data_preprocessed["lot_config"] == "Inside", 1, 0)
    ames_data_preprocessed["no_proximity"] = np.where(ames_data_preprocessed["condition_1"] == "Norm", 1, 0)
    ames_data_preprocessed["single_family_house"] = np.where(ames_data_preprocessed["bldg_type"] == "1Fam", 1, 0)
    # combine 1st and 2nd floor variables
    ames_data_preprocessed["exterior_vinyl"] = np.where(
      (ames_data_preprocessed["exterior_1st"] == "VinylSd") | (ames_data_preprocessed["exterior_2nd"] == "VinylSd"), 
      1, 0
    )
    ames_data_preprocessed["exterior_metal"] = np.where(
      (ames_data_preprocessed["exterior_1st"] == "MetalSd") | (ames_data_preprocessed["exterior_2nd"] == "MetalSd"), 
      1, 0
    )
    ames_data_preprocessed["exterior_hardboard"] = np.where(
      (ames_data_preprocessed["exterior_1st"] == "HdBoard") | (ames_data_preprocessed["exterior_2nd"] == "HdBoard"), 
      1, 0
    )
    ames_data_preprocessed["exterior_wood"] = np.where(
      (ames_data_preprocessed["exterior_1st"] == "Wd Sdng") | (ames_data_preprocessed["exterior_2nd"] == "Wd Sdng"), 
      1, 0
    )
    # combine bathroom variables
    ames_data_preprocessed["bathrooms"] = ames_data_preprocessed["full_bath"] + 0.5*ames_data_preprocessed["half_bath"] + ames_data_preprocessed["bsmt_full_bath"] + 0.5*ames_data_preprocessed["bsmt_half_bath"]
    # combine porch variables
    ames_data_preprocessed["porch"] = np.where(
      # if any porch variable is not equal to 0
      (ames_data_preprocessed["open_porch_sf"] != 0) | 
      (ames_data_preprocessed["enclosed_porch"] != 0) | 
      (ames_data_preprocessed["3ssn_porch"] != 0) |
      (ames_data_preprocessed["screen_porch"] != 0),
      1, 0
    )
    # remove the variables we no longer need
    ames_data_preprocessed = ames_data_preprocessed.drop(
       columns=["roof_style",
                "mas_vnr_type",
                "foundation",
                "electrical",
                "garage_type",
                "lot_config",
                "condition_1",
                "bldg_type",
                "exterior_1st",
                "exterior_2nd",
                "bsmt_full_bath",
                "bsmt_half_bath",
                "full_bath",
                "half_bath",
                "open_porch_sf",
                "enclosed_porch",
                "3ssn_porch",
                "screen_porch",
                # remove basement SF sub-variables if simplifying
                "bsmt_unf_sf",
                "bsmtfin_sf_1",
                "bsmtfin_sf_1",
                # remove general SF sub-variables if simplifying
                "1st_flr_sf", 
                "2nd_flr_sf", 
                "low_qual_fin_sf"])
  else:
    # if simplify_vars == FALSE, still simplify, but simplify less
    ames_data_preprocessed["gable_roof"] = np.where(ames_data_preprocessed["roof_style"] == "Gable", 1, 0)
    ames_data_preprocessed["hip_roof"] = np.where(ames_data_preprocessed["roof_style"] == "Hip", 1, 0)
    ames_data_preprocessed["masonry_veneer_brick_face"] = np.where(ames_data_preprocessed["mas_vnr_type"] == "BrkFace", 1, 0)
    ames_data_preprocessed["masonry_veneer_none"] = np.where(ames_data_preprocessed["mas_vnr_type"] == "BrkCmn", 1, 0)
    ames_data_preprocessed["masonry_veneer_stone"] = np.where(ames_data_preprocessed["mas_vnr_type"] == "Stone", 1, 0)
    ames_data_preprocessed["foundation_brick"] = np.where(ames_data_preprocessed["foundation"] == "BrkTil", 1, 0)
    ames_data_preprocessed["foundation_cinder"] = np.where(ames_data_preprocessed["foundation"] == "CBlock", 1, 0)
    ames_data_preprocessed["foundation_concrete"] = np.where(ames_data_preprocessed["foundation"] == "PConc", 1, 0)
    ames_data_preprocessed["electrical_standard"] = np.where(ames_data_preprocessed["electrical"] == "SBrkr", 1, 0)
    ames_data_preprocessed["garage_attached"] = np.where(ames_data_preprocessed["garage_type"] == "Attchd", 1, 0)
    ames_data_preprocessed["garage_detached"] = np.where(ames_data_preprocessed["garage_type"] == "Detchd", 1, 0)
    ames_data_preprocessed["lot_inside"] = np.where(ames_data_preprocessed["lot_config"] == "Inside", 1, 0)
    ames_data_preprocessed["lot_corner"] = np.where(ames_data_preprocessed["lot_config"] == "Corner", 1, 0)
    ames_data_preprocessed["railroad_adjacent"] = np.where(ames_data_preprocessed["condition_1"].isin(["RRAe", "RRAn", "RRNe", "RRNn"]), 1, 0)
    ames_data_preprocessed["main_street_adjacent"] = np.where(ames_data_preprocessed["condition_1"].isin(["Artery", "Feedr"]), 1, 0)
    ames_data_preprocessed["positive_adjacent"] = np.where(ames_data_preprocessed["condition_1"].isin(["PosA", "PosN"]), 1, 0)
    ames_data_preprocessed["single_family_house"] = np.where(ames_data_preprocessed["bldg_type"] == "1Fam", 1, 0)
    ames_data_preprocessed["townhouse"] = np.where(ames_data_preprocessed["bldg_type"].isin(["Twnhs", "TwnhsE"]), 1, 0)
    ames_data_preprocessed["exterior1_vinyl"] = np.where(ames_data_preprocessed["exterior_1st"] == "VinylSd", 1, 0)
    ames_data_preprocessed["exterior1_metal"] = np.where(ames_data_preprocessed["exterior_1st"] == "MetalSd", 1, 0)
    ames_data_preprocessed["exterior1_hardboard"] = np.where(ames_data_preprocessed["exterior_1st"] == "HdBoard", 1, 0)
    ames_data_preprocessed["exterior1_wood"] = np.where(ames_data_preprocessed["exterior_1st"] == "Wd Sdng", 1, 0)
    ames_data_preprocessed["exterior1_plywood"] = np.where(ames_data_preprocessed["exterior_1st"] == "Plywood", 1, 0)
    ames_data_preprocessed["exterior1_cement"] = np.where(ames_data_preprocessed["exterior_1st"] == "CemntBd", 1, 0)
    ames_data_preprocessed["exterior1_brick"] = np.where(ames_data_preprocessed["exterior_1st"] == "BrkFace", 1, 0)
    ames_data_preprocessed["exterior1_wood_shing"] = np.where(ames_data_preprocessed["exterior_1st"] == "WdShing", 1, 0)
    ames_data_preprocessed["exterior2_vinyl"] = np.where(ames_data_preprocessed["exterior_2nd"] == "VinylSd", 1, 0)
    ames_data_preprocessed["exterior2_metal"] = np.where(ames_data_preprocessed["exterior_2nd"] == "MetalSd", 1, 0)
    ames_data_preprocessed["exterior2_hardboard"] = np.where(ames_data_preprocessed["exterior_2nd"] == "HdBoard", 1, 0)
    ames_data_preprocessed["exterior2_wood"] = np.where(ames_data_preprocessed["exterior_2nd"] == "Wd Sdng", 1, 0)
    ames_data_preprocessed["exterior2_plywood"] = np.where(ames_data_preprocessed["exterior_2nd"] == "Plywood", 1, 0)
    ames_data_preprocessed["exterior2_cement"] = np.where(ames_data_preprocessed["exterior_2nd"] == "CemntBd", 1, 0)
    ames_data_preprocessed["exterior2_brick"] = np.where(ames_data_preprocessed["exterior_2nd"] == "BrkFace", 1, 0)
    ames_data_preprocessed["exterior2_wood_shing"] = np.where(ames_data_preprocessed["exterior_2nd"] == "WdShing", 1, 0)
    ames_data_preprocessed["porch_area"] = ames_data_preprocessed["open_porch_sf"] + ames_data_preprocessed["enclosed_porch"] + ames_data_preprocessed["3ssn_porch"] + ames_data_preprocessed["screen_porch"]

    # remove the variables we no longer need
    ames_data_preprocessed = ames_data_preprocessed.drop(
       columns=["roof_style",
                "mas_vnr_type",
                "foundation",
                "electrical",
                "garage_type",
                "lot_config",
                "condition_1",
                "bldg_type",
                "exterior_1st",
                "exterior_2nd",
                "bsmt_full_bath",
                "bsmt_half_bath",
                "full_bath",
                "half_bath",
                "open_porch_sf",
                "enclosed_porch",
                "3ssn_porch",
                "screen_porch",
                # or remove just one of the sub-SF variables
                "bsmt_unf_sf",
                "low_qual_fin_sf"])
  
  
  #-------------------- Categorical to numeric -------------------------------#
  
  if convert_categorical in ["dummy", "none"]:
    # simplify the uncommon levels to ensure that the validation set doesn't 
    # have levels that aren't in the training set

    # zoning
    zone_mapping = {
      "FV": "other", "RH": "other", "RL": "low_density", "RM": "medium_density"
    }
    lot_mapping = {
      "IR1": "irregular", "IR2": "irregular", "IR3": "irregular", "Reg": "regular"
    }
    functional_mapping = {
      "Typ": "typical", "Maj1": "atypical", "Maj2": "atypical", "Min1": "atypical",
      "Min2": "atypical", "Mod": "atypical"
    }
    exter_qual_mapping = {
      "Ex": "good", "Gd": "good", "Fa": "average", "TA": "average"
    }
    exter_cond_mapping = {
      "Ex": "good", "Gd": "good", "Po": "poor", "Fa": "poor", "TA": "poor"
    }
    heating_qc_mapping = {
      "Ex": "excellent", "Gd": "good", "Po": "poor", "Fa": "poor", "TA": "poor"
    }
    house_style_mapping = {
      "1.5Fin": "floors1.5", "1.5Unf": "floors1.5", "SFoyer": "floors1.5", "1Story": "floors1",
      "2.5Fin": "floors2", "2.5Unf": "floors2", "2Story": "floors2", "SLvl": "floors2"
    }
    kitchen_qual_mapping = {
      "Ex": "excellent", "Gd": "good", "Po": "poor", "Fa": "poor", "TA": "poor"
    }
    paved_drive_mapping = {
      "Y": "yes", "N": "no", "P": "no",
    }
    garage_finish_mapping = {
      "Fin": "finish", "RFn": "finish", "Unf": "unfinished",
    }
    bsmt_qual_mapping = {
      "Ex": "excellent", "Gd": "good", "Po": "poor", "Fa": "poor", "TA": "poor"
    }
    heating_qc_mapping = {
      "Ex": "excellent", "Gd": "good", "Po": "poor", "Fa": "poor", "TA": "poor"
    }
    garage_qual_mapping = {
      "Ex": "good", "Gd": "good", "Po": "poor", "Fa": "poor", "TA": "good"
    }
    garage_cond_mapping = {
      "Ex": "good", "Gd": "good", "Po": "poor", "Fa": "poor", "TA": "good"
    }
    fireplace_qu_mapping = {
      "Ex": "good", "Gd": "good", "Po": "poor", "Fa": "poor", "TA": "poor"
    }
  
    ames_data_preprocessed["ms_zoning"] = ames_data_preprocessed["ms_zoning"].replace(zone_mapping)
    ames_data_preprocessed["lot_shape"] = ames_data_preprocessed["lot_shape"].replace(lot_mapping)
    ames_data_preprocessed["functional"] = ames_data_preprocessed["functional"].replace(functional_mapping)
    ames_data_preprocessed["exter_qual"] = ames_data_preprocessed["exter_qual"].replace(exter_qual_mapping)
    ames_data_preprocessed["exter_cond"] = ames_data_preprocessed["exter_cond"].replace(exter_cond_mapping)
    ames_data_preprocessed["heating_qc"] = ames_data_preprocessed["heating_qc"].replace(heating_qc_mapping)
    ames_data_preprocessed["house_style"] = ames_data_preprocessed["house_style"].replace(house_style_mapping)
    ames_data_preprocessed["kitchen_qual"] = ames_data_preprocessed["kitchen_qual"].replace(kitchen_qual_mapping)
    ames_data_preprocessed["paved_drive"] = ames_data_preprocessed["paved_drive"].replace(paved_drive_mapping)
    ames_data_preprocessed["garage_finish"] = ames_data_preprocessed["garage_finish"].replace(garage_finish_mapping)
    ames_data_preprocessed["bsmt_qual"] = ames_data_preprocessed["bsmt_qual"].replace(bsmt_qual_mapping)
    ames_data_preprocessed["heating_qc"] = ames_data_preprocessed["heating_qc"].replace(heating_qc_mapping)
    ames_data_preprocessed["garage_qual"] = ames_data_preprocessed["garage_qual"].replace(garage_qual_mapping)
    ames_data_preprocessed["garage_cond"] = ames_data_preprocessed["garage_cond"].replace(garage_cond_mapping)
    ames_data_preprocessed["fireplace_qu"] = ames_data_preprocessed["fireplace_qu"].replace(fireplace_qu_mapping)



  if convert_categorical == "numeric":
    # Define mappings for different columns
    ms_zoning_mapping = {
        "RH": 3, "RM": 2, "RL": 1, "FV": 0
    }
    lot_shape_mapping = {
        "Reg": 0, "IR1": 1, "IR2": 2, "IR3": 3
    }
    functional_mapping = {
        "Typ": 8, "Min1": 7, "Min2": 6, "Mod": 5, "Maj1": 4, "Maj2": 3, "Sev": 2, "Sal": 1
    }
    house_style_mapping = {
        "1Story": 1, "SFoyer": 1, "SLvl": 1, "1.5Fin": 1.5, "1.5Unf": 1.5,
        "2Story": 2, "2.5Fin": 2.5, "2.5Unf": 2.5
    }
    paved_drive_mapping = {
       "Y": 1, "P": 0, "N":-1
    }
    garage_finish_mapping = {
      "Fin": 3, "RFn": 2, "Unf": 1, "other": 0
    }
    bsmt_exposure_mapping = {
      "Gd": 4, "Av": 3, "Mn": 2, "No": 1, "other": 0
    }
    bsmtfin_type_mapping = {
        "GLQ": 6, "ALQ": 5, "Rec": 4, "BLQ": 3, "LwQ": 2, "Unf": 1, "other": 0
    }

    # Apply the mappings using the replace() function
    ames_data_preprocessed["residential_density"] = ames_data_preprocessed["ms_zoning"].replace(ms_zoning_mapping)
    ames_data_preprocessed["irregular_lot_shape"] = ames_data_preprocessed["lot_shape"].replace(lot_shape_mapping)
    ames_data_preprocessed["functional"] = ames_data_preprocessed["functional"].replace(functional_mapping)
    ames_data_preprocessed["house_floors"] = ames_data_preprocessed["house_style"].replace(house_style_mapping)
    ames_data_preprocessed["paved_drive"] = ames_data_preprocessed["paved_drive"].replace(paved_drive_mapping)
    ames_data_preprocessed["garage_finish"] = ames_data_preprocessed["garage_finish"].replace(garage_finish_mapping)
    ames_data_preprocessed["bsmt_exposure"] = ames_data_preprocessed["bsmt_exposure"].replace(bsmt_exposure_mapping)
    ames_data_preprocessed["basement_finished_rating"] = ames_data_preprocessed["bsmtfin_type_1"].replace(bsmtfin_type_mapping)
    ames_data_preprocessed["basement_finished_rating2"] = ames_data_preprocessed["bsmtfin_type_2"].replace(bsmtfin_type_mapping)

    # For numeric columns, apply the mapping directly
    numeric_rating_columns = ["exter_qual", "exter_cond", "heating_qc", "kitchen_qual",
                              "bsmt_qual", "bsmt_cond", "garage_qual", "garage_cond", "fireplace_qu"]

    for column in numeric_rating_columns:
        mapping = {
            "Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "other": 0
        }
        ames_data_preprocessed[column] = ames_data_preprocessed[column].replace(mapping)

    ames_data_preprocessed = ames_data_preprocessed.drop(
       columns=["lot_shape", "ms_zoning", "bsmtfin_type_1", "house_style", "bsmtfin_type_2"])
    

  # create the dummy variables manually when simplified
  if convert_categorical == "simplified_dummy":
    ames_data_preprocessed["residential_density_high"] = np.where(ames_data_preprocessed["ms_zoning"] == "RH", 1, 0)
    ames_data_preprocessed["residential_density_mid"] = np.where(ames_data_preprocessed["ms_zoning"] == "RM", 1, 0)
    ames_data_preprocessed["residential_density_low"] = np.where(ames_data_preprocessed["ms_zoning"] == "RL", 1, 0)
    ames_data_preprocessed["residential_density_floating"] = np.where(ames_data_preprocessed["ms_zoning"] == "FV", 1, 0)
    ames_data_preprocessed["irregular_lot_shape"] = np.where(ames_data_preprocessed["lot_shape"].isin(["IR1", "IR2", "IR3"]), 1, 0)
    ames_data_preprocessed["home_functional"] = np.where(ames_data_preprocessed["functional"] == "Typ", 1, 0)
    ames_data_preprocessed["exter_qual_good"] = np.where(ames_data_preprocessed["exter_qual"].isin(["Gd", "Ex"]), 1, 0)
    ames_data_preprocessed["exter_cond_good"] = np.where(ames_data_preprocessed["exter_cond"].isin(["Gd", "Ex"]), 1, 0)
    ames_data_preprocessed["heating_qc_ex"] = np.where(ames_data_preprocessed["heating_qc"] == "Ex", 1, 0)
    ames_data_preprocessed["heating_qc_good"] = np.where(ames_data_preprocessed["heating_qc"] == "Gd", 1, 0)
    ames_data_preprocessed["house_1half_story"] = np.where(ames_data_preprocessed["house_style"].isin(["1.5Fin", "1.5Unf"]), 1, 0)
    ames_data_preprocessed["house_2story"] = np.where(ames_data_preprocessed["house_style"] == "2Story", 1, 0)
    ames_data_preprocessed["house_2half_story"] = np.where(ames_data_preprocessed["house_style"].isin(["2.5Fin", "2.5Unf"]), 1, 0)
    ames_data_preprocessed["kitchen_qual_good"] = np.where(ames_data_preprocessed["kitchen_qual"].isin(["Gd", "Ex"]), 1, 0)
    ames_data_preprocessed["paved_drive"] = np.where(ames_data_preprocessed["paved_drive"] == "Y", 1, 0)
    ames_data_preprocessed["garage_finish"] = np.where(ames_data_preprocessed["garage_finish"] == "Fin", 1, 0)
    ames_data_preprocessed["garage_rough_finish"] = np.where(ames_data_preprocessed["garage_finish"] == "RFn", 1, 0)
    ames_data_preprocessed["bsmt_qual_good"] = np.where(ames_data_preprocessed["bsmt_qual"].isin(["Ex", "Gd"]), 1, 0)
    ames_data_preprocessed["bsmt_cond_good"] = np.where(ames_data_preprocessed["bsmt_cond"].isin(["Ex", "Gd"]), 1, 0)
    ames_data_preprocessed["bsmt_exposure_good"] = np.where(ames_data_preprocessed["bsmt_exposure"] == "Gd", 1, 0)
    ames_data_preprocessed["bsmt_exposure_avg"] = np.where(ames_data_preprocessed["bsmt_exposure"] == "Av", 1, 0)
    ames_data_preprocessed["bsmt_exposure_min"] = np.where(ames_data_preprocessed["bsmt_exposure"] == "Mn", 1, 0)
    ames_data_preprocessed["basement_finished_good"] = np.where(ames_data_preprocessed["bsmtfin_type_1"].isin(["GLQ", "ALQ"]), 1, 0)
    ames_data_preprocessed["basement_finished_rec"] = np.where(ames_data_preprocessed["bsmtfin_type_1"] == "Rec", 1, 0)
    ames_data_preprocessed["basement_finished_low"] = np.where(ames_data_preprocessed["bsmtfin_type_1"].isin(["LwQ", "BLQ"]), 1, 0)
    ames_data_preprocessed["garage_qual_typical"] = np.where(ames_data_preprocessed["garage_qual"] == "TA", 1, 0)
    ames_data_preprocessed["garage_cond_typical"] = np.where(ames_data_preprocessed["garage_cond"] == "TA", 1, 0)
    ames_data_preprocessed["fireplace_qu_good"] = np.where(ames_data_preprocessed["fireplace_qu"].isin(["Ex", "Gd"]), 1, 0)

    # replace missing values in these columns with 0
    columns_to_fillna = [
      "exter_cond_good", "heating_qc_ex", "heating_qc_good",
      "house_1half_story", "house_2story", "house_2half_story",
      "kitchen_qual_good", "paved_drive", "garage_finish",
      "garage_rough_finish", "bsmt_qual_good", "bsmt_cond_good",
      "bsmt_exposure_good", "bsmt_exposure_avg", "bsmt_exposure_min",
      "basement_finished_good", "basement_finished_rec", "basement_finished_low",
      "garage_qual_typical", "garage_cond_typical",
      "fireplace_qu_good"
    ]

    # Apply fillna(0) to the specified columns
    ames_data_preprocessed[columns_to_fillna] = ames_data_preprocessed[columns_to_fillna].fillna(0)

    # remove variables we no longer need
    ames_data_preprocessed = ames_data_preprocessed.drop(columns=[
       "functional",
        "exter_qual",
        "exter_cond",
        "lot_shape", 
        "heating_qc",
        "ms_zoning", 
        "kitchen_qual",
        "bsmtfin_type_1",
        "garage_qual",
        "garage_cond",
        "fireplace_qu",
        "heating_qc",
        "bsmt_exposure",
        "bsmt_cond",
        "bsmt_qual",
        "house_style",
        "bsmtfin_type_2"
    ])


  # create the dummy variables using pd.get_dummies() when not simplified
  if convert_categorical == "dummy":

    ames_data_preprocessed = pd.get_dummies(
      ames_data_preprocessed, 
      columns=[
        "functional",
        "exter_qual",
        "exter_cond",
        "lot_shape",
        "heating_qc",
        "ms_zoning",
        "kitchen_qual",
        "bsmtfin_type_1",
        "garage_qual",
        "garage_cond",
        "fireplace_qu",
        "bsmt_exposure",
        "bsmt_cond",
        "bsmt_qual",
        "house_style",
        "bsmtfin_type_2"
      ],        
      drop_first=True
    )
        
  
  
  
  #------------------------ Handle identical values --------------------------#
  
  if len(column_selection) == 0:
    # get the proportion of the the most common value for each var
    prop_identical = ames_data_preprocessed.apply(lambda col: col.value_counts().values[0] / len(ames_data_preprocessed.index))
    vars_to_keep_nonidentical = prop_identical < max_identical_thresh

    # remove the variables above the threshold
    ames_data_preprocessed = ames_data_preprocessed.loc[:,vars_to_keep_nonidentical]

  
  #------------------------- Transformations ---------------------------------#
  
  # conduct log transformations
  if transform_response == "log":
    ames_data_preprocessed["saleprice"] = np.log(ames_data_preprocessed["saleprice"])

  elif transform_response == "sqrt":
    ames_data_preprocessed["saleprice"] = np.sqrt(ames_data_preprocessed["saleprice"])
    

  if log_transform_predictors != None:
    # log_transform_predictors should be a vector of predictors to transform
    ames_data_preprocessed[log_transform_predictors] = np.log(ames_data_preprocessed[log_transform_predictors])
  
  
  #----------------------- Correlation feature selection ---------------------#

  # select only features that are at least 0.5 correlated with response
  if (cor_feature_selection_threshold != None) & (len(column_selection) == 0):
    # compute pairwise correlations
    cor_saleprice = ames_data_preprocessed.select_dtypes(include="number") \
      .corr() \
      .drop(index=["saleprice"])
    # extract sale price correlations
    cor_saleprice = cor_saleprice["saleprice"]
    
    # identify variables whose corr with sale price is above the threshold
    high_cor_vars = cor_saleprice[(np.abs(cor_saleprice) >= cor_feature_selection_threshold)].index
    high_cor_vars = list(high_cor_vars)
    high_cor_vars.extend(["neighborhood", "saleprice"])
    # filter to just the highly correlated vars
    ames_data_preprocessed = ames_data_preprocessed[high_cor_vars]
    
  
  
  #--------------------------------- Tidying up ------------------------------#
  
  # create neighborhood dummy variables
  if neighborhood_dummy == True:
    ames_data_preprocessed = pd.get_dummies(
      ames_data_preprocessed, 
      columns=["neighborhood"], 
      prefix="neighborhood"
    ).drop(columns="neighborhood_other")
  

  # if specified, filter to the specified columns
  # this is helpful for ensuring that the validation and test sets have the 
  # same variables as the training set
  if len(column_selection) > 0:
    ames_data_preprocessed = ames_data_preprocessed[column_selection]
  
  # remove unneeded columns
  ames_data_preprocessed = ames_data_preprocessed.drop(columns=["date", "order", "ms_subclass"], errors='ignore')
    
  return ames_data_preprocessed
