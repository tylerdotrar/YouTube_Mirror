import urllib.request, re, argparse
from flask import Flask, request, redirect, url_for

class localFlask(Flask):
    def process_response(self, response):
        #Every response will be processed here first
        response.headers['server'] = 'nginx'
        return(response)

app = localFlask(__name__)

# HOME PAGE
@app.route('/search', methods=['GET','POST'])
def homepage():
    if request.method == 'GET':
        return """
        <body>
          <form method="POST">
            <div class="header" style="background-color: #ddd">
              <h1 align="center">HOPEFULLY THIS WORKS</h1>
            </div>
            <div class="formcontainer">
            <hr/>
            <div class="container" align="center">
              <h2>Search for Videos:</h2>
              <input type="text" placeholder="ugly websites 101" name="search" required>
              <button type="submit">Submit</button>
            </div>
          </form>
        </body>
        """
    elif request.method == 'POST':
        user_input = request.form['search']
        refined = user_input.replace(' ',"+")
        return redirect(f'/arbitrary_backend/search/{refined}')

# SEARCH FOR VIDEOS
@app.route('/arbitrary_backend/search/<string:yt_query>')
def search_page(yt_query):
    search = "https://www.youtube.com/results?search_query=" + yt_query
    pretty_search = yt_query.replace('+',' ')

    html = urllib.request.urlopen(search)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    
    message = f"""
    <div class="header" style="background-color: #ddd">
      <h1 align="center">Query: "{pretty_search}"</h1>
    </div>
    <h2 align="center">Top 10 Results:</h2>
    <p align="center">
    """

    for x in range(10):
        new_line = f'[{x}] <a href="/arbitrary_backend/watch/{video_ids[x]}" ><button class=grey style="height:40;width:300px">{video_ids[x]}</button></a><br>'
        message = '\n'.join([message,new_line])

    return '\n'.join([message,'<p align="center">'])


# PLAY EMBEDDED VIDEO
@app.route('/arbitrary_backend/watch/<string:video_id>')
def watch_video(video_id):
    return f"""
    <div class="header" style="background-color: #ddd">
        <h1 align="center">Enjoy stranger.</h1>
    </div>
    <br><br>
    <div align="center">
        <iframe src="https://invidiou.site/embed/{video_id}" width="853" height="480" frameborder="0" allowfullscreen></iframe>
    </div>
    """

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=54321, type=int)
    parser.add_argument('--ssl', action='store_const', const='adhoc', default=None)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, ssl_context=args.ssl, debug=args.debug, use_reloader=True)