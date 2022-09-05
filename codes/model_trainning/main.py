
import logging
import joblib
import pandas as pd



logging.basicConfig(
    format='%(asctime)s %(levelname)s - %(name)s - %(message)s', level=logging.INFO)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def handler(event, _):
    _MODEL = joblib.load("model.joblib")
    _features = list(_MODEL.feature_names_in_)
    LOGGER.info(event)
    _event = dict()
    for x in _features:
        _event[x] = event.get(x, 0)

    data_input = pd.DataFrame.from_dict([_event])
    prediction = int(_MODEL.predict(data_input)[0])
    LOGGER.info(prediction)
    return prediction
