def make_predictions_for_df(joined_df, num_predictions, model_path):
    from sklearn.ensemble import RandomForestRegressor
    import pandas as pd
    import joblib
    
    model = joblib.load(model_path)
    expanded_df = pd.concat([joined_df] * (num_predictions // len(joined_df) + 1), ignore_index=True)
    expanded_df = expanded_df.iloc[:num_predictions]
    predictions = model.predict(expanded_df)
    return predictions