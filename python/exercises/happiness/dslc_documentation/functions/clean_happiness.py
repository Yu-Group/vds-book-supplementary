

# a function for cleaning the world happiness dataset
def clean_happiness(happiness_orig, predictor_variable = None):
  # rename column names
  happiness_clean = happiness_orig.rename(columns={
    "Life Ladder": "happiness",
    "Log GDP per capita": "log_gdp_per_capita",
    "Social support": "social_support",
    "Healthy life expectancy at birth": "life_expectancy",
    "Freedom to make life choices": "freedom_choices",
    "Generosity": "generosity",
    "Perceptions of corruption": "corruption",
    "Positive affect": "positive_affect",
    "Negative affect": "negative_affect", 
    "Confidence in national government": "government_confidence",
    "gini of household income reported in Gallup, by wp5-year": "gini_index"})
  # filter to relevant columns
  happiness_clean = happiness_clean[["country", "year", "happiness", "log_gdp_per_capita",
                                     "social_support", "life_expectancy",
                                     "freedom_choices", "generosity",
                                     "corruption", "positive_affect", 
                                     "negative_affect", "government_confidence",
                                     "gini_index"]]
  
  if (predictor_variable is not None): 
    happiness_clean = happiness_clean[["country", "year", "happiness", predictor_variable]]
  
  return(happiness_clean)

