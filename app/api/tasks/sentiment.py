from app import celery


@celery.task
def add_to_queue(keyword):
    """
    Adds a keyword to the queue for the worker to process

    :param: keyword
        keyword to find sentiment for
    """
    print("Starting")

    import time
    time.sleep(2)

    print("Ending")
