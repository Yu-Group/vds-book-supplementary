
# function for conducting the imputation of a specified feature
imputeFeature <- function(.data,
                          .feature,
                          .group,
                          .impute_method = c("average", "previous")) {
  # identify which imputation method is being used
  .impute_method <- match.arg(.impute_method)
  
  if (.impute_method == "previous") {
    .data <- .data |>
      # duplicate the relevant column and call it "feature_imputed"
      # this {{ }} notation is "tidy eval" - it allows us to pass unquoted 
      # variable names
      mutate(feature_imputed = {{ .feature }}) |>
      # for each .group (country)
      group_by({{ .group }}) |>
      # use the fill function from the tidyr package (part of the tidyverse)
      # to impute the relevant feature
      fill(feature_imputed, .direction = "down") |>
      ungroup() |>
      # for entries whose values are still missing (e.g., countries with no 
      # data reported), fill the missing value with 0
      mutate(feature_imputed = if_else(is.na(feature_imputed), 0, feature_imputed))
  } else if (.impute_method == "average") {
    .data <- .data |>
      # duplicate the relevant column two times and call these duplicates
      # "feature_imputed_tmp_prev" and "feature_imputed_tmp_next"
      # we will fill the missing values in these columns with the previous and 
      # next non-missing values respectively
      # this {{ }} notation is "tidy eval" - it allows us to pass unquoted 
      # variable names
      mutate(imputed_feature_tmp_prev = {{ .feature }},
             imputed_feature_tmp_next = {{ .feature }}) |>
      # for each .group (country)
      group_by({{ .group }}) |>
      # use the fill function to impute the missing values with previous 
      # non-missing value 
      fill(imputed_feature_tmp_prev, .direction = "down") |>
      # use the fill function to impute the missing values with next 
      # non-missing value
      fill(imputed_feature_tmp_next, .direction = "up") |>
      ungroup() |>
      # compute the imputation as the average of the previous and next imputed 
      # value for each row.
      rowwise() |>
      mutate(feature_imputed = mean(c(imputed_feature_tmp_next, 
                                    imputed_feature_tmp_prev), na.rm = T)) |>
      # for entries whose values are still missing (e.g., countries with no 
      # data reported), fill the missing value with 0
      mutate(feature_imputed = if_else(is.nan(feature_imputed), 0, feature_imputed)) |>
      # remove the two prev, next columns
      select(-imputed_feature_tmp_prev, -imputed_feature_tmp_next)
  }
  # return just the imputed feature
  return(pull(.data, feature_imputed))
}
