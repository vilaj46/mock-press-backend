import fitz
from Google import Create_Service
from googleapiclient.http import MediaFileUpload


class Goggles:
    CLIENT_SECRET_FILE = 'client_secrets.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = {}

    folder_id = '1xjmB6OAWqZuA8dWJP0ATwjcLNAjchsKy'
    file_names = ['resume.pdf']
    mime_types = ['application/pdf']

    file = {}

    def __init__(self, uploaded_file):
        self.service = Create_Service(
            self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)
        self.file = uploaded_file

    # def upload_file(self, file):
        # for file_name, mime_type in zip(file_names, mime_types):
        #     file_metadata = {
        #         'name': file_name,
        #         'parents': [folder_id]
        #     }

    def save_to_drive(self):
        file_name = self.file.filename
        mime_type = self.file.content_type

        # Save file on server
        file_stream = self.file.stream.read()
        doc = fitz.open(stream=file_stream, filetype="pdf")
        doc.save('./tmp/{0}'.format(file_name))
        doc.close()

        # Save the file on google drive.

        media = MediaFileUpload(
            './tmp/{0}'.format(file_name), mimetype=mime_type)
        media = MediaFileUpload(
            './tmp/{0}'.format(file_name), mimetype=mime_type)

        file_metadata = {
            'name': file_name,
            'parents': [self.folder_id]
        }

        self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return file_name
