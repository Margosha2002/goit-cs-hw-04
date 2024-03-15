import threading
import time


class KeywordSearchThread(threading.Thread):
    def __init__(self, files, keyword, results):
        threading.Thread.__init__(self)
        self.files = files
        self.keyword = keyword
        self.results = results

    def run(self):
        found_files = []
        for file in self.files:
            try:
                with open(file, "r") as f:
                    if self.keyword in f.read():
                        found_files.append(file)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
        self.results[self.keyword] = found_files


def search_files_with_threads(files, keywords):
    results = {}
    threads = []
    files_per_thread = len(files) // len(keywords)
    for i in range(0, len(files), files_per_thread):
        thread_files = files[i : i + files_per_thread]
        thread = KeywordSearchThread(
            thread_files, keywords[i // files_per_thread], results
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


if __name__ == "__main__":
    files = ["files/file1.txt", "files/file2.txt", "files/file3.txt"]  # Example files
    keywords = ["може", "частота", "ігор"]  # Example keywords

    start_time = time.time()
    results = search_files_with_threads(files, keywords)
    end_time = time.time()

    print("Results:")
    for keyword, found_files in results.items():
        print(f"Keyword: {keyword}, Files: {found_files}")

    print("Execution time:", end_time - start_time)
