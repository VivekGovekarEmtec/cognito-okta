from decimal import Decimal
def convert_to_dpl(price: Decimal):
    """
    This function is used to convert price to DPL
    """
    return price / 100


def convert_to_cpl(price: Decimal):
    """
    This function is used to convert price into CPL
    """
    return price * 100
