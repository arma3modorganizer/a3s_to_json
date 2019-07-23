import Download
import JDeserialize


def getInstDecls(s: str) -> str:
    return JDeserialize.findblock(s, "instance dump")


def parse_jd(deserialize_raw: str, url_type: str) -> dict:
    instDecl = getInstDecls(deserialize_raw)

    autoconfig = dict()
    # retrieve fr.soe.a3s.domain.URL_TYPE
    autoconfig["URL_CONF"] = JDeserialize.GetInstanceAsDictWOIDesc(instDecl, url_type)

    fav_server = dict()
    try:
        fav_server = JDeserialize.GetInstanceAsDictWOIDesc(instDecl, "configration.FavoriteServer")
    except AttributeError as e:
        pass

    autoconfig["AUTO_CONFIG"] = JDeserialize.GetInstanceAsDictWOIDesc(instDecl, "repository.AutoConfig")

    autoconfig["FAV_SERVER"] = fav_server

    return autoconfig


def parse(url: str, url_type: str) -> dict:
    file_path = Download.downloadFile(url)
    deserialize_raw = JDeserialize.Deserialize(file_path)
    autoconfig = parse_jd(deserialize_raw, url_type)

    Download.cleanup(file_path)
    return autoconfig
