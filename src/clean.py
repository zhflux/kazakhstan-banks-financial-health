import pandas as pd

def load_and_clean(path: str, year: int) -> pd.DataFrame:
    """Load and clean a single NBK Excel file."""
    df = pd.read_excel(path, header=None, skiprows=8)
    df = df[[0, 1, 2, 3, 13, 14, 16, 17]].copy()
    df.columns = ["number", "bank_name", "assets", "loans",
                  "liabilities", "deposits", "equity", "net_income"]
    df = df[pd.to_numeric(df["number"], errors="coerce").notna()]
    df = df[df["assets"].notna()]
    df["year"] = year
    return df


def load_all_files(files: dict) -> pd.DataFrame:
    """Load and combine multiple NBK Excel files."""
    frames = [load_and_clean(path, year) for year, path in files.items()]
    return pd.concat(frames, ignore_index=True)