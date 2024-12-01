import re


def exctract_move_dest(doc_body: str) -> str | None:
    """Extract the move destination (in an EIPs.exposed URL) from a doc body."""
    if match := re.search(
        r"(https://github.com/ethereum/)[A-Za-z0-9\/]+((eip|erc)\-[0-9]+).md", doc_body
    ):
        doc_match = match.group(2)
        if doc_match.startswith("erc"):
            return f"/ercs/{doc_match}.html"
        return f"/eips/{doc_match}.html"
    return None
