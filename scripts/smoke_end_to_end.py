#!/usr/bin/env python3
"""Simple smoke test: signup -> create deal -> run underwriting"""
import os
import requests
import sys

BASE = os.environ.get("BASE_URL", "http://localhost:8000")

EMAIL = "smoke_test@example.com"
PASSWORD = "TestPass123!"


def signup():
    url = f"{BASE}/api/auth/signup"
    data = {"email": EMAIL, "password": PASSWORD, "full_name": "Smoke Tester"}
    r = requests.post(url, json=data, timeout=10)
    r.raise_for_status()
    return r.json().get("access_token")


def create_deal(token):
    url = f"{BASE}/api/deals"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "title": "Smoke Test Deal",
        "address": "123 Test St",
        "city": "Testville",
        "state": "CA",
        "zip_code": "90001",
        "property_type": "single_family",
        "unit_count": 1,
        "asking_price": 250000.0,
        "source_type": "manual",
    }
    r = requests.post(url, json=payload, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json().get("id")


def run_underwriting(token, deal_id):
    url = f"{BASE}/api/underwriting/{deal_id}/underwrite"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "purchase_price": 250000.0,
        "monthly_rent": 2000.0,
        "vacancy_rate": 0.05,
        "property_taxes_annual": 3000.0,
        "insurance_annual": 1000.0,
        "repairs_maintenance_annual": 1200.0,
        "management_rate": 0.08,
        "capex_reserve_annual": 500.0,
        "down_payment_percent": 0.25,
        "interest_rate": 0.065,
        "loan_term_years": 30,
        "property_type": "single_family",
    }
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()


def main():
    print("Starting smoke test against", BASE)
    try:
        token = signup()
    except Exception as e:
        print("Signup failed:", e)
        sys.exit(1)

    print("Got token (len):", len(token or ""))
    deal_id = create_deal(token)
    print("Created deal id:", deal_id)
    results = run_underwriting(token, deal_id)
    print("Underwriting results:")
    print(results)


if __name__ == "__main__":
    main()
