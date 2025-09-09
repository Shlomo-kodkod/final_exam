from pathlib import Path
import os.path
from datetime import datetime
from services.utils.logger import Logger

class Fetcher:
    def __init__(self):
        self.__logger = Logger.get_logger("Fetcher")

    def time_convert(self, time: float) -> str:
        """
        Convert timestamp from float to str in iso format.
        """
        newtime = datetime.fromtimestamp(time).date()
        return str(newtime)

        
    
    def size_format(self, size: int) -> float:
        """
        Convert file size to KB size.
        """
        newform = round(size / 1024, 2)
        return newform 

    def get_meta_data(self, file_path) -> dict:
        """
        Return file metadata.
        """
        stats = os.stat(file_path)
        abs_path = os.path.abspath(file_path)
        attrs = {
            'File Path': abs_path, 
            'File Name': Path(file_path).name,
            'Suffix':Path(file_path).suffix,
            'Size (KB)': self.size_format(stats.st_size),
            'Creation Date': self.time_convert(stats.st_birthtime),
            'Modified Date': self.time_convert(stats.st_mtime),
            'Last Access Date': self.time_convert(stats.st_atime)}
        return attrs

    def create_file_records(self, dir_path) -> list[dict]:
        """
        Create a dict with metadata for all files in the given directory.
        """
        result = list()
        for name in os.listdir(dir_path): 
            try:
                file_path = os.path.join(dir_path, name)
                meta_data = self.get_meta_data(file_path)
                result.append(meta_data)
                self.__logger.info(f"Successfully add metadata for {name}")
            except Exception as e:
                self.__logger.error(f"Failed to find metadata for {name}: {e}")
        return result
 