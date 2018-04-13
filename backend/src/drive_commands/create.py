"""
Create an empty file or folder into the specified targets.
"""

from backend.src.data import folder_ids
from backend.src.google_apis import drive_api

FileID = str


def file(file_name: str, *,
         mime_type: str,
         parent_folder_id: FileID = folder_ids.drive_playground) -> FileID:
    """
    Create an empty file.
    """
    return _create_resource(name=file_name, mime_type=mime_type, parent_folder_id=parent_folder_id)


def folder(folder_name: str, *,
           parent_folder_id: FileID = folder_ids.drive_playground) -> FileID:
    """
    Create an empty folder.
    """
    return _create_resource(name=folder_name, mime_type='folder', parent_folder_id=parent_folder_id)


def _create_resource(name: str,
                     mime_type: str,
                     parent_folder_id: FileID) -> FileID:
    """
    Create Google Drive file with specific MIME type.
    """
    service = drive_api.build_service()
    file_metadata = {
        'name': name,
        'mimeType': f'application/vnd.google-apps.{mime_type}',
        'parents': [parent_folder_id]
    }
    resource = service \
        .files() \
        .create(body=file_metadata, fields='id') \
        .execute()
    return resource.get('id')
