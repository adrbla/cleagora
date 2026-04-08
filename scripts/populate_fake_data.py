#!/usr/bin/env python3
"""Populate Discourse with fake respondent accounts and realistic posts.

Creates ~10 respondent accounts and ~30+ posts across study topics
to simulate a live qualitative research community.
"""

import os
import sys
import random
import time

from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from discourse_client import DiscourseClient
from discourse_client import users, topics

load_dotenv()

# --- Fake respondent profiles ---

RESPONDENTS = [
    {"name": "Sophie Martin", "username": "sophie_martin", "email": "sophie.martin@example.com", "age": 42, "style": "chaleureuse, détaillée"},
    {"name": "Thomas Bernard", "username": "thomas_b", "email": "thomas.bernard@example.com", "age": 35, "style": "direct, un peu piquant"},
    {"name": "Nathalie Petit", "username": "nathalie_p", "email": "nathalie.petit@example.com", "age": 58, "style": "nostalgique, cultivée"},
    {"name": "Julien Moreau", "username": "julien_m", "email": "julien.moreau@example.com", "age": 29, "style": "décontracté, humour"},
    {"name": "Claire Dubois", "username": "claire_d", "email": "claire.dubois@example.com", "age": 47, "style": "analytique, structurée"},
    {"name": "Patrick Lefèvre", "username": "patrick_l", "email": "patrick.lefevre@example.com", "age": 63, "style": "passionné, un peu ronchon"},
    {"name": "Amina Khelif", "username": "amina_k", "email": "amina.khelif@example.com", "age": 33, "style": "curieuse, ouverte"},
    {"name": "François Garnier", "username": "francois_g", "email": "francois.garnier@example.com", "age": 51, "style": "mesuré, précis"},
    {"name": "Lucie Renard", "username": "lucie_r", "email": "lucie.renard@example.com", "age": 38, "style": "spontanée, enthousiaste"},
    {"name": "Marc Fontaine", "username": "marc_f", "email": "marc.fontaine@example.com", "age": 44, "style": "laconique, pince-sans-rire"},
]

# --- Posts per topic (topic_id -> list of {username, raw, reply_to_username?}) ---

