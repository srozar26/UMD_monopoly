def calculate_rent(property_data, owner_data):
    """
    Calculates the rent a player must pay when landing on a property.
    """

    rent = property_data["base_rent"]

    group = property_data["group"]
    owned_in_group = owner_data["owned_groups"].get(group, 0)
    total_in_group = owner_data["group_sizes"].get(group, 0)

    if owned_in_group == total_in_group:
        rent *= 2

    upgrades = property_data.get("upgrades", 0)
    rent *= (1 + 0.5 * upgrades)

    return int(rent)


def test_calculate_rent():
    property_data = {
        "name": "McKeldin Library",
        "base_rent": 50,
        "group": "North Campus",
        "upgrades": 2
    }

    owner_data = {
        "owned_groups": {"North Campus": 3},
        "group_sizes": {"North Campus": 3}
    }

    result = calculate_rent(property_data, owner_data)
    print("Calculated Rent:", result)


if __name__ == "__main__":
    test_calculate_rent()
