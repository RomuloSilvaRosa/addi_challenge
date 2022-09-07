import sys
BASE_PATH = "./lambdas/model_trainning"
sys.path.append(BASE_PATH)

from main import handler
from pathlib import Path
import pandas as pd
import sys



pwd = Path(BASE_PATH)
df = pd.read_csv(pwd.joinpath("data/UCI_Credit_Card.csv"))
data = df.loc[0].to_dict()
handler(data, None)
