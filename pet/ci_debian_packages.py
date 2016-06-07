# vim:ts=4:sw=4:et:ai:sts=4
# Copyright 2016, Tiago Assunção <tiago@sof2u.com>
# Copyright 2016, Victor Cabeceira <victorfgcabeceira@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
