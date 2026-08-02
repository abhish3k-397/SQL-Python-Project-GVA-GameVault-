"""
Game Model Class representing catalog games
"""

class Game:
    """Game domain object representing catalog items"""
    def __init__(self, game_id: int, title: str, price: float, 
                 developer_name: str = "Unknown", publisher_name: str = "Unknown",
                 genres: str = "N/A", avg_rating: float = 0.0, age_rating: str = "RP"):
        self.game_id = game_id
        self.title = title
        self.price = float(price)
        self.developer_name = developer_name
        self.publisher_name = publisher_name or "Self-Published"
        self.genres = genres
        self.avg_rating = float(avg_rating or 0.0)
        self.age_rating = age_rating

    def is_discounted(self, original_price: float) -> bool:
        return self.price < original_price

    def get_rating_stars(self) -> str:
        if self.avg_rating == 0:
            return "No Ratings"
        stars = "★" * int(round(self.avg_rating))
        return f"{stars:<5} ({self.avg_rating:.2f}/5.00)"

    def __str__(self):
        return f"[{self.game_id:2d}] {self.title:<28} | Price: ₹{self.price:8.2f} | Rating: {self.get_rating_stars()}"
