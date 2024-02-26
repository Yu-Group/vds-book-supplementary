# Supplementary Code and Data for the Veridical Data Science Book

This repository contains supplementary Python and R code and data for the book "*Veridical Data Science: The Practice of Responsible Data Analysis and Decision Making*" by Bin Yu and Rebecca Barter.

## Reporting issues

Please use this repository to report any issues (such as errors or typos) for both the book and the supplementary materials by creating a new "Issue" for this repository.

## Downloading the supplementary materials in this repository

Note that the `food_nutrient.csv` data file is too large to store on GitHub. This means, that when you clone this repository, **this data file will be missing**.

You therefore have two options for downloading the supplementary materials.



### Option 1: Clone the repository using `git clone` and manually download the `food_nutrient.csv` data file

If you cloned this repository, and you want to work through the nutrition examples, you will need to download the [`food_nutrient.csv`](https://drive.google.com/file/d/16bbTE2EphlXLNSivQFi4jBYr8ehgQ5w8/view?usp=sharing) file. 

After downloading this file, you will need to place it in the `R/nutrition/data/` or `python/nutrition/data/` folder for the relevant code to work.


### Option 2: Download all materials using Google Drive

I have uploaded the R and Python VDS folders to Google Drive, and you can manually download them using the following links:

- [R code and data](https://drive.google.com/file/d/1UxD2QTNo_JD2mURPwIALIyxrnO0RQPp-/view?usp=sharing)

- [Python code and data](https://drive.google.com/file/d/1KicL3QXKkQGIeng3JidyXf_WUJKnHAcw/view?usp=sharing)

The .zip files are quite large but are under 1GB.

Note that changes made to the repo files will not automatically be reflected in these links. If you notice any discrepancies, please file an issue to let us know!



## Summary

The code and data provided in this repository are designed to reflect the projects that are discussed in the book as well as the exercise projects. 

The project code serves as a practical example to demonstrate one way to implement each of the techniques described in the book. 

While you will find both R and Python code in this repository, the examples and results that are shown in the book were all created using R. Since there is not always a 1-to-1 equivalence between R and Python, you will generally find that the results computed using R will more closely match the results shown in the book than those computed using the Python code that you will find in this repository. 

The Python code and data are located in the `python` directory, and the R code and data are located in the `R` directory. 

## Projects and Exercises by Chapter

The code in this repository is organized by project. The top-level folders in the `R/` and `python/` directories correspond to the in-chapter projects (i.e., the projects that are used to demonstrate the technique throughout the chapter), while the subfolders in the `R/exercises/` and `python/exercises` directories correspond to the projects that you are asked to complete in the exercises. 

The following table provides a reference for which chapters are associated with each project.

| Chapter | In-chapter project | Exercises project |
| --- | --- | --- |
| Chapter 1 | `bushfires/` | `reading/` |
| Chapter 2 | N/A | `reading/` & `government_spending/` |
| Chapter 3 | N/A |  N/A |
| Chapter 4 | `organ_donations/` | `reading/` & `growth_debt/` |
| Chapter 5 | `organ_donations/` | `growth_debt/` |
| Chapter 6 | `nutrition/` | `penguins/` |
| Chapter 7 | `nutrition/` | `smartphone/` |
| Chapter 8 | `ames_housing/` | N/A |
| Chapter 9 | `ames_housing/` | `exam_scores/` & `hapiness/` |
| Chapter 10 | `ames_housing/` | `happiness/` |
| Chapter 11 | `online_shopping/`  | `diabetes_nhanes/` |
| Chapter 12 | `ames_housing/` & `online_shopping/` | `happiness/` & `diabetes_nhanes/` |
| Chapter 13 | `ames_housing/` & `online_shopping/` | `happiness/` & `diabetes_nhanes/` |


