import autoconfig
import changelogs
import serverinfo
import sync


def parse(base_url: str, protocol: str, parseAutoconf: bool = True, parseServerinfo: bool = True,
          parseEvents: bool = False, parseChangelog: bool = True, parseSync: bool = True):
    x = dict()
    if parseAutoconf:
        autoconf = autoconfig.parse("{}/autoconfig".format(base_url), protocol)
        x["autoconf"] = autoconf
    if parseServerinfo:
        serverinf = serverinfo.parse("{}/serverinfo".format(base_url))
        x["serverinfo"] = serverinf
    if parseChangelog:
        changelog = changelogs.parse("{}/changelogs".format(base_url))
        x["changelog"] = changelog
    if parseSync:
        syn = sync.parse("{}/sync".format(base_url))
        x["sync"] = syn

    if parseEvents:
        # TODO currently events are not supported ! (I haven't found any community, using that feature)
        # eventc = events.parse("{}/events".format(base_url))
        eventc = dict()
        eventc[
            "NYI"] = "NOT YET SUPPORTED. Please send me an events file, if you want to use this feature (github issue)"
        x["events"] = eventc

    return x
