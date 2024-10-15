import typing as t
# import warnings

# import pandas as pd

from .interface import Repository

# warnings.filterwarnings("ignore")


class RestrictedPhoto(Repository):
    def __init__(self, engine) -> None:
        self.engine = engine

    def get(self, imei: str) -> t.Any:
        # stmt = f"""
            
        #         """
        # return pd.read_sql(stmt, self.engine)
