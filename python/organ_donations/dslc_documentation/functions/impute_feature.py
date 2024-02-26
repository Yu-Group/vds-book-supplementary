def impute_feature(data, feature, group, impute_method="average"):
    impute_method = impute_method.lower()
    
    if impute_method == "previous":
        data = (data.assign(feature_imputed=data[feature]) # create a new variable called feature_imputed that is equal to feature
                    .groupby(group) # group by 
                    .fillna(method='ffill') # impute using forward fill
                    .fillna(0)) # impute remaining missing values with 0
        return data["feature_imputed"]
    elif impute_method == "average":
        # create two temporary variables each equal to feature
        data = data.assign(imputed_feature_tmp_prev=data[feature], imputed_feature_tmp_next=data[feature])
        # fill the first variable using forward fill
        data["imputed_feature_tmp_prev"] = data.groupby(group)["imputed_feature_tmp_prev"].fillna(method='ffill')
        # fill the second variable using backward fill
        data["imputed_feature_tmp_next"] = data.groupby(group)["imputed_feature_tmp_next"].fillna(method='bfill')
        # then define feature_imputed column to be the mean of the forward and backward filled values
        data['feature_imputed'] = data[['imputed_feature_tmp_next', 'imputed_feature_tmp_prev']].mean(axis=1, skipna=True)
        # impute any remaining missing values with 0
        data['feature_imputed'].fillna(0, inplace=True)
        # remove the two temporary variables
        data = data.drop(columns=['imputed_feature_tmp_prev', 'imputed_feature_tmp_next'])
        return data["feature_imputed"]
    else:
        raise ValueError