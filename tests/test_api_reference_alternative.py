import os

import alias_api
import sgtk

engine = sgtk.platform.current_engine()

REF1_DATA = {
    "path": os.path.join(engine.disk_location, "tests", "data", "sphere.wref"),
    "source_path": os.path.join(engine.disk_location, "tests", "data", "sphere.wire"),
    "name": "sphere.wire"
}

REF2_DATA = {
    "path": os.path.join(engine.disk_location, "tests", "data", "cube.wref"),
    "source_path": os.path.join(engine.disk_location, "tests", "data", "cube.wire"),
    "name": "cube.wire"
}

ALT_DATA = {
    "name": "AlternativeTest"
}


def test_create_reference():
    ref1 = alias_api.create_reference(REF1_DATA["path"])
    assert ref1.name == REF1_DATA["name"]
    assert ref1.path == REF1_DATA["path"]
    assert ref1.source_path == REF1_DATA["source_path"]
    assert ref1.uuid is not None
    REF1_DATA["uuid"] = ref1.uuid


def test_get_references():
    refs = alias_api.get_references()
    assert len(refs) == 1
    assert refs[0].name == REF1_DATA["name"]
    assert refs[0].path == REF1_DATA["path"]
    assert refs[0].source_path == REF1_DATA["source_path"]
    assert refs[0].uuid == REF1_DATA["uuid"]


def test_get_reference_by_name():
    ref = alias_api.get_reference_by_name(REF1_DATA["name"])
    assert ref.name == REF1_DATA["name"]
    assert ref.path == REF1_DATA["path"]
    assert ref.source_path == REF1_DATA["source_path"]
    assert ref.uuid == REF1_DATA["uuid"]


def test_get_reference_by_path():
    ref = alias_api.get_reference_by_path(REF1_DATA["path"])
    assert ref.name == REF1_DATA["name"]
    assert ref.path == REF1_DATA["path"]
    assert ref.source_path == REF1_DATA["source_path"]
    assert ref.uuid == REF1_DATA["uuid"]


def test_get_reference_by_uuid():
    ref = alias_api.get_reference_by_uuid(REF1_DATA["uuid"])
    assert ref.name == REF1_DATA["name"]
    assert ref.path == REF1_DATA["path"]
    assert ref.source_path == REF1_DATA["source_path"]
    assert ref.uuid == REF1_DATA["uuid"]


def test_update_reference():
    new_ref = alias_api.update_reference(REF1_DATA["path"], REF2_DATA["path"])
    assert new_ref.name == REF2_DATA["name"]
    assert new_ref.path == REF2_DATA["path"]
    assert new_ref.source_path == REF2_DATA["source_path"]
    assert new_ref.uuid is not None


def test_create_alternative():
    alt = alias_api.create_alternative(ALT_DATA["name"])
    assert alt.name == ALT_DATA["name"]


def test_get_alternative_by_name():
    alt = alias_api.get_alternative_by_name(ALT_DATA["name"])
    assert alt.name == ALT_DATA["name"]


def test_add_reference_to_alternative():
    alt = alias_api.get_alternative_by_name(ALT_DATA["name"])
    ref = alias_api.get_reference_by_path(REF2_DATA["path"])
    alt.add_reference(ref)


def test_get_alternative_references():
    alt = alias_api.get_alternative_by_name(ALT_DATA["name"])
    refs = alt.get_references()
    assert len(refs) == 1
    assert refs[0].name == REF2_DATA["name"]
    assert refs[0].path == REF2_DATA["path"]
    assert refs[0].source_path == REF2_DATA["source_path"]
    assert refs[0].uuid is not None


test_create_reference()
test_get_references()
test_get_reference_by_name()
test_get_reference_by_path()
test_get_reference_by_uuid()
test_update_reference()
test_create_alternative()
test_get_alternative_by_name()
test_add_reference_to_alternative()
test_get_alternative_references()
