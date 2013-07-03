Import Google Reader Starred Items to Delicious
===============================================

This is a simple script to take your 
[Google Reader takeout](https://www.google.com/takeout/#custom:reader) data,
specifically the `starred.json` file within, and import it into your Delicious.com account.

To use it, make sure you have `pydelicious` installed:

    pip install pydelicious

Then, run it by specifying your delicious username and the path to your `starred.json` file:

    python reader-to-delicious.py <delicious-username> starred.json

It will prompt you for your delicious password, and then use the delicious API to create
the bookmarks.


Customisation
-------------

By default, the script will:

* the title of the Google Reader
* mark the created bookmarks as private
* preserve tags that you added in Google Reader
* add a `_from:greader` tag to allow you to easily tell which bookmarks came from
  Google Reader

If a bookmark with an identical URL already exists in Delicious,
it will not replace it. You would get an error, but the script will continue.

It does not import the annotations that you made, mainly because I never found
my own annotations to be useful. Feel free to send me a pull request.

Some (hopefully) variables are available for customisation near the top of the
script (after the import lines.)
