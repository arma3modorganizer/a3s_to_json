#!/usr/bin/env python
import re
import subprocess
# noinspection SpellCheckingInspection
from enum import Enum

from anytree import Node, PreOrderIter, AnyNode


def Deserialize(filepath: str) -> str:
    res = subprocess.run(['java', '-jar', 'jdeserialize-1.2.jar', '-noclasses', '-fixnames', '-showarrays', filepath],
                         stdout=subprocess.PIPE)
    return res.stdout.decode('utf-8')


def remove_first_and_last(s: str) -> str:
    return "\n".join(s[:s.rfind('\n')].split("\n")[1:])


def findblock(raw: str, search: str) -> str:
    search_re = r"\/\/\/\/\sBEGIN\s{}(\n|.)+END\s{}".format(search, search)
    matches = re.search(search_re, raw)
    return remove_first_and_last(matches.group())


def findDomainInstance(raw: str, inst_type: str):
    search_re = r"\[instance\s0x[0-9a-f]{6}:\s0x[0-9a-f]{6}\/fr\.soe\.a3s\.domain\." + inst_type + r"(\n|.)+?\n\]"
    matches = re.search(search_re, raw)
    return matches.group()


rINSTANCE = re.compile(r"\[instance\s0x[0-9a-f]{6}:\s0x[0-9a-f]{6}")
rFIELD_DATA = re.compile(r"field\sdata:")
rINSTANCE_DESC = re.compile(r"\s{4}0x[0-9a-f]{6}\/fr\.soe\.a3s\..+")
rENUM = re.compile(r"\[enum\s0x[0-9a-f]{6}")
rSTRING = re.compile(r"\[String\s0x[0-9a-f]{6}")
rNULL = re.compile(r"null")
rINTEGER = re.compile(r"\w+:\s\d+")
rBOOL = re.compile(r"\w+:\s(true|false)")
rSYNC_DIR_TREE = re.compile(r"fr\.soe\.a3s\.domain\.repository\.SyncTreeDirectory\s_")


class IType(Enum):
    INSTANCE = 1
    FIELD_DATA = 2
    INSTANCE_DESC = 3
    ENUM = 4
    STRING = 5
    NULL = 6
    INTEGER = 7
    BOOL = 8
    SYNC_TREE_DIR = 9


def getInstanceData(line: str) -> ():
    ls = line.split("/")
    return ls[0].split(" ")[1][:-1], ls[1][:-1].split(".")[-1]


def getEnumData(line: str) -> ():
    ls = line.split(":")
    name = ls[0].strip()
    value = ls[-1].strip()[:-1]
    return name, value


def getStringData(line: str) -> ():
    ls = line.split(":")
    name = ls[0].strip()
    value = ls[-1].strip()[1:-2]
    return name, value


def getNullData(line: str):
    ls = line.split(":")
    name = ls[0].strip()
    return name


def getIntData(line: str) -> ():
    ls = line.split(":")
    name = ls[0].strip()
    value = ls[-1].strip()
    return name, value


def getBoolData(line: str) -> ():
    ls = line.split(":")
    name = ls[0].strip()
    value = ls[-1].strip()
    return name, True if value == "true" else False


def getSyncDirTreeData(line: str) -> ():
    ls = line.split(":")
    return ls[0].strip(), ls[1].strip()[1:]


def GetLineTypeNameAndValue(line: str) -> ():
    if rINSTANCE.search(line) is not None:
        inst_n = getInstanceData(line)
        return IType.INSTANCE, inst_n[1], inst_n[0]
    elif rFIELD_DATA.search(line) is not None:
        return IType.FIELD_DATA, "FIELD_DATA", None
    elif rINSTANCE_DESC.search(line) is not None:
        return IType.INSTANCE_DESC, "INSTANCE_DESC", None
    elif rENUM.search(line) is not None:
        enum_data = getEnumData(line)
        return IType.ENUM, enum_data[0], enum_data[1]
    elif rSTRING.search(line) is not None:
        stringData = getStringData(line)
        return IType.STRING, stringData[0], stringData[1]
    elif rNULL.search(line) is not None:
        nullData = getNullData(line)
        return IType.NULL, nullData, None
    elif rINTEGER.search(line) is not None:
        IntData = getIntData(line)
        return IType.INTEGER, IntData[0], IntData[1]
    elif rBOOL.search(line) is not None:
        boolData = getBoolData(line)
        return IType.INTEGER, boolData[0], boolData[1]
    elif rSYNC_DIR_TREE.search(line) is not None:
        syncData = getSyncDirTreeData(line)
        return IType.SYNC_TREE_DIR, syncData[0], syncData[1]
    elif line == "]":
        pass
    elif "ArrayList" in line:
        pass
    else:
        print("Could not parse: {}".format(line))


