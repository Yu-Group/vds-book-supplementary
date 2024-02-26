# Cleaning function for the organ donation data



prepareOrganData <- function(.organs_original,
                             .impute_method = c("average", "previous"),
                             .vars_to_impute = c("population", "total_deceased_donors"),
                             .per_mil_vars = TRUE) {
  
  # identify which imputation method is specified
  .impute_method <- match.arg(.impute_method)
  
  # define a cleaned version of the original organs data
  organs_clean <- .organs_original |>
    # rename all variables
    select(region = REGION,
           country = COUNTRY,
           year = REPORTYEAR,
           population = POPULATION,
           total_deceased_donors = `TOTAL Actual DD`,
           deceased_donors_brain_death = `Actual DBD`,
           deceased_donors_circulatory_death = `Actual DCD`,
           total_utilized_deceased_donors = `Total Utilized DD`,
           utilized_deceased_donors_brain_death = `Utilized DBD`,
           utilized_deceased_donors_circulatory_death = `Utilized DCD`,
           deceased_kidney_tx = `DD Kidney Tx`,
           living_kidney_tx = `LD Kidney Tx`,
           total_kidney_tx = `TOTAL Kidney Tx`,
           deceased_liver_tx = `DD Liver Tx`,
           living_liver_tx = `LD Liver Tx`,
           domino_liver_tx = `DOMINO Liver Tx`,
           total_liver_tx = `TOTAL Liver TX`,
           total_heart_tx = `Total Heart`,
           deceased_lung_tx = `DD Lung Tx`,
           living_lung_tx = `DD Lung Tx`,
           total_lung_tx = `TOTAL Lung Tx`,
           total_pancreas_tx = `Pancreas Tx`,
           total_kidney_pancreas_tx = `Kidney Pancreas Tx`,
           total_small_bowel_tx = `Small Bowel Tx`) |>
    # add in the missing rows with NAs (complete the data)
    complete(country, year) |>
    # for newly added rows, fill region with the unique values from the 
    # pre-existing rows
    group_by(country) |>
    mutate(region = if_else(is.na(region), 
                            true = unique(na.omit(region)), 
                            false = region)) |>
    ungroup() |>
    # multiply the population variable by 1 million
    mutate(population = population * 1000000)
  
  # add imputed features using the specified imputation method
  # imputeFeature() is a custom function defined in imputeFeature.R
  # Note that we are only imputing the total_deceased_donors variable and the 
  # population variable (missing values were introduced when we 
  # "completed" the data). You could impute more variables if you wanted to.
  if (!is.null(.impute_method)) {
    
    organs_clean <- organs_clean |>
      mutate(population_imputed = imputeFeature(organs_clean, 
                                                .feature = population,
                                                .group = country,
                                                .impute_method = .impute_method),
             total_deceased_donors_imputed = imputeFeature(organs_clean, 
                                                           .feature = total_deceased_donors,
                                                           .group = country,
                                                           .impute_method = .impute_method))
  }
  
  # rearrange the columns 
  organs_clean <- organs_clean |> 
    select(country, year, region, 
           population, population_imputed, 
           total_deceased_donors, total_deceased_donors_imputed,
           everything())
  
  return(organs_clean)
}
