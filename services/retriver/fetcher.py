from pathlib import Path
import os.path
from datetime import datetime

class Fetcher:
    def time_convert(self, time: float) -> datetime:
        """
        Convert time from float to datetime.
        """
        newtime = datetime.fromtimestamp(time)
        return newtime
    
    def size_format(self, size: int):
        """
        Convert file size from int to string.
        """
        newform = format(size/1024, ".2f")
        return newform + " KB"

    def get_meta_data(self, file_path):
        """
        Return file metadata.
        """
        stats = os.stat(file_path)
        abs_path = os.path.abspath(file_path)
        print(stats.st_size)
        attrs = {
            'File Path': abs_path, 
            'File Name': Path(file_path).name,
            'Size (KB)': self.size_format(stats.st_size),
            'Creation Date': self.time_convert(stats.st_birthtime),
            'Modified Date': self.time_convert(stats.st_mtime),
            'Last Access Date': self.time_convert(stats.st_atime)}
        return attrs

    def create_file_records(self, dir_path):
        """
        Create a dict with metadata for all files in the given directory.
        """
        result = list()
        for name in os.listdir(dir_path): 
            file_path = os.path.join(dir_path, name)
            meta_data = self.get_meta_data(file_path)
            result.append(meta_data)
        return result


