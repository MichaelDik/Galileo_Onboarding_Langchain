"""Customer information tool."""
from langchain_core.tools import tool


CUSTOMERS = {
    "michael": {
        "id": "1",
        "name": "Michael Scott",
        "email": "michael.scott@dundermifflin.com",
        "phone": "570-555-0101",
        "title": "Regional Manager",
        "branch": "Scranton",
    },
    "jim": {
        "id": "2",
        "name": "Jim Halpert",
        "email": "jim.halpert@dundermifflin.com",
        "phone": "570-555-0102",
        "title": "Sales Representative",
        "branch": "Scranton",
    },
    "pam": {
        "id": "3",
        "name": "Pam Beesly",
        "email": "pam.beesly@dundermifflin.com",
        "phone": "570-555-0103",
        "title": "Receptionist",
        "branch": "Scranton",
    },
    "dwight": {
        "id": "4",
        "name": "Dwight Schrute",
        "email": "dwight.schrute@dundermifflin.com",
        "phone": "570-555-0104",
        "title": "Assistant Regional Manager",
        "branch": "Scranton",
    },
    "angela": {
        "id": "5",
        "name": "Angela Martin",
        "email": "angela.martin@dundermifflin.com",
        "phone": "570-555-0105",
        "title": "Head of Accounting",
        "branch": "Scranton",
    },
}


@tool
def get_customer_info(customer_name: str) -> dict:
    """Get customer information by name.
    
    Args:
        customer_name: The customer's first name (e.g., michael, jim, pam, dwight, angela)
    
    Returns:
        Customer details including ID, name, email, phone, title, and branch.
    """
    key = customer_name.lower().strip()
    if key in CUSTOMERS:
        return CUSTOMERS[key]
    return {
        "error": f"Customer '{customer_name}' not found",
        "available_customers": list(CUSTOMERS.keys())
    }
