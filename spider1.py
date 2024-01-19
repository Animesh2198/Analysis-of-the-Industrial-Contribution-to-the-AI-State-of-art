import scrapy
import csv
import json
import io

class ICRAConferenceSpider(scrapy.Spider):
    # we will Set the spiders name which is used to run it.
    name = "DOI"

    # the spider will crawl the below given start urls for instance we have given below urls 
    start_urls = [
        "https://dblp.org/search/publ/api?q=toc%3Adb/conf/aaai/aaai2022.bht%3A&h=2000&format=json",
        "https://dblp.org/search/publ/api?q=toc%3Adb/conf/ijcai/ijcai2022.bht%3A&h=1000&format=json",
        "https://dblp.org/search/publ/api?q=toc%3Adb/conf/icra/icra2022.bht%3A&h=1000&format=json"
    ]

    def parse(self, response):
        # scrapy will parse the json response 
        data = json.loads(response.body.decode('utf-8'))

        # it will extract all the metadata present in the json 
        metadata = data.get('result', {}).get('hits', {}).get('hit', [])

        # this will check if the doi is present or not 
        doi_present = any('doi' in item['info'] for item in metadata)

        # it will store the dois and urls in dedicated csv files
        if doi_present:
            filename = 'doi_metadata.csv'
            fieldnames = ['DOI']
        else:
            filename = 'url_metadata.csv'
            fieldnames = ['URL']

        # this will allow to write the data in csv files. 
        with io.open(filename, 'a', newline='', encoding='utf-8', errors='replace') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if doi_present:
                writer.writeheader()

            rows = []
            # Iterate through the metadata and extract either DOIs or URLs.
            for item in metadata:
                if doi_present and 'doi' in item['info']:
                    doi = item['info'].get('doi', '')

                    # Create a row for DOI data.
                    row_data = {
                        'DOI': doi,
                    }

                    rows.append(row_data)
                elif not doi_present:
                    url = item['info'].get('ee', '')

                    # Create a row for URL data.
                    row_data = {
                        'URL': url,
                    }

                    rows.append(row_data)

            # Write the rows to the CSV file.
            writer.writerows(rows)

        # Log the filename where the metadata is saved.
        self.log("Metadata saved to: {}".format(filename))
