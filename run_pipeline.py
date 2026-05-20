import os
import yaml
import pandas as pd
from src.clean import load_all_files
from src.scoring.metrics import calculate_all_ratios
from src.scoring.health_score import calculate_health_score
from src.utils.logger import get_logger

logger = get_logger("pipeline")


def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def run():
    config = load_config()
    raw_dir = config["data"]["raw_dir"]
    processed_dir = config["data"]["processed_dir"]

    files = {
        year: os.path.join(raw_dir, fname)
        for year, fname in config["files"].items()
    }

    logger.info("loading raw files")
    df = load_all_files(files)

    logger.info("calculating ratios")
    df = calculate_all_ratios(df)
    df.to_csv(os.path.join(processed_dir, "banks_with_ratios.csv"), index=False)

    logger.info("calculating health score")
    df_score = calculate_health_score(df)
    df_score.to_csv(os.path.join(processed_dir, "banks_health_score.csv"), index=False)

    logger.info("done")


if __name__ == "__main__":
    run()