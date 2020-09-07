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
            self.data = [json.loads(line.strip()) for line in fp.readlines()]


class MonkeyLearnClient(BaseClient):
    def __init__(self, config_obj):
        super().__init__(config_obj)
        self.model_id = self.config.MONKEYLEARN_MODEL_ID
        self.client = MonkeyLearn(self.config.MONKEYLEARN_API_TOKEN)

    def fetch_predictions(self, keyword, data_file_path):
        self.load_data(data_file_path)

        # response = self.client.classifiers.classify(
        #     model_id=self.model_id,
        #     data=self.data,
        #     auto_batch=True,
        #     retry_if_throttled=True,
        # )

        # data = {"response": response.body}
        import sys

        for data in self.data:
            print(data, file=sys.stderr)
            break
        with open("data-monkeylearn.json", "w") as fp:
            json.dump(self.data, fp)

        # return response.body


client_map = {"monkeylearn": MonkeyLearnClient}
