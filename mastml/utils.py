import sys

class Tee(object):
    """
    Makes stdout go both to file and screen
    From https://stackoverflow.com/a/616686
    """
    def __init__(self, name, mode):
        self.file = open(name, mode)
        self.stdout = sys.stdout
        sys.stdout = self
    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()
    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
    def flush(self):
        self.file.flush()

class TeeErr(object):
    """
    Makes stderr go both to file and screen
    From https://stackoverflow.com/a/616686
    """
    def __init__(self, name, mode):
        self.file = open(name, mode)
        self.stderr = sys.stderr
        sys.stderr = self
    def __del__(self):
        pass #lol
        #sys.stderr = self.stderr
        #self.file.close()
    def write(self, data):
        self.file.write(data)
        self.stderr.write(data)
    def flush(self):
        self.file.flush()
