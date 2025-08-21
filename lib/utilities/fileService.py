import os


class FileService:
    def read(self, filePath):
        with open(filePath, "r") as file:
            return file.read()

    def write(self, filePath, content):
        with open(filePath, "w") as file:
            file.write(content)

    def delete(self):
        os.remove(self.path)
