from flask import Flask, request, render_template
from hls_runner import *
app = Flask(__name__)


@app.route('/')
def main():
  return render_template('index.html', test_running=False)


@app.route('/start/', methods=['POST'])
def start():

  # Stream Parameters
  url = request.form['url']
  sleep = request.form['request_sleep']
  concurrency = request.form['concurrency']
  live = request.form['live']
  loop = request.form['loop']

  # Authentication Parameters
  auth_url = request.form['auth_url']
  auth_username = request.form['auth_username']
  auth_password = request.form['auth_password']
  auth_type = request.form['auth_type']

  print "Fetching Stream: %s (sleep: %s, concurrency: %s, live: %s, loop: %s)" %(url, sleep, concurrency, live, loop)

  if auth_url:
    authentication = {"url": auth_url, "username": auth_username, "password": auth_password, "type": auth_type}
  else:
    authentication = None

  results, status_codes, response_times, success = get_hls_stream(url, concurrency, live, loop, sleep, authentication)

  return render_template(
           'index.html', test_running=True, 
            playlist_url=url, sleep=sleep, concurrency=concurrency, live=live, loop=loop,
            auth_url=auth_url, auth_username=auth_username, auth_password=auth_password, auth_type=auth_type,
            results=results, status_codes=status_codes, response_times=response_times, success=success
          )


if __name__ == "__main__":
  app.run(debug=True)

