import threading

from pandas.io.formats.format import buffer_put_lines
from color_map import CLASS_MAP
import definitions
from utils.xml_helpers import bounds2int, bounds2p, bounds_of
from utils.device import Device
from xml.etree import ElementTree
import os
from utils.group import Groups


def big_enough(element):
    (a, b, c, d) = bounds2int(element.attrib["bounds"])
    return (d - b) >= 25 and (c - a) >= 25


def class_of_image(element):
    (a, b, c, d) = bounds2int(element.attrib["bounds"])
    x = c - a
    y = d - b
    if x <= 150 or y <= 150:
        return "icon"
    else:
        return "image"


def group_to_str(g):
    if type(g) is list:
        return f"L: {len(g)}"
    else:
        return f"E: {g.attrib.get('class')}"


def merge_bounds(es):
    bs = (bounds2int(e.attrib["bounds"]) for e in es)
    x, y, a, b = next(bs)
    for (x1, y1, x2, y2) in bs:
        x = x1 if x1 < x else x
        y = y1 if y1 < y else y
        a = x2 if x2 > a else a
        b = y2 if y2 > b else b
    return f"[{x},{y}][{a},{b}]"


def atomic_class(group, x1, y1, x2, y2, type):
    classes = set(c for e in group for c in e.attrib.get("class").split(","))
    return ",".join(classes)


def list2element(g, device):
    if type(g) is list:
        if len(g) == 1:
            return g[0]
        else:
            bounds = merge_bounds(g)
            ele = ElementTree.Element(
                "node",
                {
                    "class": atomic_class(g, *bounds2int(bounds), device),
                    "bounds": f"{bounds}",
                    "index": g[0].attrib["index"],
                },
            )
            return ele
    elif type(g) is ElementTree.Element:
        return g
    else:
        raise RuntimeError(type(g), " is not tree element")


def _group_by_position(elements, device):
    "group elements by bounds"
    groups = []
    buffer = []
    for e in elements:
        if len(buffer) == 0:
            buffer.append(e)
        else:
            (x, y) = bounds2p(buffer[-1].attrib["bounds"], center=True)
            _x, _y = bounds2p(e.attrib["bounds"], center=True)
            is_center_close = abs(x - _x) <= 10 or abs(_y - y) <= 10
            (x, y) = bounds2p(buffer[-1].attrib["bounds"])
            _x, _y = bounds2p(e.attrib["bounds"])
            is_edge_close = abs(x - _x) <= 10 or abs(_y - y) <= 10
            if is_center_close or is_edge_close:
                buffer.append(e)
            else:
                if len(buffer) != 0:
                    groups.append(list2element(buffer, device))
                    buffer = []
                buffer.append(e)
    if len(buffer) != 0:
        # TODO keep child while merging
        groups.append(list2element(buffer, device))
    return groups


def guess_group_class(group, x1, y1, x2, y2, type):
    classes = set(c for e in group for c in e.attrib.get("class").split(","))
    allbounds = list(bounds_of(e) for e in group)
    same_y = (
        len(set(b[1] for b in allbounds)) == 1 or len(set(b[3] for b in allbounds)) == 1
    )
    same_x = (
        len(set(b[0] for b in allbounds)) == 1 or len(set(b[2] for b in allbounds)) == 1
    )
    add = ""
    if len(classes) == 1 or ("horlist" in classes and len(classes) == 2):
        if same_y:
            add += "horlist,"
        if same_x:
            add += "list,"
    cls = add + ",".join(classes)
    return cls


def component_group_name(comp, first, last, type):
    if type == "tablet":
        H = 1600
        W = 2600
    else:
        H = 1800
        W = 800

    classes = set(c for c in comp.attrib.get("class").split(","))
    (x1, y1, x2, y2) = bounds_of(comp)
    x, y = x2 - x1, y2 - y1
    # elif y1 > H * 0.9:
    # return "BottomBar"
    # search
    # if cls == 'text' and 'search' in text_field.lower():
    # cls = 'Search'
    # top tab layout
    # list view
    # pic side info
    # big pic
    # side nav
    # bottom tab layout
    cls = ""

    if first and y2 < H * 0.2 and y <= 200:
        cls = "ToolBar"
    elif last and y1 > H * 0.8 and x > W * 0.9 and y <= 200:
        cls = "BottomTabLayout"
    elif "horlist" in classes and "list" in classes:
        cls = "GridLayout"
    elif set(["horlist", "text"]) == classes and y2 < H * 0.5:
        cls = "TopTabLayout"
    elif "tab" in classes:  # normal at top
        cls = "TopTabLayout"
    elif "list" in classes:
        cls = "ListView"
    elif "control" in classes:
        cls = "ControlItem"
    elif "icon" in classes:
        if "text" in classes:
            cls = "IconInfo"
        else:
            # maybe ignore?
            cls = "IconInfo"
    elif "image" in classes:
        # image size
        if "text" in classes:
            cls = "PicInfo"
        else:
            cls = "PicInfo"
    elif "text" in classes:
        text = comp.attrib.get("text")
        if text is not None and "search" in text:
            cls = "Search"
        else:
            cls = "TextInfo"
    else:
        if type == "phone":
            cls = "Others"
        else:
            cls = "GridLayout"

    cls = cls + ":" + ",".join(classes)
    comp.attrib["class"] = cls
    return cls


def grouping_atomic(g, device):
    assert type(g) is list
    if len(g) == 1:
        return g[0]

    bounds = merge_bounds(g)
    ele = ElementTree.Element(
        "node",
        {
            "class": guess_group_class(g, *bounds2int(bounds), device),
            "bounds": f"{bounds}",
            "index": g[0].attrib["index"],
        },
    )
    return ele


