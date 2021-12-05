from enum import Enum

from matching.env import MODEL_FILE_PATH


class MatchingModelType(Enum):
    BASELINE = "baseline"
    CLASSIC_ML = "classic_ml"
    MATCH_PYRAMID = "match_pyramid"
    TRANSFORMER = "transformer"


MODEL_MAPPING = {
    MatchingModelType.BASELINE: MODEL_FILE_PATH / "baseline.csv"
}
