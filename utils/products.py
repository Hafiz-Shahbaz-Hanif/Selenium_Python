"""The six SauceDemo products, with their catalogue prices.

SauceDemo's inventory is fixed, so these are safe to assert against directly.
"""
from __future__ import annotations

SAUCEDEMO_PRODUCTS: dict[str, float] = {
    "Sauce Labs Backpack": 29.99,
    "Sauce Labs Bike Light": 9.99,
    "Sauce Labs Bolt T-Shirt": 15.99,
    "Sauce Labs Fleece Jacket": 49.99,
    "Sauce Labs Onesie": 7.99,
    "Test.allTheThings() T-Shirt (Red)": 15.99,
}

ALL_PRODUCT_NAMES = list(SAUCEDEMO_PRODUCTS)


def price_of(product_name: str) -> float:
    return SAUCEDEMO_PRODUCTS[product_name]
