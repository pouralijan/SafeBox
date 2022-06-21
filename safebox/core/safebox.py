from .partitioner import Partitioner
from .luks import Luks

class SafeBox:
    def __init__(self, block_device_path, passphrase) -> None:
        self.partitioner = Partitioner(block_device_path)
        self.passphrase = passphrase
        self.luks = Luks()
    
    def create(self):
        self.partitioner.create_partition_table("gpt")
        part_path = self.partitioner.create_partition("SafeBoxLuncher", "ext4", "50MB")
        self.luks.mount(part_path, "name")

        # part_path = self.partitioner.create_partition("SafeBox", "ext4", "-1")
        # self.luks.create(part_path, self.passphrase)
        # self.luks.open(part_path, self.passphrase)


        return True