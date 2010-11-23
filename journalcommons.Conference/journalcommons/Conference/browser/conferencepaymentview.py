from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from gcommons.Core.browser import gcommonsView 
from gcommons.Core.lib.gcnumbers import gcommons_spoken_number
import logging

from journalcommons.Conference import ConferenceMessageFactory as _

logger = logging.getLogger('journalcommons.Conference.browser.conferencepaymentview')

class IConferencePaymentView(Interface):
    """
    ConferencePayment view interface
    """
    def test():
        """ test method"""


class ConferencePaymentView(gcommonsView):
    """
    ConferencePayment browser view
    """
    implements(IConferencePaymentView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_form_items(self):
        itemlist = self.context.getItems()
        items = {}
        for item in itemlist:
            items[ item['id'] ] = item
        # Sort items by id, extracting key before ':'
        itemids = items.keys() #[ a['id'] for a in itemlist ]
        itemids.sort(key=lambda x:x.split(':')[0])
        
        form = []
        for itemid in itemids:
            item = items[itemid]
            if itemid.find(':') > 0:
                type = 'radio'
                name = 'group%s' % itemid.split(':')[0]
                css = 'value'
            else:
                type = 'checkbox'
                name = 'checkbox%s' % itemid
                css = 'checkboxType'
            
            if int(item['price']) > 0:
                label = "%s ($%s)" % (item['name'],item['price'])
            else:
                label = item['name'] 
                
            form.append({'type':type, 'name':name, 'value':itemid, 'class':css,
                         'label': label, 'description':item['description']})
            #<input type="radio" name="group1" value="Butter" checked> Butter<br>
        
        return form
    
    def get_receipt(self):
        """
        return a receipt text (used just before sending user to paypal)
        """
        itemlist = self.context.getItems()
        items = {}
        for item in itemlist:
            items[ item['id'] ] = item
        # Sort items by id, extracting key before ':'
        itemids = items.keys() #[ a['id'] for a in itemlist ]
        itemids.sort(key=lambda x:x.split(':')[0])

        invoiceditems = []        
        # Most of this logic will be moved to Invoice
        receipt = "<b>You have indicated the following options:</b><br><ul>"
        total = 0
        description = []
        for itemid in itemids:
            item = items[itemid]
            if int(item['price']) > 0:
                label = "Pay $%s for %s" % (item['price'],item['name'],)
            else:
                label = "Indicated %s" % item['name'] 

            if itemid.find(':') > 0:
                groupid = 'group%s' % itemid.split(':')[0]
                if self.context.REQUEST.get(groupid) == itemid:
                    invoiceditems.append(item)
                    receipt = receipt + "<li>%s<li/>" % label
                    description.append(item['name'])
                    total = total + int(item['price'])
            else:
                name = 'checkbox%s' % itemid
                if self.context.REQUEST.get(name):
                    invoiceditems.append(item)
                    receipt = receipt + "<li>%s<li/>" % label
                    description.append(item['name'])
                    total = total + int(item['price'])
            
            if int(item['price']) > 0:
                label = "%s ($%s)" % (item['name'],item['price'])
            else:
                label = item['name'] 

        invoice = self.context.addInvoice(invoiceditems)
        receipt = receipt + "</ul><strong>The total amount is $%s (%s USD)<p/>" % (total, gcommons_spoken_number(total).upper())
        return { 'total': total,
                 'html': receipt,
                 'comment': receipt,
                 'description': '; '.join(description),
                 'invoiceno': invoice.id() }
            



    ### TODO
    ### ALL THIS AWFULL CODE will be gone in Plone 4
    """ Functions for login 'portlet'
    """
    def login_can_request_password(self):        
        return self.portal_membership.checkPermission('Mail forgotten password', self.context)

    def login_can_register(self):        
        if getToolByName(self.context, 'portal_registration', None) is None:            
            return False        
        return self.portal_membership.checkPermission('Add portal member', self.context)

    def login_form(self):        
        return '%s/login_form' % self.portal_state.portal_url()    
    
    def login_mail_password_form(self):        
        return '%s/mail_password_form' % self.portal_state.portal_url()
    
    def login_name(self):        
        auth = self.auth()        
        name = None        
        if auth is not None:            
            name = getattr(auth, 'name_cookie', None)        
        if not name:            
            name = '__ac_name'        
        return name    
    
    def login_password(self):        
        auth = self.auth()        
        passwd = None        
        if auth is not None:            
            passwd = getattr(auth, 'pw_cookie', None)        
        if not passwd:           
            passwd = '__ac_password'        
        return passwd
        
    def get_enable_self_reg(self):
        # I should learn how to call plone.app.controlpanel.security, but this is a quick fix
        app_perms = self.portal.rolesOfPermission(permission='Add portal member')
        for appperm in app_perms: 
            if appperm['name'] == 'Anonymous' and \
               appperm['selected'] == 'SELECTED':
                return True
        return False

    
    @memoize    
    def auth(self, _marker=[]):        
        acl_users = getToolByName(self.context, 'acl_users')       
        return getattr(acl_users, 'credentials_cookie_auth', None)

    def join_form(self):
        return '%s/join_form' % self.portal_state.portal_url()    
        
