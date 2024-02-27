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


## Data Sources

Each data source is referenced in the book, but the following list provides the sources for each dataset.

### Organ donation data

The organ donation data comes from Global Observatory on Donation and Transplantation (GODT) and was collected in a collaboration between the World Health Organization (WHO) and the Spanish Transplant Organization, Organización Nacional de Trasplantes (ONT). The data portal can be found at [http://www.transplant-observatory.org/export-database/](http://www.transplant-observatory.org/export-database/).

### Nutrition data

The nutrition food data comes from the US Department of Agriculture's (USDA) **Food and Nutrient Database for Dietary Studies (FNDDS)**, which contains nutrient information compiled for the foods and beverages reported in the "What We Eat in America" survey.

The nutrition databases and associated information from the UDSA website can be found at [https://fdc.nal.usda.gov/](https://fdc.nal.usda.gov/).

### Ames housing data


The Ames housing data comes from information on houses sold in Ames from 2006 to 2010 that has been [provided by Dean DeCock](https://jse.amstat.org/v19n3/decock.pdf). According to the paper that he wrote about this dataset, De Cock obtained this data directly from the Ames City Assessor's Office. 

### Online shopping data

The Online Shoppers Purchasing Intention Dataset has been made publicly available by [Sakar et al.](https://www.semanticscholar.org/paper/Real-time-prediction-of-online-shoppers%E2%80%99-purchasing-Sakar-Polat/747e098f85ca2d20afd6313b11242c0c427e6fb3) and can be [downloaded from the UCI Machine Learning repository](https://archive.ics.uci.edu/ml/datasets/Online+Shoppers+Purchasing+Intention+Dataset).]

### Government spending data

The government spending data originally comes from the American Association for the Advancement of Science Historical Trends, and the version that we are using was collated for the [Tidy Tuesday project](https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-02-12).


### Growth & Debt data

For this exercise project, the historical public debt data was downloaded from the [International Monetary Fund (IMF)](https://www.imf.org/external/datamapper/datasets) and the gross domestic product (GDP) growth data was downloaded from the [World Bank](https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG).


### Penguins data

The palmer penguins exercise data comes from the [`palmerpenguins` R package](https://allisonhorst.github.io/palmerpenguins/) curated by Horst, Hill and Gorman.


### Smartphone activity data

The smartphone activity exercise data was collected by [Anguita et al.](https://link.springer.com/chapter/10.1007/978-3-642-35395-6_30) and was downloaded from [the UCI Machine Learning repository](https://archive.ics.uci.edu/ml/datasets/human+activity+recognition+using+smartphones)


### Happiness data

The world happiness exercise data comes from the [World Happiness Report](https://worldhappiness.report/ed/2018)

### Diabetes NHANES data

The diabetes NHANES data comes from the collected from the 2016 release of the [National Health and Nutrition Examination Survey (NHANES)](https://www.cdc.gov/nchs/nhanes/index.htm), a program of studies designed to assess the health and nutritional status of adults and children in the United States.