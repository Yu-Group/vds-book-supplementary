# running the pre-processing and cleaning function for the Ames data
library(tidyverse)
library(lubridate)
library(janitor)

source("functions/cleanAmesData.R")
source("functions/preProcessAmesData.R")
# load in the original data
ames_orig <- read.table("../data/AmesHousing.txt",
                               sep = "\t", header = T)
# filter to just the relevant portion of the data
ames <- ames_orig |> 
  filter(Sale.Condition == "Normal",
         # remove agricultural, commercial and industrial
         !(MS.Zoning %in% c("A (agr)", "C (all)", "I (all)"))) |>
  dplyr::select(-Sale.Condition)

# split into training, validation, and testing
split_date <- ames_orig |>
  unite(date, Mo.Sold, Yr.Sold, 
        sep = "/", remove = FALSE) |>
  mutate(date = parse_date(date, "%m/%Y")) |>
  summarise(quantile(date, c(0.6), type = 1)) |>
  pull() |>
  ymd()
# Errata note: the following code is what is used in the book, but is incorrect. 
# define the training set
ames_train <- ames |>
  filter(Mo.Sold <= month(split_date), Yr.Sold <= year(split_date))
# This should be 
# ames_train <- ames |>
#    filter(Yr.Sold <= year(split_date) | (Mo.Sold <= month(split_date) & Yr.Sold == year(split_date)))


# define the validation set
set.seed(286734) # Do not change this seed once you have started using it!
ames_val <- ames |>
  # filter to the houses no in the training set
  filter(!(PID %in% ames_train$PID)) |>
  # take a random sample of half
  sample_frac(0.5)
ames_test <- ames |>
  # filter to the houses not in the training set or validation set
  filter(!(PID %in% c(ames_val$PID, ames_train$PID)))


# save the data so that we can use the same training, validation, and test 
# sets in python
write_csv(ames_train, "../data/train_val_test/ames_train.csv")
write_csv(ames_val, "../data/train_val_test/ames_val.csv")
write_csv(ames_test, "../data/train_val_test/ames_test.csv")


# clean the original data
ames_train_clean <- cleanAmesData(ames_train)
ames_val_clean <- cleanAmesData(ames_val)
ames_test_clean <- cleanAmesData(ames_test)




ames_train_preprocessed <- preProcessAmesData(ames_train_clean)

# extract the neighborhoods included in the training data
# this is to ensure that the validation and test sets only include the 
# same neighborhoods as the training data
train_neighborhoods <- ames_train_preprocessed |> 
  dplyr::select(contains("neighborhood_")) |>
  colnames() |>
  str_split("neighborhood_") |>
  map_chr(~.[2])

# create preprocessed validation set
ames_val_preprocessed <- 
  preProcessAmesData(ames_val_clean, 
                     column_selection = colnames(ames_train_preprocessed),
                     neighborhood_levels = train_neighborhoods,
                     keep_pid = TRUE)

# create preprocessed test set
ames_test_preprocessed <- 
  preProcessAmesData(ames_test_clean, 
                     column_selection = colnames(ames_train_preprocessed),
                     neighborhood_levels = train_neighborhoods)


