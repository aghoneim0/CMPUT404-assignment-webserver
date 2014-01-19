CMPUT404-assignment-webserver
=============================

CMPUT404-assignment-webserver

A Basic Socket Server made by Ahmed Ghoneim
Screen-shots under screenshot Folder

List of Features:
=================
1- Serve HTML and CSS files under /www folders <br>
2- if Url file/folder doesn't exist under /www folder 404 error will be thrown <br>
3- if folder is requested and doesn't contain index.html the page will return list of the Folder contents <br>
4- The server is configured to handle missing trailing slash form URL (for example both /deep/ and /deep) will return index.html <br>

Contributors / Licensing
===================================
Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

server.py contains contributions from:

Abram Hindle <br>
Eddie Antonio Santos <br>
Ahmed Ghoneim <br>

But the server.py example is derived from the python documentation examples thus some of the code is Copyright © 2001-2013 Python Software Foundation; All Rights Reserved under the PSF license (GPL compatible) http://docs.python.org/2/library/socketserver.html

