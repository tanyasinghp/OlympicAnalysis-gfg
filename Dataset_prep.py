import pandas as pd
import numpy as np

df = pd.read_csv('medals.csv')
df.drop('country_code', axis=1, inplace=True)
df.drop('country_3_letter_code', axis=1, inplace=True)
df.drop('participant_title', axis=1, inplace=True)
df.drop('athlete_url', axis=1, inplace=True)
df['country_name'] = df['country_name'].replace('Soviet Union', 'Russian Federation')
df['country_name'] = df['country_name'].replace('German Democratic Republic (Germany)', 'Germany')
df['country_name'] = df['country_name'].replace('Olympic Athletes from Russia', 'Russian Federation')
df['country_name'] = df['country_name'].replace('ROC', 'Russian Federation')
def dset():
    return df