import sys

import pandas as pd

sys.path.append("./lambdas/model_orchestrator")
from src.gateways.aws.dynamodb.credit_card_feature_store import \
    CreditCardFeatureStoreGateway


TARGET_COL = "default.payment.next.month"

def put_data(indexes):
    df = pd.read_csv("./lambdas/model_trainning/data/UCI_Credit_Card.csv")

    df.set_index("ID", inplace=True)
    df.rename(columns={"PAY_0": "PAY_1"}, inplace=True)
    
    values = df.loc[indexes]
    values_dict = values.reset_index().to_dict(orient='records')
    for x_ in values_dict:
        x = x_.copy()
        x.pop(TARGET_COL)
        x_id = x.pop("ID")
        CreditCardFeatureStoreGateway.insert_data(x_id, x)
    return values_dict

if __name__ == '__main__':
    INDEXES = [3]
    res = put_data(INDEXES)
    print(res)
