import pandas as pd
import numpy as np


from functions.preprocess_shopping_data import preprocess_shopping_data


## load in the original data
shopping_orig = pd.read_csv('../data/online_shoppers_intention.csv')


## The following code would define the training, validation, and test set equivalent to what was done in R:
## We won't run it because we are going to use the same versions of the training, validation, and test sets that
## were used in the book so that our results match the book as closely as possible
## These results will be slightly different because we can't match the random seed used in R

## filter to just the relevant portion of the data
# shopping = shopping_orig.copy()

## this code would define the training, validation, and test set equivalent to what was done in R
# shopping_train = shopping.sample(frac=0.6, random_state=3789)
## filter to sessions not in training set and randomly sample 50% of those for validation set
# shopping_val = shopping[~shopping.index.isin(shopping_train.index)].sample(frac=0.5, random_state=23789)
# the test set is then the remaining sessions
# shopping_test = shopping[~shopping.index.isin(shopping_train.index) & ~shopping.index.isin(shopping_val.index)] 


## Since we want to use the same training, validation, test set that was used in the book, we will 
## instead load the versions of the training, validation, and test sets that were computed in R
## so that our results match the book as closely as possible
shopping_train = pd.read_csv("../data/train_val_test/shopping_train.csv")
shopping_val = pd.read_csv("../data/train_val_test/shopping_val.csv")
shopping_test = pd.read_csv("../data/train_val_test/shopping_test.csv")

# clean the original data
shopping_train_preprocessed_nodummy = preprocess_shopping_data(shopping_train, dummy=False)
shopping_train_preprocessed = preprocess_shopping_data(shopping_train)

# create preprocessed validation set
shopping_val_preprocessed = preprocess_shopping_data(
    shopping_val,
    column_selection=list(shopping_train_preprocessed.columns),
    operating_systems_levels=shopping_train_preprocessed_nodummy['operating_systems'].unique(),
    browser_levels=shopping_train_preprocessed_nodummy['browser'].unique(),
    traffic_type_levels=shopping_train_preprocessed_nodummy['traffic_type'].unique()
)

# create preprocessed test set
shopping_test_preprocessed = preprocess_shopping_data(
    shopping_test,
    column_selection=list(shopping_train_preprocessed.columns),
    operating_systems_levels=shopping_train_preprocessed_nodummy['operating_systems'].unique(),
    browser_levels=shopping_train_preprocessed_nodummy['browser'].unique(),
    traffic_type_levels=shopping_train_preprocessed_nodummy['traffic_type'].unique(),
    remove_extreme=True
)