import multiprocessing
import time


def search_files(files, keyword, results_queue):
    found_files = []
    for file in files:
        try:
            with open(file, "r") as f:
                if keyword in f.read():
                    found_files.append(file)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
    results_queue.put({keyword: found_files})


def search_files_with_processes(files, keywords):
    manager = multiprocessing.Manager()
    results_queue = manager.Queue()
    processes = []
    files_per_process = len(files) // len(keywords)
    for i in range(0, len(files), files_per_process):
        process_files = files[i : i + files_per_process]
        process = multiprocessing.Process(
            target=search_files,
            args=(process_files, keywords[i // files_per_process], results_queue),
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = {}
    while not results_queue.empty():
        results.update(results_queue.get())

    return results


if __name__ == "__main__":
    files = ["files/file1.txt", "files/file2.txt", "files/file3.txt"]  # Example files
    keywords = ["може", "частота", "ігор"]  # Example keywords

    start_time = time.time()
    results = search_files_with_processes(files, keywords)
    end_time = time.time()

    print("Results:")
    for keyword, found_files in results.items():
        print(f"Keyword: {keyword}, Files: {found_files}")

    print("Execution time:", end_time - start_time)
