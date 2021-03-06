# EPrint
*EP* is a Django-SQL based webapp that aims at enabling users to utilize the printing facilities of the institution more effectively. The Portal features options to upload files, check print status and view/pay e-bills on the fly through the intranet.

## Authors
+ **Anudeep Tubati** [170010039@iitdh.ac.in]
+ **S V Praveen** [170010025@iitdh.ac.in]

## Features
+ Login ➤ Upload ➤ Confirm ➤ Collect
+ Automated server-side printing 
+ Email verification for institution
+ Easily configurable through intranet
+ Simple, Responsive and mobile friendly UI

## Installation
All the features of code can be found in detail in [codestructure.md](https://github.com/svp19/EPrint/blob/master/codestructure.md)

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
9. As it is better to use environment variables for all the passwords and keys, configure your environment variables (like [this](https://askubuntu.com/questions/58814/how-do-i-add-environment-variables)) appropriately to match those in `settings.py`

If all went well then your command line prompt should now start with `(easyprintvenv)`.

9. Install the required python libraries: `pip install -r requirements.txt`

**On the first run, create a superuser to have unrestricted access to any page by the command `python manage.py createsuperuser`**

#### II. Setting up Apache Server
1. Install [LAMP](https://howtoubuntu.org/how-to-install-lamp-on-ubuntu).
2. Copy the contents of [Apache Server](https://github.com/svp19/EPrint/tree/master/Apache%20Server) directory into your localhost folder. 
3. Give `www-data` permission to read, write, execute the media file: `sudo chown -R www-data media` 

#### III. Configuring Printer server for Django
If your printer is wired to the server or if it is connected through direct WiFi
1. Get the `ipp:` of your printer using `lpinfo -v`
2. Create a new printer class called `myprinter` using the `lpadmin` command-line utility for your online printer.
3. Set it to default.
Example : `lpadmin -p myprinter -E -v ipp://myprinter.local/ipp/print`

If your printer is on wirelessly connected to the server
1. Get the IP of your printer and add it to the printers in Linux settings.
2. Set it to default.

#### IV. Setting up RazorPay
1. In `PrinterFac` directory, go to `settings.py` and change the `API_KEY` to your razorpay_api_key and `API_PASS` to your razorpay_api_pass.

## Databases Involved
1. Only sqlite3 has been used in this program.
2. To deploy using PostgreSQL, please refer to this [link](https://docs.djangoproject.com/en/2.1/ref/databases/). Note that all changes will be made in `PrinterFac/settings.py` only.

## To-Do
- [x] ~~Integrate RazorPay payments~~
- [ ] Add support for PostScript files
- [ ] Resolve print status automatically
