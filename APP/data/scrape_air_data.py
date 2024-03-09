
def scrape_air_data(returned_url):
    import pandas as pd

    df_time = pd.read_html(returned_url)[0]
    df_similar = pd.read_html(returned_url)[1]
    df_stations = pd.read_html(returned_url)[2]
    df_index = pd.read_html(returned_url)[3]
    df_poll = pd.read_html(returned_url)[4]
    df_recomendations = pd.read_html(returned_url)[5]
    df_temp_pol_wind = pd.read_html(returned_url)[6]

    return df_time, df_similar, df_stations, df_index, df_poll, df_recomendations, df_temp_pol_wind