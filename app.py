from flask import Flask, render_template
app = Flask(__name__)

import jinja2
import tools
import wiki
import random

@app.route("/")
def hello():
    events = wiki.get_events_cached()
    return render_template('template.html', entry=random.choice(events), count=len(events)) # "Hello World!"

@app.template_filter()
def render_event(val): return tools.render_event(val)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
