import boto3 
import csv
 
file_path = 'TXTSONDAGE.txt' 
bucket_name = 'esihsondage' 
region_name = 'us-east-1' 
access_key = "AKIAQTWKRAU5JEKOFPET"  
secret_key = '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' 
 
class Student: 
    def __init__(self, int_qt_pays, age, niveau, pays_vise, r_depart, obj_depart, dure_prevu, int_retour): 
        self.int_qt_pays = int_qt_pays 
        self.age = age 
        self.niveau = niveau 
        self.pays_vise = pays_vise 
        self.r_depart = r_depart 
        self.obj_depart = obj_depart 
        self.dure_prevu = dure_prevu 
        self.int_retour = int_retour 
 
    def sauvegarder_sur_s3(self, bucket_name, region_name, access_key, secret_key): 
        # Créer un objet S3 
        client_s3 = boto3.client('s3', region_name=region_name, aws_access_key_id=access_key, aws_secret_access_key=secret_key) 
 
        # Convertir l'objet Student en liste de données 
        student_data = [ 
            self.int_qt_pays, 
            self.age, 
            self.niveau, 
            self.pays_vise, 
            self.r_depart, 
            self.obj_depart, 
            self.dure_prevu, 
            self.int_retour 
        ] 
 
            #Verifier si le fichier existe et telecharger le fichier Sur S3 
        if client_s3.head_object(Bucket=bucket_name, Key='student_data.csv'): 
            response =client_s3.get_object(Bucket=bucket_name, Key='student_data.csv') 
            s3_data = list(csv.reader(response['Body'].read().decode('ISO-8859-1').splitlines())) 
            s3_data.append(student_data) 
        with open('temp_file.csv', 'w', newline='') as temp_file: 
            csv_writer = csv.writer(temp_file) 
            csv_writer.writerows(s3_data) 
        client_s3.upload_file('temp_file.csv', bucket_name, 'student_data.csv') 
 
 
        # Envoyer le fichier temporaire vers S3 avec l'extension .csv 
        client_s3.upload_file('temp_file.csv', bucket_name, 'student_data.csv') 
        print("Enregistrement sur S3 réussi.") 
 
# Exemple d'utilisation 
student_data = Student('Non','20-24 ans','Licence 4','Canada','Qualité de vie','Études supplémentaires','1-2 ans','Oui') 
student_data.sauvegarder_sur_s3(bucket_name, region_name, access_key, secret_key)