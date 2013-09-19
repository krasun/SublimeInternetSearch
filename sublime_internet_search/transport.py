# for parsing HTTP URL parameter`s string
from urllib.parse import urlparse
# for using CLI HTTP requests
import os
# for HTTP requests which support SSL
import http.client

class HTTPSTransport: 
    """Provides transport for HTTPS requests"""

    def get(self, url): 
        """Makes response and return full content"""
        
        content = ""
        if hasattr(http.client, "HTTPSConnection"):             
            url_options = urlparse(url)

            conn = http.client.HTTPSConnection(url_options.netloc)
            conn.request('GET', url_options.path + '?' + url_options.query)
            content = conn.getresponse().read().decode('utf-8')
            conn.close()
        else: 
            p = os.popen('curl -k "' + url + '"')
            content = p.read()
            p.close()        

        return content
        