"""Concatenate the per-year FAOSTAT CSVs into single consolidated files."""

import csv
from pathlib import Path

BASE = Path(__file__).parent

SA_DIR = BASE / "[Tratados]Datasets_FAOSTAT_Rice_South_America"
BP_DIR = BASE / "[Tratados]Datasets_FAOSTAT_Rice_Biggest_Producers"

# The 12 countries actually used in the paper (drops the "South America"
# aggregate row and "French Guiana", which are not modeled).
SA_COUNTRIES = {
    "Argentina",
    "Bolivia (Plurinational State of)",
    "Brazil",
    "Chile",
    "Colombia",
    "Ecuador",
    "Guyana",
    "Paraguay",
    "Peru",
    "Suriname",
    "Uruguay",
    "Venezuela (Bolivarian Republic of)",
}


def concat(directory, prefix, out_name, filter_countries=None):
    files = sorted(directory.glob(f"{prefix}*.csv"))
    header = None
    rows = []
    for path in files:
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            file_header = next(reader)
            if header is None:
                header = file_header
            for row in reader:
                if not row or all(not cell.strip() for cell in row):
                    continue
                if filter_countries and row[0] not in filter_countries:
                    continue
                rows.append(row)
    out = BASE / out_name
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"{out_name}: {len(rows)} rows from {len(files)} files")


if __name__ == "__main__":
    concat(SA_DIR, "Rice_South_America_", "Rice_South_America_2004_2023.csv", SA_COUNTRIES)
    concat(BP_DIR, "Rice_Biggest_Producers_", "Rice_Biggest_Producers_2011_2023.csv")