POSTS = {
    # Topic 14: Racontez-nous votre rituel du matin avec la radio
    14: [
        {"username": "sophie_martin", "raw": "Alors chez moi c'est un rituel immuable depuis des années ! Le réveil sonne à 6h30 et la première chose que je fais c'est allumer la radio dans la cuisine. France Inter me tient compagnie pendant que je prépare le petit-déjeuner des enfants. Le café coule, les tartines grillent, et j'écoute d'une oreille les infos de 7h. C'est vraiment mon moment à moi avant que la maison se réveille complètement."},
        {"username": "thomas_b", "raw": "Moi c'est dans la voiture, trajet boulot, 7h45-8h30. J'écoute en podcast aussi quand je rate le direct. En vrai la matinale c'est devenu le seul moment où j'ai de l'info \"non choisie\" — tout le reste c'est des algorithmes qui me servent ce que je veux entendre."},
        {"username": "nathalie_p", "raw": "J'écoute depuis le lit, dès 6h. Mon mari dort encore, j'ai mes écouteurs. C'est un moment très intime en fait. J'ai commencé à écouter France Inter il y a presque 30 ans, à l'époque de Stéphane Paoli. La matinale a beaucoup changé mais le réflexe est resté. C'est comme un vieux ami qu'on retrouve chaque matin."},
        {"username": "julien_m", "raw": "Salle de bain + transports en commun pour moi 😄 J'écoute sur mon tel avec les écouteurs. Je commence vers 7h15 et je décroche vers 8h quand j'arrive au bureau. Des fois je reste sur le quai du métro pour finir une interview, ça m'est déjà arrivé d'être en retard à cause de ça !"},
        {"username": "patrick_l", "raw": "Radio-réveil à 6h, pas une minute de plus, pas une minute de moins. Depuis 1987. Je l'écoute en faisant mon café, en lisant les titres du journal, puis dans la voiture. C'est simple : si j'ai pas eu ma dose d'Inter le matin, ma journée commence mal. Ma femme dit que je suis accro, elle a sûrement raison."},
        {"username": "amina_k", "raw": "Je suis assez irrégulière en fait — j'écoute 2-3 fois par semaine, surtout quand je suis en télétravail. Sinon c'est le podcast le midi. Ce que j'aime c'est que c'est un bon \"baromètre\" de ce qui se passe en France, je trouve que ça donne le pouls de l'actualité."},
    ],
    # Topic 15: Ce qui vous fait rester / ce qui vous fait décrocher
    15: [
        {"username": "claire_d", "raw": "**Ce qui m'accroche** : les interviews politiques quand le journaliste ne lâche rien. Les moments où on sent que l'invité est pris au dépourvu. Et la revue de presse, j'adore.\n\n**Ce qui me fait décrocher** : les sujets \"marronnier\" qu'on a déjà entendus 15 fois. Et parfois le ton un peu condescendant de certains chroniqueurs, comme si l'auditeur était un peu bête."},
        {"username": "sophie_martin", "raw": "Moi ce qui me fait rester, c'est le ton général. C'est intelligent sans être élitiste (enfin la plupart du temps). Les chroniques de Charline Vanhoenacker par exemple, même quand je suis pas d'accord, ça me fait réfléchir.\n\nPar contre je décroche quand c'est trop Paris-centré. On a l'impression que la France s'arrête au périph parfois."},
        {"username": "marc_f", "raw": "Je reste pour le 7-9. Je décroche après. Voilà."},
        {"username": "thomas_b", "raw": "Ce qui me fait décrocher : quand ils font 15 minutes sur un sujet de société \"tendance\" qui sera oublié dans 2 semaines. Ou les séquences où tout le monde est d'accord autour de la table — c'est quoi l'intérêt ?\n\nCe qui me retient : les interviews bien menées, les reportages terrain, et les moments de direct un peu chaotiques où on sent que c'est pas scripté."},
        {"username": "francois_g", "raw": "J'apprécie beaucoup la qualité des reportages et des correspondants à l'étranger. C'est une vraie force de France Inter par rapport aux autres stations. En revanche, je trouve qu'il y a parfois un entre-soi parisien qui peut agacer. Les sujets culturels sont très orientés \"sorties parisiennes\"."},
        {"username": "lucie_r", "raw": "Oh là oui @claire_d le ton condescendant !! Des fois j'ai l'impression qu'ils s'adressent à des gens qui pensent tous pareil. Et si t'es pas dans le moule, t'existes pas.\n\nMais bon, malgré ça je reste parce que le niveau d'info est quand même très bon. Et les matins où il se passe un truc important, il n'y a pas mieux.", "reply_to": "claire_d"},
    ],
    # Topic 16: Si vous deviez décrire France Inter le matin en 3 mots
    16: [
        {"username": "sophie_martin", "raw": "**Compagnon — Intelligent — Familier**\n\nCompagnon parce que c'est vraiment une présence quotidienne. Intelligent parce que ça élève le débat (la plupart du temps). Familier parce qu'on finit par connaître les voix comme des membres de la famille."},
        {"username": "julien_m", "raw": "**Café — Neurones — Rire**\n\nParce que ça va ensemble dans cet ordre le matin 😄"},
        {"username": "patrick_l", "raw": "**Indispensable — Exaspérant — Unique**\n\nOui les trois en même temps. C'est tout le paradoxe d'Inter."},
        {"username": "amina_k", "raw": "**Ouverture — Culture — Débat**\n\nC'est ce qui manque le plus sur les autres stations je trouve. Même quand c'est imparfait, au moins ça essaie de creuser les sujets."},
        {"username": "marc_f", "raw": "Rituel. Information. Bruit de fond.\n\n(Désolé c'est honnête.)"},
        {"username": "nathalie_p", "raw": "**Exigeant — Chaleureux — Engagé**\n\nEngagé au sens noble du terme : ça prend position sans avoir honte de le faire. C'est ce qui fait aussi qu'on peut ne pas être d'accord, mais au moins c'est clair."},
    ],
    # Topic 17: Les chroniques
    17: [
        {"username": "patrick_l", "raw": "La seule chronique que j'attends vraiment c'est celle de Guillaume Meurice. Enfin, c'était. Maintenant je ne sais plus trop ce qu'il reste d'intéressant dans les chroniques humour.\n\nCelles qui m'agacent : les chroniques \"bien-être\" et \"développement personnel\". On est sur une radio d'info, pas dans un magazine féminin."},
        {"username": "lucie_r", "raw": "Moi j'adore la chronique éco ! Ça rend accessible des sujets complexes. Et Charline Vanhoenacker, même si c'est clivant, au moins ça secoue le matin.\n\nCelle que je zappe : la chronique livres. Je suis désolée mais c'est toujours des livres que personne ne va lire en dehors du 5e arrondissement."},
        {"username": "thomas_b", "raw": "Franchement les chroniques c'est le point faible de la matinale. Trop de chroniqueurs qui se regardent le nombril. J'ai pas besoin qu'on me dise quoi penser avec un ton sarcastique à 7h30.\n\nLa seule que j'écoute vraiment c'est la géopolitique. Le reste je pourrais m'en passer."},
        {"username": "sophie_martin", "raw": "@thomas_b je suis pas du tout d'accord ! Les chroniques c'est justement ce qui fait le sel de la matinale. Sans elles ce serait juste un bulletin d'info ennuyeux. Moi j'aime bien quand ça provoque un peu, ça me fait réfléchir à des angles auxquels j'aurais pas pensé.", "reply_to": "thomas_b"},
        {"username": "francois_g", "raw": "Si je devais en garder une seule : la revue de presse de Claude Askolovitch. C'est un vrai travail de synthèse et de mise en perspective. C'est ce qui manque le plus dans le paysage médiatique actuel."},
    ],
    # Topic 18: Le traitement de l'actu
    18: [
        {"username": "claire_d", "raw": "C'est équilibré dans l'ensemble. Le problème c'est pas la quantité d'actu, c'est la hiérarchie. Parfois un fait divers prend plus de place qu'une réforme importante. Et inversement, des sujets de fond sont survolés en 2 minutes.\n\nMais oui, je me sens globalement bien informée après la matinale. C'est ma source principale d'info le matin."},
        {"username": "amina_k", "raw": "Je trouve qu'il y a juste ce qu'il faut d'actu. Ce que j'apprécie c'est qu'on a à la fois le factuel ET l'analyse. Sur d'autres stations c'est soit l'un soit l'autre.\n\nPar contre le ton est parfois trop grave. L'actu c'est pas que des catastrophes, il se passe aussi des trucs bien dans le monde !"},
        {"username": "julien_m", "raw": "Pour moi le problème c'est pas trop ou pas assez, c'est le prisme. On a parfois l'impression que tout est vu à travers le même filtre idéologique. Ça manque de contradictoire. Quand ils invitent quelqu'un qui pense différemment, on sent que c'est pour le \"challenger\" pas pour l'écouter."},
        {"username": "patrick_l", "raw": "@julien_m Tout à fait d'accord. Il y a 20 ans Inter était plus pluraliste dans ses invités. Aujourd'hui on sait à l'avance ce que le journaliste pense du sujet avant même que l'interview commence. C'est dommage.", "reply_to": "julien_m"},
    ],
    # Topic 19: Humour le matin
    19: [
        {"username": "lucie_r", "raw": "POUR à 100% ! L'humour le matin c'est vital. Quand t'enchaînes guerres, inflation, climat, il FAUT un moment de respiration. Ça empêche pas de réfléchir, au contraire — le rire ça ouvre l'esprit.\n\nAprès faut que ce soit de l'humour intelligent, pas des blagues de comptoir."},
        {"username": "francois_g", "raw": "Je suis assez partagé. L'humour a sa place mais il prend parfois trop d'espace. Quand un humoriste fait 7 minutes de sketch pendant la tranche info, c'est un choix éditorial discutable. Et le mélange info/humour peut brouiller les frontières — on ne sait plus toujours si c'est du premier ou du second degré."},
        {"username": "sophie_martin", "raw": "Pour ! Mais pas n'importe quel humour. J'aimais quand c'était incisif et politique. Quand ça pointait les contradictions des puissants. L'humour \"vanne facile\" ça non merci.\n\nEt puis l'humour c'est aussi une forme de liberté. Une radio publique qui n'ose plus rire, c'est une radio qui a peur."},
        {"username": "marc_f", "raw": "Contre.\n\nJe veux les infos, pas un one-man-show. Pour rire j'ai Netflix."},
        {"username": "nathalie_p", "raw": "J'ai toujours aimé l'humour sur Inter, c'est une tradition. De Pierre Desproges aux humoristes actuels, c'est dans l'ADN de la station. Mais @francois_g a raison, il faut que ça reste à sa juste place. L'humour doit éclairer, pas envahir.", "reply_to": "francois_g"},
        {"username": "thomas_b", "raw": "C'est pas une question de pour ou contre, c'est une question de qualité. Quand c'est bon, c'est le meilleur moment de la matinale. Quand c'est raté, c'est gênant. Le problème c'est que y'a pas de demi-mesure avec l'humour en direct."},
    ],
    # Topic 20: Votre matinale idéale
    20: [
        {"username": "claire_d", "raw": "Ma matinale idéale :\n\n- 6h30-7h : infos factuelles, brèves, météo\n- 7h-8h : grande interview + reportage terrain\n- 8h-8h30 : chroniques variées (éco, géo, culture, un moment d'humour)\n- 8h30-9h : débat contradictoire avec des gens qui ne sont pas d'accord\n\nLe tout avec un équilibre Paris/régions, et des voix nouvelles régulièrement. Pas toujours les mêmes experts sur les mêmes sujets."},
        {"username": "julien_m", "raw": "Ma matinale idéale elle serait plus courte et plus dense. Genre 1h30 max au lieu de 3h. Parce que franchement qui écoute 3h d'affilée ? Concentrez le meilleur et coupez le remplissage.\n\nEt plus de reportages sonores ! Des trucs immersifs, pas juste des gens qui parlent en studio."},
        {"username": "sophie_martin", "raw": "En fait ma matinale idéale ça ressemble beaucoup à Inter... en mieux 😄\n\nPlus de reportages en régions, plus de parole aux \"gens normaux\" (pas que des experts et des politiques), et un vrai moment de respiration vers 8h — musique, poésie, un truc qui fait du bien.\n\nEt un ton un peu moins \"on va vous expliquer la vie\". Plus de curiosité, moins de certitudes."},
        {"username": "amina_k", "raw": "J'aimerais une matinale qui m'ouvre au monde. Plus d'international, de correspondants. Qu'on m'emmène à Tokyo, à Nairobi, à São Paulo le matin. Et aussi plus de place aux solutions, pas que des problèmes. Le journalisme de solutions ça existe et c'est pas du bisounours."},
    ],
    # Topic 21: Si vous étiez directeur des programmes
    21: [
        {"username": "patrick_l", "raw": "Première décision : remettre une vraie tranche musicale entre les séquences parlées. Inter c'est aussi une radio MUSICALE, on l'oublie trop.\n\nDeuxième décision : imposer un quota de 50% d'invités qui ne sont pas parisiens. Sérieusement.\n\nTroisième : arrêter de changer la grille tous les ans. Laissez les gens s'installer, créer des habitudes. C'est épuisant ces changements permanents."},
        {"username": "thomas_b", "raw": "Moi je supprime le dernier quart d'heure de la matinale qui sert à rien, et je rajoute un segment \"fact-check du jour\" — un sujet d'actu vérifié en profondeur, sources à l'appui. Genre 5 minutes, carré, factuel. Ça manque cruellement."},
        {"username": "nathalie_p", "raw": "Ce que je changerais : le recrutement des chroniqueurs. Trop de profils similaires (même génération, même milieu, même vision du monde). Il faut de la diversité de pensée, pas juste de la diversité démographique.\n\nCe que j'ajouterais : une chronique \"retour sur l'actu d'il y a un an\" — pour donner de la perspective et sortir de l'immédiateté permanente."},
        {"username": "lucie_r", "raw": "Je virerais les pubs (oui je sais c'est pas France Inter mais France Culture ok passons 😂).\n\nPlus sérieusement : j'ajouterais une séquence interactive avec les auditeurs chaque matin. Pas un standard téléphonique à l'ancienne, mais un truc moderne — questions par message, réactions en direct. Donner la parole aux gens quoi."},
    ],
    # Topic 22: Ce qu'il ne faut surtout pas changer
    22: [
        {"username": "nathalie_p", "raw": "Le ton. Cette espèce d'équilibre entre sérieux et légèreté qui n'existe nulle part ailleurs. France Inter c'est la seule radio où on peut passer d'une interview de ministre à un éclat de rire en 30 secondes sans que ça soit bizarre.\n\nEt la voix de 7h. Le journal de 7h, c'est sacré. On touche pas."},
        {"username": "sophie_martin", "raw": "La liberté de ton. Le fait que les chroniqueurs puissent dire ce qu'ils pensent, même quand c'est dérangeant. C'est rare et précieux.\n\nEt aussi : le fait que ce soit du service public. Pas de course à l'audience, pas de sensationnalisme (enfin moins qu'ailleurs). C'est le socle. On y touche pas."},
        {"username": "marc_f", "raw": "Le journal de 7h.\nLa météo marine.\nLe générique.\n\n(Dans cet ordre.)"},
        {"username": "julien_m", "raw": "La météo marine !! 😂 @marc_f t'es un homme de goût. Sérieusement c'est le ASMR original.\n\nPour moi ce qu'il faut garder : l'exigence. Le fait qu'ils partent du principe que l'auditeur est intelligent. Ça se fait de moins en moins dans les médias.", "reply_to": "marc_f"},
        {"username": "amina_k", "raw": "L'ouverture culturelle. Inter c'est la radio qui m'a fait découvrir des auteurs, des musiciens, des idées que j'aurais jamais croisés autrement. Cette fonction de passeur culturel c'est irremplaçable.\n\nEt oui, la liberté de ton comme dit @sophie_martin. Une radio publique qui s'autocensure ça sert à rien.", "reply_to": "sophie_martin"},
    ],
}

