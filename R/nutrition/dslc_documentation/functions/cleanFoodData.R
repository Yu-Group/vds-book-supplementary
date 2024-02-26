# Cleaning function for the food data

# Clean the food data
cleanFoodData <- function(.nutrient_amount_data,
                          .food_name_data,
                          .nutrient_name_data,
                          .select_data_type = c("survey_fndds_food",
                                               "branded_food",
                                               "foundation_food",
                                               "sr_legacy_food",
                                               "sub_sample_food",
                                               "agricultural_acquisition")) {
  
  .select_data_type <- match.arg(.select_data_type)
  
  # filter the nutrient and food ID datasets to the relevant columns and
  nutrient_amount_lite <- .nutrient_amount_data |> 
    select(fdc_id, nutrient_id, amount) 
  food_name_lite <- .food_name_data |> 
    select(fdc_id, data_type, description)
  
  # join the tables to create one dataset
  food_clean <- nutrient_amount_lite |> 
    left_join(food_name_lite, by = "fdc_id") |>
    left_join(.nutrient_name_data, by = "nutrient_id") 
  
  # filter to just fndds foods (default)
  food_clean <- food_clean |> 
    filter(data_type %in% .select_data_type)
  
  # convert to wide tidy form
  food_clean <- food_clean |>
    distinct(description, amount, nutrient_name) |>
    drop_na(nutrient_name) |>
    pivot_wider(values_from = amount, 
                names_from = nutrient_name, 
                # non-unique "branded_food" measurements will be averaged
                values_fn = mean)
  
  return(food_clean)
}

