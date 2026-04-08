#!/usr/bin/env python3
"""Set up the France Inter study structure on Discourse.

Creates groups, categories, permissions, and sample topics
as defined in the CLEAgora design doc.
"""

import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from discourse_client import DiscourseClient, categories, topics, users

load_dotenv()


def get_client() -> DiscourseClient:
    url = os.environ["DISCOURSE_URL"]
    key = os.environ["DISCOURSE_API_KEY"]
    username = os.environ.get("DISCOURSE_API_USERNAME", "system")
    return DiscourseClient(url, key, username)


# --- Group definitions ---

GROUPS = [
    {"name": "auditeurs", "full_name": "Auditeurs"},
    {"name": "animateurs", "full_name": "Animateurs"},
    {"name": "chercheurs", "full_name": "Chercheurs"},
]

# --- Category definitions ---
# Permissions: 1=see, 2=reply(+see), 3=create(+see+reply)

CATEGORIES = [
    {
        "name": "Bienvenue",
        "slug": "bienvenue",
        "color": "12A89D",
        "description": "Informations pratiques et règles de fonctionnement.",
        "permissions": {"auditeurs": 1, "animateurs": 3, "chercheurs": 1},
    },
    {
        "name": "Semaine 1 — Votre matinale",
        "slug": "semaine-1-votre-matinale",
        "color": "ED207B",
        "description": "Partagez vos habitudes d'écoute, votre relation à la matinale.",
        "permissions": {"auditeurs": 2, "animateurs": 3, "chercheurs": 1},
    },
    {
        "name": "Semaine 2 — Réactions & débats",
        "slug": "semaine-2-reactions-debats",
        "color": "F7941D",
        "description": "Réagissez à des extraits, débattez des choix éditoriaux.",
        "permissions": {"auditeurs": 2, "animateurs": 3, "chercheurs": 1},
    },
    {
        "name": "Semaine 3 — Et si on imaginait...",
        "slug": "semaine-3-et-si-on-imaginait",
        "color": "3AB54A",
        "description": "Imaginez la matinale idéale, proposez vos idées.",
        "permissions": {"auditeurs": 2, "animateurs": 3, "chercheurs": 1},
    },
    {
        "name": "Le café",
        "slug": "le-cafe",
        "color": "92278F",
        "description": "Espace libre — discussions hors-sujet, échanges entre auditeurs.",
        "permissions": {"auditeurs": 3, "animateurs": 3, "chercheurs": 1},
    },
    {
        "name": "Coulisses",
        "slug": "coulisses",
        "color": "808281",
        "description": "Espace réservé à l'équipe de recherche.",
        "permissions": {"animateurs": 3, "chercheurs": 3},
    },
]

# --- Topic definitions ---