# Le café — conversations libres
CAFE_TOPIC_TITLE = "Vous écoutez quoi d'autre ?"
CAFE_TOPIC_RAW = (
    "Petite question hors-sujet : en dehors de France Inter, "
    "vous écoutez quoi comme radio / podcast le matin ?\n\n"
    "Ou alors c'est Inter et rien d'autre ? 😄"
)
CAFE_REPLIES = [
    {"username": "julien_m", "raw": "France Culture le week-end ! Et pas mal de podcasts : Les Pieds sur terre, Le Biais de Nora Hamadi, et Affaires sensibles en replay. En musique : FIP évidemment 🎵"},
    {"username": "claire_d", "raw": "RTL pour comparer le traitement de l'info parfois. Et Radio Nova quand j'ai besoin de décompresser. Mais le matin c'est Inter, point final."},
    {"username": "patrick_l", "raw": "France Musique le dimanche matin. Et parfois RFI pour l'actu africaine, c'est excellent et sous-estimé."},
    {"username": "sophie_martin", "raw": "J'avoue que je triche parfois avec Europe 1 pour la matinale de Demorand (ah non il est parti... je suis plus à jour 😅). Sinon Inter c'est ma base. Et @julien_m FIP c'est la vie oui !", "reply_to": "julien_m"},
]


