#!/usr/bin/env python3
"""Apply text overrides, category renames, and sidebar customizations.

- Replaces "catégorie" with "module" across Discourse UI strings
- Renames "Semaine N" categories to "Module N"
- Updates category descriptions with intro text
- Configures sidebar links
"""

import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from discourse_client import DiscourseClient, categories
from discourse_client.settings import update_setting

load_dotenv()


# --- Translation overrides: catégorie → module ---

TEXT_OVERRIDES = {
    # Core UI
    "js.categories.category": "Module",
    "js.category_title": "Module",
    "js.search.advanced.in_category.label": "Module",
    "js.category.sort_options.category": "Module",
    "js.review.filters.category": "Module",
    "js.search.categories": "Modules",
    "search.types.category": "Modules",
    "js.search.type.categories": "Modules",
    "js.category.none": "(aucun module)",
    "js.review.filters.all_categories": "(tous les modules)",

    # Sidebar
    "js.sidebar.sections.categories.header_link_text": "Modules",

    # Category page
    "js.category_page_style.categories_only": "Modules seuls",
    "js.categories.n_more.other": "Modules (%{count} autres)\u2026",
    "js.filters.categories.title_in": "Module - %{categoryName}",
    "js.categories.category_list": "Afficher la liste des modules",
    "js.filters.categories.help": "tous les sujets regroupés par module",

    # About topic prefix
    "category.topic_prefix": "À propos du module %{category}",

    # Category row
    "js.category_row.subcategory_count.one": "+%{count} sous-module",
    "js.category_row.subcategory_count.other": "+%{count} sous-modules",

    # Edit topic
    "js.edit_topic": "modifier le titre et le module de ce sujet",

    # Misc
    "topics_in_category": "Sujets dans le module « %{category} »",
    "activerecord.attributes.category.name": "Nom du module",
    "activerecord.attributes.topic.category_id": "Module",
    "js.action_codes.category_changed": "Module mis à jour %{when}",
    "js.category.position": "Position sur la page des modules :",
    "reviewables.reasons.links.category": "paramètres du module",
    "js.search.tips.category_tag": "filtres par module ou par étiquette",
    "js.styleguide.sections.categories_list.title": "Liste des modules",
    "js.shared_drafts.destination_category": "Module de destination",
}

# --- Category renames and updated descriptions ---

CATEGORY_UPDATES = {
    "semaine-1-votre-matinale": {
        "name": "Module 1 — Votre matinale",
        "description": (
            "**Dans ce module, on explore votre relation à la matinale de France Inter.**\n\n"
            "On cherche à comprendre vos habitudes d'écoute, ce qui vous accroche, "
            "ce qui vous fait décrocher, et les mots qui vous viennent spontanément "
            "quand vous pensez à cette émission.\n\n"
            "Répondez aux discussions ci-dessous et n'hésitez pas à réagir aux messages des autres !"
        ),
    },
    "semaine-2-reactions-debats": {
        "name": "Module 2 — Réactions & débats",
        "description": (
            "**Dans ce module, on passe aux réactions concrètes.**\n\n"
            "On cherche à comprendre ce que vous pensez des chroniques, "
            "du traitement de l'actu et de la place de l'humour dans la matinale. "
            "C'est le moment de donner votre avis et de débattre entre vous !\n\n"
            "Répondez aux discussions ci-dessous et rebondissez sur les avis des autres."
        ),
    },
    "semaine-3-et-si-on-imaginait": {
        "name": "Module 3 — Et si on imaginait...",
        "description": (
            "**Dans ce module, on passe du constat à la proposition.**\n\n"
            "On cherche à comprendre quelle serait votre matinale idéale, "
            "ce que vous changeriez si vous aviez les pleins pouvoirs, "
            "et ce qu'il ne faut surtout pas toucher.\n\n"
            "Laissez libre cours à votre imagination et réagissez aux idées des autres !"
        ),
    },
    "bienvenue": {
        "description": (
            "**Bienvenue dans votre espace auditeurs !**\n\n"
            "Vous trouverez ici les informations pratiques et les règles de fonctionnement. "
            "Lisez le message épinglé ci-dessous avant de commencer."
        ),
    },
    "le-cafe": {
        "description": (
            "**Le café, c'est votre espace libre.**\n\n"
            "Discutez de ce que vous voulez, échangez entre auditeurs, "
            "partagez vos découvertes. Pas de sujet imposé ici !"
        ),
    },
    "coulisses": {
        "description": (
            "**Espace réservé à l'équipe de recherche.**\n\n"
            "Notes d'animation, signaux à creuser, coordination entre chercheurs et animateurs."
        ),
    },
}


def apply_text_overrides(client: DiscourseClient):
    """Override Discourse translation strings."""
    print("1. Applying text overrides (catégorie → module)...")
    success = 0
    for text_id, value in TEXT_OVERRIDES.items():
        try:
            client.put(
                f"/admin/customize/site_texts/{text_id}",
                json={"site_text": {"value": value, "locale": "fr"}},
            )
            success += 1
        except Exception as e:
            print(f"  WARNING: {text_id}: {e}")
    print(f"   {success}/{len(TEXT_OVERRIDES)} overrides applied\n")


def rename_categories(client: DiscourseClient):
    """Rename categories and update descriptions."""
    print("2. Renaming categories and updating descriptions...")
    cats = categories.list_categories(client)
    slug_to_id = {c["slug"]: c["id"] for c in cats}

    for slug, updates in CATEGORY_UPDATES.items():
        cat_id = slug_to_id.get(slug)
        if not cat_id:
            print(f"  WARNING: Category {slug} not found")
            continue
        try:
            categories.update_category(client, cat_id, **updates)
            print(f"  {slug} (id={cat_id}): updated")
        except Exception as e:
            print(f"  WARNING: {slug}: {e}")
    print()


def configure_sidebar(client: DiscourseClient):
    """Configure sidebar links."""
    print("3. Configuring sidebar...")

    # Show "my posts" link in community section
    # The sidebar community section links are controlled by these settings
    # We want: my-posts (not messages), about, faq
    # Check available community section links
    try:
        resp = client.get("/admin/site_settings.json", params={"filter": "community_section"})
        for s in resp.get("site_settings", []):
            if "community" in s["setting"]:
                print(f"  {s['setting']}: {s['value']}")
    except Exception as e:
        print(f"  {e}")

    print()


def main():
    print("=== CLEAgora — Apply Customizations ===\n")

    url = os.environ["DISCOURSE_URL"]
    key = os.environ["DISCOURSE_API_KEY"]
    username = os.environ.get("DISCOURSE_API_USERNAME", "system")
    client = DiscourseClient(url, key, username)

    apply_text_overrides(client)
    rename_categories(client)
    configure_sidebar(client)

    client.close()
    print("=== Done ===")


if __name__ == "__main__":
    main()
