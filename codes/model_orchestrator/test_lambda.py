from main import *
import json
event = ExpectedEvent(
    model=ExpectedModelEvent(
        model_name="addi",
        model_version=1,
    ),
    client=ExpectedClientEvent(id=1),
)
# p = event.to_json()
# print(p)
# with open("input_data.json", "w") as f:
#     f.write(json.dumps(p))
handler(event.to_dict(), None)
