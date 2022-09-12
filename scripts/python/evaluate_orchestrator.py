import argparse
import json

from scripts.python.put_data_on_dynamo import TARGET_COL, put_data
from scripts.python.run_orchestrator import (ExpectedClientEvent,
                                             ExpectedEvent, ExpectedModelEvent,
                                             handler)


def main(client_id: int, model_name: str, model_version: int):
    d = put_data([client_id])[0]
    t = d.pop(TARGET_COL)
    event = ExpectedEvent(
        model=ExpectedModelEvent(
            model_name=model_name,
            model_version=model_version,
        ),
        client=ExpectedClientEvent(id=client_id),
    )
    r = handler(event.to_dict(), None)
    prediction = r['prediction']
    print(5*"-=", "Evaluating", 5*"-=")
    print("target:", t)
    print("prediction:", prediction)
    print(5*"-=", "Lambda Json Event", 5*"-=")
    print(json.dumps(event.to_dict()))
    print(5*"-=", "Variables", 5*"-=")
    print(json.dumps(d))
    assert t == prediction, "Something went wrong"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="script to evaluate the architecture")
    parser.add_argument("-c", '--client-id', metavar="client_id",
                        required=True, type=int, default=3, help="The client id desired to evaluate")
    parser.add_argument("-m", '--model-name', metavar="model_name",
                        required=False, type=str, default="addi-challenge", help="The model name desired to evaluate")
    parser.add_argument("-v", '--model_version', metavar="model_version",
                        required=False, type=int, default=1, help="The model version desired to evaluate")
    args = parser.parse_args()
    main(args.client_id, args.model_name, args.model_version)
