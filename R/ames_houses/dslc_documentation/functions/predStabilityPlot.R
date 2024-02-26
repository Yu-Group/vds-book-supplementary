predStabilityPlot <- function(.perturbed_pred_df,
                              .true_var,
                              .pred_var,
                              .title = NULL) {
  
  perturbed_pred_interval <- .perturbed_pred_df |> 
    pivot_longer({{ .pred_var }}, 
                 names_to = "fit", values_to = "pred") |>
    group_by(pid, fit) |>
    # compute the range (interval) of predictions for each response
    summarise(true = unique({{ .true_var }}),
              min_pred = min(pred),
              max_pred = max(pred)) |>
    ungroup() 
  
  perturbed_pred_interval |>
    # plot the intervals
    ggplot() +
    geom_abline(intercept = 0, slope = 1, alpha = 0.5) +
    geom_segment(aes(y = true, yend = true, x = min_pred, xend = max_pred),
                 alpha = 0.5) +
    scale_y_continuous(name = "Observed sale response", labels = label_dollar()) +
    scale_x_continuous(name = "Predicted sale response range", labels = label_dollar())  +
    ggtitle(.title)
}
