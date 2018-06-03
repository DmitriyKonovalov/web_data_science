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
        analysis_dict = self.analysis.__dict__
        analysis_dict['file_data'] = self.analysis.file_data.path

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
        if os.path.exists(os.path.join(to_dir, f'{name_zip}.zip')):
            os.remove(os.path.join(to_dir, f'{name_zip}.zip'))
        if os.path.exists(os.path.join(to_dir, f'{name_zip}_pack.zip')):
            os.remove(os.path.join(to_dir, f'{name_zip}_pack.zip'))

        file_name = os.path.join(to_dir, f'{name_zip}_pack.zip')
        zip_archive = zipfile.ZipFile(file_name, "w")
        for file in os.listdir(from_dir):
            print(os.path.join(from_dir, file))
            zip_archive.write(os.path.join(from_dir, file), file)
        zip_archive.close()
        return zip_archive
