#!/usr/bin/env python3
"""Create and apply CLEAgora theme component for UI customizations.

Hides unwanted Discourse UI elements, renames labels, and applies
CSS overrides for a clean research community experience.
"""

import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from discourse_client import DiscourseClient

load_dotenv()

CSS = """
/* === Force light header === */
.d-header-wrap .d-header {
  background-color: #fff !important;
  border-bottom: 1px solid #e0e0e0;
}
.d-header-wrap .d-header .d-header-icons .icon,
.d-header-wrap .d-header .d-header-icons .btn,
.d-header-wrap .d-header .title a,
.d-header .hamburger-panel,
.d-header .header-sidebar-toggle button {
  color: #0E131B !important;
}

/* === Hide default welcome banner + search bar === */
.welcome-banner,
.welcome-banner__wrapper,
.search-banner,
.custom-search-banner,
.homepage-hero-search,
.search-banner-container,
.custom-homepage-welcome-header {
  display: none !important;
}

/* === Custom welcome banner === */
.cleagora-welcome {
  text-align: center;
  padding: 24px 20px 16px;
  margin-bottom: 8px;
}
.cleagora-welcome h2 {
  font-size: 1.6rem;
  font-weight: 700;
  color: #0E131B;
  margin: 0 0 12px 0;
}
.cleagora-welcome .welcome-text {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}
.cleagora-welcome .welcome-text a {
  color: #425779;
  text-decoration: underline;
}

/* === Hide "catégories" dropdown breadcrumb on topic lists === */
.category-breadcrumb .category-drop .select-kit-header .name {
  font-size: 0;
}
.category-breadcrumb .category-drop .select-kit-header .name::after {
  content: "modules";
  font-size: 1rem;
}

/* === Logo sizing: 25% smaller === */
.d-header .title .logo-big {
  max-height: 30px !important;
  height: 30px !important;
}

/* === Community title next to logo === */
.d-header .title .header-community-title {
  font-size: 0.9rem;
  font-weight: 500;
  color: #86898D;
  margin-left: 12px;
  white-space: nowrap;
  border-left: 1px solid #ddd;
  padding-left: 12px;
}

/* === Hide "Alimenté par Discourse" footer === */
.footer-message,
#powered-by-discourse,
.crawl-below-body,
a[href*="discourse.org"],
.custom-footer,
footer .powered-by,
#topic-footer-buttons + div,
.below-footer-outlet {
  display: none !important;
}
/* Catch-all: hide any element containing "Discourse" link in footer area */
#main-outlet-wrapper ~ *:not(script):not(link) a[href*="discourse.org"] {
  display: none !important;
}
#main-outlet-wrapper ~ *:not(script):not(link) {
  visibility: visible;
}

/* === Hide unwanted sidebar links === */
.sidebar-section-link[data-link-name="invite"],
.sidebar-section-link[data-link-name="filter"],
.sidebar-section-link[data-link-name="everything"],
.sidebar-section-link[data-link-name="all-categories"],
.sidebar-section-link[data-link-name="my-messages"] {
  display: none !important;
}

/* === Keep "Mes posts" visible, rename to "Mes posts" === */
.sidebar-section-link[data-link-name="my-posts"] .sidebar-section-link-content-text {
  font-size: 0;
  line-height: 0;
}
.sidebar-section-link[data-link-name="my-posts"] .sidebar-section-link-content-text::after {
  content: "Mes posts";
  font-size: 1rem;
  line-height: normal;
}

/* === Hide "Créer un sujet" button for non-staff === */
body:not(.staff) #create-topic,
body:not(.staff) .btn-default.create-topic {
  display: none !important;
}

/* === Hide tags everywhere === */
.discourse-tags,
.tag-list,
.topic-tag,
.tag-drop,
.tags-admin-menu,
.sidebar-section[data-section-name="tags"] {
  display: none !important;
}

/* === Topic footer: hide everything except Reply button === */
/* Hide Partager, Mettre un signet, Signaler buttons at bottom of topic */
.topic-footer-main-buttons .btn:not(.create),
.topic-footer-main-buttons .topic-footer-button:not(.create) {
  display: none !important;
}
/* Keep the Reply button visible */
.topic-footer-main-buttons .btn.create {
  display: inline-flex !important;
}
/* Hide notification level button row */
.topic-notifications-button,
.timeline-footer-controls .topic-notifications-button {
  display: none !important;
}

/* === Category description banners (CSS-only, per-category) === */
body[class*="category-"] .category-breadcrumb::after {
  display: block;
  background: #f4f6f8;
  border-left: 4px solid var(--tertiary);
  padding: 12px 16px;
  margin: 12px 0 4px 0;
  border-radius: 0 6px 6px 0;
  font-size: 0.95em;
  line-height: 1.5;
  color: #333;
}
body.category-bienvenue .category-breadcrumb::after {
  content: "Bienvenue dans votre espace auditeurs ! Vous trouverez ici les informations pratiques et les règles de fonctionnement.";
}
body.category-semaine-1-votre-matinale .category-breadcrumb::after {
  content: "Dans ce module, on explore votre relation à la matinale de France Inter. Vos habitudes d'écoute, ce qui vous accroche, ce qui vous fait décrocher.";
}
body.category-semaine-2-reactions-debats .category-breadcrumb::after {
  content: "Dans ce module, on passe aux réactions concrètes. Donnez votre avis sur les chroniques, le traitement de l'actu et la place de l'humour !";
}
body.category-semaine-3-et-si-on-imaginait .category-breadcrumb::after {
  content: "Dans ce module, on passe du constat à la proposition. Quelle serait votre matinale idéale, que changeriez-vous ?";
}
body.category-le-cafe .category-breadcrumb::after {
  content: "Le café, c'est votre espace libre. Discutez de ce que vous voulez, échangez entre auditeurs !";
}
body.category-coulisses .category-breadcrumb::after {
  content: "Espace réservé à l'équipe de recherche. Notes d'animation, signaux à creuser, coordination.";
}

/* === Rename "Catégories" to "Modules" in sidebar === */
.sidebar-section[data-section-name="categories"] .sidebar-section-header-text {
  font-size: 0;
  line-height: 0;
}
.sidebar-section[data-section-name="categories"] .sidebar-section-header-text::after {
  content: "Modules";
  font-size: 0.857rem;
  line-height: normal;
}
"""

