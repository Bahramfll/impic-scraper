import time
import requests

from src.config import (
    BASE_URL,
    HEADERS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    REQUEST_DELAY,
    PAGE_DELAY,
)

from src.parser import (
    extract_company_ids,
    parse_company_details,
    is_valid_company,
)

from src.storage import Storage


class Scraper:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(HEADERS)

        self.storage = Storage()

        self.failed_ids = []

    def post(self, payload):

        response = self.session.post(
            BASE_URL,
            data=payload,
            timeout=REQUEST_TIMEOUT
        )

        return response

    def get_page(
        self,
        district,
        company_class,
        page,
    ):

        payload = {

            "id_type": "8",

            "id_object": "18",

            "pesquisar": "true",

            "loadTable": "1",

            "pageSearch": str(page),

            "distrito": district,

            "classe_maxima": str(company_class),

        }

        for attempt in range(1, MAX_RETRIES + 1):

            try:

                response = self.post(payload)

                if response.status_code == 200:

                    time.sleep(PAGE_DELAY)

                    return response.text

                print(
                    f"[PAGE] HTTP {response.status_code}"
                    f" | Retry {attempt}/{MAX_RETRIES}"
                )

            except requests.RequestException as e:

                print(
                    f"[PAGE] {e}"
                    f" | Retry {attempt}/{MAX_RETRIES}"
                )

            time.sleep(RETRY_DELAY)

        return None


    def get_details(
        self,
        company_id,
        district,
        company_class,
    ):

        payload = {

            "id_type": "8",

            "id_object": "18",

            "informacao": "true",

            "info": "NUMERO_LICENCA",

            "value": company_id,

            "nl": company_id,

        }

        for attempt in range(1, MAX_RETRIES + 1):

            try:

                response = self.post(payload)

                if response.status_code == 200:

                    company = parse_company_details(
                        response.text,
                        company_id,
                        district,
                        company_class,
                    )

                    if is_valid_company(company):

                        time.sleep(REQUEST_DELAY)

                        return company

                    print(
                        f"[DETAIL] Invalid parser result"
                        f" ({company_id})"
                    )

                elif response.status_code == 500:

                    print(
                        f"[DETAIL] Server 500"
                        f" ({company_id})"
                        f" Retry {attempt}/{MAX_RETRIES}"
                    )

                else:

                    print(
                        f"[DETAIL] HTTP {response.status_code}"
                        f" ({company_id})"
                    )

            except requests.RequestException as e:

                print(
                    f"[DETAIL] {company_id}"
                )

                print(e)

            time.sleep(RETRY_DELAY)

        self.failed_ids.append(company_id)

        self.storage.save_failed(company_id)

        return None


    def get_company_ids(
        self,
        district,
        company_class,
        page,
    ):

        html = self.get_page(
            district,
            company_class,
            page,
        )

        if html is None:

            return None, None

        ids = extract_company_ids(html)

        return ids, html
    

    def scrape(
        self,
        districts,
        classes,
    ):

        total_saved = self.storage.total_processed()

        print(
            f"\nAlready processed: {total_saved} companies\n"
        )

        for district in districts:

            for company_class in classes:

                print(
                    f"\n{'=' * 60}"
                )

                print(
                    f"{district} | Class {company_class}"
                )

                print(
                    f"{'=' * 60}"
                )

                page = 1

                while True:

                    ids, html = self.get_company_ids(
                        district,
                        company_class,
                        page,
                    )

                    if html is None:

                        print(
                            "Unable to load page."
                        )

                        break

                    if not ids:

                        print(
                            "No more companies."
                        )

                        break

                    print(
                        f"Page {page} : {len(ids)} companies"
                    )

                    page_saved = 0
                    page_skipped = 0

                    for company_id in ids:

                        # ---------------------------------
                        # Resume Support
                        # ---------------------------------

                        if self.storage.is_processed(
                            company_id
                        ):

                            page_skipped += 1

                            continue

                        # ---------------------------------
                        # Get Details
                        # ---------------------------------

                        company = self.get_details(
                            company_id,
                            district,
                            company_class,
                        )

                        if company is None:

                            self.storage.update_checkpoint(
                                company_id,
                                district,
                                company_class,
                                "FAILED",
                            )

                            continue

                        # ---------------------------------
                        # Save Immediately
                        # ---------------------------------

                        self.storage.save_company(
                            company
                        )

                        self.storage.update_checkpoint(
                            company_id,
                            district,
                            company_class,
                            "DONE",
                        )

                        page_saved += 1

                        total_saved += 1

                        print(
                            f"[{total_saved}] "
                            f"{company['Company Name']}"
                        )

                    print()

                    print(
                        f"Saved   : {page_saved}"
                    )

                    print(
                        f"Skipped : {page_skipped}"
                    )

                    # ---------------------------------
                    # Next Page?
                    # ---------------------------------

                    if "SEGUINTE" not in html:

                        print(
                            "Last page reached."
                        )

                        break

                    page += 1

        print()

        print("=" * 60)

        print(
            f"Finished."
        )

        print(
            f"Saved Companies : {self.storage.total_processed()}"
        )

        print(
            f"Failed IDs : {self.storage.total_failed()}"
        )

        print("=" * 60)


    def retry_failed(self):

        failed_ids = self.storage.load_failed()

        if not failed_ids:

            print("\nNo failed IDs to retry.\n")

            return

        checkpoint = self.storage.get_checkpoint()

        print("\nRetrying failed companies...\n")

        success = 0

        still_failed = []

        for company_id in failed_ids:

            row = checkpoint[
                checkpoint["ID"].astype(str) == str(company_id)
            ]

            if row.empty:
                continue

            district = row.iloc[0]["District"]
            company_class = int(row.iloc[0]["Class"])

            print(
                f"Retry -> {company_id}"
            )

            company = self.get_details(
                company_id,
                district,
                company_class,
            )

            if company:

                self.storage.save_company(
                    company
                )

                self.storage.update_status(
                    company_id,
                    "DONE"
                )

                success += 1

            else:

                still_failed.append(
                    company_id
                )

        self.storage.clear_failed()

        for company_id in still_failed:

            self.storage.save_failed(
                company_id
            )

        print()

        print(
            f"Recovered : {success}"
        )

        print(
            f"Remaining : {len(still_failed)}"
        )
    

    def run(
        self,
        districts,
        classes,
    ):

        start = time.time()

        self.scrape(
            districts,
            classes,
        )

        self.retry_failed()

        elapsed = time.time() - start

        print()

        print("=" * 60)

        print(
            f"Completed in {elapsed:.1f} seconds"
        )

        print(
            f"Companies : {self.storage.total_processed()}"
        )

        print(
            f"Remaining Failed : {self.storage.total_failed()}"
        )

        print("=" * 60)

from src.config import (
    DISTRICTS,
    CLASSES,
)


def main():

    scraper = Scraper()

    scraper.run(
        DISTRICTS,
        CLASSES,
    )


if __name__ == "__main__":

    main()