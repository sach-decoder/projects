from zipfile import ZipFile 

with ZipFile('C:/Users/sachi/Downloads/archive(1).zip', 'r') as zObject:
    zObject.extractall(
        path='C:/Users/sachi/Downloads/detection_model'
    )
    