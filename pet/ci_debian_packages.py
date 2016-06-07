import requests, json
"""
Package
Version
Status
Blame
Message
"""
def get_ci_debian_json():
    url = "https://ci.debian.net/data/status/unstable/amd64/packages.json"
    request_of_ci_debian = requests.get(url)
    file_ci_debian = request_of_ci_debian.content
    open("packages.json" , 'wb').write(file_ci_debian)
    data = None
    with open('packages.json') as data_file:
        data = json.load(data_file)

    return data
