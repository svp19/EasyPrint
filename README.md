# EPrint
*EP* is a django-MySQL based webapp that aims at enabling users to utilize the printing facilities of the institution more effectively. The Portal features options to upload files, check print status and view/pay e-bills on the fly through the intranet.

## Authors
+ **Anudeep Tubati** [170010039@iitdh.ac.in]
+ **S V Praveen** [170010025@iitdh.ac.in]

## Features
+ Login -> Upload -> Confirm -> Collect
+ Automated server-side printing 
+ Email verification for institution
+ Easily configurable through intranet
+ Simple, Responsive and mobile friendly UI

## Installation
Apache server is used to serve media files to the Admin page.
Django server must be setup on a linux-based system and connected to the printer server.

#### I. Setting up Django Server
1. Clone this repository: `git clone https://github.com/svp19/EPrint`
2. `cd` into `EPrint/PrinterFac`: `cd EPrint/PrinterFac`.
3. Install [pyenv](https://github.com/yyuu/pyenv#installation).
4. Install [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv#installation).
5. Install Python 3.6.4: `pyenv install 3.6.4`.
6. Create a new virtualenv called `easyprintvenv`: `pyenv virtualenv 3.6.4 easyprintvenv`.
7. Set the local virtualenv to `easyprintvenv`: `pyenv local easyprintvenv`.
8. Reload the `pyenv` environment: `pyenv rehash`.

If all went well then your command line prompt should now start with `(easyprintvenv)`.

9. Install the required python libraries: `pip install requirements.txt`

#### II. Setting up Apache Server
1. Install [LAMP](https://howtoubuntu.org/how-to-install-lamp-on-ubuntu).
2. Copy the contents of [Apache Server](https://github.com/svp19/EPrint/tree/master/Apache%20Server) directory into your localhost folder. 
3. Give `www-data` permission to read, write, execute the media file: `sudo chown -R www-data media` 

#### III. Configuring Printer server for Django
1. Get the `ipp:` of your printer using `lpinfo -v`
2. Create a new printer class called `myprinter` using the `lpadmin` command-line utility for your online printer.
Example : `lpadmin -p myprinter -E -v ipp://myprinter.local/ipp/print`
