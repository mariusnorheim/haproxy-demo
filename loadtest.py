import requests
import threading
import time
from collections import defaultdict
from queue import Queue
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Configuration
URL = "http://127.0.0.1"
CONCURRENT_REQUESTS = 250
TOTAL_REQUESTS = 10000

# Metrics
response_times = []
failed_requests = 0
lock = threading.Lock()

# Track server response counts
server_responses = defaultdict(int)

def make_request(session, queue):
    global failed_requests
    while not queue.empty():
        try:
            queue.get()
            start_time = time.time()
            response = session.get(URL)
            elapsed_time = time.time() - start_time

            # Record server information from response headers
            server_id = response.headers.get("X-Server-ID", "Unknown")
            lock.acquire()
            response_times.append(elapsed_time)
            server_responses[server_id] += 1
            lock.release()
        except requests.exceptions.RequestException:
            lock.acquire()
            failed_requests += 1
            lock.release()
        finally:
            queue.task_done()

def load_test():
    global failed_requests
    # Create a queue with the number of requests
    request_queue = Queue()
    for _ in range(TOTAL_REQUESTS):
        request_queue.put(1)

    # Create a session to reuse connections
    session = requests.Session()

    # Create threads
    threads = []
    for _ in range(CONCURRENT_REQUESTS):
        thread = threading.Thread(target=make_request, args=(session, request_queue))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Calculate statistics
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"Failed Requests: {failed_requests}")
    if response_times:
        print(f"Average Response Time: {sum(response_times) / len(response_times):.2f} seconds")
        print(f"Min Response Time: {min(response_times):.2f} seconds")
        print(f"Max Response Time: {max(response_times):.2f} seconds")

    # Visualize responses
    fig = plt.figure(figsize=(10, 5))
    fig.canvas.manager.set_window_title("Server Load Distribution")

    # Plot 1: Response Time Distribution
    plt.subplot(1, 2, 1)
    plt.hist(response_times, bins=20, edgecolor='black')
    plt.title("Response Time Distribution")
    plt.xlabel("Response Time (seconds)")
    plt.ylabel("Frequency")

    # Plot 2: Server Request Distribution
    plt.subplot(1, 2, 2)
    servers = list(server_responses.keys())
    requests_handled = list(server_responses.values())
    plt.bar(servers, requests_handled)
    plt.title("Requests Handled by Server")
    plt.xlabel("Server ID")
    plt.ylabel("Number of Requests")

    # Show the plots
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    load_test()
