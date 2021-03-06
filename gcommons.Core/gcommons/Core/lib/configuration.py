


import os
import logging

# XML - renamed to allow other implementations in the future 
from xml.dom.minidom import parseString as XMLParseString
from xml.parsers.expat import ExpatError as XMLError

logger = logging.getLogger('gcommons.Core.lib.gcConfiguration')


def readFile(*rnames): 
    return open(os.path.join(*rnames)).read()


def xmlgetchild_text(xmlnode, name):
    try:
        string = xmlnode.getElementsByTagName(name)[0].childNodes[0].nodeValue
        return string
    except IndexError:
        return None



class gcommonsRelatorType:
    def __init__(self, xmlnode = None, values=None):
        if xmlnode is None:
            self._id = values['marccode']
            self._name = values['name']
            self._description = values['description']
            self._displayorder = values['displayorder']
        
        else:
            self._id = xmlgetchild_text(xmlnode, 'marccode')
            self._name = xmlgetchild_text(xmlnode, 'name')
            self._description = xmlgetchild_text(xmlnode, 'description')
            self._displayorder = xmlgetchild_text(xmlnode, 'displayorder')
    def id(self):
        return self._id
    def name(self):
        return self._name
    def description(self):
        return self._description
    def displayorder(self):
        return int(self._displayorder)


class gcommonsSubmittableSubtype:
    def __init__(self, xmlnode = None):
        self._id = xmlgetchild_text(xmlnode, 'id')
        self._name = xmlgetchild_text(xmlnode, 'name')
        self._description = xmlgetchild_text(xmlnode, 'description')
        self._requirements = xmlgetchild_text(xmlnode, 'requirements')
        self._words_per_page = xmlgetchild_text(xmlnode, 'words-per-page')
        
    def id(self):
        return self._id
    def name(self):
        return self._name
    def description(self):
        return self._description
    def requirements(self):
        return self._requirements
    def words_per_page(self):
        if self._words_per_page is not None:
            return int(self._words_per_page)
        else:
            return 0

class gcommonsNotification:
    def __init__(self, xmlnode = None):
        self._id = xmlgetchild_text(xmlnode, 'id')
        self._type = xmlgetchild_text(xmlnode, 'type')
        self._template = xmlgetchild_text(xmlnode, 'template')
    def id(self):
        return self._id
    def type(self):
        return self._type
    def template(self):
        return self._template
        
        
class gcommonsSubmittableItem:
    def __init__(self, name=None, portal_type = None, description=None, xmlnode=None):
        
        if xmlnode is None:
            # TODO: this construction sounds deprecated
            logger.info("Deprecated construction of gcommonsSubmittableItem") 
            self._name = name
            self._portal_type = portal_type
            self._description = description
        else:
            self._name = xmlgetchild_text(xmlnode, 'name')
            self._portal_type = xmlgetchild_text(xmlnode, 'type')
            self._description = xmlgetchild_text(xmlnode, 'description')
            self._subtypes = {}
            self._relators = {}
            # Relators
            xmlrelators = xmlnode.getElementsByTagName('relators')
            if xmlrelators.length:
                self._readRelators(xmlrelators[0])
                
            # Subtypes?
            xmlsubtypes = xmlnode.getElementsByTagName('subtypes')
            if xmlsubtypes.length:
                self._readSubtypes(xmlsubtypes[0])
            # Notifications?
            self._notifications = {}
            xmlnotifications = xmlnode.getElementsByTagName('notifications')
            if xmlnotifications.length:
                self._readNotifications(xmlnotifications[0])
        
    def _readRelators(self, xmlnode):
        for item in xmlnode.getElementsByTagName('relator'):
            relator = gcommonsRelatorType(xmlnode=item)
            self._relators[ relator.id() ] = relator

    def _readSubtypes(self, xmlnode):
        for item in xmlnode.getElementsByTagName('subtype'):
            subtype = gcommonsSubmittableSubtype(xmlnode=item)
            self._subtypes[ subtype.id() ] = subtype
            
    def _readNotifications(self, xmlnode):
        for notif in xmlnode.getElementsByTagName('notification'):
            notification = gcommonsNotification(xmlnode=notif)
            self._notifications[notification.id()] = notification 

    def name(self):
        return self._name
    
    def portal_type(self):
        return self._portal_type
    
    def description(self):
        return self._description
    
    def relators(self):
        return sorted(self._relators.values(), key=gcommonsRelatorType.displayorder)

    def getRelator_byId(self, id):
        if self._relators.has_key(id):
            return self._relators[id]
        else:
            return None        
    
    def subtypes(self):
        # reverse this to left as they came in XML
        values = self._subtypes.values()
        values.reverse()
        return values
    
    def getSubtype_byId(self, id):
        if self._subtypes.has_key(id):
            return self._subtypes[id]
        else:
            return None
    
    def notifications(self):
        return self._notifications.values()
    
    def getNotification_byId(self, id):
        if self._notifications.has_key(id):
            return self._notifications[id]
        else:
            return None


class gcConfiguration:
    #
    # TODO: more efficient than this, caching
    # or drop xml alltogether
    
    def __init__(self, xmlstring=None, parsedxml=None):
        
        if parsedxml is None:
            dom = XMLParseString(xmlstring)
            self.parsedxml = dom.documentElement
        else:
            self.parsedxml = parsedxml
        
        # Parse parameters
        self.parameters = {}
        container = self.parsedxml.getElementsByTagName('Container')[0]
        # read Container/name and type
        self.parameters['name'] = xmlgetchild_text(container, 'name')
        self.parameters['type'] = xmlgetchild_text(container, 'type')
        # read Container/params
        try:
            params = container.getElementsByTagName('params')[0]
        except IndexError:
            return
            
        for param in params.childNodes:
            value = xmlgetchild_text(params, param.nodeName)
            if value == 'True' or value == 'true':
                value = True
            elif value == 'False' or value == 'false':
                value = False
                
            if value is not None:
                self.parameters[ param.nodeName ] = value 
        
            
    
    def getContainerConfig(self):
        """
        return dictionary with name and type
        sort of back-compatibility, maybe params should be it
        """
        config = {}
        config['name'] = self.parameters['name']
        config['type'] = self.parameters['type']
        return config
        
    def getContainerName(self):
        """
        return name
        """
        return self.getContainerConfig()['name']
    
    def getParameter(self, param, default=None):
        if self.parameters.has_key(param):
            return self.parameters[param]
        else:
            return default
    
    def getItems(self):
        """
        """
        return self.getSubmittableItems()
    
    def getSubmittableItems(self):
        """
        """
        items = []
        contained = self.parsedxml.getElementsByTagName('Items')[0]
        for item in contained.getElementsByTagName('Item'):
            items.append(gcommonsSubmittableItem(xmlnode=item))
            
        return items
    
    def getItemType_byName(self, name):
        
        # ugly
        for item in self.getItems():
            if item.name() == name:
                return item

    def getItemType_byPortalType(self, portal_type):
        
        # ugly
        for item in self.getItems():
            if item.portal_type() == portal_type:
                return item
            
    
    