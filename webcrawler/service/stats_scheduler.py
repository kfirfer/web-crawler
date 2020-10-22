import csv
import threading
import time

from webcrawler.loggings.logger import logger
from webcrawler.repository.sites import get_sites

log = logger(__name__)


def start_print_stats_scheduler():
    thread = threading.Thread(target=scheduler)
    thread.setDaemon(True)
    thread.start()


def scheduler():
    while True:
        try:
            sites = get_sites()
            if len(sites) == 0:
                continue
            with open('mycsvfile.csv', 'w') as f:
                w = csv.writer(f)
                w.writerow(sites[0].keys())
                for site in sites:
                    w.writerow(site.values())
            log.info(sites)
        except Exception as e:
            log.exception(e)
            time.sleep(2)
        finally:
            time.sleep(2)
