from wq.io.base import IO

class FileIO(IO):
    filename = None

    def open(self):
        self.file = open(self.filename)

class BinaryFileIO(FileIO):
    def open(self):
        self.file = open(self.filename, 'rb')