TOPICS = {
    "bienvenue": [
        {
            "title": "Comment ça marche",
            "raw": (
                "## Bienvenue dans votre espace auditeurs !\n\n"
                "Pendant 3 semaines, vous allez pouvoir échanger avec d'autres auditeurs "
                "de la matinale de France Inter.\n\n"
                "**Comment participer ?**\n\n"
                "- Chaque semaine, de nouvelles discussions seront ouvertes.\n"
                "- Répondez aux questions posées, réagissez aux messages des autres.\n"
                "- Il n'y a pas de bonne ou mauvaise réponse : on veut votre avis sincère.\n"
                "- L'espace \"Le café\" est à vous pour discuter librement.\n\n"
                "**Quelques règles simples :**\n\n"
                "- Respectez les opinions de chacun.\n"
                "- Exprimez-vous librement et spontanément.\n"
                "- Essayez de participer régulièrement (quelques minutes par jour suffisent).\n\n"
                "Bonne discussion à tous !"
            ),
            "pin": True,
        },
    ],
    "semaine-1-votre-matinale": [
        {
            "title": "Racontez-nous votre rituel du matin avec la radio",
            "raw": (
                "Comment se passe votre matinée avec France Inter ?\n\n"
                "- À quelle heure allumez-vous la radio ?\n"
                "- Où êtes-vous (lit, cuisine, voiture, transports...) ?\n"
                "- Est-ce que vous écoutez seul(e) ou avec d'autres ?\n"
                "- Qu'est-ce que vous faites en même temps ?\n\n"
                "Racontez-nous votre rituel, même les petits détails !"
            ),
        },
        {
            "title": "Ce qui vous fait rester / ce qui vous fait décrocher",
            "raw": (
                "Quand vous écoutez la matinale :\n\n"
                "- **Qu'est-ce qui vous accroche ?** Les moments où vous montez le son, "
                "où vous tendez l'oreille...\n"
                "- **Qu'est-ce qui vous fait décrocher ?** Les moments où vous changez "
                "de station, où vous éteignez...\n\n"
                "Soyez aussi précis que possible : une rubrique, un chroniqueur, "
                "un type de sujet, un ton..."
            ),
        },
        {
            "title": "Si vous deviez décrire France Inter le matin en 3 mots...",
            "raw": (
                "Un petit exercice rapide :\n\n"
                "**Quels sont les 3 mots qui vous viennent spontanément "
                "quand vous pensez à la matinale de France Inter ?**\n\n"
                "Pas besoin de réfléchir longtemps — les premiers mots qui viennent "
                "sont souvent les plus intéressants.\n\n"
                "Et si vous voulez, expliquez pourquoi ces mots-là !"
            ),
        },
    ],
    "semaine-2-reactions-debats": [
        {
            "title": "Les chroniques : lesquelles vous parlent, lesquelles vous agacent ?",
            "raw": (
                "La matinale de France Inter, c'est aussi ses chroniqueurs.\n\n"
                "- **Quelle(s) chronique(s) attendez-vous chaque matin ?** Pourquoi ?\n"
                "- **Quelle(s) chronique(s) vous agacent ou vous laissent indifférent(e) ?**\n"
                "- Si vous pouviez en garder une seule, laquelle ?\n\n"
                "N'hésitez pas à rebondir sur les avis des autres !"
            ),
        },
        {
            "title": "Le traitement de l'actu : trop / pas assez / juste ce qu'il faut ?",
            "raw": (
                "France Inter le matin, c'est de l'info, des analyses, des débats.\n\n"
                "- Trouvez-vous qu'il y a **trop d'actu** dans la matinale ? "
                "Ou **pas assez** ?\n"
                "- Le ton est-il **trop sérieux** ? **Trop léger** ?\n"
                "- Avez-vous le sentiment d'être **bien informé(e)** en sortant "
                "de la matinale ?\n\n"
                "Partagez votre ressenti !"
            ),
        },
        {
            "title": "Débat : humour le matin, pour ou contre ?",
            "raw": (
                "L'humour a une place importante dans la matinale de France Inter.\n\n"
                "**Qu'en pensez-vous ?**\n\n"
                "- L'humour le matin, ça vous met de bonne humeur ?\n"
                "- Ou au contraire, ça vous dérange / vous fatigue ?\n"
                "- Y a-t-il des humoristes que vous trouvez particulièrement réussis ? "
                "Ou ratés ?\n\n"
                "Débattez entre vous !"
            ),
        },
    ],
    "semaine-3-et-si-on-imaginait": [
        {
            "title": "Votre matinale idéale : décrivez-la",
            "raw": (
                "Imaginez que vous pouvez créer **votre matinale radio idéale**.\n\n"
                "- Elle ressemblerait à quoi ?\n"
                "- Quelles rubriques ? Quel ton ? Quels intervenants ?\n"
                "- À quelle heure commencerait-elle et finirait-elle ?\n"
                "- Qu'est-ce qu'elle vous apporterait que la matinale actuelle "
                "ne vous apporte pas ?\n\n"
                "Laissez libre cours à votre imagination !"
            ),
        },
        {
            "title": "Si vous étiez directeur des programmes, que changez-vous ?",
            "raw": (
                "Vous avez les pleins pouvoirs sur la grille de France Inter.\n\n"
                "**Qu'est-ce que vous changez dans la matinale ?**\n\n"
                "- Quoi ajouter ?\n"
                "- Quoi supprimer ?\n"
                "- Quoi déplacer ?\n\n"
                "Et surtout : **pourquoi** ?"
            ),
        },
        {
            "title": "Ce qu'il ne faut surtout pas changer",
            "raw": (
                "Après 3 semaines de discussions, un dernier sujet :\n\n"
                "**Qu'est-ce qui fait le sel de la matinale de France Inter "
                "et qu'il ne faudrait surtout pas toucher ?**\n\n"
                "- Un ton ? Une rubrique ? Un chroniqueur ? Une ambiance ?\n"
                "- Qu'est-ce qui rend cette matinale unique à vos yeux ?\n\n"
                "C'est le moment de défendre ce que vous aimez !"
            ),
        },
    ],
    "coulisses": [
        {
            "title": "Guide d'animation — semaine par semaine",
            "raw": (
                "## Guide d'animation\n\n"
                "### Semaine 1 — Exploration\n"
                "- Objectif : recueillir les habitudes et perceptions spontanées.\n"
                "- Ton : ouvert, accueillant, pas de jugement.\n"
                "- Relancer les silencieux via MP après J+2.\n\n"
                "### Semaine 2 — Approfondissement\n"
                "- Objectif : faire réagir sur des éléments concrets.\n"
                "- Stimuli : extraits audio, captures de grille.\n"
                "- Encourager le débat entre participants.\n\n"
                "### Semaine 3 — Co-construction\n"
                "- Objectif : passer du constat à la proposition.\n"
                "- Synthétiser les thèmes émergents des semaines 1-2.\n"
                "- Topic de synthèse en fin de semaine."
            ),
            "pin": True,
        },
        {
            "title": "Signaux intéressants à creuser",
            "raw": (
                "Espace pour noter les signaux faibles et forts repérés "
                "dans les discussions.\n\n"
                "*À compléter au fil de l'étude.*"
            ),
        },
    ],
}


