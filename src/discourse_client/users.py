"""User, group, and invite management for Discourse."""

from typing import Any

from discourse_client.client import DiscourseClient

# --- Groups ---

def list_groups(client: DiscourseClient) -> list[dict]:
    resp = client.get("/groups.json")
    return resp["groups"]


def create_group(
    client: DiscourseClient,
    name: str,
    *,
    full_name: str | None = None,
    visibility_level: int = 2,  # 0=public, 1=logged-in, 2=members, 3=staff, 4=owners
    members_visibility_level: int = 2,
    mentionable_level: int = 3,  # 0=nobody, 1=admins+mods, 3=members, 99=everyone
    messageable_level: int = 3,
    **extra: Any,
) -> dict:
    payload: dict[str, Any] = {
        "group": {
            "name": name,
            "visibility_level": visibility_level,
            "members_visibility_level": members_visibility_level,
            "mentionable_level": mentionable_level,
            "messageable_level": messageable_level,
            **extra,
        }
    }
    if full_name:
        payload["group"]["full_name"] = full_name
    return client.post("/admin/groups.json", json=payload)


def get_group(client: DiscourseClient, name: str) -> dict:
    resp = client.get(f"/groups/{name}.json")
    return resp["group"]


def add_group_members(client: DiscourseClient, group_id: int, usernames: list[str]) -> dict:
    return client.put(f"/groups/{group_id}/members.json", json={
        "usernames": ",".join(usernames),
    })


def remove_group_members(client: DiscourseClient, group_id: int, usernames: list[str]) -> dict:
    return client.delete(f"/groups/{group_id}/members.json")


# --- Users ---

def list_users(client: DiscourseClient, flag: str = "active") -> list[dict]:
    resp = client.get(f"/admin/users/list/{flag}.json")
    return resp


def get_user(client: DiscourseClient, username: str) -> dict:
    resp = client.get(f"/u/{username}.json")
    return resp["user"]


def create_user(
    client: DiscourseClient,
    name: str,
    email: str,
    username: str,
    password: str,
    *,
    active: bool = True,
    approved: bool = True,
) -> dict:
    return client.post("/users.json", json={
        "name": name,
        "email": email,
        "username": username,
        "password": password,
        "active": active,
        "approved": approved,
    })


# --- Invites ---

def create_invite(
    client: DiscourseClient,
    email: str,
    *,
    group_ids: list[int] | None = None,
    custom_message: str | None = None,
    topic_id: int | None = None,
) -> dict:
    payload: dict[str, Any] = {"email": email}
    if group_ids:
        payload["group_ids"] = group_ids
    if custom_message:
        payload["custom_message"] = custom_message
    if topic_id:
        payload["topic_id"] = topic_id
    return client.post("/invites.json", json=payload)


def bulk_invite(
    client: DiscourseClient,
    emails: list[str],
    group_ids: list[int] | None = None,
) -> list[dict]:
    """Invite multiple users. Returns list of invite results."""
    results = []
    for email in emails:
        result = create_invite(client, email, group_ids=group_ids)
        results.append(result)
    return results
