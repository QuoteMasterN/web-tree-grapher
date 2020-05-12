'''Page class

Used to represent a page'''

class Page:
    def __init__(self):
        self.title = " "
        self.url = " "
        self.childLinks = []
        self.notes = " "
    
    # appends current Page object to the text file named domainName in output
    def appendToFile(self, domainName):
        with open('output/%s' % domainName, 'a') as f:
            # write opening bracket
            f.write('{\n')
            f.write(str(self.title) + '\n')
            f.write(str(self.url) + '\n')
            f.write(' '.join(self.childLinks))
            f.write(str(self.notes) + '\n')
            f.write('}\n')

    
