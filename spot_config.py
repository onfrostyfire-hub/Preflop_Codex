from dataclasses import dataclass
from typing import Optional

POSITIONS = ["EP", "MP", "CO", "BTN", "SB", "BB"]

@dataclass(frozen=True)
class SpotConfig:
    hero: str
    villain: Optional[str]
    dealer: str
    hero_bet: Optional[float] = None
    villain_bet: Optional[float] = None

SPOT_CONFIGS = {
    # Open raise
    "EP open raise": SpotConfig(hero="EP", villain=None, dealer="BTN"),
    "MP open raise": SpotConfig(hero="MP", villain=None, dealer="BTN"),
    "CO open raise": SpotConfig(hero="CO", villain=None, dealer="BTN"),
    "BTN open raise": SpotConfig(hero="BTN", villain=None, dealer="BTN"),
    "SB open raise": SpotConfig(hero="SB", villain=None, dealer="BTN"),

    # Def vs 3bet (пока только EP ветка)
    "EP vs 3bet MP": SpotConfig(hero="EP", villain="MP", dealer="BTN", hero_bet=2.5, villain_bet=7.5),
    "EP vs 3bet CO/BU": SpotConfig(hero="EP", villain="CO", dealer="BTN", hero_bet=2.5, villain_bet=7.5),
    "EP vs 3bet Blinds": SpotConfig(hero="EP", villain="SB", dealer="BTN", hero_bet=2.5, villain_bet=10.0),
}

def get_spot_config(spot_name: str) -> SpotConfig:
    return SPOT_CONFIGS.get(spot_name, SpotConfig(hero="EP", villain=None, dealer="BTN"))
