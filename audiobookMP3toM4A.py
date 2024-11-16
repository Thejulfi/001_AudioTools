import os
from pydub import AudioSegment

def merge_mp3_files(input_folder, output_file, title, author, cover_image=None):
    # Récupération des fichiers MP3 du dossier, triés par leur numéro
    mp3_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.mp3')],
                       key=lambda x: int(x.split('.')[0]))

    # Chargement et concaténation des fichiers audio
    combined_audio = AudioSegment.empty()
    for mp3 in mp3_files:
        file_path = os.path.join(input_folder, mp3)
        audio = AudioSegment.from_mp3(file_path)
        combined_audio += audio

    # Exportation du fichier M4B
    combined_audio.export(output_file, format="mp4", codec="aac")

    # Ajouter les métadonnées (titre, auteur, couverture)
    add_metadata(output_file, title, author, cover_image)

def add_metadata(output_file, title, author, cover_image):
    try:
        # Création de la commande ffmpeg pour ajouter les métadonnées
        ffmpeg_command = [
            'ffmpeg', '-i', output_file, 
            '-metadata', f'title={title}', 
            '-metadata', f'artist={author}', 
            '-metadata', f'album={title}'
        ]

        if cover_image:
            ffmpeg_command += ['-i', cover_image, '-map', '0', '-map', '1', '-c:v', 'png', '-c:a', 'aac']

        # Réexécuter la commande ffmpeg pour intégrer les métadonnées et la couverture
        ffmpeg_command += [output_file]
        os.system(" ".join(ffmpeg_command))

        print(f"Fichier {output_file} créé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ajout des métadonnées : {e}")

# Exemple d'utilisation
input_folder = '/Users/julienfichet/Downloads/Le_mythe_de_Sisyphe'  # Remplacer par le chemin vers ton dossier contenant les fichiers MP3
output_file = '/Users/julienfichet/Downloads/Le_mythe_de_Sisyphe/LeMytheDeSisyphe.m4b'  # Chemin de sortie du fichier M4B final
title = "Le Mythe de Sisyphe"  # Remplacer par le titre du livre
author = "Albert Camus"  # Remplacer par le nom de l'auteur
cover_image = '/Users/julienfichet/Downloads/Image1276x2102.jpg'  # Optionnel, chemin vers l'image de couverture (peut être None)

merge_mp3_files(input_folder, output_file, title, author, cover_image)
