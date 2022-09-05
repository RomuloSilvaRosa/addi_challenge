from main import handler
import pandas as pd

df = pd.read_csv('./data/UCI_Credit_Card.csv')
data = df.loc[0].to_dict()
print(data)
handler(data, None)