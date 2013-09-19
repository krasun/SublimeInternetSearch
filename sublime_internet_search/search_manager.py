# for detecting search engines
import inspect 
# for using current module
import sys
# for serialization and deserialization
import pickle
# for path manipulation
import os.path
# for UNIX timestamp 
import time
# for "hashing" filenames`
import hashlib

# search engines 
from .search_engine import GoogleCustomSearchEngine, DuckDuckGoSearchEngine, ConfigurationError as SearchEngineConfiguration
# transport 
from .transport import HTTPSTransport

class ConfigurationError(Exception): 
    pass

class SearchError(Exception):     
    pass 

class SearchManager:
    """Manages search through the Internet"""

    def __init__(self):         
        self.engines = {}
        self.__load_engines()

    def __load_engines(self): 
        self.engines[GoogleCustomSearchEngine.get_alias()] = GoogleCustomSearchEngine()
        self.engines[DuckDuckGoSearchEngine.get_alias()] = DuckDuckGoSearchEngine()
                
    def try_configure(self, settings):         
        try:
            if (settings.get('preferred_search_engine') not in self.engines): 
                raise ConfigurationError('Please, specify available search engine alias: "duck_duck_go" or "google_cse"')

            for engine_key in self.engines: 
                engine = self.engines[engine_key]
                engine.try_configure(settings)
                engine.set_transport(HTTPSTransport())

            self.settings = settings
        except SearchEngineConfiguration as e: 
            raise ConfigurationError(str(e))

    def get_preferred_engine(self): 
        engine_key = self.settings.get('preferred_search_engine')

        return self.engines[engine_key]

    def search(self, query):
        try: 
            cache_ttl = self.settings.get('cache').get('ttl')
            cache_file = os.path.dirname(os.path.realpath(__file__)) + '/../cache/' +  hashlib.sha224(str.encode(query)).hexdigest() + '.pickle'

            if cache_ttl != 0: 
                if os.path.exists(cache_file): 
                    if (time.time() - os.path.getmtime(cache_file)) < cache_ttl: 
                        with open(cache_file, 'rb') as f: 
                            return pickle.load(f)
                    else: 
                        os.remove(cache_file)

            engine = self.get_preferred_engine()
            result = engine.search(query)   

            if cache_ttl != 0: 
                # cache results
                with open(cache_file, 'wb') as f:
                    pickle.dump(result, f) 

            return result
                
        except: 
            raise SearchError('Maybe you have forgotten to configure Google CSE API or API is not available')