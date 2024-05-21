import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

DUKE_CLAN_MEMBERS = [
    "credit score", "sruc", "lord hystad", "ghostm1ner", "slidinshadow", "verrsi",
    "das hound", "ulysses1222", "yvaesaek", "whitefire8", "spart167", "sourturd",
    "sase", "warhawks2011", "mattywilko1", "the doomles", "ancienttrees", "m r p3wp3w",
    "crimson fear", "da don djr", "riotu", "elfrunner2", "kctron", "er ii c", "hala sauce",
    "shinnya01", "suckulus", "augma", "dewxs", "creamyrhino", "ezeem", "j i b z", "lexxion",
    "retr0gr", "herculooo", "mrpotstonks", "fook12345", "2meo dmt", "a dullard", "glitchzzz",
    "sallesr2", "strclychaos", "pappa potion", "prof tiddys", "uimayhem x", "kit sunii",
    "markes45", "ev_n", "re 2", "yojizzie", "daimondlv", "j a h m i r", "jerbear2548",
    "gnomenipples", "m r s p3wp3w", "gooberdoo111", "grainesjr", "emzri", "raithnos",
    "godlikerim", "rutraru", "cbd oil king", "lizardkingv", "luonteri", "dranyur", "maremoo2",
    "fen rau", "strictlychaos", "mrs p3wp3w", "ayeitzdeabo", "expireduncle", "raithnos",
    "dranyur", "minty boy900", "cr3sp chompy", "paumal", "k h o", "re 1", "gooberdoo111",
    "luonteri", "kit sunii", "visit lisboa", "sallesr4", "ev_n", "sallesr2", "maremoo2",
    "sweeet turds", "mc cheaks69", "credits uim", "hallies", "grainesjr gim", "minnowmalist",
    "j i b z uim", "i am atomic", "botbuster3k", "utoir", "sallesr4", "tz tok-bigkok",
    "verrsi uim", "lords uim"
]


