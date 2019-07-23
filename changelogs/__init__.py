import Download
import JDeserialize


def getInstDecls(s: str) -> str:
    return JDeserialize.findblock(s, "instance dump")


def preprocessJArrayList(jarr: dict) -> list:
    jarr.pop("ArrayList", None)
    jarr.pop("size", None)
    jarr = list(jarr.values())
    return jarr


def connect_pointers(changelog_instances, array_list_instances) -> dict:
    for id in changelog_instances:
        cl_i = changelog_instances[id]

        updatedAddons = array_list_instances[cl_i["updatedAddons"]]
        deletedAddons = array_list_instances[cl_i["deletedAddons"]]
        newAddons = array_list_instances[cl_i["newAddons"]]
        addons = array_list_instances[cl_i["addons"]]

        updatedAddons = preprocessJArrayList(updatedAddons)
        deletedAddons = preprocessJArrayList(deletedAddons)
        newAddons = preprocessJArrayList(newAddons)
        addons = preprocessJArrayList(addons)

        cl_i["addons"] = addons
        cl_i["newAddons"] = newAddons
        cl_i["deletedAddons"] = deletedAddons
        cl_i["updatedAddons"] = updatedAddons

        cl_i.pop("Changelog", None)
        cl_i.pop("buildDate", None)

        changelog_instances[id] = cl_i

    return changelog_instances


def parse_jd(deserialize_raw: str) -> dict:
    instDecl = getInstDecls(deserialize_raw)

    changelog_instances = JDeserialize.GetAllInstancesOfType(instDecl, "repository.Changelog")
    array_list_instances = JDeserialize.GetAllInstancesOfType(instDecl, "java.util.ArrayList", True)

    changelog = connect_pointers(changelog_instances, array_list_instances)

    return changelog


def parse(url: str) -> dict:
    file_path = Download.downloadFile(url)
    deserialize_raw = JDeserialize.Deserialize(file_path)
    autoconfig = parse_jd(deserialize_raw)

    Download.cleanup(file_path)
    return autoconfig
