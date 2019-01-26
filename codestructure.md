## The root consists of 2 directories:
1. Apache Server
2. PrinterFac

## I. Apache Server
- Serves as a content delivery network to serve media files
- Stores all print documents in  `media/documents/user-hash/doc-name`
- `EP_upload_post.php` transfers media from django to apache server
  - target directory (line 5), file_upload_size (line 22) and filetype extension (line 15) can be configured here.

## II. Django Server

### To get an in-depth understanding of the code, it is recommended to watch this [playlist](https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p).
#### All the macros for the server can be configured in `PrinterFac/settings.py`, which has it in a systematic format with comments to help in configuring them.

- The functionality of each feature is defined in `app/views.py`
- The templates rendered for each view is in the `app/templates/app/template.html`
- All the urls are defined in `app/urls.py`
- Models stored for the database are in `app/models.py`
  - Any changes to models.py has to be supplemented by
    `python manage.py makemigrations`
    `python manage.py migrate`
    to make the necessary changes to the database
- All the form logic can be found in `app/forms.py`
 
The django webapp consists of three main apps:

##### A) baseApp [Eprint/PrinterFac/baseApp]
  - Comprises of following features, Login, Logout, Home, about page, and payments
  - On cancelling the print job by user, in the confirm portal, the user is redirected to this page where all the unconfirmed documents are removed
  - For the payment portal, all the variables are sent from `payment` view
  - `check_ack.html` is the template rendered when a user is asked to check email for confirmation or clicks on the confirmation link sent to them

##### B) Eprint_users [Eprint/PrinterFac/Eprint_users]
  - Comprises of Register, Profile, Upload document, History, Bill and activating account [acc_active_email.html is the template for activation email]
  - Any changes to the activation email procedure are to be made in this view itself, in the `register` and `activate` functions in `views.py`
  - In `views.py`, the view `confirm` has the logic for uploading the files to Apache server and sending the prints to the printer
  - For checking the PDFs during upload, `subset_pdf` function is used in `views.py`
  - To add any custom specifications and restrictions on the files and upload form, other than those mentioned in line 7 of this document, you can add them to the form cleaning method in `forms.py` or `views.py`

##### C) Eprint_admin [Eprint/PrinterFac/Eprint_admin]
  - Comprises of Task Management and Update Prices
  - Ability to view, reprint and update status of each document
  - Control over the database can be found at the url `http://domain/admin` (section III).
  - To change any of the uploading attributes, refer to line 7 in this document


## III. Additional Admin Functions
For the additional, rather common, admin functions, the default django administration portal is used.

The url `http://domain/admin` has admin-only functions like viewing/modifying/deleting all the users and other models used in the program.

The interface is very user-friendly and the admin can easily figure out where to go for a certain task.
