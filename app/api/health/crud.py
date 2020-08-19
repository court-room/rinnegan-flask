def get_health_status():
    """
    Health check utility to tell if the python server is up or not.
    If the server is down then this call will fail.

    :returns:
        Dict defining the health status fo the server.
    """
    return {"health": "good"}
