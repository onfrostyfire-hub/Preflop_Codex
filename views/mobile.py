import utils

def show():
    ranges_db = utils.load_ranges()
    utils.choose_task(ranges_db, view_name="Mobile")
