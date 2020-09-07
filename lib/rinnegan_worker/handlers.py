import concurrent.futures
import logging

from lib.rinnegan_worker.factory import NLPModelClientFactory
from lib.rinnegan_worker.factory import SourceClientFactory
from lib.rinnegan_worker.factory import StorageVendorClientFactory


log_format_string = "%(asctime)s PID- %(process)d %(levelname)s %(pathname)s %(funcName)s %(lineno)d %(message)s"  # noqa: E501
logging.basicConfig(level=logging.INFO, format=log_format_string)

logger = logging.getLogger(__name__)


def start_analysis(params):
    """
    Adds a keyword to the queue for the worker to process

    :param: params
        Dict for storing the arguments for this worker process
    """
    keyword = params["keyword"]["data"]
    request_id = params["meta"]["request_id"]

    logger.info(f"Starting analysis for {keyword}")

    local_file_path = (
        f"/usr/src/app/data/worker-data/{keyword}-{request_id}.jsonl"
    )

    data_source_client = SourceClientFactory.build_client(
        params["source"]["data_source"]
    )
    storage_vendor_client = StorageVendorClientFactory.build_client(
        params["vendor"]["object_storage_vendor"]
    )
    model_client = NLPModelClientFactory.build_client(params["meta"]["model"])

    data_source_client.fetch_data(
        keyword=keyword, data_file_path=local_file_path
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            storage_vendor_client.upload, local_file_path=local_file_path
        )
        model_callback = executor.submit(
            model_client.fetch_predictions, keyword, local_file_path
        )
        nlp_response = model_callback.result()

        import sys

        print(nlp_response, file=sys.stderr)

    logger.info(f"Analysis for {keyword} completed")
