import hashlib
import json
import time
import timeit
import os
import plotly.graph_objs as go

SHAKE_HASH_LENGTH = os.getenv('SHAKE_HASH_LENGTH')
PATH_TO_FILE = os.getenv('PATH_TO_FILE')


def hash_all(text: str) -> None:
    """This function hashes prompted text using all hash algorithms in hashlib.algorithms_available set

    text (str) : prompted text that is going to be hashed in all hash algorithms

    returns None, saves to file hashed result - default result file path - ./resutls/hashes.json

    """
    result = []

    for algorithm in hashlib.algorithms_available:
        hash_json = {}
        start_time = time.time()
        hash_object = hashlib.new(algorithm)

        if 'shake' in algorithm:
            digest = hash_object.digest(int(SHAKE_HASH_LENGTH))
            end_time = time.time()
            hash_json[algorithm] = {
                "text": f"{text}",
                "hash": f"{digest}",
                "time_to_hash": f"{end_time - start_time}"
            }
        else:
            digest = hash_object.digest()
            end_time = time.time()
            hash_json[algorithm] = {
                "text": f"{text}",
                "hash": f"{digest}",
                "time_to_hash": f"{end_time - start_time}"
            }
        result.append(hash_json)

    with open("./results/hashes.json", 'w') as result_file:
        result_file.write(json.dumps({"hashAlgorithmList": result}, indent=1, default=str))


def hash_file(filename: str = PATH_TO_FILE) -> str:
    """"This function returns the SHA-1 hash
   of the file passed into it; path default to ./files/ubuntu

   filename (str): path to file

   returns string which is hash of file which path is provided as argument

   """

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


# Funkcja do generowania hasha i pomiaru czasu
def measure_hash_time(message: str):
    """
    This function measures the time taken to hash a message and returns time difference

    message (str) : message that is hashed

    returns time difference (hashing time)
    """
    start_time = timeit.default_timer()
    hashlib.sha256(message.encode()).hexdigest()
    end_time = timeit.default_timer()
    return end_time - start_time


def main():
    """Main driver function"""
    hash_all(input('Enter text to hash:\n'))
    hash_digest = hash_file(PATH_TO_FILE)
    print(hash_digest)

    # plotly graph part

    message_sizes = [10, 10000, 100000, 1000000, 10000000]  # in bytes

    hash_times = []
    for size in message_sizes:
        message = 'a' * size
        hash_time = measure_hash_time(message)
        hash_times.append(hash_time)

    fig = go.Figure(data=go.Scatter(x=message_sizes, y=hash_times, mode='markers+lines'))
    fig.update_layout(
        title='Time to generate hash depending on the size of the text',
        xaxis_title='Size (bytes)',
        yaxis_title='Time (s)',
        showlegend=False
    )
    fig.show()


if __name__ == '__main__':
    main()
