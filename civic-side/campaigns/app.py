from .crawler import get_contributions, save_contributions
from .cleanup import clean, merge_candidates, process_contributions
from .stats import zip_stats, chi_stats
from .utils import PAGES_TO_SCRAPE, START, END, ZIP_STRS

# page_file --> raw_data
def run():
    clean_files = []
    for page, raw_data in PAGES_TO_SCRAPE:
        contributions = get_contributions(page)
        save_contributions(contributions, raw_data)
        clean(raw_data)
        clean_files.append(raw_data.split(".")[0] + "_clean.json")
    contributions = merge_candidates(clean_files)
    processed_contributions = process_contributions(contributions, START, END)
    zip_stats(processed_contributions, ZIP_STRS, "campaigns/contributions/stats_by_zip.json")
    chi_stats("campaigns/contributions/stats_by_zip.json", 
              "campaigns/contributions/city_stats.json")
