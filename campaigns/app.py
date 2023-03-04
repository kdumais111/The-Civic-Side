from .crawler import get_contributions, save_contributions
from .utils import SAVED_PAGES

def run():
    for page, destination in SAVED_PAGES:
        contributions = get_contributions(page)
        save_contributions(contributions, destination)

    print("It worked!")
