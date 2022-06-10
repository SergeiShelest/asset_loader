import requests


class HttpError(Exception):
    pass


def download_file(url, path):
    r = requests.get(url, stream=True)

    if r.status_code != 200:
        raise HttpError("HTTP status {0}".format(r.status_code))

    size = int(r.headers.get('content-length'))

    with open(path, 'wb') as f:
        loaded = 0
        for chunk in r:
            f.write(chunk)
            loaded += len(chunk)

            yield loaded, size
