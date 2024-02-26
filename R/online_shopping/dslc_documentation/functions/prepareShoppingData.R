# Preparing (cleaning/pre-processing) the shopping data and split into training, validation, test sets
source("functions/preprocessShoppingData.R")

# load in the original data
shopping_orig <- read_csv("../data/online_shoppers_intention.csv")

# split into training, validation, and testing
set.seed(24648765)
shopping_orig <- shopping_orig %>%
  mutate(id = 1:n())
# split into training, testing, and validation
shopping_train <- shopping_orig %>% sample_frac(0.6) 
shopping_test <- shopping_orig %>% filter(!(id %in% shopping_train$id)) %>%
  sample_frac(0.5) 
shopping_val <- shopping_orig %>% 
  filter(!(id %in% shopping_train$id) & !(id %in% shopping_test$id)) 

# save these datasets as csv files so that we can use them in the python analysis
# write_csv(select(shopping_train, -id), "../data/train_val_test/shopping_train.csv")
# write_csv(select(shopping_val, -id), "../data/train_val_test/shopping_val.csv")
# write_csv(select(shopping_test, -id), "../data/train_val_test/shopping_test.csv")




# clean each dataset
shopping_train_preprocessed <- preprocessShoppingData(shopping_train)

# create version of training data without dummy variables
shopping_train_preprocessed_nodummy <- 
  preprocessShoppingData(shopping_train, .dummy = FALSE)
# extract training levels for categorical variables
operating_systems_levels <- 
  levels(shopping_train_preprocessed_nodummy$operating_systems)
browser_levels <- 
  levels(shopping_train_preprocessed_nodummy$browser)
traffic_type_levels <- 
  levels(shopping_train_preprocessed_nodummy$traffic_type)

# preprocess val data
shopping_val_preprocessed <- 
  preprocessShoppingData(shopping_val, 
                         .operating_systems_levels = operating_systems_levels, 
                         .browser_levels = browser_levels, 
                         .traffic_type_levels = traffic_type_levels, 
                         .column_selection = colnames(shopping_train_preprocessed),
                         .id = TRUE)

shopping_val_preprocessed_nodummy <- 
  preprocessShoppingData(shopping_val, .dummy = FALSE)


# preprocess test data
shopping_test_preprocessed <- 
  preprocessShoppingData(shopping_test,
                         .operating_systems_levels = operating_systems_levels, 
                         .browser_levels = browser_levels, 
                         .traffic_type_levels = traffic_type_levels,
                         .column_selection = colnames(shopping_train_preprocessed))



