import sqlite3
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
        # connect to database and insert class members
        data = sqlite3.connect('output/%s' % domainName)
        c = data.cursor()

        c.execute('INSERT INTO domain VALUES (:title, :url, :childLinks, :notes)',
        {
            'title' : self.title,
            'url' : self.url,
            'childLinks' : ' '.join(self.childLinks),
            'notes' : self.notes
        })

        data.commit()

        data.close()

    
