import logging

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
    logger.info(f"Starting analysis for {params['keyword']}")

    local_file_path = (
        f"/tmp/worker-data/{params['keyword']}-{params['request_id']}.json"
    )

    data_source_factory = SourceClientFactory(params["source"])
    data_source_client = data_source_factory.build_client()

    data_source_client.fetch_data(
        keyword=params["keyword"], request_id=params["request_id"]
    )

    storage_vendor_factory = StorageVendorClientFactory(params["source"])
    storage_vendor_client = storage_vendor_factory.build_client()

    storage_vendor_client.upload(local_file_path=local_file_path)

    logger.info(f"Analysis for {params['keyword']} completed")
