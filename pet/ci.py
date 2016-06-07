from os import path, makedirs
import json
import pet
import pet.models
import pet.update
import requests
import subprocess


def update_ci_status():
    """The main method.
    Creates an instance of the database and change the status of each package.
    It also returns the amount of packages that were updated."""
    engine = pet.engine(True)
    connection_instance = engine.connect()
    result = connection_instance.execute("select * from named_tree")
    connection_instance.close()

    count_changed_packages = 0
    for row in result:
        if row.source is not None:
            status = found_on_json(row.source)
            if status is not False:
                count_changed_packages += 1
                change_status(row, status)
    return count_changed_packages


def change_status(row, status):
    """Changes the status column of the package (of given row)."""
    engine = pet.engine(True)
    connection_instance = engine.connect()

    script_sql = "update named_tree set status='%s' where id=%s" \
        % (status, row.id)
    status = connection_instance.execute(script_sql)

    connection_instance.close()


def found_on_json(source):
    """Searches the packages that are on the database on the json.
    It returns the status of each found package."""
    data = get_ci_debian_json()
    for package in data:
        package_name = package["package"]
        if package_name == source:
            return package["status"]
    return False


def get_packages_from_url(url):
    """Downloads the json file."""
    try:
        print "Downloading json file with ci debian status..."
        request_of_ci_debian = requests.get(url)
        file_ci_debian = request_of_ci_debian.content
        file_status = open("pet/.debian_ci/packages.json", 'w')
        file_status.write(file_ci_debian)
        file_status.close()
    except IOError:
        print "File package.json coundn't open"
    except:
        print "Coundn't acess json of packages on url: ", url


def create_dir():
    """This method creates the directory where the .debian_ci will be stored."""
    dir_path = path.abspath(path.dirname(__file__))
    dir_path += "/.debian_ci"
    if not path.exists(dir_path):
        makedirs(dir_path)
    return dir_path


def get_ETag(url):
    """Verifies if the content of the json was modified and need to be
    downloaded again."""
    bashCommand = "HEAD %s | grep ETag" % url
    output = subprocess.check_output(['bash', '-c', bashCommand])
    ETAG = slice(7, -2, 1)
    ETag = output[ETAG]

    method_response = False
    try:
        file_version = open("pet/.debian_ci/etag_version", "r")
        file_read = file_version.read()
        if ETag != file_read:
            method_response = True
    except IOError:
        file_version = open("pet/.debian_ci/etag_version", "w+")
        file_version.write(ETag)
        method_response = True

    file_version.close()
    return method_response


def get_ci_debian_json():
    """Verifies if the file exists and if not, downloads and parses the json."""
    data = None
    url = "https://ci.debian.net/data/status/unstable/amd64/packages.json"
    create_dir()

    if not get_ETag(url):
        try:
            packages_status = open('pet/.debian_ci/packages.json')
            data = json.load(packages_status)
            packages_status.close()
        except IOError, e:
            print e
    else:
        print("Outdated version of ci")
        get_packages_from_url(url)
        data = get_ci_debian_json()

    return data
