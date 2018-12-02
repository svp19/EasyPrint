The root consists Two directories:

## I] Apache Server
- Serves as a content delivery network to serve media files
- Stores all print documents in  `media/documents/user-hash/doc-name`
- `EP_upload_post.php` transfers media from django to apache server
  - target directory(line 5), fileuploadsize(line 22) and filetype extension(line 15) can be configured here.
- `PaytmKit`
  - All the macros can be configured from `PaytmKit/lib`

## II]  Django Server

#### All the macros for the server can be configured in `PrinterFac/settings.py`

- The functionality of each feature is defined in `app/views.py`
- The templates rendered for each view is in the `app/templates/app/file`
- urls are defined in `app/urls.py`
- models stored for the database are in `app/models.py`
  - Any changes to models.py has to be supplemented by
    `python manage.py makemigrations`
    `python manage.py migrate`
    to make the necessary changes to the database.
- all form logic can be found in `app/forms.py`
 
The django webapp consists of three main apps:

A) baseApp [Eprint/PrinterFac/baseApp]
  - Comprises of following features, Login, Logout, Home, about page, and payments.

B) Eprint_users [Eprint/PrinterFac/Eprint_users]
  - Comprises of Register, Profile, Upload document, History, Bill and activating account [acc_active_email.html is the template for activation email]
  - In views.py, the view `confirm` has the logic for uploading the files to Apache server and sending the prints to the printer.

C) Eprint_admin [Eprint/PrinterFac/Eprint_admin]
  - Comprises of Task Management and Update Prices
  - Ability to view, reprint and update status of each document.
  - Control over the database can be found at the url `http://domain/admin`
  - To change any of the uploading attributes, refer to line 7 in this document.
