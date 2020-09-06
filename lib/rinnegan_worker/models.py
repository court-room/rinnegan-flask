import abc
import json

from monkeylearn import MonkeyLearn


class BaseClient(abc.ABC):
    def __init__(self, config_obj):
        self.count = 0
        self.data = []
        self.config = config_obj

    @abc.abstractmethod
    def fetch_predictions(self):
        pass

    def load_data(self, data_file_path):
        with open(data_file_path, "r") as fp:
            self.data = json.load(fp)


class MonkeyLearnClient(BaseClient):
    def __init__(self, config_obj):
        super().__init__(config_obj)
        self.model_id = self.config.MONKEYLEARN_MODEL_ID
        self.client = MonkeyLearn(self.config.MONKEYLEARN_API_TOKEN)

    def _send_request(self, keyword, data):
        if len(data) > 0:
            response = self.client.classifiers.classify(
                model_id=self.model_id, data=data
            )
            return response.body

    def fetch_predictions(self, keyword, data_file_path):
        self.load_data(data_file_path)

        count = 0
        batch, result = [], []
        for tweet in self.data:
            count += 1
            batch.append(tweet)

            if count == 500:
                result.append(self._send_request(keyword, batch))
                count = 0
                batch = []

        result.append(self._send_request(keyword, batch))

        import sys

        print(result[0:3], file=sys.stderr)


client_map = {"monkeylearn": MonkeyLearnClient}
