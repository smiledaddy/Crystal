# -*- coding: utf-8 -*-
import requests
import hashlib
import json
import logging

_LOGGER = logging.getLogger(__name__)

class FileTransfer(object):
    """ file transfer class
    provide `upload` function to upload file to file server 
    provide `get_url` function to get file url from file server
    """

    _FILE_SERVER_HOST = 'http://file.dahuo.la'
    _START_API = '/api/1.0/file/upload/start'
    _UPLOAD_API = '/api/1.0/file/upload/sessions/'
    _GET_URL_API = '/api/1.0/file/maintain/url'

    _HTTP_HEADER = {
        'X_App_Key': 'kaopu',
        'X_Auth_Token': 'e778530f-fda3-43e5-8246-3352e93aa55b'
    }

    def __init__(self, file_path):
        self._file_obj = open(file_path, 'rb').read()
        self.guid = None
        self.session_id = None
        self.storage_key = None
        self.url = None

    def start(self): 
        self.__start_session()
        self.url = FileTransfer.get_url(self.storage_key)
        return (self.guid, self.url)

    def get_guid(self):
        return self.guid

    @staticmethod
    def get_url(storage_key):
        get_url = FileTransfer._FILE_SERVER_HOST + FileTransfer._GET_URL_API
        data = 'storagekey=%s&preview_size=%d' % (storage_key, 0)
        download_url = None 
        try:
            response = requests.post(get_url, data=data,
                                     headers=FileTransfer._HTTP_HEADER)
            response_obj = json.loads(response.text)
            if int(response_obj.get('err')) == 0:
                resp = response_obj['resp']
                download_url = resp['download_url']
        except Exception as e:
            _LOGGER.error("FileTransfer, get_url error, %s" % e)
            print "FileTransfer, get_url error, %s" % e

        return download_url
            

    def __start_session(self):
        start_url = FileTransfer._FILE_SERVER_HOST + FileTransfer._START_API
        data = 'md5='+self.__md5_sum()
        try:
            response = requests.post(start_url, data=data,
                                     headers=FileTransfer._HTTP_HEADER)
            response_obj = json.loads(response.text)
            if int(response_obj.get('err')) == 0:
                resp = response_obj['resp']
                if resp.get('guid'):
                    # has uploaded
                    self.guid = resp['guid']
                    self.storage_key = resp['storagekey']
                else:
                    self.session_id = resp['session_id']
                    self.__upload_file()

        except Exception as e:
            _LOGGER.error("FileTransfer, __start_session error, %s" % e)
            print "FileTransfer, __start_session error, %s" % e
    
    def __upload_file(self):
        upload_url = FileTransfer._FILE_SERVER_HOST +\
                     FileTransfer._UPLOAD_API + self.session_id
        try:
            response = requests.post(upload_url, data=self._file_obj,
                                     headers=FileTransfer._HTTP_HEADER)
            response_obj = json.loads(response.text)
            if int(response_obj.get('err')) == 0:
                resp = response_obj['resp']
                self.guid = resp['guid']
                self.storage_key = resp['storagekey']
        except Exception as e:
            _LOGGER.error("FileTransfer, __upload_file error, %s" % e)
            print "FileTransfer, __upload_file error, %s" % e

    def __md5_sum(self):
        return hashlib.md5(self._file_obj).hexdigest()


if __name__ == "__main__":
    file_path = '/root/dolphin.com222.png'
    file_transfer = FileTransfer(file_path)
    (guid, url) = file_transfer.start()
    print (guid, url)
