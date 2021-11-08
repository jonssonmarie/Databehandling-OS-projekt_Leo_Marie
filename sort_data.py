from load_data import create_df

athlete_event, noc_regions = create_df()

medalists = athlete_event.dropna(subset='Medal')

winter = medalists[medalists['Season'] == 'Winter']
summer = medalists[medalists['Season'] == 'Summer']
