import gdown

link = "https://drive.google.com/drive/folders/1Hto9ITBDOZYRZ6NfNYERCeFUADEhNfVM?usp=drive_link"
gdown.download_folder(link, quiet=True)