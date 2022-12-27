import json
import sys

sys.path.append("./lambdas/model_orchestrator")
from main import ExpectedEvent, ExpectedModelEvent, ExpectedClientEvent, handler




def main():
    event = ExpectedEvent(
        model=ExpectedModelEvent(
            model_name="company-showcase",
            model_version=1,
        ),
        client=ExpectedClientEvent(id=2),
    )
    print("event to test in lambda console")
    print(json.dumps(event.to_dict()))
    r = handler(event.to_dict(), None)
    print("response:", r)

if __name__ == '__main__':
    main()

