import pandas as pd
import numpy as np
import datetime


from functions.clean_ames_data import clean_ames_data
from functions.preprocess_ames_data import preprocess_ames_data



## load in the original data
ames_orig = pd.read_table("../data/AmesHousing.txt", sep="\t", header=0, 
                          na_values=["", "NA"], keep_default_na=False)


## The following code would define the training, validation, and test set equivalent to what was done in R:
## We won't run it because we are going to use the same versions of the training, validation, and test sets that
## were used in the book so that our results match the book as closely as possible
## These results will be slightly different because we can't match the random seed used in R

## filter to just the relevant portion of the data
# ames = ames_orig.copy()
# ames = ames.query("(`Sale Condition` == 'Normal') & (`MS Zoning` != ['A (agr)', 'C (all)', 'I (all)'])")
# ames = ames.drop(columns="Sale Condition")

## compute the date
# ames["date"] = pd.to_datetime(dict(year=ames["Yr Sold"], month=ames["Mo Sold"], day=1))
# split_date = ames["date"].quantile(0.6)
# split_date_month = int(split_date.month)
# split_date_year = int(split_date.year)

## this code would define the training, validation, and test set equivalent to what was done in R
# ames_train = ames.query("`Mo Sold` <= @split_date_month & `Yr Sold` <= @split_date_year")
## filter to houses not in training set
# ames_val = ames.query("~PID.isin(@ames_train.PID)")
## randomly select half of the houses for the validation set
# ames_val = ames_val.sample(round(len(ames_val.index)*0.5), random_state=3789)
## filter to houses not in training and validation sets for the test set
# ames_test = ames.query("~PID.isin(@ames_train.PID) & ~PID.isin(@ames_val.PID)")

## Since we want to use the same training, validation, test set that was used in the book, we will 
## instead load the versions of the training, validation, and test sets that were computed in R
## so that our results match the book as closely as possible
ames_train = pd.read_csv("../data/train_val_test/ames_train.csv",
                         na_values=["", "NA"], keep_default_na=False)
ames_val = pd.read_csv("../data/train_val_test/ames_val.csv",
                       na_values=["", "NA"], keep_default_na=False)
ames_test = pd.read_csv("../data/train_val_test/ames_test.csv",
                        na_values=["", "NA"], keep_default_na=False)

# clean the original data
ames_train_clean = clean_ames_data(ames_train)
ames_val_clean = clean_ames_data(ames_val)
ames_test_clean = clean_ames_data(ames_test)

ames_train_preprocessed = preprocess_ames_data(ames_train_clean)

# extract the neighborhoods included in the training data
# this is to ensure that the validation and test sets only include the 
# same neighborhoods as the training data
neighborhood_cols = list(ames_train_preprocessed.filter(regex="neighborhood").columns)
train_neighborhoods = [x.replace("neighborhood_", "") for x in neighborhood_cols]

# create preprocessed validation set
ames_val_preprocessed = preprocess_ames_data(
    ames_val_clean,
    column_selection=list(ames_train_preprocessed.columns),
    neighborhood_levels=train_neighborhoods
)

# create preprocessed test set
ames_test_preprocessed = preprocess_ames_data(
    ames_test_clean,
    column_selection=list(ames_train_preprocessed.columns),
    neighborhood_levels=train_neighborhoods
)