def GetInstanceAsDictWOIDesc(instDecl: str, sIType: str):
    """
    Generates Java Instance data without Instance description
    """
    instance = findDomainInstance(instDecl, sIType)

    x_point = dict()
    for line in instance.split("\n"):
        line_info = GetLineTypeNameAndValue(line)
        if line_info is None:
            continue

        itype: IType = line_info[0]
        name: str = line_info[1]
        value: str = line_info[2]

        if itype == IType.STRING:
            x_point[name] = value
        elif itype == IType.ENUM:
            x_point[name] = value
        elif itype == IType.INTEGER:
            x_point[name] = value

    return x_point


def findDomainInstances(raw: str, inst_type: str):
    search_re = r"(\[instance\s0x[0-9a-f]{6}:\s0x[0-9a-f]{6}\/fr\.soe\.a3s\.domain\." + inst_type + r"(\n|.)+?\n\])"
    matches = re.findall(search_re, raw)
    return matches


def GetAllInstancesOfType(instDecl: str, t: str) -> dict:
    instances = findDomainInstances(instDecl, t)

    instances_x = dict()

    for instance in instances:
        inx = instance[0]
        inxv = dict()
        for line in inx.split("\n"):
            line_info = GetLineTypeNameAndValue(line)
            if line_info is None:
                continue

            if line_info[0] == IType.FIELD_DATA:
                continue
            if line_info[0] == IType.INSTANCE_DESC:
                continue

            inxv[line_info[1]] = line_info[2]

        instances_x[inxv[t.split(".")[-1]]] = inxv

    return instances_x


def BuildTree(std: dict, stl: dict):
    idTree = None
    idNodes = dict()

    idDirMap = dict()

    for dir_id in sorted(std):
        dir = std[dir_id]
        n = AnyNode(name=dir_id)
        if dir["parent"] is None:
            idTree = n
        idNodes[dir_id] = n

        idDirMap[dir_id] = dir

    for dir_id in sorted(std):
        dir = std[dir_id]
        n = idNodes[dir_id]
        if dir["parent"] is None:
            continue
        n.parent = idNodes[dir["parent"]]

    for dir_id in sorted(stl):
        dir = stl[dir_id]
        n = AnyNode(name=dir_id)
        if dir["parent"] is None:
            idTree = n
        idNodes[dir_id] = n

        idDirMap[dir_id] = dir

    for dir_id in sorted(stl):
        dir = stl[dir_id]
        n = idNodes[dir_id]
        if dir["parent"] is None:
            continue
        n.parent = idNodes[dir["parent"]]

    # print(RenderTree(idTree))

    nameNode = None
    namedNodeDict = dict()

    node: Node
    for node in PreOrderIter(idTree):
        dir = idDirMap[node.name]

        # Generic attributes
        name = dir["name"]
        deleted = dir["deleted"]
        updated = dir["updated"]

        t = "Directory" if "markAsAddon" in dir else "File"
        if t == "Directory":
            # Folder only attributes
            markAsAddon = dir["markAsAddon"]
            hidden = dir["hidden"]
            n = AnyNode(name=name, type=t, deleted=deleted, updated=updated, markAsAddon=markAsAddon, hidden=hidden)
        else:
            # File only attributes
            size = dir["size"]
            compressedSize = dir["compressedSize"]
            compressed = dir["compressed"]
            sha1 = dir["sha1"]
            n = AnyNode(name=name, type=t, deleted=deleted, updated=updated, size=size, compressedSize=compressedSize,
                        compressed=compressed, sha1=sha1)

        namedNodeDict[node.name] = n

        if node.parent is None:
            nameNode = n
            continue

        parent = node.parent
        n.parent = namedNodeDict[parent.name]

    return nameNode
