import sys
sys.path.append("./lambdas/model_orchestrator")

from src.devices.aws.lambda_function import LambdaClient
from main import *
import json

event = ExpectedEvent(
    model=ExpectedModelEvent(
        model_name="addi-challenge",
        model_version=1,
    ),
    client=ExpectedClientEvent(id=2),
)
# p = event.to_json()
# print(p)
# with open("input_data.json", "w") as f:
#     f.write(json.dumps(p))

# print(json.dumps(event.to_dict()))
r = handler(event.to_dict(), None)
# print("response:", r)
