import json
import logging
import warnings
from pathlib import Path

import joblib
import pandas as pd

logging.basicConfig(
    format="%(asctime)s %(levelname)s - %(name)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def handler(event, _):
    pwd = Path(__file__).parent.resolve()
    warnings.filterwarnings("ignore")
    _MODEL = joblib.load(pwd.joinpath("model.joblib"))
    _features = list(_MODEL.feature_names_in_)
    LOGGER.info(json.dumps({"input": event}))
    _event = dict()
    event = event or {}
    for x in _features:
        _event[x] = event.get(x, 0)

    data_input = pd.DataFrame.from_dict([_event])
    prediction = int(_MODEL.predict(data_input)[0])
    LOGGER.info(json.dumps({"output": prediction}))
    return {"prediction": prediction}
