#Import the important libraries 
import scrapy
import csv
import re
import pandas as pd
import time
import json
import requests

# setting a name for the spider 
class DataSpider(scrapy.Spider):
    name = 'data_spider'

    custom_settings = {
        'DOWNLOAD_DELAY': 1  # Set a delay of 1 second between requests
    }

    # Initialize the spider and set the initial list of URLs to crawl
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = []

    # this will Generate the initial requests to start crawling
    def start_requests(self):
        # the doi which we have stored in csv will be read 
        df = pd.read_csv('/content/myproject/myproject/spiders/doi_metadata.csv')
        dois = df['DOI'].tolist()

        # third party openalex will yield the data thorugh url 
        for doi in dois:
            url = f'https://api.openalex.org/works/https://doi.org/{doi}'
            yield scrapy.Request(url=url, callback=self.parse, meta={'doi': doi})

    # Parse the response from the API
    def parse(self, response):
        # Parse the JSON response from the API
        data = json.loads(response.body)

        # Extract various data fields from the JSON response
        doi = data.get('doi', '')
        title = data.get('title', '')
        publication_date = data.get('publication_date', '')

        # Extract year, month, and day from the publication date
        year, month, day = self.extract_date_parts(publication_date)

        # Extract and preprocess the abstract from the JSON response
        abstract_inverted_index = data.get('abstract_inverted_index', {})
        abstract = self.extract_abstract(abstract_inverted_index)

        # Extract authorship information
        authorships = []
        for authorship in data.get('authorships', []):
            author_name = authorship.get('author', {}).get('display_name', '')
            author_affiliations = []
            for institution in authorship.get('institutions', []):
                affiliation = institution.get('display_name', '')
                author_affiliations.append(affiliation)
            authorship_info = {'author': author_name, 'affiliations': ', '.join(author_affiliations)}
            authorships.append(authorship_info)

        # If affiliations are missing for authors, try to fetch from Crossref API
        if any(not authorship['affiliations'] for authorship in authorships):
            crossref_doi = response.meta['doi']
            crossref_url = f'https://api.crossref.org/v1/works/{crossref_doi}'
            crossref_response = requests.get(crossref_url)
            crossref_data = crossref_response.json()

            # Extract the missing affiliations from Crossref response
            if crossref_response.status_code == 200 and 'message' in crossref_data:
                crossref_authors = crossref_data['message'].get('author', [])
                for i, authorship in enumerate(authorships):
                    if not authorship['affiliations']:
                        crossref_author = crossref_authors[i] if i < len(crossref_authors) else None
                        if crossref_author:
                            affiliations = crossref_author.get('affiliation', [])
                            author_affiliations = [aff.get('name', '') for aff in affiliations]
                            authorships[i]['affiliations'] = ', '.join(author_affiliations)

        # Extract additional information from the JSON response
        ids = data.get('ids', {})
        openalex_id = ids.get('openalex', '')
        language = data.get('language', '')
        primary_location = data.get('primary_location', {})
        is_oa = primary_location.get('is_oa', False)
        landing_page_url = primary_location.get('landing_page_url', '')
        pdf_url = primary_location.get('pdf_url', '')
        source = primary_location.get('source', {})
        source_id = source.get('id', '')
        source_display_name = source.get('display_name', '')
        conference_type = source.get('type', '')
        open_access = data.get('open_access', {})
        oa_status = open_access.get('oa_status', '')
        oa_url = open_access.get('oa_url', '')
        cited_by_count = data.get('cited_by_count', 0)

        # Extract concepts from the JSON response
        concepts = [concept.get('display_name', '') for concept in data.get('concepts', [])]

        # Write the extracted data to a CSV file
        with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(
                    ['DOI', 'Title', 'Publication Year', 'Publication Month', 'Publication Day', 'Abstract',
                     'Author Name and Affiliation', 'OpenAlex ID', 'Language', 'Is Open Access', 'Landing Page URL',
                     'PDF URL', 'Source ID', 'Source Display Name', 'Conference Type', 'OA Status', 'OA URL',
                     'Cited By Count', 'Concepts'])
            writer.writerow(
                [doi, title, year, month, day, abstract, '|'.join(
                    [f"{author['author']} ({author['affiliations']})" for author in authorships]),
                 openalex_id, language, is_oa, landing_page_url, pdf_url, source_id, source_display_name,
                 conference_type, oa_status, oa_url, cited_by_count, '|'.join(concepts)])

        # Log a message indicating that the data has been saved
        self.log('Data saved in output.csv')

        # Delay for 1 second before making the next request to be polite to the server
        time.sleep(1)

    # Static method to extract year, month, and day from a publication date string
    @staticmethod
    def extract_date_parts(publication_date):
        # Extract year, month, and day from the publication date
        if publication_date:
            date_parts = publication_date.split('-')
            if len(date_parts) == 3:
                return date_parts
        return '', '', ''

    # Static method to extract and preprocess the abstract
    @staticmethod
    def extract_abstract(abstract_inverted_index):
        abstract_words = []
        for word, indices in abstract_inverted_index.items():
            for index in indices:
                abstract_words.append((index, word))
        abstract_words.sort(key=lambda x: x[0])
        abstract = ' '.join([word for _, word in abstract_words])
        abstract = re.sub(r'([^\w\s])\s+', r'\1', abstract)
        return abstract