def _group_by_pos_cls(elements, type, dir="hor"):
    "group elements by bounds"
    groups = []
    buffer = []
    for e in elements:
        if len(buffer) == 0:
            buffer.append(e)
        else:
            (ax1, ay1, ax2, ay2) = bounds_of(buffer[-1])
            (bx1, by1, bx2, by2) = bounds_of(e)

            def is_close(a, b):
                return abs(a - b) <= 10

            if dir == "hor":
                inrange1 = ay1 <= by1 < ay2
                inrange2 = ay1 < by2 <= ay2
                inrange3 = by1 <= ay1 < by2
                inrange4 = by1 < ay2 <= by2
                cmp_pos = inrange1 or inrange2 or inrange3 or inrange4
                cmp_cls = True
            else:
                center_ax = (ax1 + ax2) / 2
                center_bx = (bx1 + bx2) / 2
                is_center_close = is_close(center_ax, center_bx)
                is_edge_close = is_close(ax1, bx1) or is_close(ax2, bx2)
                cmp_pos = is_center_close or is_edge_close
                is_same_cls = buffer[-1].attrib["class"] == e.attrib["class"]
                cmp_cls = is_same_cls if dir != "hor" else True
            if cmp_cls and cmp_pos:
                buffer.append(e)
            else:
                if len(buffer) != 0:
                    groups.append(grouping_atomic(buffer, type))
                    buffer = []
                buffer.append(e)
    if len(buffer) != 0:
        groups.append(grouping_atomic(buffer, type))
    return groups


def _group_by_structure(element, type):
    assert len(element) != 0, "spliting a leaf node"
    ungrouped = []
    grouped = []
    buffer = []
    for child in element:
        if len(child) == 0:
            buffer.append(child)
        else:
            if len(buffer) != 0:
                grouped.extend(_group_by_position(buffer, type))
                buffer = []
            ungrouped.append(child)

    if len(buffer) != 0:
        grouped.extend(_group_by_position(buffer, type))

    def group_by_type(g):
        return list2element(g, type)

    grouped = list(map(group_by_type, grouped))
    return ungrouped, grouped


def print_g(g):
    for e in g:
        e = e.attrib
        print(
            f"{e['index']} {e['class']} {e['bounds']} {e.get('text')} {e.get('resource-id')}"
        )


def group_elements(tree, pkg, type):
    # preprocess tree
    tree = tree.find(f"./node[@package='{pkg}']")
    for i, e in enumerate(tree.iter()):
        if len(e) == 1:  # one child
            e[0].attrib["bounds"] = e.attrib["bounds"]

        e.attrib["index"] = str(i)
        text_field = e.attrib.get("text")
        cls = CLASS_MAP.get(e.attrib.get("class"))
        if cls is None:
            if len(text_field) > 0:
                cls = "text"
            else:
                cls = e.attrib["class"].split(".")[-1]
                # common errors
                if cls == "View":
                    cls = "text"
                elif cls == "LinearLayout" and len(e) == 0:
                    (x1, y1, x2, y2) = bounds_of(e)
                    if (y2 - y1) / (x2 - x1) < 1.5:
                        cls = "image"
        if cls == "image":
            cls = class_of_image(e)
        e.attrib["class"] = cls

    queue = [tree]
    grouped = []
    while True:
        try:
            e = queue.pop(0)
        except IndexError:
            break
        try:
            ungrouped, groupedd = _group_by_structure(e, type)
            grouped.extend(groupedd)
            queue.extend(ungrouped)
        except AssertionError:
            grouped.append(e)
    assert len(queue) == 0
    res = grouped

    def by_index(e):
        return int(e.attrib["index"])

    res = filter(big_enough, res)
    res = sorted(res, key=by_index)
    res = _group_by_pos_cls(res, type, "hor")
    res = _group_by_pos_cls(res, type, "ver")
    # res = _group_by_pos_cls(res, type, "hor")
    for i, e in enumerate(res):
        first, last = False, False
        if i == 0:
            first = True
        if i == len(res) - 1:
            last = True
        component_group_name(e, first, last, type)

    # newtree = ElementTree.Element("node")
    # for e in pes:
    #     newtree.append(e)
    # ElementTree.indent(newtree)
    # ElementTree.dump(newtree)
    return res


def _test():
    base = definitions._create(os.path.join(definitions.DATA_DIR, "test-grouping1"))
    source = os.path.join(definitions.DATA_DIR, "unique")

    gid = "1664012114"
    gid = None
    pkg = "com.google.android.youtube"
    pkg = None
    if pkg is None:
        for folder in os.scandir(source):
            definitions._create(os.path.join(base, folder.name))
        groups = (g for g in Groups.from_out_dir(source) if g.is_legit())
    else:
        source = os.path.join(source, pkg)
        groups = (g for g in Groups.from_folder(source, pkg) if g.is_legit())

    def _grouping_one(g):
        print(g)
        out = os.path.join(base, g.pkg)
        pt = g.ptree()
        pes = group_elements(pt, g.pkg, "phone")
        tt = g.ttree()
        tes = group_elements(tt, g.pkg, "tablet")
        g.xml_copy_to(out, pes, tes)
        g.draw(out, [pes, tes])

    if pkg is None:
        threads = [
            threading.Thread(target=_grouping_one, args=[g])
            for i, g in enumerate(groups)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    else:
        for g in groups:
            if gid:
                if g.id == gid:
                    _grouping_one(g)
            else:
                _grouping_one(g)


if __name__ == "__main__":
    _test()
