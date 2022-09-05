from src.usecases.model.remote import RemoteModelPredictor
from src.utils.sync import non_wait


class RemotePocSortChevette(RemoteModelPredictor):
    model_name: str = "poc_sort_chevette"
    model_version: int = 1


non_wait(RemotePocSortChevette.get_model_info())
