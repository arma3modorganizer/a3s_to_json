import JDeserialize
import Download


def getInstDecls(s: str) -> str:
    return JDeserialize.findblock(s, "instance dump")


def parse_jd(deserialize_raw: str) -> dict:
    instDecl = getInstDecls(deserialize_raw)

    serverinfo = dict()
    serverinfo["SERVER_INFO"] = JDeserialize.GetInstanceAsDictWOIDesc(instDecl, "repository.ServerInfo")

    return serverinfo


def parse(url: str) -> dict:
    file_path = Download.downloadFile(url)
    deserialize_raw = JDeserialize.Deserialize(file_path)
    autoconfig = parse_jd(deserialize_raw)

    Download.cleanup(file_path)
    return autoconfig
