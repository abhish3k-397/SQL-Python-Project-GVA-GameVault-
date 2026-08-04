"""
Script to update all Games in MariaDB GameVault with official Steam CDN header image URLs
Format: https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database import DatabaseConnection

# Mapping of Game Title substrings to Steam App IDs
STEAM_MAPPINGS = {
    "Cyberpunk 2077: Phantom Liberty": "1091500",
    "Elden Ring: Shadow of the Erdtree": "1245620",
    "Baldur's Gate 3": "1086940",
    "Red Dead Redemption 2": "1174180",
    "Grand Theft Auto VI": "271590",
    "Black Myth: Wukong": "2358720",
    "Hades II": "1145350",
    "The Last of Us Part II": "1888930",
    "The Witcher 3: Wild Hunt": "292030",
    "God of War Ragnarök": "2322010",
    "Grand Theft Auto V": "271590",
    "Red Dead Redemption": "2668510",
    "Horizon Forbidden West": "2420110",
    "Spider-Man 2": "1817070",
    "Ghost of Tsushima: Director's Cut": "2215430",
    "Resident Evil 4 Remake": "2050650",
    "Resident Evil Village": "1196590",
    "Monster Hunter World": "582010",
    "Monster Hunter Wilds": "2246340",
    "Dark Souls III": "374320",
    "Sekiro: Shadows Die Twice": "814380",
    "Armored Core VI: Fires of Rubicon": "1888160",
    "Fallout 4": "377160",
    "The Elder Scrolls V: Skyrim": "489830",
    "Starfield": "1716740",
    "Doom Eternal": "782330",
    "Cyberpunk 2077": "1091500",
    "Final Fantasy XVI": "2515020",
    "Final Fantasy VII Rebirth": "1462040",
    "Dragon's Dogma 2": "2054970",
    "Alan Wake 2": "108710",
    "Control": "870780",
    "Death Stranding Director's Cut": "1850570",
    "Forza Horizon 5": "1551360",
    "EA Sports FC 24": "2195250",
    "Battlefield 2042": "1517290",
    "Star Wars Jedi: Survivor": "1774580",
    "Apex Legends": "1172470",
    "Call of Duty: Modern Warfare III": "1938090",
    "Diablo IV": "2344520",
    "Hogwarts Legacy": "990080",
    "Assassin's Creed Valhalla": "2208920",
    "Far Cry 6": "2369390",
    "Hades": "1145360",
    "Hollow Knight": "367520",
    "Hollow Knight: Silksong": "1030300",
    "Celeste": "504230",
    "Stardew Valley": "413150",
    "Dead Cells": "588650",
    "Slay the Spire": "646570",
    "Balatro": "2379780",
    "Sea of Stars": "1244090",
    "Dave the Diver": "1868140",
    "Manor Lords": "1363080",
    "Palworld": "1623730",
    "Lethal Company": "2093590",
    "Cuphead": "268910",
    "Risk of Rain 2": "632360"
}

def update_images():
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT GameID, Title FROM Games;")
        games = cursor.fetchall()
        
        updated_count = 0
        for g in games:
            gid = g['GameID']
            title = g['Title']
            app_id = STEAM_MAPPINGS.get(title)
            
            # If not exact match, search key
            if not app_id:
                for k, v in STEAM_MAPPINGS.items():
                    if k.lower() in title.lower() or title.lower() in k.lower():
                        app_id = v
                        break
            
            if not app_id:
                app_id = "1091500" # Fallback Cyberpunk header

            steam_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg"
            cursor.execute("UPDATE Games SET CoverImage = %s WHERE GameID = %s", (steam_url, gid))
            updated_count += 1
            print(f"Updated Game {gid} '{title}' -> {steam_url}")

        print(f"\n🎉 Successfully updated {updated_count} games with official Steam CDN header images!")

if __name__ == '__main__':
    update_images()
