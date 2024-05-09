import time
import redis
from flask import Flask, render_template
import os
from dotenv import load_dotenv

# Connect Redis database via docker-compose.yaml with password
load_dotenv() 
cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379,  password=os.getenv('REDIS_PASSWORD'))
app = Flask(__name__) # Creates the Flask object app that represent the main application
#cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')#will increase the counter 'hits' and then return the increased counter value
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

#python decorator for calling a function via a web request.
@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)

#  checks whether the script is being run directly or imported as a module.
#  If it's being run directly, the following code block will execute.
#starts a web server using the Flask framework.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
