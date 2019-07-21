import json
from pprint import pprint

import autoconfig
import serverinfo
import sync


def parse(base_url: str, protocol: str):
    autoconf = autoconfig.parse("{}/autoconfig".format(base_url), protocol)
    serverinf = serverinfo.parse("{}/serverinfo".format(base_url))

    # TODO currently events are not supported ! (I haven't found any community, using that feature)
    # eventc = events.parse("{}/events".format(base_url))

    # TODO currently changelogs are not supported !
    # changelog = changelogs.parse("{}/events".format(base_url))

    syn = sync.parse("{}/sync".format(base_url))

    # pprint(syn)
    # pprint(autoconf)
    # pprint(serverinf)

    x = dict()
    x["autoconf"] = autoconf
    x["serverinfo"] = serverinf
    x["sync"] = syn

    return x
