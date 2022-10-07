from ast import Str
import sys
import os

class WinSys:
    def version():
        return "{},{}".format( sys.platform,sys.version)

class Path:
    def combine(*pathItems) -> Str:
        return os.path.join(pathItems)

    def exist(path:Str) -> bool:
        return os.path.exists(path)

class Directory:
    def __init__(self,path:Str) -> None:
        self.path=path

    def create(path:Str):
        os.mkdir(path)

    def delete(path:Str):
        os.rmdir(path)

    def get_work_dir():
        return os.getcwd()

    def change_work_dir(path:Str):
        return os.chdir(path)

class File:
    def __init__(self) -> None:
        pass

    def Exist(path:Str) -> bool:
        pass