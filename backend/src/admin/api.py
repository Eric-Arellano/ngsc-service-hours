import flask

from backend.src.drive_commands import copy, create, move, remove, rename

admin_api = flask.Blueprint('admin_api', __name__)


@admin_api.route('/test')
def api_test():
    """
    Throw away text connecting google drive api
    """
    return 'Testing admin api'


@admin_api.route('/copy/file', methods=['POST'])
def api_copy_file():
    data = flask.request.get_json()
    copy.file(data)


@admin_api.route('/copy/folder', methods=['POST'])
def api_copy_folder():
    data = flask.request.get_json()
    copy.folder(data)


@admin_api.route('/create/file', methods=['POST'])
def api_create_file():
    data = flask.request.get_json()
    create.file(data)


@admin_api.route('/create/folder', methods=['POST'])
def api_create_folder():
    data = flask.request.get_json()
    return create.folder(data)


@admin_api.route('/move/file', methods=['POST'])
def api_move_file():
    data = flask.request.get_json()
    move.file(data)


@admin_api.route('/move/folder', methods=['POST'])
def api_move_folder():
    data = flask.request.get_json()
    move.folder(data)


@admin_api.route('/rename/file', methods=['POST'])
def api_rename_file():
    data = flask.request.get_json()
    rename.file(data)


@admin_api.route('/rename/folder', methods=['POST'])
def api_rename_folder():
    data = flask.request.get_json()
    rename.folder(data)


@admin_api.route('/remove/file', methods=['POST'])
def api_remove_file():
    data = flask.request.get_json()
    remove.file(data)


@admin_api.route('/remove/folder', methods=['POST'])
def api_remove_folder():
    data = flask.request.get_json()
    remove.folder(data)