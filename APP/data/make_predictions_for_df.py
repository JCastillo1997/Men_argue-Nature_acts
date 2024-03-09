def make_predictions_for_df(joined_df, num_predictions):
    # Assuming you have imported RandomForestRegressor
    from sklearn.ensemble import RandomForestRegressor
    import pandas as pd
    import joblib

    # Load the model (assuming it's a RandomForestRegressor)
    model_path = "C://Users//Usuario//Documents//Men_argue-Nature_acts//APP//model//pred_model.joblib"
    model = joblib.load(model_path)

    # Expand the joined DataFrame to create a larger dataset for making predictions
    expanded_df = pd.concat([joined_df] * (num_predictions // len(joined_df) + 1), ignore_index=True)
    expanded_df = expanded_df.iloc[:num_predictions]

    # Apply the model's prediction method to the expanded DataFrame
    predictions = model.predict(expanded_df)

    return predictions