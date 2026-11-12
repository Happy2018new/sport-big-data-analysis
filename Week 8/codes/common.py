from pathlib import Path


class Config:
    ROOT: Path = Path(__file__).resolve().parent.parent
    DATA: Path = ROOT / "data"
    FIGURES: Path = ROOT / "figures"
    FEATURES: list[str] = ["steps", "bpm"]
    SEED: int = 42
