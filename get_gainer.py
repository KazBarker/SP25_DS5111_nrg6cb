'''
Gainer Factory Template

Serves as the interface for the gainer methods located in bin/gainers/ and
can be called using "python get_gainers.py <gainer choice>" or using the
makefile: "make gainer SRC=<gainer choice>"
'''

class ProcessGainer:
    '''
    ProcessGainer class: used to run initialized gainer methods.
    '''
    def __init__(self, gainer_downloader, gainer_normalizer):
        self.downloader = gainer_downloader
        self.normalizer = gainer_normalizer

    def _download(self):
        self.downloader.download()

    def _normalize(self):
        self.normalizer.normalize()

    def _save_to_file(self):
        self.normalizer.save_with_timestamp()

    def process(self):
        '''Runs the initialized gainer methods.'''
        self._download()
        self._normalize()
        self._save_to_file()

if __name__=="__main__":
    import sys
    from bin.gainers.factory import GainerFactory

    # Make our selection, 'one' choice
    choice = sys.argv[1]

    # let our factory get select the family of objects for processing
    factory = GainerFactory(choice)
    downloader = factory.get_downloader()
    normalizer = factory.get_processor()

    # create our process
    runner = ProcessGainer(downloader, normalizer)
    runner.process()
