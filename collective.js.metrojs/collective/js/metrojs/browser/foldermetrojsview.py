from Products.Five import BrowserView
import random
import logging

logger = logging.getLogger('collective.js.metrojs.browser.foldermetrojsview')


class FolderMetroJSView(BrowserView):

    @property
    def randint(self):
        """ Random integer
        """
        return random.randint(0, 1500)
    
    
    def truncate(self, text, word_count=60, split_on=';?&@!$#-/\\"\''):
        words = text.split()
        if len(words) > word_count:
            return ' '.join(text.split()[:word_count]) + "..."
        else:
            return text
        
    def test(self, condition, value_true, value_false):
        if condition:
            return value_true
        else:
            return value_false
        
        
    def getTileClass(self, item_index):
        logger.info(item_index)
        if item_index < 3:
            return "tileItem large-live-tile live-tile blue"
        else:
            return "tileItem live-tile blue"

    