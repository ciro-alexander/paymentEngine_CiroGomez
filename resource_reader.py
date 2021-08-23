import pandas as pd


class ResourceLoader:

    __df = None

    def read_file(self, resource_name):
        assert resource_name is not None, "Resource file name is None"
        assert resource_name, "Resource file name is empty"

        try:
            self.__df = pd.read_csv(resource_name)
            return self.__df
        except Exception as error:
            print('error:', error)
