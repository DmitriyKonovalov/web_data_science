from ds_class.ds_class import DataScienceRun
from django.core.files import File
from django.conf import settings
import zipfile
import shutil
import os


class WebDataScienceExecute():
    def __init__(self, analysis):
        self.analysis = analysis

    def execute(self):
        output_dir = os.path.join(settings.MEDIA_ROOT, self.analysis.name)
        download_dir = os.path.join(settings.MEDIA_ROOT, "downloads")
        self.create_dirs(output_dir, download_dir)
        analysis_dict = {'name': self.analysis.name, 'ws': self.analysis.ws, 'ws_start': self.analysis.ws_start,
                         'ws_stop': self.analysis.ws_stop, 'wd': self.analysis.wd, 'wd_step': self.analysis.wd_step,
                         'wd_start': self.analysis.wd_start, 'wd_stop': self.analysis.wd_stop,
                         'file_data': self.analysis.file_data.path}

        ds_runner = DataScienceRun(analysis_dict, output_dir)
        ds_runner.data_science_execute()
        self.packing_zip(output_dir, download_dir, self.analysis.name)

        zip_pack_file = os.path.join(download_dir, f'{self.analysis.name}_pack.zip')
        zip_pack = File(open(zip_pack_file, 'rb'))
        self.analysis.file_zip.save(f'{self.analysis.name}.zip', zip_pack, save=True)
        zip_pack.close()
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, self.analysis.name))
        if os.path.exists(zip_pack_file):
            os.remove(zip_pack_file)

    @staticmethod
    def create_dirs(*dirs):
        for dir in dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)

    @staticmethod
    def packing_zip(from_dir, to_dir, name_zip):

        file_zip_name = os.path.join(to_dir, f'{name_zip}.zip')
        file_zip_name_pack = os.path.join(to_dir, f'{name_zip}_pack.zip')

        if os.path.exists(file_zip_name):
            os.remove(file_zip_name)
        if os.path.exists(file_zip_name_pack):
            os.remove(file_zip_name_pack)

        file_name = file_zip_name_pack
        zip_archive = zipfile.ZipFile(file_name, "w")
        for file in os.listdir(from_dir):
            zip_archive.write(os.path.join(from_dir, file), file)
        zip_archive.close()
        return zip_archive
