import subprocess
import parted
import os

class Partitioner:
    def __init__(self, block_device_path):
        self.block_device_path = block_device_path
        # self.disk = parted.getDevice(block_device_path)
        self.device = parted.Device(block_device_path)
        self.disk = None
        self._first_free_sector = None

        # self.umount(block_device_path)
    
    @property
    def first_free_sector(self):
        if self._first_free_sector is None:
            self._first_free_sector = 1
        return self._first_free_sector
    def is_mounted(self, path):
        with open("/proc/mounts", "r") as mounts:
            if  path in mounts.read():
                return True
            return False
    def check_for_mount(self, block_device_path):
        print("Checking for mounted partitions.")
        path = "/dev/"
        dev_name = block_device_path.split("/")[-1]
        dev_name = [f"{file}" for file in os.listdir(path) if file.startswith(dev_name)]
        print(dev_name)
        for device in dev_name:
            dev_path = f"{path}{device}"
            print(dev_path)
            if self.is_mounted(dev_path):
                print(f"Device: {dev_path} is mounted. Try to Umount it.")

                self.umount(f"{dev_path}")


    def umount(self, partition_path):
        print(f"Umounting {partition_path}")
        command = [
            "umount",
            f"{partition_path}"
        ]
        print(command)
        subprocess.check_output(command)
        return True

    def create_partition_table(self, partition_table_type):
        self.check_for_mount(self.block_device_path)
        print(f"Creating partition table {partition_table_type}")
        self.disk = parted.freshDisk(self.device, partition_table_type)
        res = self.disk.commit()
        print(res)

    def create_partition(self,name,partition_type, size):
        
        print(f"Creating partition {partition_type} {size}")
        if self.device.busy:
            print("Disk is busy")

        # TODO: Add logger ...
        # print(f"FirstSector: {self.first_free_sector} length: {self.device.getLength()}")
        if self.first_free_sector >= self.device.getLength():
            print("No free sectors")

        start_sector = self.first_free_sector
        if size == "-1":
            end_sector = start_sector + self.device.getLength() - 1
        else:
            # TODO: I don't know why I did multiply by 2 here.
            end_sector = start_sector + self.to_size(size) * 2

        if end_sector >= self.device.getLength() - 1:
            end_sector = self.device.getLength() - 1

        # TODO: Add logger ...
        # print(f"Sector size: {self.device.sectorSize}")
        length = end_sector - start_sector

        # TODO: Add logger ...
        # print(f"From: {start_sector} to {end_sector} with size: {size}, length: {length}")
        geometry = parted.Geometry(device=self.device, start=start_sector, length=length)
        filesystem = parted.FileSystem(type=partition_type, geometry=geometry)
        partition = parted.Partition(disk=self.disk, type=parted.PARTITION_NORMAL, geometry=geometry, fs=filesystem)
        partition.set_name(name)
        self.disk.addPartition(partition=partition, constraint=self.device.optimalAlignedConstraint)

        self._first_free_sector = end_sector
        self.commit()
        self.mkfs(partition.path, partition_type)
        return partition.path

    def commit(self):
        self.disk.commit()
    
    def mkfs(self, partition_path, filesystem_type):
        print(f"Formatting the {partition_path} by {filesystem_type}")
        command = [
            f"mkfs.{filesystem_type}",
            f"{partition_path}"
        ]
        print(command)
        subprocess.check_output(command)
        print("Formatting done")
        return True
         
    def to_size(self, size):
        if size.endswith("MB"):
            return int(size[:-2]) * 2 ** 10
        elif size.endswith("GB"):
            return int(size[:-2]) * 2 ** 20
        elif size.endswith("TB"):
            return int(size[:-2]) * 2 ** 30
        elif size.endswith("PB"):
            return int(size[:-2]) * 2 ** 40
        elif size.endswith("EB"):
            return int(size[:-2]) * 2 ** 50
        else:
            return int(size)
            
    def size(self):
        self.device.removeFromCache()
        if self.device.getSize() < 2 ** 10:
            return f"{self.device.getSize():.2f} MB"
        elif self.device.getSize() < 2 ** 20:
            return f"{self.device.getSize() / 2 ** 10:.2f} GB"
        elif self.device.getSize() < 2 ** 30:
            return f"{self.device.getSize() / 2 ** 20:.2f} TB"
        elif self.device.getSize < 2 ** 40:
            return f"{self.device.getSize() / 2 ** 30:.2f} PB"
        else:
            return f"{self.device.getSize() / 2 ** 40:.2f} EB"