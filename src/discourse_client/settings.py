"""Site settings management for Discourse."""

from typing import Any

from discourse_client.client import DiscourseClient


def get_setting(client: DiscourseClient, name: str) -> Any:
    resp = client.get(f"/admin/site_settings/{name}.json")
    return resp


def update_setting(client: DiscourseClient, name: str, value: Any) -> dict:
    return client.put(f"/admin/site_settings/{name}.json", json={name: value})


def update_settings(client: DiscourseClient, settings: dict[str, Any]) -> dict[str, bool]:
    """Apply multiple settings. Returns {name: success} mapping."""
    results = {}
    for name, value in settings.items():
        try:
            update_setting(client, name, value)
            results[name] = True
        except Exception as e:
            print(f"  WARNING: Failed to set {name}={value}: {e}")
            results[name] = False
    return results
