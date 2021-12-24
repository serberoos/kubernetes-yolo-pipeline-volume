from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

path_dir = '/usr/src/app/yolo_pipeline_volume/detect_result'

class GoogleDrive():
    def __init__(self):
        '''
        인증 정보를 설정하는 부분
        '''
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
                'https://www.googleapis.com/auth/drive.file']

        creds = service_account.Credentials.from_service_account_file('/usr/src/app/yolo_pipeline_volume/airflow-yolo-gdrive-9cba51135bc8.json',
                                                                    scopes=SCOPES)
        # return Google Drive API service
        self.gdrive = build('drive', 'v3', credentials=creds)


    def upload_files(self, folder_id='1iZyfcksah0R3jaWpUcBcHZ4oS-HLu3Q4', file='/usr/src/app/yolo_pipeline_volume/detect_result/mask.mp4'):
        '''
        folder_id 를 갖는 폴더에 file 을 Google Drive 에 업로드 함
        '''
        service = self.gdrive
        print("Folder ID:", folder_id)
        # upload a file text file
        # first, define file metadata, such as the name and the parent folder ID
        file_metadata = {
            "name": file,
            "parents": [folder_id]
        }
        # upload
        media = MediaFileUpload(file, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("File created, id:", file.get("id"))



google_drive = GoogleDrive()

file_list = os.listdir(path_dir)

for result_file in file_list:
    google_drive.upload_files(file=f'/usr/src/app/yolo_pipeline_volume/detect_result/{result_file}')
