"""
Script to insert 50 AAA and Indie titles into MariaDB GameVault database
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database import DatabaseConnection

def get_or_create_developer(cursor, name, country="USA", founded=2000):
    cursor.execute("SELECT DeveloperID FROM Developers WHERE DeveloperName = %s", (name,))
    row = cursor.fetchone()
    if row:
        return row['DeveloperID']
    cursor.execute("INSERT INTO Developers (DeveloperName, Country, FoundedYear) VALUES (%s, %s, %s)", (name, country, founded))
    cursor.execute("SELECT LAST_INSERT_ID() AS id;")
    return cursor.fetchone()['id']

def get_or_create_publisher(cursor, name, country="USA"):
    cursor.execute("SELECT PublisherID FROM Publishers WHERE PublisherName = %s", (name,))
    row = cursor.fetchone()
    if row:
        return row['PublisherID']
    cursor.execute("INSERT INTO Publishers (PublisherName, Country) VALUES (%s, %s)", (name, country))
    cursor.execute("SELECT LAST_INSERT_ID() AS id;")
    return cursor.fetchone()['id']

def get_or_create_genre(cursor, name):
    cursor.execute("SELECT GenreID FROM Genres WHERE GenreName = %s", (name,))
    row = cursor.fetchone()
    if row:
        return row['GenreID']
    cursor.execute("INSERT INTO Genres (GenreName) VALUES (%s)", (name,))
    cursor.execute("SELECT LAST_INSERT_ID() AS id;")
    return cursor.fetchone()['id']

games_data = [
    # AAA TITLES
    {
        "title": "The Witcher 3: Wild Hunt",
        "developer": ("CD Projekt Red", "Poland", 1994),
        "publisher": ("CD Projekt", "Poland"),
        "price": 1999.00,
        "release_date": "2015-05-19",
        "description": "Geralt of Rivia, a monster hunter for hire, embarks on an epic quest in a dark fantasy open world.",
        "age_rating": "M",
        "genres": ["RPG", "Open World", "Action"],
        "cover": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "God of War Ragnarök",
        "developer": ("Santa Monica Studio", "USA", 1999),
        "publisher": ("Sony Interactive Entertainment", "USA"),
        "price": 3999.00,
        "release_date": "2022-11-09",
        "description": "Kratos and Atreus embark on a mythic journey for answers across Nine Realms before Ragnarök.",
        "age_rating": "M",
        "genres": ["Action", "Adventure"],
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
        "discount": 15.0
    },
    {
        "title": "Grand Theft Auto V",
        "developer": ("Rockstar Games", "USA", 1998),
        "publisher": ("Take-Two Interactive", "USA"),
        "price": 2499.00,
        "release_date": "2013-09-17",
        "description": "When a young street hustler, a retired bank robber and a terrifying psychopath find themselves entangled, they must pull off a series of dangerous heists.",
        "age_rating": "M",
        "genres": ["Action", "Open World"],
        "cover": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
        "discount": 30.0
    },
    {
        "title": "Red Dead Redemption",
        "developer": ("Rockstar Games", "USA", 1998),
        "publisher": ("Take-Two Interactive", "USA"),
        "price": 2499.00,
        "release_date": "2010-05-18",
        "description": "Former outlaw John Marston is forced by the government to hunt down his former gang members across the American frontier.",
        "age_rating": "M",
        "genres": ["Action", "Open World"],
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80",
        "discount": 0.0
    },
    {
        "title": "Horizon Forbidden West",
        "developer": ("Guerrilla Games", "Netherlands", 2000),
        "publisher": ("Sony Interactive Entertainment", "USA"),
        "price": 3499.00,
        "release_date": "2022-02-18",
        "description": "Explore distant lands, fight bigger awe-inspiring machines, and encounter startling new tribes as Aloy returns.",
        "age_rating": "T",
        "genres": ["Action", "Open World", "RPG"],
        "cover": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
        "discount": 20.0
    },
    {
        "title": "Spider-Man 2",
        "developer": ("Insomniac Games", "USA", 1994),
        "publisher": ("Sony Interactive Entertainment", "USA"),
        "price": 3999.00,
        "release_date": "2023-10-20",
        "description": "Spider-Men Peter Parker and Miles Morales face the ultimate test of strength inside and outside the mask as Venom threatens New York.",
        "age_rating": "T",
        "genres": ["Action", "Open World"],
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80",
        "discount": 10.0
    },
    {
        "title": "Ghost of Tsushima: Director's Cut",
        "developer": ("Sucker Punch Productions", "USA", 1997),
        "publisher": ("Sony Interactive Entertainment", "USA"),
        "price": 3499.00,
        "release_date": "2021-08-20",
        "description": "A storm is coming. Venture into the open world of feudal Japan as samurai warrior Jin Sakai.",
        "age_rating": "M",
        "genres": ["Action", "Open World"],
        "cover": "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?auto=format&fit=crop&w=800&q=80",
        "discount": 25.0
    },
    {
        "title": "Resident Evil 4 Remake",
        "developer": ("Capcom", "Japan", 1983),
        "publisher": ("Capcom", "Japan"),
        "price": 2999.00,
        "release_date": "2023-03-24",
        "description": "Leon S. Kennedy is sent on a mission to rescue the US President's kidnapped daughter in a secluded European village.",
        "age_rating": "M",
        "genres": ["Horror", "Action"],
        "cover": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
        "discount": 20.0
    },
    {
        "title": "Resident Evil Village",
        "developer": ("Capcom", "Japan", 1983),
        "publisher": ("Capcom", "Japan"),
        "price": 2499.00,
        "release_date": "2021-05-07",
        "description": "Experience survival horror like never before in Ethan Winters' terrifying journey through a snowy castle village.",
        "age_rating": "M",
        "genres": ["Horror", "Action"],
        "cover": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "discount": 40.0
    },
    {
        "title": "Monster Hunter World",
        "developer": ("Capcom", "Japan", 1983),
        "publisher": ("Capcom", "Japan"),
        "price": 1999.00,
        "release_date": "2018-01-26",
        "description": "Welcome to a new world! Take on the role of a hunter and slay ferocious monsters in a living ecosystem.",
        "age_rating": "T",
        "genres": ["Action", "RPG"],
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "Monster Hunter Wilds",
        "developer": ("Capcom", "Japan", 1983),
        "publisher": ("Capcom", "Japan"),
        "price": 3999.00,
        "release_date": "2025-02-28",
        "description": "Unbridled nature is dynamic and ever-changing. A story of monsters and humans in a world with two faces.",
        "age_rating": "T",
        "genres": ["Action", "RPG"],
        "cover": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
        "discount": 0.0
    },
    {
        "title": "Dark Souls III",
        "developer": ("FromSoftware", "Japan", 1986),
        "publisher": ("Bandai Namco", "Japan"),
        "price": 2499.00,
        "release_date": "2016-03-24",
        "description": "As fires fade and the world falls into ruin, journey into a universe filled with colossal enemies and dark environments.",
        "age_rating": "M",
        "genres": ["Souls-like", "RPG", "Action"],
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "Sekiro: Shadows Die Twice",
        "developer": ("FromSoftware", "Japan", 1986),
        "publisher": ("Activision", "USA"),
        "price": 2999.00,
        "release_date": "2019-03-22",
        "description": "Carve your own clever path to vengeance in a game awarded Game of the Year by FromSoftware.",
        "age_rating": "M",
        "genres": ["Action", "Souls-like"],
        "cover": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "Armored Core VI: Fires of Rubicon",
        "developer": ("FromSoftware", "Japan", 1986),
        "publisher": ("Bandai Namco", "Japan"),
        "price": 3499.00,
        "release_date": "2023-08-25",
        "description": "A mech action game offering omnidirectional high-speed battle encounters on the remote planet Rubicon 3.",
        "age_rating": "T",
        "genres": ["Action", "Shooter"],
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80",
        "discount": 20.0
    },
    {
        "title": "Fallout 4",
        "developer": ("Bethesda Game Studios", "USA", 1986),
        "publisher": ("Bethesda Softworks", "USA"),
        "price": 1499.00,
        "release_date": "2015-11-10",
        "description": "As the sole survivor of Vault 111, enter a world destroyed by nuclear war. Every second is a fight for survival.",
        "age_rating": "M",
        "genres": ["RPG", "Open World"],
        "cover": "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?auto=format&fit=crop&w=800&q=80",
        "discount": 60.0
    },
    {
        "title": "The Elder Scrolls V: Skyrim",
        "developer": ("Bethesda Game Studios", "USA", 1986),
        "publisher": ("Bethesda Softworks", "USA"),
        "price": 1799.00,
        "release_date": "2011-11-11",
        "description": "The Dragonborn returns in an epic open-world fantasy masterpiece that reshaped modern RPG gaming.",
        "age_rating": "M",
        "genres": ["RPG", "Open World"],
        "cover": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
        "discount": 75.0
    },
    {
        "title": "Starfield",
        "developer": ("Bethesda Game Studios", "USA", 1986),
        "publisher": ("Bethesda Softworks", "USA"),
        "price": 3999.00,
        "release_date": "2023-09-06",
        "description": "Starfield is the first new universe in 25 years from Bethesda Game Studios, creators of Skyrim.",
        "age_rating": "M",
        "genres": ["RPG", "Open World"],
        "cover": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "discount": 30.0
    },
    {
        "title": "Doom Eternal",
        "developer": ("id Software", "USA", 1991),
        "publisher": ("Bethesda Softworks", "USA"),
        "price": 1999.00,
        "release_date": "2020-03-20",
        "description": "Hell's armies have invaded Earth. Become the Slayer in an epic single-player campaign to conquer demons.",
        "age_rating": "M",
        "genres": ["Shooter", "Action"],
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
        "discount": 67.0
    },
    {
        "title": "Cyberpunk 2077",
        "developer": ("CD Projekt Red", "Poland", 1994),
        "publisher": ("CD Projekt", "Poland"),
        "price": 2999.00,
        "release_date": "2020-12-10",
        "description": "An open-world action-adventure RPG set in Night City, a megalopolis obsessed with power, glamour and body modification.",
        "age_rating": "M",
        "genres": ["Action", "RPG", "Open World"],
        "cover": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "Final Fantasy XVI",
        "developer": ("Square Enix", "Japan", 1986),
        "publisher": ("Square Enix", "Japan"),
        "price": 3799.00,
        "release_date": "2023-06-22",
        "description": "An epic dark fantasy world where the fate of the land is decided by the mighty Eikons and the Dominants.",
        "age_rating": "M",
        "genres": ["RPG", "Action"],
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80",
        "discount": 20.0
    },
    {
        "title": "Final Fantasy VII Rebirth",
        "developer": ("Square Enix", "Japan", 1986),
        "publisher": ("Square Enix", "Japan"),
        "price": 3999.00,
        "release_date": "2024-02-29",
        "description": "Cloud and his comrades escape Midgar and embark on an unknown adventure across the planet in search of Sephiroth.",
        "age_rating": "T",
        "genres": ["RPG", "Action"],
        "cover": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
        "discount": 15.0
    },
    {
        "title": "Dragon's Dogma 2",
        "developer": ("Capcom", "Japan", 1983),
        "publisher": ("Capcom", "Japan"),
        "price": 3499.00,
        "release_date": "2024-03-22",
        "description": "A single player, narrative driven action-RPG that challenges the players to choose their own experience.",
        "age_rating": "M",
        "genres": ["Action", "RPG", "Open World"],
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80",
        "discount": 10.0
    },
    {
        "title": "Alan Wake 2",
        "developer": ("Remedy Entertainment", "Finland", 1995),
        "publisher": ("Epic Games", "USA"),
        "price": 2999.00,
        "release_date": "2023-10-27",
        "description": "A string of ritualistic murders threatens Bright Falls. Saga Anderson and Alan Wake fight dark forces in Pacific Northwest.",
        "age_rating": "M",
        "genres": ["Horror", "Action"],
        "cover": "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?auto=format&fit=crop&w=800&q=80",
        "discount": 20.0
    },
    {
        "title": "Control",
        "developer": ("Remedy Entertainment", "Finland", 1995),
        "publisher": ("505 Games", "Italy"),
        "price": 1999.00,
        "release_date": "2019-08-27",
        "description": "After a secretive agency in New York is invaded by an otherworldly threat, Jesse Faden becomes the new Director.",
        "age_rating": "M",
        "genres": ["Action", "Adventure"],
        "cover": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
        "discount": 70.0
    },
    {
        "title": "Death Stranding Director's Cut",
        "developer": ("Kojima Productions", "Japan", 2015),
        "publisher": ("505 Games", "Italy"),
        "price": 2499.00,
        "release_date": "2021-09-24",
        "description": "From legendary game creator Hideo Kojima comes a genre-defying experience, now expanded in the Director's Cut.",
        "age_rating": "M",
        "genres": ["Action", "Open World"],
        "cover": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "discount": 40.0
    },
    {
        "title": "Forza Horizon 5",
        "developer": ("Playground Games", "UK", 2010),
        "publisher": ("Xbox Game Studios", "USA"),
        "price": 3499.00,
        "release_date": "2021-11-09",
        "description": "Your Ultimate Horizon Adventure awaits! Explore the vibrant and ever-evolving open world landscapes of Mexico.",
        "age_rating": "E",
        "genres": ["Racing", "Open World"],
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "EA Sports FC 24",
        "developer": ("EA Vancouver", "Canada", 1991),
        "publisher": ("Electronic Arts", "USA"),
        "price": 3499.00,
        "release_date": "2023-09-29",
        "description": "Welcome to a new era for The World's Game, bringing unmatched authenticity to the pitch.",
        "age_rating": "E",
        "genres": ["Sports"],
        "cover": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
        "discount": 60.0
    },
    {
        "title": "Battlefield 2042",
        "developer": ("DICE", "Sweden", 1992),
        "publisher": ("Electronic Arts", "USA"),
        "price": 2999.00,
        "release_date": "2021-11-19",
        "description": "A first-person shooter that marks the return to the iconic all-out warfare of the franchise.",
        "age_rating": "M",
        "genres": ["Shooter"],
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80",
        "discount": 70.0
    },
    {
        "title": "Star Wars Jedi: Survivor",
        "developer": ("Respawn Entertainment", "USA", 2010),
        "publisher": ("Electronic Arts", "USA"),
        "price": 3499.00,
        "release_date": "2023-04-28",
        "description": "The story of Cal Kestis continues in Star Wars Jedi: Survivor, a galaxy-spanning action-adventure game.",
        "age_rating": "T",
        "genres": ["Action", "Adventure"],
        "cover": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
        "discount": 45.0
    },
    {
        "title": "Apex Legends",
        "developer": ("Respawn Entertainment", "USA", 2010),
        "publisher": ("Electronic Arts", "USA"),
        "price": 0.00,
        "release_date": "2019-02-04",
        "description": "Conquer with character in Apex Legends, a free-to-play Hero shooter where legendary characters fight for glory.",
        "age_rating": "T",
        "genres": ["Shooter", "Action"],
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80",
        "discount": 0.0
    },
    {
        "title": "Call of Duty: Modern Warfare III",
        "developer": ("Infinity Ward", "USA", 2002),
        "publisher": ("Activision", "USA"),
        "price": 4999.00,
        "release_date": "2023-11-10",
        "description": "In the direct sequel to the record-breaking Call of Duty: Modern Warfare II, Captain Price and Task Force 141 face off against Makarov.",
        "age_rating": "M",
        "genres": ["Shooter", "Action"],
        "cover": "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?auto=format&fit=crop&w=800&q=80",
        "discount": 15.0
    },
    {
        "title": "Diablo IV",
        "developer": ("Blizzard Entertainment", "USA", 1991),
        "publisher": ("Blizzard Entertainment", "USA"),
        "price": 3999.00,
        "release_date": "2023-06-05",
        "description": "The endless battle between the High Heavens and the Burning Hells continues as Sanctuary is consumed by hatred.",
        "age_rating": "M",
        "genres": ["RPG", "Action"],
        "cover": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
        "discount": 35.0
    },
    {
        "title": "Hogwarts Legacy",
        "developer": ("Avalanche Software", "USA", 1995),
        "publisher": ("Warner Bros. Games", "USA"),
        "price": 3499.00,
        "release_date": "2023-02-10",
        "description": "Experience Hogwarts in the 1800s. Your character is a student who holds the key to an ancient secret.",
        "age_rating": "T",
        "genres": ["RPG", "Open World"],
        "cover": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "Assassin's Creed Valhalla",
        "developer": ("Ubisoft Montreal", "Canada", 1997),
        "publisher": ("Ubisoft", "France"),
        "price": 2999.00,
        "release_date": "2020-11-10",
        "description": "Become Eivor, a legendary Viking raider on a quest for glory across 9th-century England.",
        "age_rating": "M",
        "genres": ["Action", "Open World"],
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
        "discount": 75.0
    },
    {
        "title": "Far Cry 6",
        "developer": ("Ubisoft Toronto", "Canada", 2010),
        "publisher": ("Ubisoft", "France"),
        "price": 2999.00,
        "release_date": "2021-10-07",
        "description": "Welcome to Yara, a tropical paradise frozen in time. As dictator Antón Castillo, fight for freedom.",
        "age_rating": "M",
        "genres": ["Action", "Open World"],
        "cover": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
        "discount": 75.0
    },

    # INDIE TITLES
    {
        "title": "Hades",
        "developer": ("Supergiant Games", "USA", 2009),
        "publisher": ("Supergiant Games", "USA"),
        "price": 1100.00,
        "release_date": "2020-09-17",
        "description": "Defy the god of the dead as you hack and slash your way out of the Underworld in this rogue-like dungeon crawler.",
        "age_rating": "T",
        "genres": ["Rogue-like", "Action"],
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "Hollow Knight",
        "developer": ("Team Cherry", "Australia", 2014),
        "publisher": ("Team Cherry", "Australia"),
        "price": 699.00,
        "release_date": "2017-02-24",
        "description": "Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects and heroes.",
        "age_rating": "E10+",
        "genres": ["Action", "Adventure"],
        "cover": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "Hollow Knight: Silksong",
        "developer": ("Team Cherry", "Australia", 2014),
        "publisher": ("Team Cherry", "Australia"),
        "price": 1199.00,
        "release_date": "2025-06-01",
        "description": "Discover a haunted kingdom in Hollow Knight: Silksong! Play as Hornet, princess-protector of Hallownest.",
        "age_rating": "E10+",
        "genres": ["Action", "Adventure"],
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80",
        "discount": 0.0
    },
    {
        "title": "Celeste",
        "developer": ("Maddy Makes Games", "Canada", 2018),
        "publisher": ("Maddy Makes Games", "Canada"),
        "price": 699.00,
        "release_date": "2018-01-25",
        "description": "Help Madeline survive her inner demons on her journey to the top of Celeste Mountain in a tight precision platformer.",
        "age_rating": "E10+",
        "genres": ["Puzzle", "Adventure"],
        "cover": "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?auto=format&fit=crop&w=800&q=80",
        "discount": 75.0
    },
    {
        "title": "Stardew Valley",
        "developer": ("ConcernedApe", "USA", 2016),
        "publisher": ("ConcernedApe", "USA"),
        "price": 479.00,
        "release_date": "2016-02-26",
        "description": "You've inherited your grandfather's old farm plot in Stardew Valley. Can you learn to live off the land?",
        "age_rating": "E",
        "genres": ["Simulation", "RPG"],
        "cover": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
        "discount": 30.0
    },
    {
        "title": "Dead Cells",
        "developer": ("Motion Twin", "France", 2001),
        "publisher": ("Motion Twin", "France"),
        "price": 899.00,
        "release_date": "2018-08-07",
        "description": "Dead Cells is a rogue-lite, Metroidvania inspired action platformer. You'll explore a sprawling, ever-changing castle.",
        "age_rating": "T",
        "genres": ["Rogue-like", "Action"],
        "cover": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "discount": 50.0
    },
    {
        "title": "Slay the Spire",
        "developer": ("MegaCrit", "USA", 2017),
        "publisher": ("Humble Games", "USA"),
        "price": 899.00,
        "release_date": "2019-01-23",
        "description": "We fused card games and roguelikes together to make the best single player deckbuilder we could.",
        "age_rating": "E10+",
        "genres": ["Strategy", "Rogue-like"],
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
        "discount": 66.0
    },
    {
        "title": "Balatro",
        "developer": ("LocalThunk", "Canada", 2024),
        "publisher": ("Playstack", "UK"),
        "price": 649.00,
        "release_date": "2024-02-20",
        "description": "The poker roguelike. Balatro is a hypnotically satisfying deckbuilder where you play illegal poker hands.",
        "age_rating": "E10+",
        "genres": ["Rogue-like", "Strategy", "Puzzle"],
        "cover": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
        "discount": 10.0
    },
    {
        "title": "Sea of Stars",
        "developer": ("Sabotage Studio", "Canada", 2016),
        "publisher": ("Sabotage Studio", "Canada"),
        "price": 1299.00,
        "release_date": "2023-08-29",
        "description": "Sea of Stars is a turn-based RPG inspired by the classics. It tells the story of two Children of the Solstice.",
        "age_rating": "E10+",
        "genres": ["RPG"],
        "cover": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80",
        "discount": 20.0
    },
    {
        "title": "Dave the Diver",
        "developer": ("MINTROCKET", "South Korea", 2022),
        "publisher": ("MINTROCKET", "South Korea"),
        "price": 899.00,
        "release_date": "2023-06-28",
        "description": "DAVE THE DIVER is a casual, singleplayer adventure RPG featuring deep-sea exploration and fishing during the day and sushi restaurant management at night.",
        "age_rating": "E10+",
        "genres": ["Simulation", "Adventure"],
        "cover": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
        "discount": 25.0
    },
    {
        "title": "Manor Lords",
        "developer": ("Slavic Magic", "Poland", 2020),
        "publisher": ("Hooded Horse", "USA"),
        "price": 1499.00,
        "release_date": "2024-04-26",
        "description": "Manor Lords is a medieval strategy game featuring in-depth city building, tactical battles, and complex economic simulations.",
        "age_rating": "T",
        "genres": ["Strategy", "Simulation"],
        "cover": "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80",
        "discount": 25.0
    },
    {
        "title": "Palworld",
        "developer": ("Pocketpair", "Japan", 2015),
        "publisher": ("Pocketpair", "Japan"),
        "price": 1299.00,
        "release_date": "2024-01-19",
        "description": "Fight, farm, build and work alongside mysterious creatures called 'Pals' in this completely new multiplayer survival crafting game.",
        "age_rating": "T",
        "genres": ["Open World", "Action"],
        "cover": "https://images.unsplash.com/photo-1579373903781-fd5c0c30c4cd?auto=format&fit=crop&w=800&q=80",
        "discount": 10.0
    },
    {
        "title": "Lethal Company",
        "developer": ("Zeekerss", "USA", 2023),
        "publisher": ("Zeekerss", "USA"),
        "price": 479.00,
        "release_date": "2023-10-23",
        "description": "A co-op horror about scavenging abandoned moons to sell scrap to the Company.",
        "age_rating": "T",
        "genres": ["Horror", "Action"],
        "cover": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80",
        "discount": 20.0
    },
    {
        "title": "Cuphead",
        "developer": ("Studio MDHR", "Canada", 2013),
        "publisher": ("Studio MDHR", "Canada"),
        "price": 699.00,
        "release_date": "2017-09-29",
        "description": "Cuphead is a classic run and gun action game heavily focused on boss battles, inspired by 1930s cartoons.",
        "age_rating": "E10+",
        "genres": ["Action"],
        "cover": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "discount": 30.0
    },
    {
        "title": "Risk of Rain 2",
        "developer": ("Hopoo Games", "USA", 2012),
        "publisher": ("Gearbox Publishing", "USA"),
        "price": 999.00,
        "release_date": "2020-08-11",
        "description": "Escape a chaotic alien planet by fighting through hordes of frenzied monsters with your friends.",
        "age_rating": "T",
        "genres": ["Rogue-like", "Shooter", "Action"],
        "cover": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80",
        "discount": 60.0
    }
]

def run_import():
    with DatabaseConnection() as cursor:
        inserted_count = 0
        for g in games_data:
            # Check if game title already exists in Games table
            cursor.execute("SELECT GameID FROM Games WHERE Title = %s", (g["title"],))
            if cursor.fetchone():
                continue

            dev_id = get_or_create_developer(cursor, g["developer"][0], g["developer"][1], g["developer"][2])
            pub_id = get_or_create_publisher(cursor, g["publisher"][0], g["publisher"][1])

            # Insert Game
            cursor.execute("""
                INSERT INTO Games (Title, DeveloperID, PublisherID, Price, ReleaseDate, Description, AgeRating, CoverImage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (g["title"], dev_id, pub_id, g["price"], g["release_date"], g["description"], g["age_rating"], g["cover"]))

            cursor.execute("SELECT LAST_INSERT_ID() AS id;")
            game_id = cursor.fetchone()['id']

            # Insert Genres mapping
            for genre_name in g["genres"]:
                genre_id = get_or_create_genre(cursor, genre_name)
                cursor.execute("INSERT IGNORE INTO Game_Genres (GameID, GenreID) VALUES (%s, %s)", (game_id, genre_id))

            # Insert Discount if > 0
            if g.get("discount", 0) > 0:
                cursor.execute("""
                    INSERT INTO Discounts (GameID, DiscountPercent, StartDate, EndDate)
                    VALUES (%s, %s, '2026-01-01', '2026-12-31')
                """, (game_id, g["discount"]))

            inserted_count += 1

        print(f"🎉 Successfully inserted {inserted_count} AAA & Indie titles into MariaDB GameVault!")

if __name__ == '__main__':
    run_import()