def create_respondents(client: DiscourseClient) -> dict[str, bool]:
    """Create respondent accounts and add to auditeurs group."""
    print("1. Creating respondent accounts...")
    created = {}
    for r in RESPONDENTS:
        if r["username"] == "marie_dupont":
            continue  # Already exists
        try:
            users.create_user(
                client, r["name"], r["email"], r["username"],
                password="Cleagora2026!",  # Dummy password
                active=True, approved=True,
            )
            print(f"   {r['username']} ({r['name']})")
            created[r["username"]] = True
        except Exception as e:
            if "already" in str(e).lower() or "422" in str(e):
                print(f"   {r['username']} (already exists)")
                created[r["username"]] = True
            else:
                print(f"   {r['username']} ERROR: {e}")
                created[r["username"]] = False
    return created


def add_to_group(client: DiscourseClient):
    """Add all respondents to auditeurs group."""
    print("\n2. Adding respondents to 'auditeurs' group...")
    group = users.get_group(client, "auditeurs")
    group_id = group["id"]
    all_usernames = [r["username"] for r in RESPONDENTS]
    # Include marie_dupont
    all_usernames.append("marie_dupont")
    try:
        users.add_group_members(client, group_id, all_usernames)
        print(f"   Added {len(all_usernames)} users to auditeurs (group_id={group_id})")
    except Exception as e:
        print(f"   Warning: {e}")


