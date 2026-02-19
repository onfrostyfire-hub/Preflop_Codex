from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SpotConfig:
    hero: str
    villain: Optional[str]
    dealer: str
    hero_bet: Optional[float] = None
    villain_bet: Optional[float] = None


SPOT_CONFIGS = {
    "EP open raise": SpotConfig("EP", None, "BTN"),
    "MP open raise": SpotConfig("MP", None, "BTN"),
    "CO open raise": SpotConfig("CO", None, "BTN"),
    "BTN open raise": SpotConfig("BTN", None, "BTN"),
    "SB open raise": SpotConfig("SB", None, "BTN"),
    "EP vs 3bet MP": SpotConfig("EP", "MP", "BTN", 2.5, 7.5),
    "EP vs 3bet CO/BU": SpotConfig("EP", "CO", "BTN", 2.5, 7.5),
    "EP vs 3bet Blinds": SpotConfig("EP", "SB", "BTN", 2.5, 9.0),
    "CO def vs 3bet BU": SpotConfig("CO", "BTN", "SB", 2.5, 7.5),
    "CO def vs 3bet SB": SpotConfig("CO", "SB", "BTN", 2.5, 9.0),
    "CO def vs 3bet BB": SpotConfig("CO", "BB", "BTN", 2.5, 9.0),
    "BU def vs 3bet SB": SpotConfig("BTN", "SB", "BTN", 2.5, 9.0),
    "BU def vs 3bet BB": SpotConfig("BTN", "BB", "BTN", 2.5, 9.0),
    "SB def vs 3bet BB": SpotConfig("SB", "BB", "BTN", 3.0, 9.0),
    "BBvsBU x2.5 nl500": SpotConfig("BB", "BTN", "BTN", 1.0, 2.5),
    "BBvsBU x2.5 nl100": SpotConfig("BB", "BTN", "BTN", 1.0, 2.5),
}


def get_spot_config(spot_name: str) -> SpotConfig:
    return SPOT_CONFIGS.get(spot_name, SpotConfig("EP", None, "BTN"))
