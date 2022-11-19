# Reresearch

Browser bookmarks ain't enough.


### What?

Inspired by traditional bookmarks from common web browsers, Reresearch offers extra features to keep the saved links organized, allowing to easily find them again when needed.


### Why?

When I do intensive web surfing to research and learn about a software library, or when I'm reading interesting news about astronomy, or genetics, I often end up with lots of tabs open in my web browser and it becomes hard to organize them. An easy exit is to save all the tabs in a folder, but then it's not funny to browse a messed up bag of links.

Sometimes I find myself researching my own bookmarks collected during some research, trying to figure out which of them is that one I remember I found, say, a month ago. The *re-research* process would be easier keeping some metadata, like date added, and adding custom tags to categorize the links.


### How?

Reresearch consists of a simple web API that receives the links of interest from the users and stores the appropriate data, and a web dashboard to interact with the collected items.

Built with [Django](https://www.djangoproject.com/), [REST Framework](https://www.django-rest-framework.org/) and a bunch of plugins.


## Models

### Item

An object that represents a saved link. The only required value to create an Item is the URL to be stored. Some fields are automatically calculated. The fields are:
- owner (fk)
- link
- domain (auto)
- title (auto)
- dt (auto)
- tags (fks, optional)


### Tag

Simple, few-word descriptive labels that may be related to one or more Items. New rows in this table may be created by any user. Tags are shared across users (it reduces the amount of data). The fields:
- label
- items (fks)
