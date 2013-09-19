# for building HTTP URL parameter`s string
from urllib.parse import urlencode
# for processing search results
import json 

class ConfigurationError(Exception):
    pass

class SearchResultItem: 
    """For search result encapsulation"""

    def __init__(self, title, url, description): 
        self.title = title
        self.url = url
        self.description = description

class SearchEngine: 
    """Search engine abstraction"""

    @staticmethod
    def get_alias():
        """Must return search engine alias"""
        pass

    def try_configure(self, settings): 
        """ Allows to configure search engine"""
        pass

    def search(self, query): 
        """Allows to search throught the Internet"""
        pass

    def set_transport(self, transport): 
        """Sets transport for making HTTPS requests"""
        
        self.transport = transport

class GoogleCustomSearchEngine(SearchEngine):
    """Search engine that uses Google Custom Search Engine API"""
            
    @staticmethod
    def get_alias():        
        return "google_cse"

    def try_configure(self, settings): 
        settings = settings.get(self.get_alias())
        if not ('developer_key' in settings and 'engine_id' in settings): 
            raise ConfigurationError('Google CSE API requires developer key and engine id')
        
        self.settings = settings

    def search(self, query): 
        """Allows to search throught the Internet"""

        url = 'https://www.googleapis.com/customsearch/v1?' + urlencode({ 
            'alt' : 'json',
            'key': self.settings.get('developer_key'),
            'cx': self.settings.get('engine_id'), 
            'q': query
        })

        result = json.loads(self.transport.get(url))

        items = []
        for item in result['items']:
            items.append(SearchResultItem(item['title'], item['link'], item['snippet']))

        return items

class DuckDuckGoSearchEngine(SearchEngine): 
    """Search engine that uses DuckDuckGo API"""

    def get_alias():        
        return "duck_duck_go"

    def search(self, query): 
        """Allows to search throught the Internet"""
        
        url = 'https://api.duckduckgo.com/?' + urlencode({ 
            'format' : 'json',            
            'q': query, 
            'no_html': 1
        })

        result = json.loads(self.transport.get(url))
        
        items = []
        for item in result['RelatedTopics']:
            if 'Topics' in item: 
                for nestedItem in item['Topics']:
                    items.append(SearchResultItem(nestedItem['Text'], nestedItem['FirstURL'], nestedItem['Text']))    
            else:
                items.append(SearchResultItem(item['Text'], item['FirstURL'], item['Text']))

        return items