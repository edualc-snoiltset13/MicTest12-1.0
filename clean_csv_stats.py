import pandas as pd

INPUT_PATH = "input.csv"
OUTPUT_PATH = "summary_stats.csv"


def clean_missing(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())
        else:
            mode = df[col].mode(dropna=True)
            if not mode.empty:
                df[col] = df[col].fillna(mode.iloc[0])
    return df


def main() -> None:
    df = pd.read_csv(INPUT_PATH)
    df = clean_missing(df)
    stats = df.describe()
    stats.to_csv(OUTPUT_PATH)
    print(stats)


if __name__ == "__main__":
    main()
