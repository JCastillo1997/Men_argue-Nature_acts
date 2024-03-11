def make_predictions_for_df(joined_df, num_predictions):
    from joblib import load
    import pandas as pd
    
    model_path = "C:\\Users\\Usuario\\Documents\\Men_argue-Nature_acts\\APP\\model\\pred_model.joblib"
      
    
    columns_to_drop = ['latitude', 'longitude', 'name', 'country', 'is_capital', 'population','co','overall_aqi']
    
    
    modified_joined_df = joined_df.copy()
    
    
    modified_joined_df = modified_joined_df.drop(columns_to_drop, axis=1, errors='ignore')
    
    
    model = load(model_path)
    
    
    expanded_df = pd.concat([modified_joined_df] * (num_predictions // len(modified_joined_df) + 1), ignore_index=True)
    expanded_df = expanded_df.iloc[:num_predictions]

    
    predictions = model.predict(expanded_df)
    
    
    predictions_df = pd.DataFrame(predictions, columns=modified_joined_df.columns)
    
    
    for col in columns_to_drop:
        if col in joined_df.columns:
            predictions_df[col] = joined_df[col].iloc[:predictions_df.shape[0]].values

    
    return predictions_df