import time
import requests
import csv

def nyt2csv(API, q, begin_date, end_date):
    # Define initial variables
    dates = range(begin_date, end_date)
    output_file = f"{q}_{begin_date}_{end_date}.csv"
    begin_time = time.time()
    retry = True
    n_records = 0
    # Iterate over every date as defined in variable dates
    for x in dates:
        # Set up initial conditions for working through the date
        page = 0
        more = True

        # Check that more is available and then make a request
        while more:
            print(x, page)
            input_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?' \
                        f'q={q}' \
                        f'&api-key={API}' \
                        f'&page={page}' \
                        f'&begin_date={begin_date}' \
                        f'&end_date={end_date}'
            print(input_url)
            r = requests.get(input_url)
            r = r.json()
            # Take a look at what has returned and then process it.
            try:
                docs = r['response']['docs']
                for n in range(len(docs)):
                    raw_date = docs[n]['pub_date']
                    # This date processing is inelegant and should be improved, though it works
                    processed_date = raw_date.split("T")
                    processed_date = processed_date[0]
                    processed_date = processed_date.split("-")
                    date = int(processed_date[0])
                    month = int(processed_date[1])
                    day = int(processed_date[2])
                    url = docs[n]['web_url']
                    abstract = docs[n]['abstract']
                    abstract = f'"{abstract}"'
                    lead = docs[n]['lead_paragraph']
                    lead = f'"{lead}"'
                    headline = docs[n]['headline']['main']
                    headline = f'"{headline}"'
                    desk = docs[n]['news_desk']
                    section = docs[n]['section_name']
                    output = [date, month, day, desk, section, headline, abstract, lead, url]
                    print(output)
                    f = open(output_file, "a", encoding="utf-8")
                    with f:
                        writer = csv.writer(f)
                        writer.writerow(output)
                        n_records += 1
                    # if we made it this far things must be working again so retry is set back to True
                    retry = True
                # Check to see if there are more available pages
                if len(docs) == 10 and page <= 200:
                    page = page + 1
                    more = True
                else:
                    more = False
            # Catch KeyError exception which indicates an error and
            # retry in two minutes if retry is True
            except KeyError:
                print(r['status'])
                if retry:
                    print("Sorry NYT. I will back off for four minutes.")
                    time.sleep(10)
                    # The retry may fail again if you have gone over the daily limit on the API
                    # Retry is thus set to False to prevent constant retrying after that limit is hit
                    # In the future a server based version will simply back off for 24 hours.
                    retry = False
                else:
                    print("Ending script due to error")
                    exit()
            time.sleep(3)
    end_time = time.time()
    run_time = end_time - begin_time
    print(f"Run completed with {n_records} records processed in {run_time} seconds")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("search_word")
    parser.add_argument("begin_date")
    parser.add_argument("end_date")
    args = parser.parse_args()

    with open("nyt_api_key.txt", "r", encoding="utf-8") as f:
        API_key = f.readline()
    Q = str(args.search_word)
    BEGIN_date = int(args.begin_date)
    END_date = int(args.end_date)
    nyt2csv(API_key, Q, BEGIN_date, END_date)
