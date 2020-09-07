import abc
import json
import sys

from monkeylearn import MonkeyLearn


class BaseClient(abc.ABC):
    def __init__(self, config_obj):
        self.count = 0
        self.data = []
        self.config = config_obj

    @abc.abstractmethod
    def fetch_sentiments(self, keyword, data_file_path):
        pass


class MonkeyLearnClient(BaseClient):
    def __init__(self, config_obj):
        super().__init__(config_obj)
        self.model_id = self.config.MONKEYLEARN_MODEL_ID
        self.client = MonkeyLearn(self.config.MONKEYLEARN_API_TOKEN)

    def _load_data(self, data_file_path):
        with open(data_file_path, "r") as fp:
            for line in fp.readlines():
                try:
                    data = line.strip()
                    self.data.append(data)
                except json.decoder.JSONDecodeError:
                    print(f"Failing {data}", file=sys.stderr)

    def fetch_sentiments(self, keyword, data_file_path):
        self._load_data(data_file_path)

        response = self.client.classifiers.classify(
            model_id=self.model_id,
            data=self.data,
            auto_batch=True,
            retry_if_throttled=True,
        )

        return response.body


client_map = {"monkeylearn": MonkeyLearnClient}
