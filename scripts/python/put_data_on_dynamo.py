import sys

import pandas as pd

sys.path.append("./codes/model_orchestrator")
from src.gateways.aws.dynamodb.credit_card_feature_store import \
    CreditCardFeatureStoreGateway


def put_data(indexes):
    df = pd.read_csv("./codes/model_trainning/data/UCI_Credit_Card.csv")

    df.set_index("ID", inplace=True)
    df.rename(columns={"PAY_0": "PAY_1"}, inplace=True)
    features = df.drop("default.payment.next.month", axis=1)
    # target = df["default.payment.next.month"]
    values = features.iloc[indexes]
    values_dict = values.reset_index().to_dict(orient='records')
    for x in values_dict:
        x_id = x.pop("ID")
        print(x)
        CreditCardFeatureStoreGateway.insert_data(x_id, x)


INDEXES = [0, 1]
put_data(INDEXES)
