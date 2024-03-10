def make_predictions_for_df(joined_df, num_predictions):
    from joblib import load
    import pandas as pd
    # Define the model path
    model_path = "C:\\Users\\Usuario\\Documents\\Men_argue-Nature_acts\\APP\\model\\pred_model.joblib"
      
    # Define which columns we want to drop for the predictions
    columns_to_drop = ['latitude', 'longitude', 'name', 'country', 'is_capital', 'population','co','overall_aqi']
    
    # Create a copy of the original DataFrame to work with
    modified_joined_df = joined_df.copy()
    
    # Drop specified columns from the copied DataFrame
    modified_joined_df = modified_joined_df.drop(columns_to_drop, axis=1, errors='ignore')
    
    # Load the model from the provided path
    model = load(model_path)
    
    # Expand the DataFrame to match the desired number of predictions
    expanded_df = pd.concat([modified_joined_df] * (num_predictions // len(modified_joined_df) + 1), ignore_index=True)
    expanded_df = expanded_df.iloc[:num_predictions]

    # Make predictions using the model
    predictions = model.predict(expanded_df)
    
    # Create a new DataFrame for predictions with the original columns
    predictions_df = pd.DataFrame(predictions, columns=modified_joined_df.columns)
    
    # Reintegrate the removed columns back into the predictions DataFrame
    for col in columns_to_drop:
        if col in joined_df.columns:
            predictions_df[col] = joined_df[col].iloc[:predictions_df.shape[0]].values

    
    return predictions_df