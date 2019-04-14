# Project 1

#Book Review Site

Project Overview (per Harvardx)

In this project, you’ll build a book review website. Users will be able to register for your website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. You’ll also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via your website’s API.

Link to Youtube Demonstration:
https://youtu.be/YXXO10GUM8E


How To Run This:
Create Heroku account and add the database variables to your project.
From Heroku, create a database with three tables, users, books and reviews.
users columns:id,name,password
reviews columns:id(integer),rating(integer),message(varchar...can be text too, to accommodate long reviews),isbn(varchar),name(varchar),review_date(timestamp default current_timestamp)
books columns:id(integer),isbn(varchar),title(varchar),author(varchar),year(integer)
Clone the repo into your directory of your choice.
cd into it.


You need the following,replace these credentials with yours.
export DATABASE_URL=postgres://ob92jours(*This is from Heroku credntial please replace it.*)
*These will still be the same*
export FLASK_ENV=development
export FLASK_APP=application.py


Application structure

application.py


static files
A.1 images folder

This folder includes images used in the index.html landing page.


A.2 styling.css and style2.css


These two files contain generic css applied throughout the site.

books.csv

This file list 500 books to be imported into database using import.py file.

import.py

This file contains a script written to import the books books.csv into database.

set db variables before doing the import
create db with the columns as in sql attachec

templates files includes :

A.1 book.html
This file contains specific details about a book. This details include:
Title,Author, Year, ISBN, Total Reviews, Average Review, Rating from this websites, text review from this website and the link to the book api (http://127.0.0.1:5000/api/book/0062284835)

A.2 index.html
This is the landing page, there is not action happening in this page.It displays data dynamically from the database.The images are static however.

A.3 login.html


This is the login page with full authentication.
The user needs username and password to login.The password and username must agree to the one stored on the databasebase otherwise an error message will be displayed and redirecting the user to the login page.


A.4 register.html

This is the registration page that enables the user to access the platform.
The registration process is one step, a user must provide a username and password.These fields are both required otherwise the user will not be allowed to use the platform.The confirm password field is required as well.

Once a user register successfuly he/she then gets redirected to the login page to login using the same credential used to register.

A.5 dashboard.html


Upon successful login, a user is then redirected to the dashboard.
A dashboard display reviews done by the user and others.It also display recommended books that a user can choose from to review.
The dashboard is guarded routes meaning that a user cannot use a GET or slash to access the routes and the user must be authenticated to have access to the dashboard.
At the far top right of the dashboard, there is a drop down menu to LOGOUT the user.


A.6 layout.html


This file contains the base of the site, all the bootstrap libraries and the site layout.
However an inline stylesheet has been used for the page specific features that cannot be applied to the generic site layout.


A.7 search.html


This file contains a search bar for the user to type the book title, isbn or author for the purpose of reviewing.If the book is not found, an appropriate message is displayed.
If the book is found, the user can click into it and will get redirected to book.html where the book details can be found.


A.8 books.html
This file display all the books from the database.if the user does not feel like searching, she/he can just scroll in the displayed books and choose a book to review.

B.Template have a Folder called includes(within templates directory) that have the following files:


_messsages.html


This file contain a customized error messages taking advantage of bootstrap's class categories and flask's flash function.


_navbar.html


This file contains the site navigation bar.It is based on Bootstrap's default nav bar.

Others
I do not own the images used, and no intellectual property rights violation intended.I used them for illustration.

images used obtained from:

https://pixabay.com/photos/golden-cup-coffee-basket-books-791072/
https://pixabay.com/photos/bookshelf-library-literature-books-413705/
