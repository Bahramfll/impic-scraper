from bs4 import BeautifulSoup


def extract_company_ids(html):
    """
    Extract company IDs from search results page.

    Returns:
        list[str]
    """

    soup = BeautifulSoup(html, "html.parser")

    ids = []

    rows = soup.select("tr")

    for row in rows:

        columns = row.find_all("td")

        if len(columns) < 3:
            continue

        company_link = columns[2].select_one("a[data-nl]")

        if company_link is None:
            continue

        company_id = company_link.get("data-nl")

        if not company_id:
            continue

        ids.append(company_id)

    return ids


def parse_company_details(html, company_id, district, company_class):
    """
    Parse company details page.

    Returns:
        dict
    """

    soup = BeautifulSoup(html, "html.parser")

    company = {
        "ID": company_id,
        "Company Name": "",
        "Email": "",
        "District": district,
        "Class": company_class,
    }


    for field in soup.select(".information-field"):

        label = field.find("label")

        value = field.find("span")

        if label is None or value is None:
            continue

        label_text = label.get_text(strip=True)

        value_text = value.get_text(" ", strip=True)

        if "Denominação" in label_text:
            company["Company Name"] = value_text

        elif "E-mail" in label_text:
            company["Email"] = value_text


    if not company["Company Name"]:

        text = soup.get_text("\n", strip=True)

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for i, line in enumerate(lines):

            if line.startswith("Denominação"):

                if i + 1 < len(lines):

                    company["Company Name"] = lines[i + 1]

            elif line.startswith("E-mail"):

                if i + 1 < len(lines):

                    company["Email"] = lines[i + 1]

    return company


def is_valid_company(company):

    if not company:
        return False

    if not company["ID"]:
        return False

    if not company["Company Name"]:
        return False

    return True


def print_company(company):
    """
    Pretty print company.
    """

    print("-" * 60)

    print(f"ID       : {company['ID']}")
    print(f"Company  : {company['Company Name']}")
    print(f"Email    : {company['Email']}")
    print(f"District : {company['District']}")
    print(f"Class    : {company['Class']}")

    print("-" * 60)