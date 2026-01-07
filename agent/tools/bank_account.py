"""Bank account balance tool."""
from langchain_core.tools import tool


ACCOUNTS = {
    "1": {"holder": "Michael Scott", "balance": 45250.00, "account_type": "Checking"},
    "2": {"holder": "Jim Halpert", "balance": 78340.50, "account_type": "Checking"},
    "3": {"holder": "Pam Beesly", "balance": 32100.75, "account_type": "Savings"},
    "4": {"holder": "Dwight Schrute", "balance": 156780.25, "account_type": "Checking"},
    "5": {"holder": "Angela Martin", "balance": 89450.00, "account_type": "Savings"},
}


@tool
def get_bank_balance(customer_id: str) -> dict:
    """Get bank account balance for a customer by their ID.
    
    Args:
        customer_id: The customer's unique ID (e.g., 1, 2, 3, 4, 5)
    
    Returns:
        Account details including holder name, balance, and account type.
    """
    key = customer_id.strip()
    if key in ACCOUNTS:
        account = ACCOUNTS[key]
        return {
            "customer_id": key,
            "holder": account["holder"],
            "balance": f"${account['balance']:,.2f}",
            "account_type": account["account_type"],
        }
    return {
        "error": f"Account '{customer_id}' not found",
        "available_accounts": list(ACCOUNTS.keys())
    }
