import Download
import JDeserialize


def getInstDecls(s: str) -> str:
    return JDeserialize.findblock(s, "instance dump")


def parse_jd(deserialize_raw: str) -> dict:
    raise NotImplementedError

    """
    instDecl = getInstDecls(deserialize_raw)

    events = dict()
    events["EVENTS"] = JDeserialize.GetInstanceAsDictWOIDesc(instDecl, "TODO")

    return events
    """


def parse(url: str) -> dict:
    file_path = Download.downloadFile(url)
    deserialize_raw = JDeserialize.Deserialize(file_path)
    autoconfig = parse_jd(deserialize_raw)

    Download.cleanup(file_path)
    return autoconfig
