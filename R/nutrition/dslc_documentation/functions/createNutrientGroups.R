# A function for creating the separate nutrient group datasets
createNutrientGroups <- function(.food_data) {
  
  food_fats <- .food_data %>% 
    select(contains(c("_acid", "fat", "cholesterol"))) 
  
  food_vitamins <- .food_data %>%
    select(beta_carotene, alpha_carotene, lutein_zeaxanthin, phylloquinone, vitamin_c, riboflavin, thiamine, folate, niacin, vitamin_b6, alpha_tocopherol, retinol, vitamin_b12, lycopene, cryptoxanthin)
  
  food_major_minerals <- .food_data %>%
    select(sodium, potassium, calcium, phosphorus, magnesium, total_choline)
  
  food_trace_minerals <- .food_data %>%
    select(iron, zinc, selenium, copper)
  
  food_carbs <- .food_data %>%
    select(total_dietary_fiber, carbohydrates)
  
  # return a tibble with list columns: each entry corresponds to one of the 
  # nutrient datasts
  return(tibble(nutrient_group = c("fats", "vitamins", "major_minerals", 
                                   "trace_minerals", "carbs"),
                data = list(food_fats, food_vitamins, food_major_minerals, 
                            food_trace_minerals, food_carbs),
                description = list(.food_data$description,
                                   .food_data$description,
                                   .food_data$description,
                                   .food_data$description,
                                   .food_data$description)))
}
