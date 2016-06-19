import requests
import json
import pet.models
import pet.update
import pet


def update_ci_status():
    engine = pet.engine(True)
    connection_instance = engine.connect()
    result = connection_instance.execute("select * from named_tree")
    connection_instance.close()

    count_changed_packtes = 0
    for row in result:
        if row.source is not None:
            print row.source
            status = found_on_json(row.source)
            if status is not False:
                count_changed_packtes += 1
                change_status(row, status)
    return count_changed_packtes


def change_status(row, status):
    engine = pet.engine(True)
    connection_instance = engine.connect()

    script_sql = "update named_tree set status='%s' where id=%s" \
        % (status, row.id)
    status = connection_instance.execute(script_sql)

    connection_instance.close()


def found_on_json(source):
    data = get_ci_debian_json()
    for package in data:
        package_name = package["package"]
        if package_name == source:
            return package["status"]
    return False


def get_packages_from_url():
    url = "https://ci.debian.net/data/status/unstable/amd64/packages.json"
    try:
        request_of_ci_debian = requests.get(url)
        file_ci_debian = request_of_ci_debian.content
        open("packages.json", 'wb').write(file_ci_debian)
    except IOError:
        print "Coundn't acess json of packages on url: ", url


def get_ci_debian_json():
    data = None

    try:
        packages_status = open('packages.json')
        data = json.load(packages_status)
    except IOError:
        get_packages_from_url()
        data = get_ci_debian_json()

    return data
