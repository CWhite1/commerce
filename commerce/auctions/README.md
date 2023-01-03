# CS50 W - Commerce
#### Video Demo:  <https://youtu.be/y9FZAVLpmRI>
#### Description:

>The purpose of this project was to create a website that functions the same the well known e-commerce site E-bay.  

### Specifications

1. Models: This application has four models in addition to the User model: one for auction listings, one for bids, one for comments and one for the users watchlist. 
The fields for the each model are listed within models.py; however, foreign keys were used in the listings to connect the user to the listing.  The Bids also used the user and lsting foreign key to connect the logged in user to the bid and the listing the bid was made on in addition to a DecimalField for the actual bid. The listing foreign key was used to connect the comment to a particular listing and the User and Listting Foreign Key was used to connect the watchlist to a user and the listing to the actual watchlist.  Additioinally, in apps.py the primary key for each model is inserted through an AutoField.

2. Create Listing: Users are able to visit a page to create a new listing. They are able to specify a title for the listing, a text-based description, the starting bid and the Category that their item should be in. Users can also connect to an image by pressing an upload button and inserting the image from the saved images in their computer.  I felt that this method provides the user with a much better experience for submitting images vs. inserting a url.  Additonally, through a specified form in forms.py which is connected to the model, all fields were given a class for css as well as place holders and a required field. 

3. Active Listings Page: The default route of your web application lets any user, logged in or not, view all of the currently active auction listings. For each active listing, the title, description, current price, and photo are displayed.  Additonally, the page displays 3 listings in each row, all the samae sized with varying text size for each field.  This gives the site an even style where each listing is displayed in the same size.  Additionally, the page displays each active listing from newest to oldest and their is a link for All listings which displays all of the listings posted. 

4. Listing Page: Clicking anywhere on a listing takes the user to a page specific to that listing. On that page, users are able to view all details about the listing, including the current price for the listing.

>1. If the user is signed in, the user is able to add the item to their “Watchlist.” with an Add to Watchlist button. If the item is already on the watchlist, the user is able to remove it with a Remove From Watchlist button.
>2. If the user is signed in, the user is able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed. If the bid doesn’t meet those criteria, the user is presented with an error page which displays the amount of the highest bid to date or one that the displays the starting price if no bids have been made.  If the bid is the largest, the items lsiting and a Congrations you have the highest bid and the amount is displayed.
>3. If the user is signed in and is the one who created the listing, the user has ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.  However, if no bids have been made, it displays "No bids have been made."  The user can, of course a bid an accept it to close it. 
>4. If a user is signed in on a closed listing page, and the user has won that auction, the page displays the item and "Congratulations you have won the bid!".
>5. Users who are able to add comments to the listing page. The listing page displays all comments that have been made for the listing.

5. Watchlist: Users who are signed are able to visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing’s page.

6. Categories: Users are able to visit a page that displays a list of all listing categories that have been insered into the category field on the create a listing page. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.

7. Django Admin Interface: Via the Django admin interface, a site administrator is able to view, add, edit, and delete any listings, comments, bids and watchlist items made on the site.

## Issues

The main issue that I had on this project was not creating the models, but adding fields to the current models that already had data inserted into the database.  On one occasion with a foreign key, I inserted a string default which required an integer.  This caused the database to be unrecoverable and I had to start from scratch.  The second time I was careful to ensure that null=True, blank=True was inserted into the field prior to migration.

The second issue I had was getting the forms to display placeholders and the field names above the input field and size the fields.  I did this by creating a class for each field and using css to control the size, hover and look of the inputs.  