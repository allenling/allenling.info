# coding=utf-8
from __future__ import unicode_literals
import os
import zipfile
import shutil


def compress_dir(target_file, dir_path):
    f = zipfile.ZipFile(str(target_file), "w", compression=zipfile.ZIP_DEFLATED)
    dir_path = str(dir_path.replace("\\", "/"))
    start = len(dir_path)
    filelist = []
    _get_file_list(dir_path, filelist)
    zipfilelist = [filename[start:] for filename in filelist]
    for i in range(len(filelist)):
        f.write(filelist[i], zipfilelist[i])
    f.close()


def _get_file_list(dir_path, filelist):
    for filename in os.listdir(dir_path):
        filename = "/".join([dir_path, filename])
        if os.path.isfile(filename):
            if filename.endswith('.pyc'):
                filelist.append(str(filename))
        elif os.path.isdir(filename):
            _get_file_list(filename, filelist)
        else:
            raise IOError("Unknow error %s!" % filename)


if __name__ == '__main__':
    _cur_dir = os.path.dirname(os.path.abspath(__file__))
    _project_dir = os.path.dirname(_cur_dir)
    celery_name = [filename for filename in os.listdir(_project_dir) if filename.endswith("_celery") and not filename.startswith('.') and os.path.isdir(os.path.join(_project_dir, filename))][0]
    tmp_dir = os.path.join(_cur_dir, 'tmp')
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    src_dir = os.path.join(os.path.dirname(_cur_dir), celery_name)
    target_dir = os.path.join(tmp_dir, celery_name)
    os.mkdir(target_dir)
    open(os.path.join(target_dir, '__init__.py'), 'w').close()
    shutil.copy(os.path.join(src_dir, 'celery.py'), os.path.join(target_dir, 'celery.py'))
    shutil.copy(os.path.join(src_dir, 'celeryconfig.py'), os.path.join(target_dir, 'celeryconfig.py'))
    shutil.copy(os.path.join(_cur_dir, 'tasks_client_template.py'), os.path.join(target_dir, 'tasks.py'))
    import compileall
    compileall.compile_dir(target_dir)
    compress_dir(os.path.join(_cur_dir, '%s.py.zip' % celery_name), tmp_dir)
    shutil.rmtree(tmp_dir)
