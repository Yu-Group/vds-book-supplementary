

# a function for cleaning the world happiness dataset
cleanHappiness <- function(happiness_orig,
                           .predictor_variable = NULL) {
  happiness_clean <- happiness_orig %>%
    select(country = country, 
           year = year,
           happiness = `Life Ladder`,
           log_gdp_per_capita = `Log GDP per capita`,
           social_support = `Social support`,
           life_expectancy = `Healthy life expectancy at birth`,
           freedom_choices = `Freedom to make life choices`,
           generosity = Generosity,
           corruption = `Perceptions of corruption`,
           positive_affect = `Positive affect`,
           negative_affect = `Negative affect`,
           government_confidence = `Confidence in national government`,
           gini_index = `gini of household income reported in Gallup, by wp5-year`)
  
  if (!is.null(.predictor_variable)) {
    happiness_clean <- happiness_clean %>%
      select(all_of(c("country", "year", "happiness", .predictor_variable)))
  }
  return(happiness_clean)
}
