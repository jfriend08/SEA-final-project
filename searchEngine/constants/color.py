class bcolors(object):
    def __init__(self):
        self.HEADER = '\033[31m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.LIGHTBLUE = '\x1b[1;34m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'


    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''