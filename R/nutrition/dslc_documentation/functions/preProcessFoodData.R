# Preprocessing function for the food data


# perform pre-processing steps
preProcessFoodData <- function(.food_clean, 
                               .log_transform = TRUE,
                               .center = TRUE,
                               .scale = TRUE,
                               .remove_fat = FALSE) {
  
  food_pre_processed <- .food_clean
  # perform log transformation
  if (.log_transform) {
    food_pre_processed <- food_pre_processed |>
      mutate(across(where(is.numeric), ~log(. + 1)))
  } 
  
  # perform centering
  if (.center) {
    food_pre_processed <- food_pre_processed |>
      mutate(across(where(is.numeric), ~(. - mean(., .na.rm = T))))
  } 
  # perform SD-scaling
  if (.scale) {
    food_pre_processed <- food_pre_processed |>
      mutate(across(where(is.numeric), ~(. / sd(., na.rm = T))))
  }
  
  if (.remove_fat) {
    food_pre_processed <- food_pre_processed |>
      select(-fat)
  }
  
  # do some mean imputation
  food_pre_processed <- food_pre_processed %>%
    mutate(across(where(is.numeric), ~if_else(is.na(.), mean(., na.rm = T), .)))
  
  
  return(food_pre_processed)
}