def setup_groups(client: DiscourseClient) -> dict[str, int]:
    """Create groups and return {name: id} mapping."""
    group_ids = {}
    for g in GROUPS:
        print(f"  Creating group: {g['name']}...")
        try:
            resp = users.create_group(client, g["name"], full_name=g.get("full_name"))
            group_ids[g["name"]] = resp["basic_group"]["id"]
            print(f"    -> id={group_ids[g['name']]}")
        except Exception as e:
            # Group might already exist
            print(f"    -> Error: {e}. Trying to fetch existing...")
            existing = users.get_group(client, g["name"])
            group_ids[g["name"]] = existing["id"]
            print(f"    -> Found existing id={group_ids[g['name']]}")
    return group_ids


def setup_categories(client: DiscourseClient) -> dict[str, int]:
    """Create categories and return {slug: id} mapping."""
    cat_ids = {}
    for c in CATEGORIES:
        print(f"  Creating category: {c['name']}...")
        try:
            cat = categories.create_category(
                client,
                c["name"],
                slug=c["slug"],
                color=c["color"],
                description=c.get("description"),
                permissions=c["permissions"],
            )
            cat_ids[c["slug"]] = cat["id"]
            print(f"    -> id={cat_ids[c['slug']]}")
        except Exception as e:
            print(f"    -> Error: {e}")
            # Try to find it in existing categories
            existing = categories.list_categories(client)
            for ec in existing:
                if ec.get("slug") == c["slug"]:
                    cat_ids[c["slug"]] = ec["id"]
                    print(f"    -> Found existing id={cat_ids[c['slug']]}")
                    break
    return cat_ids


def setup_topics(client: DiscourseClient, cat_ids: dict[str, int]) -> None:
    """Create topics in their respective categories."""
    for cat_slug, topic_list in TOPICS.items():
        cat_id = cat_ids.get(cat_slug)
        if not cat_id:
            print(f"  Skipping topics for {cat_slug} (category not found)")
            continue
        for t in topic_list:
            print(f"  Creating topic: {t['title'][:50]}...")
            try:
                resp = topics.create_topic(
                    client,
                    t["title"],
                    t["raw"],
                    cat_id,
                )
                topic_id = resp.get("topic_id") or resp.get("id")
                print(f"    -> topic_id={topic_id}")
                if t.get("pin") and topic_id:
                    topics.pin_topic(client, topic_id)
                    print("    -> pinned")
            except Exception as e:
                print(f"    -> Error: {e}")


def main():
    print("=== CLEAgora — France Inter Study Setup ===\n")

    client = get_client()

    print("1. Creating groups...")
    group_ids = setup_groups(client)
    print(f"   Groups: {group_ids}\n")

    print("2. Creating categories...")
    cat_ids = setup_categories(client)
    print(f"   Categories: {cat_ids}\n")

    print("3. Creating topics...")
    setup_topics(client, cat_ids)

    print("\n=== Setup complete! ===")
    print(f"Visit {os.environ['DISCOURSE_URL']} to see your community.")

    client.close()


if __name__ == "__main__":
    main()
