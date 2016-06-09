import requests, json
"""
Package
Version
Status
Blame
Message
"""

def get_packages_from_url():
    url = "https://ci.debian.net/data/status/unstable/amd64/packages.json"
    request_of_ci_debian = requests.get(url)
    file_ci_debian = request_of_ci_debian.content
    open("packages.json" , 'wb').write(file_ci_debian)

def get_ci_debian_json():
    data = None

    try:
        packages_status = open('packages.json')
        data = json.load(packages_status)
    except IOError:
        get_packages_from_url()
        data = get_ci_debian_json()

    return data
