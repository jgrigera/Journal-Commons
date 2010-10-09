import logging
logger = logging.getLogger('gcommons.Journal.subscribers')

def set_article_default_view(self,event):
    """
      Set article default view depending on the action changing the state. 
    """
    views =  {'publish': 'gc_articlepublish_view', 'retract': 'gcommons_article_view'}

    if event.action == 'publish' or event.action == 'retract': 
        event.object.setLayout(views[event.action]) 
        logger.info("action=%s, view changed to %s" % (event.action, views[event.action]))
