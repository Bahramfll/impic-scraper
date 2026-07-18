from pathlib import Path

import pandas as pd

from src.config import (
    CSV_COLUMNS,
    OUTPUT_CSV,
    CHECKPOINT_CSV,
    FAILED_IDS_FILE,
)


class Storage:

    def __init__(self):

        self.processed_ids = set()

        self._initialize_files()

        self._load_processed()


    def _initialize_files(self):

        if not OUTPUT_CSV.exists():

            pd.DataFrame(
                columns=CSV_COLUMNS
            ).to_csv(
                OUTPUT_CSV,
                index=False,
                encoding="utf-8-sig"
            )


        if not CHECKPOINT_CSV.exists():

            pd.DataFrame(
                columns=[
                    "ID",
                    "District",
                    "Class",
                    "Status",
                ]
            ).to_csv(
                CHECKPOINT_CSV,
                index=False,
                encoding="utf-8-sig"
            )


        if not FAILED_IDS_FILE.exists():

            FAILED_IDS_FILE.touch()


    def _load_processed(self):

        df = pd.read_csv(
            OUTPUT_CSV,
            dtype=str
        )

        if not df.empty:

            self.processed_ids = set(
                df["ID"].astype(str)
            )


    def is_processed(
        self,
        company_id
    ):

        return str(company_id) in self.processed_ids


    def mark_processed(
        self,
        company_id
    ):

        self.processed_ids.add(
            str(company_id)
        )


    def save_company(
        self,
        company
    ):

        df = pd.DataFrame(
            [company]
        )

        df.to_csv(

            OUTPUT_CSV,

            mode="a",

            header=False,

            index=False,

            encoding="utf-8-sig"

        )

        self.mark_processed(
            company["ID"]
        )


    def update_checkpoint(
        self,
        company_id,
        district,
        company_class,
        status,
    ):
        """
        Insert or update checkpoint.
        Every company ID exists only once.
        """

        df = self.get_checkpoint()

        company_id = str(company_id)

        if df.empty:

            df = pd.DataFrame(columns=[
                "ID",
                "District",
                "Class",
                "Status",
            ])

        mask = df["ID"].astype(str) == company_id

        if mask.any():

            df.loc[mask, "District"] = district
            df.loc[mask, "Class"] = company_class
            df.loc[mask, "Status"] = status

        else:

            df.loc[len(df)] = {
                "ID": company_id,
                "District": district,
                "Class": company_class,
                "Status": status,
            }

        df.to_csv(
            CHECKPOINT_CSV,
            index=False,
            encoding="utf-8-sig",
        )


    def save_failed(
        self,
        company_id
    ):

        with open(
            FAILED_IDS_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"{company_id}\n"
            )


    def load_failed(self):

        with open(
            FAILED_IDS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            ids = [

                line.strip()

                for line in f.readlines()

                if line.strip()

            ]

        return ids


    def clear_failed(self):

        FAILED_IDS_FILE.write_text(
            "",
            encoding="utf-8"
        )


    def total_processed(self):

        return len(
            self.processed_ids
        )


    def total_failed(self):

        return len(
            self.load_failed()
        )


    def get_output(self):

        return pd.read_csv(
            OUTPUT_CSV
        )


    def get_checkpoint(self):

        return pd.read_csv(
            CHECKPOINT_CSV,
            dtype=str
        )


    def update_status(
        self,
        company_id,
        status,
    ):

        df = self.get_checkpoint()

        if df.empty:
            return

        company_id = str(company_id)

        mask = df["ID"].astype(str) == company_id

        if not mask.any():
            return

        df.loc[
            mask,
            "Status"
        ] = status

        df.to_csv(
            CHECKPOINT_CSV,
            index=False,
            encoding="utf-8-sig"
        )