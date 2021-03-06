import os

import flask
import flask_sslify

from backend.src.admin.api import admin_api
from backend.src.app.api import app_api

app = flask.Flask(
    __name__,
    static_folder="../../frontend/build/static",
    template_folder="../../frontend/build",
)

# allow slash after endpoint
app.url_map.strict_slashes = False

# force HTTPS
if "DYNO" in os.environ:
    sslify = flask_sslify.SSLify(app)

# register sub-APIs
app.register_blueprint(app_api, url_prefix="/api/app")
app.register_blueprint(admin_api, url_prefix="/api/admin")


@app.route("/api/test")
def api_test():
    return "Server is running! Good luck debugging :O"


@app.route("/assets/<path:path>")
def render_react_asset(path):
    return flask.send_from_directory("../../frontend/build/assets", path)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def render_react(path):
    return flask.send_from_directory("../../frontend/build", "index.html")