def post_replies(client: DiscourseClient):
    """Post fake respondent replies across all topics."""
    print("\n3. Posting replies in study topics...")
    total = 0
    for topic_id, post_list in sorted(POSTS.items()):
        print(f"\n   Topic {topic_id}:")
        for p in post_list:
            username = p["username"]
            raw = p["raw"]

            # Find reply_to post number if specified
            reply_to = None
            if "reply_to" in p:
                # We'll skip reply threading for simplicity — just post as reply
                raw = raw  # Content already references the user with @mention

            try:
                # Post as the respondent user
                resp = client._request(
                    "POST", "/posts.json",
                    json={"topic_id": topic_id, "raw": raw},
                    headers={"Api-Username": username},
                )
                post_id = resp.get("id", "?")
                print(f"     {username}: post_id={post_id}")
                total += 1
                time.sleep(0.3)  # Rate limiting
            except Exception as e:
                print(f"     {username}: ERROR {e}")

    print(f"\n   Total posts created: {total}")


def create_cafe_topic(client: DiscourseClient):
    """Create a free discussion topic in Le café."""
    print("\n4. Creating topic in Le café...")
    try:
        resp = client._request(
            "POST", "/posts.json",
            json={
                "title": CAFE_TOPIC_TITLE,
                "raw": CAFE_TOPIC_RAW,
                "category": 9,  # le-cafe
            },
            headers={"Api-Username": "julien_m"},
        )
        topic_id = resp.get("topic_id", resp.get("id"))
        print(f"   Created: '{CAFE_TOPIC_TITLE}' (topic_id={topic_id})")

        # Post replies
        for r in CAFE_REPLIES:
            try:
                client._request(
                    "POST", "/posts.json",
                    json={"topic_id": topic_id, "raw": r["raw"]},
                    headers={"Api-Username": r["username"]},
                )
                print(f"     {r['username']}: replied")
                time.sleep(0.3)
            except Exception as e:
                print(f"     {r['username']}: ERROR {e}")

    except Exception as e:
        print(f"   ERROR: {e}")


def main():
    print("=== CLEAgora — Populate Fake Data ===\n")

    url = os.environ["DISCOURSE_URL"]
    key = os.environ["DISCOURSE_API_KEY"]
    # Use system user for account creation
    client = DiscourseClient(url, key, "system")

    create_respondents(client)
    add_to_group(client)
    post_replies(client)
    create_cafe_topic(client)

    client.close()
    print("\n=== Done! ===")


if __name__ == "__main__":
    main()
