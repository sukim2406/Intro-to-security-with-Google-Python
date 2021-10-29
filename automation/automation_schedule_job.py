from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import pandas as pd
from datetime import datetime

class TestJob:
    @staticmethod
    def run_job():
        s = requests.Session()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': '127.0.0.1',
            'Referer': 'http://127.0.0.1:5000/item_search'
        }

        page_url = "http://127.0.0.1:5000/item_search"
        payload = {"searchText": "tom"}
        response = s.post(page_url, headers=headers, data=payload)

        df_table_list = pd.read_html(response.text)
        df = df_table_list[0]
        print("crawling time: " + str(datetime.now()))
        print("*" * 50)
        print(df)
        print("*"*50)


if __name__ == "__main__":
    schedule = BlockingScheduler(timezone="MST", standalone=True)
    test_job = TestJob()

    schedule.add_job(test_job.run_job, "interval", seconds=5)
    try:
        schedule.start()
    except (KeyboardInterrupt):
        print("Ended")