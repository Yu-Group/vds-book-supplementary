# Cleaning/pre-processing the shopping data

preprocessShoppingData <- function(shopping_data,
                                   .replace_negative_na = TRUE,
                                   .numeric_to_cat = TRUE,
                                   .remove_missing = TRUE,
                                   .impute_missing = FALSE,
                                   .durations_to_minutes = TRUE,
                                   .visitor_binary = TRUE,
                                   .dummy = TRUE,
                                   .month_numeric = FALSE,
                                   .log_page = FALSE,
                                   .remove_extreme = FALSE,
                                   # arguments for ensuring training/val/test sets match up
                                   .operating_systems_levels = NULL,
                                   .browser_levels = NULL,
                                   .traffic_type_levels = NULL,
                                   .column_selection = NULL, 
                                   .id = FALSE) {
  
  shopping <- shopping_data |>
    # clean the names
    clean_names() |>
    # reorder the response levels so 1 is first and rename it to "purchase"
    mutate(purchase = fct_relevel(as.factor(as.numeric(revenue)), "1")) |>
    dplyr::select(-revenue)
  
  # convert weekend to numeric
  shopping <- shopping |>
    mutate(weekend = as.numeric(weekend))
  
  # replace negative values with NA
  if (.replace_negative_na) {
    shopping <- shopping |> 
      mutate(administrative_duration = if_else(administrative_duration < 0, 
                                               true = NA_real_, 
                                               false = administrative_duration),
             informational_duration = if_else(informational_duration < 0, 
                                              true = NA_real_, 
                                              false = informational_duration),
             product_related_duration = if_else(product_related_duration < 0, 
                                                true = NA_real_, 
                                                false = product_related_duration))
  } # otherwise leave them as they are
  
  # convert numeric features to categorical
  if (.numeric_to_cat) {
    shopping <- shopping |>
      mutate(operating_systems = as.factor(operating_systems),
             browser = as.factor(browser),
             traffic_type = as.factor(traffic_type),
             region = as.factor(region))
  } 
  
  # convert durations to minutes
  if (.durations_to_minutes) {
    shopping <- shopping |>
      mutate_at(vars(contains("duration")), ~. / 60)
  }
  
  
  
  # convert visitor_type to binary variable
  if (.visitor_binary) {
    shopping <- shopping |>
      mutate(return_visitor = as.numeric(visitor_type == "Returning_Visitor")) |>
      dplyr::select(-visitor_type)
  }
  
  
  # remove rows with missing values
  if(.remove_missing) {
    shopping <- shopping |>
      drop_na()
  } else if (.impute_missing) {
    # otherwise impute with 0
    shopping <- shopping |>
      mutate_if(is.numeric, ~replace_na(., 0))
  }
  
  # combine rare levels of categorical variables
  # match to the provided levels (for validation and test sets)
  
  # operating systems:
  if (is.factor(shopping$operating_systems) & !is.null(.operating_systems_levels)) {
    # identify levels that aren't included in the provided levels vector
    excluded_operating_systems <- !(unique(shopping$operating_systems) %in% .operating_systems_levels)
    # Combine them into an "other" category
    operating_systems_levels_combine <- unique(shopping$operating_systems)[excluded_operating_systems] |>
      as.character()
    shopping <- shopping |>
      mutate(operating_systems = fct_collapse(operating_systems, 
                                              other = operating_systems_levels_combine))
  } else if (is.factor(shopping$operating_systems) & is.null(.operating_systems_levels)) {
    # otherwise, just lump any levels with fewer than 50 occurences into an "other" category
    shopping <- shopping |>
      mutate(operating_systems = fct_lump_min(operating_systems, 50, 
                                              other_level = "other"))
  }
  # browser:
  if (is.factor(shopping$browser) & !is.null(.browser_levels)) {
    # identify levels that aren't included in the provided levels vector
    excluded_browser <- !(unique(shopping$browser) %in% .browser_levels)
    # Combine them into an "other" category
    browser_levels_combine <- unique(shopping$browser)[excluded_browser] |>
      as.character()
    shopping <- shopping |>
      mutate(browser = fct_collapse(browser, 
                                    other = browser_levels_combine))
  } else if (is.factor(shopping$browser) & is.null(.browser_levels)) {
    # otherwise, just lump any levels with fewer than 50 occurences into an "other" category
    shopping <- shopping |>
      mutate(browser = fct_lump_min(browser, 50, 
                                    other_level = "other"))
  }
  # traffic type
  if (is.factor(shopping$traffic_type) & !is.null(.traffic_type_levels)) {
    # identify levels that aren't included in the provided levels vector
    excluded_traffic_type <- !(unique(shopping$traffic_type) %in% .traffic_type_levels)
    # Combine them into an "other" category
    traffic_type_levels_combine <- unique(shopping$traffic_type)[excluded_traffic_type] |>
      as.character()
    shopping <- shopping |>
      mutate(traffic_type = fct_collapse(traffic_type, 
                                         other = traffic_type_levels_combine))
  } else if (is.factor(shopping$traffic_type) & is.null(.traffic_type_levels)) {
    # otherwise, just lump any levels with fewer than 50 occurences into an "other" category
    shopping <- shopping |>
      mutate(traffic_type = fct_lump_min(traffic_type, 50, 
                                         other_level = "other"))
  }
  
  
  
  # should we treat month as categorical or numeric?
  if (.month_numeric) {
    shopping <- shopping |>
      mutate(month = case_when(month == "Feb" ~ 2,
                               month == "Mar" ~ 3,
                               month == "May" ~ 5, 
                               month == "June" ~ 6,
                               month == "Jul" ~ 7,
                               month == "Aug" ~ 8,
                               month == "Sep" ~ 9, 
                               month == "Oct" ~ 10, 
                               month == "Nov" ~ 11, 
                               month == "Dec" ~ 12))
  } else {
    shopping <- shopping |>
      mutate(month = factor(month))
  }
  
  
  # create dummy variables
  if (.dummy) {
    # identify the names of the categorical variables
    fct_vars <- shopping |> 
      dplyr::select(where(is.factor), -purchase) |>
      colnames()
    # if there is at least one categorical variable
    if (length(fct_vars) > 0) {
      # convert them to dummy variables
      shopping <- shopping |>
        dummy_cols(select_columns = fct_vars, 
                   remove_first_dummy = TRUE, 
                   remove_selected_columns = TRUE)
    }
    
  }
  
  # remove extreme
  if (.remove_extreme) {
    shopping <- shopping |>
      filter(product_related <= 400,
             product_related_duration <= 720 * 60)
  }
  
  
  
  # log-tranform predictors
  if (.log_page) {
    shopping <- shopping |>
      mutate(administrative = log(administrative + 1),
             informational = log(informational + 1),
             product_related = log(product_related + 1),
             administrative_duration = log(administrative_duration + 1),
             informational_duration = log(informational_duration + 1),
             product_related_duration = log(product_related_duration + 1),
             exit_rates = log(exit_rates + 0.0001),
             bounce_rates = log(bounce_rates + 0.00001))
  }
  
  
  # filter to specified columns (helpful for making val/test sets match training set)
  if (!is.null(.column_selection)) {
    shopping <- shopping |>
      dplyr::select(one_of(.column_selection, "id"))
  } 
  
  if (!.id) {
    shopping <- shopping |>
      dplyr::select(-one_of("id"))
  }
  
  return(shopping)
}

