import http.server
import socketserver
import http.client
from urllib.parse import urlparse

PORT = 8000

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':
            # Fetch the Time.com homepage using http.client
            parsed_url = urlparse('https://time.com')
            conn = http.client.HTTPSConnection(parsed_url.netloc)
            conn.request("GET", parsed_url.path)
            response = conn.getresponse()
            html_content = response.read().decode('utf-8')
            conn.close()
            
            # Extract stories (simple parsing approach)
            stories = []
            start_index = html_content.find('<h3 class="headline">')
            while start_index != -1 and len(stories) < 6:
                end_index = html_content.find('</h3>', start_index)
                title = html_content[start_index:end_index].split('>')[1].strip()
                
                # Extract the link for the story
                link_start = html_content.find('href="', start_index)
                link_end = html_content.find('"', link_start + 6)
                link = html_content[link_start + 6:link_end]
                
                stories.append({"title": title, "link": link})
                
                # Move to the next story
                start_index = html_content.find('<h3 class="headline">', end_index)

            # Prepare JSON response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(str(stories).replace("'", '"'), 'utf-8'))

# Set up the server
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()