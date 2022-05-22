import json, os, requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class CoinMarketCap:
    __API_URL_BASE = 'https://pro-api.coinmarketcap.com/'
    __API_KEY = os.getenv("CMC_PRO_API_KEY")

    def __init__(self, api_base_url=__API_URL_BASE, api_key=__API_KEY):
        self.api_base_url = api_base_url
        self.request_timeout = 120

        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.headers.update({'X-CMC_PRO_API_KEY': api_key})

    def __request(self, url):
        # print(url)
        try:
            response = self.session.get(url, timeout=self.request_timeout)
        except requests.exceptions.RequestException:
            raise

        try:
            response.raise_for_status()
            content = json.loads(response.content.decode('utf-8'))
            return content
        except Exception as e:
            # check if json (with error message) is returned
            try:
                content = json.loads(response.content.decode('utf-8'))
                raise ValueError(content)
            # if no json
            except json.decoder.JSONDecodeError:
                pass

            raise

    def key_info(self):
        """Get key info about CMC API account"""

        api_url = '{0}v1/key/info'.format(self.api_base_url)
        return self.__request(api_url)

    def list_listing(self):
        api_url = '{0}v1/cryptocurrency/listings/latest'.format(self.api_base_url)
        # api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url)
