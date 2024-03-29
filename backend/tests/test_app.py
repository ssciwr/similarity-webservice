import os
import base64


def test_verify(client, apikey):
    res = client.post("/api/verify", headers={"API-Key": apikey})
    assert res.status_code == 200


def test_list_collections(client):
    res = client.get("/api/collection/list")
    assert res.status_code == 200
    assert tuple(res.json["ids"]) == (1, 2, 3)


def test_info_collection(client):
    for id in [1, 2, 3]:
        res = client.get(f"/api/collection/{id}/info")
        assert res.status_code == 200
        assert res.json["id"] == id
        assert res.json["name"] == f"collection{id}"
        assert res.json["last_modified"] is not None
        assert res.json["last_finetuned"] is None


def test_info_collection_invalid_id(client):
    res = client.get("/api/collection/4/info")
    assert res.status_code == 400


def test_create_collection(client, apikey):
    res = client.post(
        "/api/collection/create",
        json={"name": "newcollection"},
        headers={"API-Key": apikey},
    )
    assert res.status_code == 200
    assert res.json["id"] == 4

    res = client.get("/api/collection/list")
    assert res.status_code == 200
    assert tuple(res.json["ids"]) == (1, 2, 3, 4)


def test_create_collection_missing_name(client, apikey):
    res = client.post("/api/collection/create", headers={"API-Key": apikey}, json={})
    assert res.status_code == 400


def test_delete_collection(client, apikey):
    res = client.post("/api/collection/1/delete", headers={"API-Key": apikey})
    assert res.status_code == 200

    res = client.get("/api/collection/list")
    assert res.status_code == 200
    assert tuple(res.json["ids"]) == (2, 3)


def test_delete_collection_invalid_id(client, apikey):
    res = client.post("/api/collection/700/delete", headers={"API-Key": apikey})
    assert res.status_code == 400


def test_update_name_collection(client, apikey):
    res = client.post(
        "/api/collection/1/updatename",
        json={"name": "newname"},
        headers={"API-Key": apikey},
    )
    assert res.status_code == 200

    res = client.get("/api/collection/1/info")
    assert res.status_code == 200
    assert res.json["name"] == "newname"


def test_update_name_collection_invalid_id(client, apikey):
    res = client.post(
        "/api/collection/700/updatename",
        json={"name": "newname"},
        headers={"API-Key": apikey},
    )
    assert res.status_code == 400


def test_update_collection(client, apikey):
    res = client.post(
        "/api/collection/1/updatecontent",
        json={"content": ["new", "content"]},
        headers={"API-Key": apikey},
    )
    assert res.status_code == 200

    res = client.get("/api/collection/1/info")
    assert res.status_code == 200


def test_update_collection_invalid_id(client, apikey):
    res = client.post(
        "/api/collection/700/updatecontent",
        json={"content": ["new", "content"]},
        headers={"API-Key": apikey},
    )
    assert res.status_code == 400


def test_csvfile_download(client):
    res = client.get("/api/collection/1/csvfile")
    assert res.status_code == 200
    assert res.headers["Content-Type"] == "text/csv; charset=utf-8"
    assert res.headers["Content-Disposition"] == "attachment; filename=collection1.csv"


def test_csvfile_download_invalid_id(client):
    res = client.get("/api/collection/5/csvfile")
    assert res.status_code == 400


def test_finetune_collection(client, apikey):
    res = client.post(
        "/api/collection/1/finetune",
        headers={"API-Key": apikey},
        data="https://www.ssc.uni-heidelberg.de/sites/default/files/styles/img_free_aspect_1540/public/2021-06/dummyuser.png?itok=yL_ne0Qs, https://www.ssc.uni-heidelberg.de/sites/default/files/styles/img_free_aspect_1540/public/2021-06/dummyuser.png?itok=yL_ne0Qs\nhttps://www.ssc.uni-heidelberg.de/sites/default/files/styles/img_free_aspect_1540/public/2021-06/dummyuser.png?itok=yL_ne0Qs, https://www.ssc.uni-heidelberg.de/sites/default/files/styles/img_free_aspect_1540/public/2021-06/dummyuser.png?itok=yL_ne0Qs",
    )
    assert res.status_code == 200


def test_finetune_collection_invalid_id(client, apikey):
    res = client.post(
        "/api/collection/112/finetune",
        headers={"API-Key": apikey},
        data="https://www.ssc.uni-heidelberg.de/sites/default/files/styles/img_free_aspect_1540/public/2021-06/dummyuser.png?itok=yL_ne0Qs, https://www.ssc.uni-heidelberg.de/sites/default/files/styles/img_free_aspect_1540/public/2021-06/dummyuser.png?itok=yL_ne0Qs\nhttps://www.ssc.uni-heidelberg.de/sites/default/files/styles/img_free_aspect_1540/public/2021-06/dummyuser.png?itok=yL_ne0Qs, https://www.ssc.uni-heidelberg.de/sites/default/files/styles/img_free_aspect_1540/public/2021-06/dummyuser.png?itok=yL_ne0Qs",
    )
    assert res.status_code == 400


def test_similarity_search(client):
    image_path = os.path.join(os.path.dirname(__file__), "dum_similarity_img.png")
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()

    # Encode the image data as base64
    encoded_image = base64.b64encode(image_data)
    res = client.post("/api/collection/1/search", data=encoded_image)
    assert res.status_code == 200


def test_similarity_search_invalid_id(client):
    image_path = os.path.join(os.path.dirname(__file__), "dum_similarity_img.png")
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()

    # Encode the image data as base64
    encoded_image = base64.b64encode(image_data)
    res = client.post("/api/collection/112/search", data=encoded_image)
    assert res.status_code == 400
