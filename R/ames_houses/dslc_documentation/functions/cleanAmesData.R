# Cleaning function for the Ames housing data

# Clean the Ames data
cleanAmesData <- function(ames_data) {
  
  # Replace 'blank' categorical entries with `NA`
  ames_data <- ames_data |>
    mutate_if(is.character, 
              function(.x) if_else(.x == "",  
                                   true = as.character(NA), 
                                   false = .x))
  
  # Convert the character variables to factors.
  ames_data <- ames_data |>
    mutate_if(is.character, as.factor)
  
  # impute missing garage year with house built year
  ames_data <- ames_data |> 
    mutate(Garage.Yr.Blt = if_else(!is.na(Garage.Yr.Blt), 
                                     Garage.Yr.Blt, 
                                     Year.Built))
  
  # replace `Year.Remod.Add` value of 1950 with the `Year.Built` value
  ames_data <- ames_data |> 
    mutate(Year.Remod.Add = if_else(Year.Remod.Add == 1950, 
                                    Year.Built, 
                                    Year.Remod.Add))
  
  # create a date variable
  ames_data <- ames_data |>
    unite(date, Mo.Sold, Yr.Sold, 
          sep = "/", remove = FALSE) |>
    mutate(date = parse_date(date, "%m/%Y"))
  
  # clean the column names
  ames_data <- clean_names(ames_data)
  
  return(ames_data)
}

