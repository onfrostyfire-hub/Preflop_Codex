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

    "CO def vs 3bet BU": SpotConfig(hero="CO", villain="BTN", dealer="SB", hero_bet=2.5, villain_bet=7.5),
    "CO def vs 3bet SB": SpotConfig(hero="CO", villain="SB", dealer="BTN", hero_bet=2.5, villain_bet=12),
    "CO def vs 3bet BB": SpotConfig(hero="CO", villain="BB", dealer="BTN", hero_bet=2.5, villain_bet=12),
    "BU def vs 3bet SB": SpotConfig(hero="BTN", villain="SB", dealer="BTN", hero_bet=2.5, villain_bet=12),
    "BU def vs 3bet BB": SpotConfig(hero="BTN", villain="BB", dealer="BTN", hero_bet=2.5, villain_bet=12),
    "SB def vs 3bet BB": SpotConfig(hero="SB", villain="BB", dealer="BTN", hero_bet=3.0, villain_bet=9),
    "BBvsBU x2.5 nl500": SpotConfig(hero="BB", villain="BTN", dealer="BTN", hero_bet=1.0, villain_bet=2.5),
    "BBvsBU x2.5 nl100": SpotConfig(hero="BB", villain="BTN", dealer="BTN", hero_bet=1.0, villain_bet=2.5),

}

def get_spot_config(spot_name: str) -> SpotConfig:
    return SPOT_CONFIGS.get(spot_name, SpotConfig(hero="EP", villain=None, dealer="BTN"))
