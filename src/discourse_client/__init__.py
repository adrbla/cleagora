"""Discourse API client for CLEAgora."""

from discourse_client import categories, topics, users
from discourse_client.client import DiscourseClient

__all__ = ["DiscourseClient", "categories", "topics", "users"]
