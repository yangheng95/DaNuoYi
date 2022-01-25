# -*- coding: utf-8 -*-
# file: net_utils.py
# time: 2021/8/12
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os

from findfile import find_cwd_dir
from google_drive_downloader import GoogleDriveDownloader as gdd


def download_runtime_materials():
    if not find_cwd_dir('translation_datasets'):
        file_id = '1ZOXg3WMEy_-IGp5pg96-HxRuK8gcmHVY'
        gdd.download_file_from_google_drive(file_id=file_id,
                                            dest_path=os.path.join(os.getcwd(), 'materials.zip'),
                                            unzip=True,
                                            showsize=True)
