def total(lines):
    """Order total in dollars. Each line is (unit_price, quantity)."""
    return sum(price * quantity for price, quantity in lines)
