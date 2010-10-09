Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True


-*- extra stuff goes here -*-
The SpecialIssue content type
===============================

In this section we are tesing the SpecialIssue content type by performing
basic operations like adding, updadating and deleting SpecialIssue content
items.

Adding a new SpecialIssue content item
---------------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'SpecialIssue' and click the 'Add' button to get to the add form.

    >>> browser.getControl('SpecialIssue').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'SpecialIssue' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'SpecialIssue Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'SpecialIssue' content item to the portal.

Updating an existing SpecialIssue content item
-----------------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New SpecialIssue Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New SpecialIssue Sample' in browser.contents
    True

Removing a/an SpecialIssue content item
---------------------------------------

If we go to the home page, we can see a tab with the 'New SpecialIssue
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New SpecialIssue Sample' in browser.contents
    True

Now we are going to delete the 'New SpecialIssue Sample' object. First we
go to the contents tab and select the 'New SpecialIssue Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New SpecialIssue Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New SpecialIssue
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New SpecialIssue Sample' in browser.contents
    False

Adding a new SpecialIssue content item as contributor
-----------------------------------------------------

Not only site managers are allowed to add SpecialIssue content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'SpecialIssue' and click the 'Add' button to get to the add form.

    >>> browser.getControl('SpecialIssue').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'SpecialIssue' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'SpecialIssue Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new SpecialIssue content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



The Section content type
========================

In this section we are tesing the Section content type by performing
basic operations like adding, updadating and deleting Section content
items.

Adding a new Section content item
---------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Section' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Section').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Section' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Section Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Section' content item to the portal.

Updating an existing Section content item
-----------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Section Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Section Sample' in browser.contents
    True

Removing a/an Section content item
----------------------------------

If we go to the home page, we can see a tab with the 'New Section
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Section Sample' in browser.contents
    True

Now we are going to delete the 'New Section Sample' object. First we
go to the contents tab and select the 'New Section Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Section Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Section
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Section Sample' in browser.contents
    False

Adding a new Section content item as contributor
------------------------------------------------

Not only site managers are allowed to add Section content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Section' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Section').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Section' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Section Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Section content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Article content type
========================

In this section we are tesing the Article content type by performing
basic operations like adding, updadating and deleting Article content
items.

Adding a new Article content item
---------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Article' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Article').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Article' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Article Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Article' content item to the portal.

Updating an existing Article content item
-----------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Article Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Article Sample' in browser.contents
    True

Removing a/an Article content item
----------------------------------

If we go to the home page, we can see a tab with the 'New Article
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Article Sample' in browser.contents
    True

Now we are going to delete the 'New Article Sample' object. First we
go to the contents tab and select the 'New Article Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Article Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Article
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Article Sample' in browser.contents
    False

Adding a new Article content item as contributor
------------------------------------------------

Not only site managers are allowed to add Article content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Article' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Article').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Article' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Article Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Article content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Issue content type
===============================

In this section we are tesing the Issue content type by performing
basic operations like adding, updadating and deleting Issue content
items.

Adding a new Issue content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Issue' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Issue').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Issue' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Issue Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Issue' content item to the portal.

Updating an existing Issue content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Issue Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Issue Sample' in browser.contents
    True

Removing a/an Issue content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Issue
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Issue Sample' in browser.contents
    True

Now we are going to delete the 'New Issue Sample' object. First we
go to the contents tab and select the 'New Issue Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Issue Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Issue
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Issue Sample' in browser.contents
    False

Adding a new Issue content item as contributor
------------------------------------------------

Not only site managers are allowed to add Issue content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Issue' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Issue').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Issue' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Issue Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Issue content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Journal content type
========================

In this section we are tesing the Journal content type by performing
basic operations like adding, updadating and deleting Journal content
items.

Adding a new Journal content item
---------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Journal' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Journal').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Journal' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Journal Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Journal' content item to the portal.

Updating an existing Journal content item
-----------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Journal Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Journal Sample' in browser.contents
    True

Removing a/an Journal content item
----------------------------------

If we go to the home page, we can see a tab with the 'New Journal
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Journal Sample' in browser.contents
    True

Now we are going to delete the 'New Journal Sample' object. First we
go to the contents tab and select the 'New Journal Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Journal Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Journal
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Journal Sample' in browser.contents
    False

Adding a new Journal content item as contributor
------------------------------------------------

Not only site managers are allowed to add Journal content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Journal' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Journal').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Journal' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Journal Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Journal content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



