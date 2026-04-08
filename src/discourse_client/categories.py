"""Category CRUD and permission management for Discourse."""

from typing import Any

from discourse_client.client import DiscourseClient

# Discourse permission levels
PERMISSION_SEE = 1        # Can see
PERMISSION_REPLY = 2      # Can reply (implies see)
PERMISSION_CREATE = 3     # Can create topics (implies see + reply)
PERMISSION_FULL = 1       # Full access (for staff) — same as "see" but combined with group


def list_categories(client: DiscourseClient) -> list[dict]:
    resp = client.get("/categories.json")
    return resp["category_list"]["categories"]


def get_category(client: DiscourseClient, id_or_slug: int | str) -> dict:
    resp = client.get(f"/c/{id_or_slug}/show.json")
    return resp["category"]


def create_category(
    client: DiscourseClient,
    name: str,
    *,
    slug: str | None = None,
    color: str = "0088CC",
    text_color: str = "FFFFFF",
    parent_category_id: int | None = None,
    permissions: dict[str, int] | None = None,
    description: str | None = None,
    **extra: Any,
) -> dict:
    """Create a category with optional group permissions.

    permissions: dict mapping group name to permission level.
        e.g. {"auditeurs": 2, "animateurs": 3}  # reply / create
        If None, default Discourse permissions apply.
    """
    payload: dict[str, Any] = {
        "name": name,
        "color": color,
        "text_color": text_color,
    }
    if slug:
        payload["slug"] = slug
    if parent_category_id:
        payload["parent_category_id"] = parent_category_id
    if description:
        payload["description"] = description
    if permissions:
        payload["permissions"] = permissions
    payload.update(extra)
    resp = client.post("/categories.json", json=payload)
    return resp["category"]


def update_category(client: DiscourseClient, category_id: int, **kwargs: Any) -> dict:
    resp = client.put(f"/categories/{category_id}.json", json=kwargs)
    return resp["category"]


def delete_category(client: DiscourseClient, category_id: int) -> dict:
    return client.delete(f"/categories/{category_id}.json")
