from anytree.exporter import DictExporter

import Download
import JDeserialize


def getInstDecls(s: str) -> str:
    return JDeserialize.findblock(s, "instance dump")


def parse_jd(deserialize_raw: str) -> dict:
    instDecl = getInstDecls(deserialize_raw)

    SyncTreeLeafs = JDeserialize.GetAllInstancesOfType(instDecl, "repository.SyncTreeLeaf")
    SyncTreeDirs = JDeserialize.GetAllInstancesOfType(instDecl, "repository.SyncTreeDirectory")

    tree = JDeserialize.BuildTree(SyncTreeDirs, SyncTreeLeafs)

    # print(RenderTree(tree))

    di = DictExporter().export(tree)

    return di


def parse(url: str) -> dict:
    file_path = Download.downloadFile(url)
    deserialize_raw = JDeserialize.Deserialize(file_path)
    autoconfig = parse_jd(deserialize_raw)

    Download.cleanup(file_path)
    return autoconfig
