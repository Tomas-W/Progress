from typing import Final

WEIGHTS_DIR: Final[str] = "images/weights"
CALORIES_DIR: Final[str] = "images/calories"
INSTA_DIR: Final[str] = "images/insta"


def get_weight_months() -> list[tuple[str, str]]:
    """Returns a list of tuples of months with weights."""
    data = [
        ("September", "2025"),
        ("August", "2025"),
        ("July", "2025"),
    ]
    return data


def get_calories_months() -> list[tuple[str, str]]:
    """Returns a list of tuples of months with calories."""
    data = [
        ("September", "2025"),
        ("August", "2025"),
        ("July", "2025"),
    ]
    return data


def get_insta_months() -> list[tuple[str, str]]:
    """Returns a list of tuples of months with insta."""
    data = [
        ("September", "2025"),
    ]
    return data


def get_weight_path(year: str | None, month: str | None) -> str:
    """Returns a weight image path for a given month and year."""
    if month == "last_30":
        path = f"{WEIGHTS_DIR}/weight_last_30.png"
    elif month is None:
        path = f"{WEIGHTS_DIR}/weight.png"
    else:
        path = f"{WEIGHTS_DIR}/weight_{month.lower()}_{year}.png"
    return path


def get_calories_path(year: str | None, month: str | None) -> str:
    """Returns a calories image path for a given month and year."""
    if month == "last_30":
        path = f"{CALORIES_DIR}/calories_last_30.png"
    elif month is None:
        path = f"{CALORIES_DIR}/calories.png"
    else:
        path = f"{CALORIES_DIR}/calories_{month.lower()}_{year}.png"
    return path


def get_insta_paths(year: str | None, month: str | None) -> tuple[str, str, str]:
    """Returns a tuple of insta image paths for a given month and year."""
    if month is None or year is None:
        month, year = get_insta_months()[0]
    
    left = f"{INSTA_DIR}/insta_left_{month.lower()}_{year}.png"
    body = f"{INSTA_DIR}/insta_body_{month.lower()}_{year}.png"
    right = f"{INSTA_DIR}/insta_right_{month.lower()}_{year}.png"
    return left, body, right


def get_weight_title(path: str, month: str | None) -> str:
    """Returns the capitalized month and year from the path."""
    return _get_title(path, month)


def _get_title(path: str, month: str | None) -> str:
    """Returns the capitalized month and year from the path."""
    if month is None:
        return "All"
    if month == "last_30":
        return "Last 30"
    
    path_end = path.split("/")[-1].replace(".png", "")
    month_year = path_end.split("_")[1:]
    return " ".join(month_year).title()


def get_insta_title(year: str | None, month: str | None) -> str:
    """Returns the capitalized month of the insta image path."""
    if month is None or year is None:
        month, year = get_insta_months()[0]
    
    return " ".join([month, year]).title()
