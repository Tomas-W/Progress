import os

from datetime import datetime

from utils.config import CFG


def get_image_path(year: str | None, month: str | None, dir: str) -> str:
    """Returns a weight image path for a given month and year."""
    type = dir.split("/")[-1]
    if month == "last_30":
        path = f"{dir}/{type}_last_30.png"
    elif month is None:
        path = f"{dir}/{type}.png"
    else:
        path = f"{dir}/{type}_{month.lower()}_{year}.png"
    return path


def get_insta_paths(year: str | None, month: str | None) -> tuple[str, str, str, str]:
    """Returns a tuple of insta image paths for a given month and year."""
    if month is None or year is None:
        month, year = get_insta_months_from_path(CFG.dir.INSTA)[0]
    
    left = f"{CFG.dir.INSTA_REL}/insta_left_{month.lower()}_{year}.png"
    back = f"{CFG.dir.INSTA_REL}/insta_back_{month.lower()}_{year}.png"
    front = f"{CFG.dir.INSTA_REL}/insta_front_{month.lower()}_{year}.png"
    right = f"{CFG.dir.INSTA_REL}/insta_right_{month.lower()}_{year}.png"
    return left, back, front, right


def get_title(path: str, month: str | None) -> str:
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
        month, year = get_insta_months_from_path(CFG.dir.INSTA)[0]
    
    return " ".join([month, year]).title()


def get_file_data(names: list[str]) -> list[tuple[str, datetime]]:
    """Returns a list of tuples of names and dates from the path."""
    file_data = []
    for name in names:
        parts = name.split("_")
        # Filter all and last_30
        if len(parts) > 2 and "last_30" not in name:
            month, year = parts[1], parts[2]
            # Make datetime for sorting
            date = datetime.strptime(f"{month} {year}", "%B %Y")
            file_data.append((name, date))
    return file_data


def get_months_from_path(path: str) -> list[tuple[str, str]]:
    """Returns a list of tuples of names from the path, sorted by date (newest first)."""
    file_names = [file.replace(".png", "") for file in os.listdir(path)]
    file_data = get_file_data(file_names)
    # Sort newest first
    file_data.sort(key=lambda x: x[1], reverse=True)
    # Format names to (month, year)
    names = [(name.split("_")[1].title(), name.split("_")[2]) 
            for name, _ in file_data]
    return names


def get_insta_file_data(names: list[str]) -> list[tuple[str, datetime]]:
    """Returns a list of tuples of names and dates from the path."""
    file_data = []
    for name in names:
        parts = name.split("_")
        month, year = parts[2], parts[3]
        # Make datetime for sorting
        date = datetime.strptime(f"{month} {year}", "%B %Y")
        file_data.append((name, date))
    return file_data


def get_insta_months_from_path(path: str) -> list[tuple[str, str]]:
    """Returns a list of tuples of names from the path, sorted by date (newest first)."""
    file_names = [file.replace(".png", "") for file in os.listdir(path)]
    file_data = get_insta_file_data(file_names)
    # Sort newest first
    file_data.sort(key=lambda x: x[1], reverse=True)
    # Format names to (month, year) and remove duplicates
    names = list(set([(name.split("_")[2].title(), name.split("_")[3]) 
            for name, _ in file_data]))
    return names
