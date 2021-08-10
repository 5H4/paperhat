# Require JAVA
# Windows & Linux 
# Download: https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html
# pip install tika
from tika import parser
from shutil import copyfile
from datetime import datetime
from datetime import date
import glob, os
import shutil

now_date = datetime.now()
today = date.today()
current_time = now_date.strftime("%H-%M-%S")
current_date = today.strftime("%d-%m-%Y")

# Windows path
files_root = "C://Users//SHALLY//Desktop//git//PaperHat"
mount_root = "C://Users//SHALLY//Desktop//git//PaperHat//mount"
processed_root = "C://Users//SHALLY//Desktop//git//PaperHat//processed"
failed_root = "C://Users//SHALLY//Desktop//git//PaperHat//failed"
logs = "C://Users//SHALLY//Desktop//git//PaperHat//logs//paperhat_"

# Linux path
#files_root = "/home/arm/FTP/files"
#mount_root = "/home/arm/FTP/files/mount"
#processed_root = "/home/arm/FTP/files/processed"
#logs = "/home/arm/FTP/files/logs/paperhat_"
#failed_root = "/home/arm/FTP/files/failed"

'''
    Server RPI, Mount external drive.
    Tools: vsftpd
    $ useradd arm
    $ password arm
    $ sudo chown nobody:nogroup /home/arm/FTP
    $ sudo chmod a-w /home/arm/FTP
    $ sudo chown arm:arm /home/arm/FTP/files
    - $ sudo nano /etc/vsftpd.conf
    - - user_sub_token=$USER
    - - local_root=/home/$USER/FTP/files
    - - userlist_enable=YES
    - - userlist_file=/etc/vsftpd.userlist
    - - - arm
    - - userlist_deny=NO
'''

'''
    Scanned document via printer send to server via FTP in root folder -> files_root
    When paperhat done, move file from files_root to processed_root
    if paperhat failed log error to -> logs paperhat.log, file move to filed_root.
'''

# Create dir.
ROOT_DIR = os.path.abspath(os.curdir)
create_dir = ['mount', 'processed', 'logs', 'failed']
for d in  create_dir:
        if not os.path.isdir(ROOT_DIR+'/'+d):
            os.mkdir(ROOT_DIR+'/'+d)

class bc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

os.chdir(files_root)

file_count, root_index , failed, success = glob.glob("*.pdf"), 0, 0, 0

for file in glob.glob("*.pdf"):
    root_index +=1
    raw = parser.from_file(file)
    index = 0
    this = False
    for x in raw['content'].splitlines(0):
        index += 1
        if x.find('Internal no:') == 0:
            '''
                Dynamic logic stuff.
                2 argv = PDF name and Date [Year, Month]
            '''
            # From content get Date.
            # When find is true on index plus 1 to get date.
            get_date = raw['content'].splitlines(0)[index+1].split(": ")[1].split('.')
            # Extract invoice number here.
            invoice_number = x.split(': ')[1].split(" ")[0]
            # Get day , month, year
            day = get_date[0]
            month = get_date[1]
            year = get_date[2]
            '''
                End dynamic logic stuff.
            '''
            # Folder structure ..... logic
            # Folder name is eaqual year + month
            dynamic_folder = "{}-{}".format(year, month)
            # Remove all whitespace from string , folder name.
            dynamic_folder = ''.join(dynamic_folder.split())
            # If folder not exists create new folder.
            if not os.path.exists(mount_root+'/'+dynamic_folder):
                os.makedirs(mount_root+'/'+dynamic_folder)
        
            copyfile('{}/{}'.format(files_root, file), '{}/{}/{}.pdf'.format(mount_root, dynamic_folder, invoice_number))
            shutil.move('{}/{}'.format(files_root, file), '{}'.format(processed_root, file))
            success +=1
            this = True

    if this == False:
        failed +=1
        print(bc.WARNING+'Error found filename: {}{}'.format(bc.FAIL, file))
        shutil.move('{}/{}'.format(files_root, file), '{}'.format(failed_root, file))
        with open(logs+current_date+'#'+current_time+'.log', 'a') as fd:
            fd.write(f'\n{file}')

    if root_index % 10 == 0:
        # Log terminal
        print('Success: {}/{} Failed: {}'.format(success, len(file_count), failed))