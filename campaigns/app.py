from .crawler import get_contributions, save_contributions
from .cleanup import clean, merge_candidates, process_contributions
from .stats import zip_stats, chi_stats
from .utils import SAVED_PAGES, START, END, ZIP_STRS

def run():
    clean_files = []
    for page, page_file in SAVED_PAGES:
        contributions = get_contributions(page)
        save_contributions(contributions, page_file)
        clean(page_file)
        clean_files.append(page_file.split(".")[0] + "-clean.json")
    contributions = merge_candidates(clean_files)
    processed_contributions = process_contributions(contributions, START, END)
    zip_stats(process_contributions, ZIP_STRS, "stats-by-zip.json") # TODO: Update file name / path
    chi_stats("stats-by-zip.json", "citywide-stats.json") # TODO: Update file name / path

