from pathlib import Path
from .pipeline import traitement


sources_folder = Path(__file__).resolve().parent/"sources"
CSV_PATH= sources_folder/"srce.csv"
JSON_PATH= sources_folder/"srce.json"
LOG_PATH= sources_folder/"srce.log"


def main():
    ids_traites = set()
    print(f"Enregistrements valides et normalises par source:")
    traitement(JSON_PATH, ids_traites)
    traitement(CSV_PATH, ids_traites)
    traitement(LOG_PATH, ids_traites)


if __name__ == "__main__":
    main()
