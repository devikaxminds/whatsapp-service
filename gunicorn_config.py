import multiprocessing

bind = "0.0.0.0:8000"
timeout = 600  # Timeout in seconds - Possible solution for [CRITICAL] WORKER TIMEOUT
workers = (multiprocessing.cpu_count() * 2) + 1
preload_app = True
