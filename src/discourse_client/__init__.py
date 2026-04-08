"""Discourse API client for CLEAgora."""

from discourse_client import categories, settings, topics, users
from discourse_client.client import DiscourseClient

__all__ = ["DiscourseClient", "categories", "settings", "topics", "users"]