HEADER_HTML_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "theme-head.html")


def main():
    print("=== CLEAgora — Apply Theme Component ===\n")

    url = os.environ["DISCOURSE_URL"]
    key = os.environ["DISCOURSE_API_KEY"]
    # Theme admin requires system user
    client = DiscourseClient(url, key, "system")

    # Check if component already exists
    resp = client.get("/admin/themes.json")
    themes = resp.get("themes", resp) if isinstance(resp, dict) else resp
    existing_id = None
    for t in themes:
        if t["name"] == "CLEAgora Customizations":
            existing_id = t["id"]
            print(f"Found existing component id={existing_id}, updating...")
            break

    if existing_id:
        theme_id = existing_id
    else:
        resp = client.post("/admin/themes.json", json={
            "theme": {
                "name": "CLEAgora Customizations",
                "component": True,
            }
        })
        theme = resp.get("theme", resp)
        theme_id = theme["id"]
        print(f"Created theme component id={theme_id}")

    # Apply CSS and header HTML
    client.put(f"/admin/themes/{theme_id}.json", json={
        "theme": {
            "theme_fields": [
                {"target": "common", "name": "scss", "value": CSS},
                {"target": "common", "name": "head_tag", "value": open(HEADER_HTML_PATH).read()},
            ]
        }
    })
    print("CSS + JS applied")

    # Add component to Foundation theme (id=-1)
    foundation = client.get("/admin/themes/-1.json")
    current_children = [c["id"] for c in foundation.get("theme", foundation).get("child_themes", [])]
    if theme_id not in current_children:
        current_children.append(theme_id)
        client.put("/admin/themes/-1.json", json={
            "theme": {
                "child_theme_ids": current_children,
            }
        })
        print("Component added to Foundation theme")
    else:
        print("Component already attached to Foundation theme")

    client.close()
    print("\n=== Done ===")


if __name__ == "__main__":
    main()
