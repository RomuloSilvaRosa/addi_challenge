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
print("event to test in lambda console")
print(json.dumps(event.to_dict()))
r = handler(event.to_dict(), None)
# print("response:", r)
