from app import celery


@celery.task
def start_analysis(keyword):
    """
    Adds a keyword to the queue for the worker to process

    :param: keyword
        keyword to find sentiment for
    """
    print(f"Starting {keyword}")

    import time

    time.sleep(2)

    print(f"Ending {keyword}")
