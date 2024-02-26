import pandas as pd
import numpy as np

def preprocess_shopping_data(shopping_data,
                            replace_negative_na=True,
                            numeric_to_cat=True,
                            remove_missing=True,
                            impute_missing=False,
                            durations_to_minutes=True,
                            visitor_binary=True,
                            dummy=True,
                            month_numeric=False,
                            log_page=False,
                            remove_extreme=False,
                            operating_systems_levels=None,
                            browser_levels=None,
                            traffic_type_levels=None,
                            column_selection=None):
    
    shopping = shopping_data.copy()

    # manually add underscores for column names that use CamelCase, e.g., change "OperatingSystems" to "Operating_Systems"
    shopping = shopping.rename(columns={'ProductRelated': 'Product_Related',
                                        'ProductRelated_Duration': 'Product_Related_Duration',
                                        'BounceRates': 'Bounce_Rates',
                                        'ExitRates': 'Exit_Rates',
                                        'PageValues': 'Page_Values',
                                        'SpecialDay': 'Special_Day',
                                        'OperatingSystems': 'Operating_Systems',
                                        'TrafficType': 'Traffic_Type',
                                        'VisitorType': 'Visitor_Type'})
                                        
                                        
    
    
    
    # change the name of the column "Revenue" to "purchase"
    shopping['purchase'] = shopping['Revenue']
    shopping = shopping.drop(columns=['Revenue'])
    
    # convert weekend to numeric
    shopping['Weekend'] = shopping['Weekend'].astype(int)
    
    # replace negative duration values with NA
    if replace_negative_na:
        shopping[["Administrative_Duration", "Informational_Duration", "Product_Related_Duration"]] = shopping[["Administrative_Duration", "Informational_Duration", "Product_Related_Duration"]].apply(lambda x: x.where(x >= 0))
    
    # convert operating systems, browser, traffic type and region numeric features to categorical 
    if numeric_to_cat:
        shopping[["Operating_Systems", "Browser", "Traffic_Type", "Region"]] = shopping[["Operating_Systems", "Browser", "Traffic_Type", "Region"]].astype(str)
    
    # convert durations to minutes
    if durations_to_minutes:
        shopping[["Administrative_Duration", "Informational_Duration", "Product_Related_Duration"]] = shopping[["Administrative_Duration", "Informational_Duration", "Product_Related_Duration"]].apply(lambda x: x/60)
    
    # convert visitor type to binary numeric (ignoring "other")
    if visitor_binary:
        shopping['Visitor_Type'] = shopping['Visitor_Type'].map({'Returning_Visitor': 1, 'New_Visitor': 0, 'Other': 0})
    
    # remove rows with missing values or impute them with 0
    if remove_missing:
        shopping = shopping.dropna()
    elif impute_missing:
        shopping = shopping.fillna(0)
        
    # combine rare levels of categorical variables
    # match to the provided levels (for validation and test sets)
    # operating systems:
    if operating_systems_levels is not None:
        shopping['Operating_Systems'] = shopping['Operating_Systems'].apply(lambda x: x if x in operating_systems_levels else "Other")
    else:
        # just lump any levels with fewer than 50 occurences into "Other"
        shopping['Operating_Systems'] = shopping['Operating_Systems'].apply(lambda x: x if shopping['Operating_Systems'].value_counts()[x] >= 50 else "Other")
    # traffic type:
    if traffic_type_levels is not None:
        shopping['Traffic_Type'] = shopping['Traffic_Type'].apply(lambda x: x if x in traffic_type_levels else "Other")
    else:
        shopping['Traffic_Type'] = shopping['Traffic_Type'].apply(lambda x: x if shopping['Traffic_Type'].value_counts()[x] >= 50 else "Other")
    # browser:
    if browser_levels is not None:
        shopping['Browser'] = shopping['Browser'].apply(lambda x: x if x in browser_levels else "Other")
    else:
        shopping['Browser'] = shopping['Browser'].apply(lambda x: x if shopping['Browser'].value_counts()[x] >= 50 else "Other")
    
    # convert month to numeric
    if month_numeric:
        shopping['Month'] = shopping['Month'].map({'Feb': 2, 'Mar': 3, 'May': 5, 'June': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12})
    
    # create dummy variables for categorical features
    if dummy:
        shopping = pd.get_dummies(shopping, drop_first=True)
    
    # remove extreme product-related duration observations
    if remove_extreme:
        shopping = shopping[(shopping['Product_Related_Duration'] < 400) & (shopping['Product_Related_Duration'] <= 720 * 60)]
        
    # convert boolean variables to integer variables
    bool_columns = shopping.columns[shopping.dtypes == bool]
    # do not convert purchase to integer
    bool_columns = bool_columns[bool_columns != 'purchase']
    shopping[bool_columns] = shopping[bool_columns].astype(int)    
        
    # log-transform predictors
    if log_page:
        # log-transform predictors
        if log_page:
            shopping[['Administrative', 'Informational', 'Product_Related', 'Administrative_Duration', 'Informational_Duration', 'Product_Related_Duration']] = np.log(shopping[['Administrative', 'Informational', 'Product_Related', 'Administrative_Duration', 'Informational_Duration', 'Product_Related_Duration']] + 1)
            shopping[['Exit_Rates']] = np.log(shopping[['Exit_Rates']] + 0.0001)
            shopping[['Bounce_Rates']] = np.log(shopping[['Bounce_Rates']] + 0.00001)
    
    # clean column names
    shopping.columns = shopping.columns.str.replace(' ', '_').str.lower()
    shopping = shopping.rename(columns={"productrelated": "product_related", 
                                        "productrelated_duration": "product_related_duration", 
                                        "bouncerates": "bounce_rates",
                                        "exitrates": "exit_rates",
                                        "pagevalues": "page_values",
                                        "specialday": "special day",
                                        "operatingsystems": "operating_systems",
                                        "traffictype": "traffic_type",
                                        "visitortype": "visitor_type"})
    
    # filter to specified columns (helpful for making val/test sets match training set)
    if column_selection is not None:
        shopping = shopping[column_selection]
        
    shopping = shopping.reset_index(drop=True)
    
    return shopping
