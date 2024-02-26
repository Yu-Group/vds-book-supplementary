preProcessAmesData <- function(ames_data_clean,
                               column_selection = NULL,
                               max_identical_thresh = 0.8,
                               max_missing_thresh = 0.5,
                               neighborhood_levels = NULL,
                               n_neighborhoods = 10,
                               neighborhood_dummy = TRUE,
                               impute_missing_categorical = c("other", "mode"),
                               simplify_vars = TRUE,
                               log_transform_predictors = NULL,
                               transform_response = c("none", "log", "sqrt"),
                               cor_feature_selection_threshold = NULL,
                               convert_categorical = c("numeric", "simplified_dummy", "dummy", "none"),
                               keep_pid = FALSE) {
  
  transform_response <- match.arg(transform_response)
  convert_categorical <- match.arg(convert_categorical)
  impute_missing_categorical <- match.arg(impute_missing_categorical)
  
  ames_data_preprocessed <- ames_data_clean
  
  
  
  
  
  #------------------------- Handle missing values ---------------------------#
  
  if (is.null(column_selection)) {
    # if we have not specified which columns to keep
    # remove variables with more than max_missing_thresh missing proportion
    
    # identify the proportion of missing values for each column
    prop_missing <- ames_data_preprocessed |>
      map_dbl(~sum(is.na(.)) / nrow(ames_data_preprocessed))
    
    # remove the variables above the threshold
    ames_data_preprocessed <- ames_data_preprocessed |>
      select(one_of(names(prop_missing[prop_missing < max_missing_thresh])))
  }
  
  
  # assume that missing basement bathrooms and mas_vnr_area is 0
  ames_data_preprocessed <- ames_data_preprocessed |>
    mutate(bsmt_full_bath = replace_na(bsmt_full_bath, 0),
           bsmt_half_bath = replace_na(bsmt_half_bath, 0),
           full_bath = replace_na(full_bath, 0),
           half_bath = replace_na(half_bath, 0),
           mas_vnr_area = replace_na(mas_vnr_area, 0))
  
  # impute lot frontage with median lot frontage
  ames_data_preprocessed <- ames_data_preprocessed |>
    mutate(lot_frontage = replace_na(lot_frontage, 
                                     median(lot_frontage, na.rm = TRUE)))
  
  # impute categorical values per `impute_missing_categorical` argument
  if (impute_missing_categorical == "other") {
    ames_data_preprocessed <- ames_data_preprocessed |>
      mutate_if(is.factor, ~as.factor(replace_na(as.character(.), "other")))
  } else if (impute_missing_categorical == "mode") {
    ames_data_preprocessed <- ames_data_preprocessed |>
      # replace with most common entry
      mutate_if(is.factor, 
                ~replace_na(., names(sort(table(., useNA = "ifany"), decreasing = TRUE)[1])))
  }
  
  
  #--------------------- Neighborhood levels ---------------------------------#
  
  # if cleaning validation or testing data, you want the levels to match
  # the training data
  if (is.null(neighborhood_levels)) {
    # neighborhoods
    ames_data_preprocessed <- ames_data_preprocessed |>
      # lump uncommon neighborhoods together
      mutate(neighborhood = fct_lump(neighborhood,
                                     n = n_neighborhoods, 
                                     other_level = "other")) 
  } else {
    # convert all nhbd levels not provided in neighborhood_levels to "other"
    # this is helpful for ensuring that the validation and test sets have the 
    # same neighborhood levels as the training set
    excluded_neighborhoods <- !(unique(ames_data_preprocessed$neighborhood)) %in% neighborhood_levels
    levels_combine <- unique(ames_data_preprocessed$neighborhood)[excluded_neighborhoods] |>
      as.character()
    ames_data_preprocessed <- ames_data_preprocessed |>
      mutate(neighborhood = fct_collapse(neighborhood, 
                                         other = levels_combine))
  }
  
  
  #------------------------ Simplify variables -------------------------------#
  
  
  # manually simplify several variables with rare levels
  if (simplify_vars) {
    # if simplify_vars == TRUE, simplify more
    ames_data_preprocessed <- ames_data_preprocessed |>
      # manually simplify variables with many levels
      mutate(gable_roof = if_else(roof_style == "Gable", 1, 0),
             masonry_veneer_brick = if_else(mas_vnr_type %in% c("BrkFace", "BrkCmn"), 1, 0),
             foundation_cinder = if_else(foundation == "CBlock", 1, 0),
             foundation_concrete = if_else(foundation == "PConc", 1, 0),
             electrical_standard = if_else(electrical == "SBrkr", 1, 0),
             garage_attached = if_else(garage_type %in% c("Attchd", "BuiltIn", "2Types", "Basement"), 1, 0),
             lot_inside = if_else(lot_config == "Inside", 1, 0),
             no_proximity = if_else(condition_1 == "Norm", 1, 0),
             single_family_house = if_else(bldg_type == "1Fam", 1, 0),
             # combine 1st and 2nd floor variables
             exterior_vinyl = if_else(exterior_1st == "VinylSd" |
                                        exterior_2nd == "VinylSd", 1, 0),
             exterior_metal = if_else(exterior_1st == "MetalSd" |
                                        exterior_2nd == "MetalSd", 1, 0),
             exterior_hardboard = if_else(exterior_1st == "HdBoard" |
                                            exterior_2nd == "HdBoard", 1, 0),
             exterior_wood = if_else(exterior_1st == "Wd Sdng" |
                                       exterior_2nd == "Wd Sdng", 1, 0),
             # combine bathroom variables
             bathrooms = full_bath + 0.5 * half_bath + bsmt_full_bath + 0.5 * bsmt_half_bath,
             # combine porch variables
             porch = if_else(open_porch_sf != 0 |
                               enclosed_porch != 0 |
                               x3ssn_porch != 0 |
                               screen_porch != 0, 1, 0)) |>
      # remove the variables we no longer need
      select(-any_of(c("roof_style",
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
                       "x3ssn_porch",
                       "screen_porch",
                       # remove basement SF sub-variables if simplifying
                       "bsmt_unf_sf",
                       "bsmt_fin_sf_1",
                       "bsmt_fin_sf_1",
                       # remove general SF sub-variables if simplifying
                       "x1st_flr_sf", 
                       "x2nd_flr_sf", 
                       "low_qual_fin_sf")))
  } else {
    # if simplify_vars == FALSE, still simplify, but simplify less
    ames_data_preprocessed <- ames_data_preprocessed |>
      mutate(gable_roof = if_else(roof_style == "Gable", 1, 0),
             hip_roof = if_else(roof_style == "Hip", 1, 0),
             masonry_veneer_brick_face = if_else(mas_vnr_type == "BrkFace", 1, 0),
             masonry_veneer_none = if_else(mas_vnr_type == "BrkCmn", 1, 0),
             masonry_veneer_stone = if_else(mas_vnr_type == "Stone", 1, 0),
             foundation_brick = if_else(foundation == "BrkTil", 1, 0),
             foundation_cinder = if_else(foundation == "CBlock", 1, 0),
             foundation_concrete = if_else(foundation == "PConc", 1, 0),
             electrical_standard = if_else(electrical == "SBrkr", 1, 0),
             garage_attached = if_else(garage_type %in% c("Attchd"), 1, 0),
             garage_detached = if_else(garage_type %in% c("Detchd"), 1, 0),
             lot_inside = if_else(lot_config == "Inside", 1, 0),
             lot_corner = if_else(lot_config == "Corner", 1, 0),
             railroad_adjacent = if_else(condition_1 %in% c("RRAe", "RRAn",
                                                            "RRNe",
                                                            "RRNn"), 1, 0),
             main_street_adjacent = if_else(condition_1 %in% c("Artery", "Feedr"), 1, 0),
             positive_adjacent = if_else(condition_1 %in% c("PosA", "PosN"), 1, 0),
             single_family_house = if_else(bldg_type == "1Fam", 1, 0),
             townhouse = if_else(bldg_type %in% c("Twnhs", "TwnhsE"), 1, 0),
             exterior1_vinyl = if_else(exterior_1st == "VinylSd", 1, 0),
             exterior1_metal = if_else(exterior_1st == "MetalSd", 1, 0),
             exterior1_hardboard = if_else(exterior_1st == "HdBoard", 1, 0),
             exterior1_wood = if_else(exterior_1st == "Wd Sdng", 1, 0),
             exterior1_plywood = if_else(exterior_1st == "Plywood", 1, 0),
             exterior1_cement = if_else(exterior_1st == "CemntBd", 1, 0),
             exterior1_brick = if_else(exterior_1st == "BrkFace", 1, 0),
             exterior1_wood_shing = if_else(exterior_1st == "WdShing", 1, 0),
             exterior2_vinyl = if_else(exterior_2nd == "VinylSd", 1, 0),
             exterior2_metal = if_else(exterior_2nd == "MetalSd", 1, 0),
             exterior2_hardboard = if_else(exterior_2nd == "HdBoard", 1, 0),
             exterior2_wood = if_else(exterior_2nd == "Wd Sdng", 1, 0),
             exterior2_plywood = if_else(exterior_2nd == "Plywood", 1, 0),
             exterior2_cement = if_else(exterior_2nd == "CemntBd", 1, 0),
             exterior2_brick = if_else(exterior_2nd == "BrkFace", 1, 0),
             exterior2_wood_shing = if_else(exterior_2nd == "WdShing", 1, 0),
             porch_area = open_porch_sf + enclosed_porch + x3ssn_porch + screen_porch) |>
      # remove the variables we no longer need
      select(-any_of(c("roof_style",
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
                       "x3ssn_porch",
                       "screen_porch",
                       # or remove just one of the sub-SF variables
                       "bsmt_unf_sf",
                       "low_qual_fin_sf")))
  }
  
  
  
  
  
  #-------------------- Categorical to numeric -------------------------------#
  
  if (convert_categorical %in% c("dummy", "none")) {
    # simplify the uncommon levels to ensure that the validation set doesn't 
    # have levels that aren't in the training set
    ames_data_preprocessed <- ames_data_preprocessed |>
      mutate(ms_zoning = fct_collapse(ms_zoning,
                                      other = c("FV", "RH"),
                                      low_density = "RL",
                                      medium_density = "RM"),
             lot_shape = fct_collapse(lot_shape,
                                      regular = "Reg",
                                      irregular = c("IR1", "IR2", "IR3")),
             functional = fct_collapse(functional, 
                                       typical = "Typ",
                                       atypical = c("Maj1", "Maj2", "Min1", "Min2", "Mod")),
             exter_qual = fct_collapse(exter_qual, 
                                       good = c("Ex", "Gd"),
                                       average = c("Fa", "TA")),
             exter_cond = fct_collapse(exter_cond,  
                                       good = c("Ex", "Gd"), 
                                       poor = c("Po", "Fa", "TA")),
             heating_qc = fct_collapse(heating_qc,
                                       excellent = c("Ex"),
                                       good = c("Gd"),
                                       poor = c("Fa", "Po", "TA")),
             house_style = fct_collapse(house_style, 
                                        floors1.5 = c("1.5Fin", "1.5Unf", "SFoyer"),
                                        floors1 = c("1Story"),
                                        floors2 = c("2.5Fin", "2.5Unf", "2Story", "SLvl")),
             kitchen_qual = fct_collapse(kitchen_qual,
                                         excellent = c("Ex"),
                                         good = c("Gd"),
                                         poor = c("TA", "Po", "Fa")),
             paved_drive = fct_collapse(paved_drive, 
                                        yes = "Y",
                                        no = c("N", "P")),
             garage_finish = fct_collapse(garage_finish,
                                          finish = c("Fin", "RFn"),
                                          unfinished = c("Unf")),
             bsmt_qual = fct_collapse(bsmt_qual,
                                      excellent = "Ex",
                                      good = "Gd",
                                      average = c("TA", "Fa")),
             heating_qc = fct_collapse(heating_qc, 
                                       excellent = "Ex",
                                       good = c("Gd"),
                                       average = c("TA", "Fa", "Po")),
             garage_qual = fct_collapse(garage_qual,
                                        good = c("Ex", "Gd", "TA"),
                                        poor = c("Fa", "Po")),
             garage_cond = fct_collapse(garage_cond,
                                        good = c("Ex", "Gd", "TA"),
                                        poor = c("Fa", "Po")),
             fireplace_qu = fct_collapse(fireplace_qu,
                                         good = c("Ex", "Gd"),
                                         poor = c("TA", "Po", "Fa"))) |>
      suppressWarnings()
  } 
  if (convert_categorical == "numeric") {
    ames_data_preprocessed <- ames_data_preprocessed |>
      mutate(residential_density = case_when(ms_zoning == "RH" ~ 3,
                                             ms_zoning == "RM" ~ 2,
                                             ms_zoning == "RL" ~ 1,
                                             ms_zoning == "FV" ~ 0),
             irregular_lot_shape = case_when(lot_shape == "Reg" ~ 0,
                                             lot_shape == "IR1" ~ 1,
                                             lot_shape == "IR2" ~ 2,
                                             lot_shape == "IR3" ~ 3),
             functional = case_when(functional == "Typ" ~ 8,
                                    functional == "Min1" ~ 7,
                                    functional == "Min2" ~ 6,
                                    functional == "Mod" ~ 5,
                                    functional == "Maj1" ~ 4,
                                    functional == "Maj2" ~ 3,
                                    functional == "Sev" ~ 2,
                                    functional == "Sal" ~ 1),
             exter_qual = case_when(exter_qual == "Ex" ~ 5,
                                    exter_qual == "Gd" ~ 4,
                                    exter_qual == "TA" ~ 3,
                                    exter_qual == "Fa" ~ 2,
                                    exter_qual == "Po" ~ 1),
             exter_cond = case_when(exter_cond == "Ex" ~ 5,
                                    exter_cond == "Gd" ~ 4,
                                    exter_cond == "TA" ~ 3,
                                    exter_cond == "Fa" ~ 2,
                                    exter_cond == "Po" ~ 1),
             heating_qc = case_when(heating_qc == "Ex" ~ 5,
                                    heating_qc == "Gd" ~ 4,
                                    heating_qc == "TA" ~ 3,
                                    heating_qc == "Fa" ~ 2,
                                    heating_qc == "Po" ~ 1),
             house_floors = case_when(house_style %in% c("1Story", "SFoyer", "SLvl") ~ 1,
                                      house_style %in% c("1.5Fin", "1.5Unf") ~ 1.5,
                                      house_style %in% c("2Story") ~ 2,
                                      house_style %in% c("2.5Fin", "2.5Unf") ~ 2.5),
             kitchen_qual = case_when(kitchen_qual == "Ex" ~ 5,
                                      kitchen_qual == "Gd" ~ 4,
                                      kitchen_qual == "TA" ~ 3,
                                      kitchen_qual == "Fa" ~ 2,
                                      kitchen_qual == "Po" ~ 1),
             paved_drive = case_when(paved_drive == "Y" ~ 1,
                                     paved_drive == "P" ~ 0,
                                     paved_drive == "N" ~ -1),
             garage_finish = case_when(garage_finish == "Fin" ~ 3,
                                       garage_finish == "RFn" ~ 2,
                                       garage_finish == "Unf" ~ 1,
                                       garage_finish == "other" ~ 0),
             bsmt_qual = case_when(bsmt_qual == "Ex" ~ 5,
                                   bsmt_qual == "Gd" ~ 4,
                                   bsmt_qual == "TA" ~ 3,
                                   bsmt_qual == "Fa" ~ 2,
                                   bsmt_qual == "Po" ~ 1,
                                   bsmt_qual == "other" ~ 0),
             bsmt_cond = case_when(bsmt_cond == "Ex" ~ 5,
                                   bsmt_cond == "Gd" ~ 4,
                                   bsmt_cond == "TA" ~ 3,
                                   bsmt_cond == "Fa" ~ 2,
                                   bsmt_cond == "Po" ~ 1,
                                   bsmt_cond == "other" ~ 0),
             bsmt_exposure = case_when(bsmt_exposure == "Gd" ~ 4,
                                       bsmt_exposure == "Av" ~ 3,
                                       bsmt_exposure == "Mn" ~ 2,
                                       bsmt_exposure == "No" ~ 1,
                                       bsmt_exposure == "other" ~ 0),
             basement_finished_rating = case_when(bsmt_fin_type_1 == "GLQ" ~ 6,
                                                  bsmt_fin_type_1 == "ALQ" ~ 5,
                                                  bsmt_fin_type_1 == "Rec" ~ 4,
                                                  bsmt_fin_type_1 == "BLQ" ~ 3,
                                                  bsmt_fin_type_1 == "LwQ" ~ 2,
                                                  bsmt_fin_type_1 == "Unf" ~ 1,
                                                  bsmt_fin_type_1 == "other" ~ 0),
             basement_finished_rating2 = case_when(bsmt_fin_type_2 == "GLQ" ~ 6,
                                                   bsmt_fin_type_2 == "ALQ" ~ 5,
                                                   bsmt_fin_type_2 == "Rec" ~ 4,
                                                   bsmt_fin_type_2 == "BLQ" ~ 3,
                                                   bsmt_fin_type_2 == "LwQ" ~ 2,
                                                   bsmt_fin_type_2 == "Unf" ~ 1,
                                                   bsmt_fin_type_2 == "other" ~ 0),
             garage_qual = case_when(garage_qual == "Ex" ~ 5,
                                     garage_qual == "Gd" ~ 4,
                                     garage_qual == "TA" ~ 3,
                                     garage_qual == "Fa" ~ 2,
                                     garage_qual == "Po" ~ 1,
                                     garage_qual == "other" ~ 0),
             garage_cond = case_when(garage_cond == "Ex" ~ 5,
                                     garage_cond == "Gd" ~ 4,
                                     garage_cond == "TA" ~ 3,
                                     garage_cond == "Fa" ~ 2,
                                     garage_cond == "Po" ~ 1,
                                     garage_cond == "other" ~ 0),
             fireplace_qu = case_when(fireplace_qu == "Ex" ~ 5,
                                      fireplace_qu == "Gd" ~ 4,
                                      fireplace_qu == "TA" ~ 3,
                                      fireplace_qu == "Fa" ~ 2,
                                      fireplace_qu == "Po" ~ 1,
                                      fireplace_qu == "other" ~ 0)) |>
      select(-lot_shape, 
        -ms_zoning, 
        -bsmt_fin_type_1, 
        -house_style,
        -bsmt_fin_type_2)
  } 
  # create the dummy variables manually when simplified
  if (convert_categorical == "simplified_dummy") {
    ames_data_preprocessed <- ames_data_preprocessed |>
      mutate(residential_density_high = if_else(ms_zoning == "RH", 1, 0, missing = 0),
             residential_density_mid = if_else(ms_zoning == "RM", 1, 0, missing = 0),
             residential_density_low = if_else(ms_zoning == "RL", 1, 0, missing = 0),
             residential_density_floating = if_else(ms_zoning == "FV", 1, 0, missing = 0),
             irregular_lot_shape = if_else(lot_shape %in% c("IR1", "IR2", "IR3"), 1, 0, missing = 0),
             home_functional = if_else(functional == "Typ", 1, 0, missing = 0),
             exter_qual_good = if_else(exter_qual %in% c("Gd", "Ex"), 1, 0, missing = 0),
             exter_cond_good = if_else(exter_cond %in% c("Gd", "Ex"), 1, 0, missing = 0),
             heating_qc_ex = if_else(heating_qc == "Ex", 1, 0, missing = 0),
             heating_qc_good = if_else(heating_qc == "Gd", 1, 0, missing = 0),
             house_1half_story = if_else(house_style %in% c("1.5Fin", "1.5Unf"), 1, 0, missing = 0),
             house_2story = if_else(house_style %in% c("2Story"), 1, 0, missing = 0),
             house_2half_story = if_else(house_style %in% c("2.5Fin", "2.5Unf"), 1, 0, missing = 0),
             kitchen_qual_good = if_else(kitchen_qual %in% c("Gd", "Ex"), 1, 0, missing = 0),
             paved_drive = if_else(paved_drive == "Y", 1, 0, missing = 0),
             garage_finish = if_else(garage_finish == "Fin", 1, 0, missing = 0),
             garage_rough_finish = if_else(garage_finish == "RFn", 1, 0, missing = 0),
             bsmt_qual_good = if_else(bsmt_qual %in% c("Ex", "Gd"), 1, 0, missing = 0),
             bsmt_cond_good = if_else(bsmt_cond %in% c("Ex", "Gd"), 1, 0, missing = 0),
             bsmt_exposure_good = if_else(bsmt_exposure == "Gd", 1, 0, missing = 0),
             bsmt_exposure_avg = if_else(bsmt_exposure == "Av", 1, 0, missing = 0),
             bsmt_exposure_min = if_else(bsmt_exposure == "Mn", 1, 0, missing = 0),
             basement_finished_good = if_else(bsmt_fin_type_1 %in% c("GLQ", "ALQ"), 1, 0, missing = 0),
             basement_finished_rec = if_else(bsmt_fin_type_1 == "Rec", 1, 0, missing = 0),
             basement_finished_low = if_else(bsmt_fin_type_1 %in% c("LwQ", "BLQ"), 1, 0, missing = 0),
             heating_qc_good = if_else(heating_qc %in% c("Ex", "Gd"), 1, 0, missing = 0),
             garage_qual_typical = if_else(garage_qual == "TA", 1, 0, missing = 0),
             garage_cond_typical = if_else(garage_cond == "TA", 1, 0, missing = 0),
             fireplace_qu_good = if_else(fireplace_qu %in% c("Ex", "Gd"), 1, 0, missing = 0)) |>
      # remove variables we no longer need
      select(-functional,
        -exter_qual,
        -exter_cond,
        -lot_shape, 
        -heating_qc,
        -ms_zoning, 
        -kitchen_qual,
        -bsmt_fin_type_1,
        -garage_qual,
        -garage_cond,
        -fireplace_qu,
        -heating_qc,
        -bsmt_exposure,
        -bsmt_cond,
        -bsmt_qual,
        -house_style,
        -bsmt_fin_type_2)
  } 
  # create the dummy variables using dummy_cols() when not simplified
  if (convert_categorical == "dummy") {
    ames_data_preprocessed <- ames_data_preprocessed |>
      dummy_cols(select_columns = c(
        "functional",
        "exter_qual",
        "exter_cond",
        "lot_shape", 
        "heating_qc",
        "ms_zoning", 
        "kitchen_qual",
        "bsmt_fin_type_1",
        "garage_qual",
        "garage_cond",
        "fireplace_qu",
        "heating_qc",
        "bsmt_exposure",
        "bsmt_cond",
        "bsmt_qual",
        "house_style",
        "bsmt_fin_type_2"),
        remove_first_dummy = TRUE)
  } 
  
  
  
  
  
  #------------------------ Handle identical values --------------------------#
  
  if (is.null(column_selection)) {
    prop_identical_values <- ames_data_preprocessed |> 
      # get the proportion of the the most common value
      map_dbl(~sort(table(.), decreasing = TRUE)[1] / nrow(ames_data_preprocessed)) 
    
    # identify the variables that are above the threshold of identical values
    vars_identical_values <-  which(prop_identical_values > max_identical_thresh) |>
      names()
    
    # remove these variables
    ames_data_preprocessed <- ames_data_preprocessed |>
      select(-one_of(vars_identical_values))
  }
  
  #------------------------- Transformations ---------------------------------#
  
  # conduct log transformations
  if (transform_response == "log") {
    ames_data_preprocessed <- ames_data_preprocessed |>
      mutate(sale_price = log(sale_price))
  } else if (transform_response == "sqrt") {
    ames_data_preprocessed <- ames_data_preprocessed |>
      mutate(sale_price = sqrt(sale_price))
  } 
  
  if (!is.null(log_transform_predictors)) {
    # log_transform_predictors should be a vector of predictors to transform
    ames_data_preprocessed <- ames_data_preprocessed |>
      mutate_at(vars(one_of(log_transform_predictors)), log)
  }
  
  #----------------------- Correlation feature selection ---------------------#
  
  # select only features that are at least 0.5 correlated with response
  if (!is.null(cor_feature_selection_threshold) & is.null(column_selection)) {
    cor_df <- cor(select_if(ames_data_preprocessed, is.numeric))[, "sale_price"] |> 
      enframe() |>
      filter(!(name %in% c("sale_price", "pid"))) |>
      arrange(desc(abs(value))) 
    
    high_cor_vars <- cor_df |> 
      filter(abs(value) >= cor_feature_selection_threshold) |>
      pull(name)
    ames_data_preprocessed <-  ames_data_preprocessed |>
      select(one_of(high_cor_vars, "sale_price", "neighborhood"))
    
  }
  
  #--------------------------------- Tidying up ------------------------------#
  
  # create neighborhood dummy variables
  if (neighborhood_dummy) {
    # separate into dummy variables
    ames_data_preprocessed <- ames_data_preprocessed |> 
      mutate(one = 1) |>
      mutate(id_tmp = 1:n()) |>
      pivot_wider(names_from = neighborhood, 
                  names_prefix = "neighborhood_",
                  values_from = one, 
                  values_fill = list(one = 0)) |>
      # remove reference variable
      select(-neighborhood_other, -id_tmp) 
  }
  

  # if specified, filter to the specified columns
  # this is helpful for ensuring that the validation and test sets have the 
  # same variables as the training set
  if (!is.null(column_selection)) {
    ames_data_preprocessed <- ames_data_preprocessed |>
      select(one_of(column_selection), "pid")
  }
  
  
  # place sale_price first
  ames_data_preprocessed <- ames_data_preprocessed |>
    relocate(sale_price, everything()) |>  
    # remove some variables we don't need
    select(-any_of(c("date", "order", "ms_sub_class")))
  
  if (!keep_pid) {
    ames_data_preprocessed <- ames_data_preprocessed |>
      select(-any_of("pid"))
  }
  
  return(as_tibble(ames_data_preprocessed))
}

