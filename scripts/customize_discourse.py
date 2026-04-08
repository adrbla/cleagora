#!/usr/bin/env python3
"""Apply CLEAgora UX customization to Discourse.

Strips Discourse down to a clean, focused research community experience:
- Closed community (invite-only, login required)
- No gamification (badges, likes, trust level indicators)
- Simplified navigation (categories-only, no suggested topics)
- Lower posting thresholds for respondents
- French locale defaults
"""

import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from discourse_client import DiscourseClient
from discourse_client.settings import update_settings

load_dotenv()


# --- Site settings to apply ---
# Organized by category for readability.

SETTINGS: dict[str, object] = {
    # === Access control ===
    "login_required": True,
    "invite_only": True,
    "must_approve_users": False,
    "enable_local_logins": True,

    # === Registration & onboarding ===
    "default_trust_level": 1,  # TL1 = Basic — skip TL0 restrictions
    "disable_discourse_narrative_bot": True,  # No Discobot
    "discourse_narrative_bot_enabled": False,
    "send_welcome_message": True,

    # === Gamification — disable ===
    "enable_badges": False,
    "enable_badge_granted_title": False,
    "default_other_enable_quoting": True,

    # === Likes — disable ===
    "post_menu": "reply|share|bookmark|flag",  # Remove "like" from post actions
    "post_menu_hidden_items": "flag|bookmark",

    # === Trust levels — minimize impact ===
    "tl1_requires_topics_entered": 0,
    "tl1_requires_read_posts": 0,
    "tl1_requires_time_spent_mins": 0,
    "tl2_requires_topics_entered": 0,
    "tl2_requires_read_posts": 0,
    "tl2_requires_time_spent_mins": 0,
    "tl2_requires_days_visited": 0,
    "tl2_requires_likes_received": 0,
    "tl2_requires_likes_given": 0,
    "tl2_requires_topic_reply_count": 0,

    # === Posting thresholds — lower for respondents ===
    "min_post_length": 5,  # Default 20 is too long for quick reactions
    "min_first_post_length": 5,
    "min_topic_title_length": 5,
    "body_min_entropy": 1,
    "title_min_entropy": 1,
    "newuser_max_replies_per_topic": 0,  # 0 = unlimited
    "newuser_max_links": 5,
    "newuser_max_images": 5,
    "newuser_spam_host_threshold": 0,  # Disable spam host check

    # === Navigation & homepage ===
    "top_menu": "categories|latest",  # Simplified top menu
    "desktop_category_page_style": "categories_with_featured_topics",
    "default_navigation_menu_categories": "",  # Will be set after categories are created

    # === Suggested topics — disable ===
    "suggested_topics": 0,
    "suggested_topics_unread_max_days_old": 0,

    # === User directory — hide ===
    "enable_user_directory": False,

    # === User profiles — simplify ===
    "enable_user_status": False,

    # === Digest & notifications ===
    "default_email_digest_frequency": 10080,  # Weekly (minutes)
    "default_email_level": 2,  # Only when away
    "disable_digest_emails": False,
    "default_notification_level": 1,  # Normal

    # === Formatting & content ===
    "default_locale": "fr",
    "allow_html_tables": True,

    # === Search ===
    "log_search_queries": True,

    # === Other cleanup ===
    "enable_whispers": True,  # Useful for staff-only notes
    "allow_uncategorized_topics": False,
    "show_subcategory_list": False,
    "enable_group_directory": False,
}


def main():
    print("=== CLEAgora — Discourse UX Customization ===\n")

    url = os.environ["DISCOURSE_URL"]
    key = os.environ["DISCOURSE_API_KEY"]
    username = os.environ.get("DISCOURSE_API_USERNAME", "system")
    client = DiscourseClient(url, key, username)

    print(f"Target: {url}")
    print(f"Settings to apply: {len(SETTINGS)}\n")

    results = update_settings(client, SETTINGS)

    success = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)

    print(f"\n=== Done: {success} applied, {failed} failed ===")

    if failed:
        print("\nFailed settings:")
        for name, ok in results.items():
            if not ok:
                print(f"  - {name}")

    client.close()


if __name__ == "__main__":
    main()
