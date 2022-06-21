import pathlib
import subprocess


class Luks:
    def __init__(self):
        pass

    def create(self, block_device_path, passphrase):
        print("Formatting ...")
        key_file = pathlib.Path("/tmp/key")
        
        key_file.write_text(passphrase)
        
        command = [
            'cryptsetup',
            '--batch-mode',
            'luksFormat',
            f'--key-file={str(key_file)}',
            block_device_path,
            '--verbose',
        ]
        print(command)
        subprocess.check_output(command)
    
    def open(self, block_device_path, passphrase):
        print("Opening ...")
        key_file = pathlib.Path("/tmp/key")
        key_file.write_text(passphrase)
        
        command = [
            'cryptsetup',
            '--batch-mode',
            'luksOpen',
            f'--key-file={str(key_file)}',
            block_device_path,
            "golabi",
            '--verbose',
        ]
        print(command)
        subprocess.check_output(command)
    def mount(self, source_path, name):
        '''
        /dev/sde1 on /run/media/hassan/Ventoy
        type fuseblk
        (rw,nosuid,nodev,relatime,user_id=0,group_id=0,default_permissions,
        allow_other,blksize=4096,uhelper=udisks2)
        ''' 
        import os
        mount_point = pathlib.Path(f"/run/media/{os.getlogin()}/{name}")
        if not mount_point.exists():
            mount_point.mkdir(parents=True)
        command = [
            'mount',
            '-o rw,nosuid,nodev,relatime,user_id=0,group_id=0,default_permissions,allow_other,uhelper=udisks2',
            source_path,
            str(mount_point)
        ]
        print(command)
        subprocess.check_output(command)
    def close(self):
        pass