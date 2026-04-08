"""Topic and post CRUD for Discourse."""

from typing import Any

from discourse_client.client import DiscourseClient


def list_topics(client: DiscourseClient, category_slug: str, category_id: int) -> list[dict]:
    resp = client.get(f"/c/{category_slug}/{category_id}.json")
    return resp["topic_list"]["topics"]


def get_topic(client: DiscourseClient, topic_id: int) -> dict:
    resp = client.get(f"/t/{topic_id}.json")
    return resp


def create_topic(
    client: DiscourseClient,
    title: str,
    raw: str,
    category_id: int,
    *,
    tags: list[str] | None = None,
    **extra: Any,
) -> dict:
    payload: dict[str, Any] = {
        "title": title,
        "raw": raw,
        "category": category_id,
    }
    if tags:
        payload["tags"] = tags
    payload.update(extra)
    return client.post("/posts.json", json=payload)


def create_post(
    client: DiscourseClient,
    topic_id: int,
    raw: str,
    *,
    reply_to_post_number: int | None = None,
    **extra: Any,
) -> dict:
    payload: dict[str, Any] = {
        "topic_id": topic_id,
        "raw": raw,
    }
    if reply_to_post_number:
        payload["reply_to_post_number"] = reply_to_post_number
    payload.update(extra)
    return client.post("/posts.json", json=payload)


def update_topic(client: DiscourseClient, topic_id: int, **kwargs: Any) -> dict:
    return client.put(f"/t/-/{topic_id}.json", json=kwargs)


def pin_topic(client: DiscourseClient, topic_id: int, *, globally: bool = False) -> dict:
    return client.put(f"/t/{topic_id}/status.json", json={
        "status": "pinned_globally" if globally else "pinned",
        "enabled": "true",
    })


def close_topic(client: DiscourseClient, topic_id: int) -> dict:
    return client.put(f"/t/{topic_id}/status.json", json={
        "status": "closed",
        "enabled": "true",
    })


def delete_topic(client: DiscourseClient, topic_id: int) -> dict:
    return client.delete(f"/t/{topic_id}.json")