def get_player_data(player_name):
    url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.json?player={player_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Replace -1 with 0 in skills and activities
        for skill in data['skills']:
            if skill['level'] == -1:
                skill['level'] = 0
        for activity in data['activities']:
            if activity['score'] == -1:
                activity['score'] = 0
        return data
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def compare_players():
    if request.method == "POST":
        player_names = [request.form[key] for key in request.form.keys() if key.startswith("player") and request.form[key]]
        comparison_type = request.form.get("comparison_type")
        skill_filters = request.form.getlist("skill_filter")
        activities_type = request.form.getlist("activities_type")
        tier_groups = request.form.get("tier_groups") == "yes"
        duke_clan = request.form.get("duke_clan") == "on"

        if duke_clan:
            player_names = DUKE_CLAN_MEMBERS

        if tier_groups and "monsters" not in activities_type:
            activities_type.append("monsters")

        player_data_list = [get_player_data(name) for name in player_names]
        player_data_list = [data for data in player_data_list if data is not None]

        if player_data_list:
            all_skills = [
                "Overall", "Attack", "Defence", "Strength", "Hitpoints", "Ranged", "Prayer", "Magic", 
                "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking", "Crafting", "Smithing", 
                "Mining", "Herblore", "Agility", "Thieving", "Slayer", "Farming", "Runecrafting", 
                "Hunter", "Construction"
            ]

            combat_skills = ["Attack", "Defence", "Strength", "Hitpoints", "Ranged", "Prayer", "Magic"]
            non_combat_skills = [skill for skill in all_skills if skill not in combat_skills + ["Overall"]]

            skills = []
            if "combat" in skill_filters:
                skills.extend(combat_skills)
            if "non_combat" in skill_filters:
                skills.extend(non_combat_skills)
            if not skills:
                skills = all_skills

            activities = {
                "Other": [
                    "League Points", "Deadman Points", "Bounty Hunter - Hunter", "Bounty Hunter - Rogue", 
                    "Bounty Hunter (Legacy) - Hunter", "Bounty Hunter (Legacy) - Rogue", "LMS - Rank", 
                    "PvP Arena - Rank", "Soul Wars Zeal", "Rifts closed", "Colosseum Glory"
                ],
                "Clues": [
                    "Clue Scrolls (all)", "Clue Scrolls (beginner)", "Clue Scrolls (easy)", 
                    "Clue Scrolls (medium)", "Clue Scrolls (hard)", "Clue Scrolls (elite)", 
                    "Clue Scrolls (master)"
                ],
                "Monsters": [
                    "Abyssal Sire", "Alchemical Hydra", "Artio", "Barrows Chests", "Bryophyta", 
                    "Callisto", "Cal'varion", "Cerberus", "Chaos Elemental", "Chaos Fanatic", 
                    "Commander Zilyana", "Corporeal Beast", "Crazy Archaeologist", "Dagannoth Prime", 
                    "Dagannoth Rex", "Dagannoth Supreme", "Deranged Archaeologist", "Duke Sucellus", 
                    "General Graardor", "Giant Mole", "Grotesque Guardians", "Hespori", 
                    "Kalphite Queen", "King Black Dragon", "Kraken", "Kree'Arra", "K'ril Tsutsaroth", 
                    "Lunar Chests", "Mimic", "Nex", "Nightmare", "Phosani's Nightmare", "Obor", 
                    "Phantom Muspah", "Sarachnis", "Scorpia", "Scurrius", "Skotizo", "Sol Heredit", 
                    "Spindel", "Tempoross", "The Gauntlet", "The Corrupted Gauntlet", "The Leviathan", 
                    "The Whisperer", "Thermonuclear Smoke Devil", "Vardorvis", "Venenatis", 
                    "Vet'ion", "Vorkath", "Wintertodt", "Zalcano", "Zulrah"
                ],
                "Raids": [
                    "Chambers of Xeric", "Chambers of Xeric: Challenge Mode", "Theatre of Blood", 
                    "Theatre of Blood: Hard Mode", "Tombs of Amascut", "Tombs of Amascut: Expert Mode", 
                    "TzKal-Zuk", "TzTok-Jad"
                ]
            }

            comparison_data = {"skills": [], "activities": {}}
            player_totals = {name: {'total_level': 0, 'monster_level': 0} for name in player_names}
            
            # Skills comparison
            for skill in skills:
                total_level = 0
                levels = []

                for player_data in player_data_list:
                    level = player_data['skills'][all_skills.index(skill)]['level']
                    total_level += level
                    levels.append(level)

                if comparison_type == "average":
                    avg_level = total_level / len(player_data_list)
                    comparison_data["skills"].append({
                        "skill": "Total" if skill == "Overall" else skill,
                        "avg_level": avg_level,
                        "compare_type": comparison_type
                    })
                else:  # compare
                    comparison_data["skills"].append({
                        "skill": "Total" if skill == "Overall" else skill,
                        "levels": levels,
                        "compare_type": comparison_type
                    })

                # For tier groups calculation
                if skill == "Overall":  # Only use the Overall level for Total Skill Levels
                    for i, player_data in enumerate(player_data_list):
                        player_totals[player_names[i]]['total_level'] = levels[i]

            # Activities comparison
            for category, activity_list in activities.items():
                if category.lower() in activities_type:
                    comparison_data["activities"][category] = []
                    for activity in activity_list:
                        idx = next((i for i, a in enumerate(player_data_list[0]['activities']) if a['name'] == activity), None)
                        if idx is not None:
                            total_score = 0
                            scores = []
                            for i, player_data in enumerate(player_data_list):
                                score = player_data['activities'][idx]['score']
                                total_score += score
                                scores.append(score)

                                # For tier groups calculation
                                if category == 'Monsters':
                                    player_totals[player_names[i]]['monster_level'] += score

                            if comparison_type == "average":
                                avg_score = total_score / len(player_data_list)
                                comparison_data["activities"][category].append({
                                    "activity": activity,
                                    "avg_score": avg_score,
                                    "compare_type": comparison_type
                                })
                            else:  # compare
                                comparison_data["activities"][category].append({
                                    "activity": activity,
                                    "scores": scores,
                                    "compare_type": comparison_type
                                })

            if tier_groups:
                sorted_total_skill = sorted(player_totals.items(), key=lambda x: x[1]['total_level'], reverse=True)
                sorted_monster_skill = sorted(player_totals.items(), key=lambda x: x[1]['monster_level'], reverse=True)
                
                tier_groups_data = {
                    'total_skill': [{'name': name, 'total_level': data['total_level']} for name, data in sorted_total_skill],
                    'monster_skill': [{'name': name, 'monster_level': data['monster_level']} for name, data in sorted_monster_skill]
                }
                return render_template("comparison.html", player_names=player_names, data=comparison_data, tier_groups=tier_groups_data)

            return render_template("comparison.html", player_names=player_names, data=comparison_data)
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


