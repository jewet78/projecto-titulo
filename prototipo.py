from Bio import SeqIO
from tensorflow import keras as kr
import numpy as np
import tensorflow as tf


import glob
from nombreCarpetas import ver_carpetas
import pandas as pd
import joblib
import time
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def get_fastq_files(path):
    #print(f'{path}/*.fastq')
    fastq_files = glob.glob(f'{path}/*.fastq')  # This pattern assumes the files are in subdirectories, adjust it as needed
    #print(fastq_files)
    file_groups = {}
    for file in fastq_files:
        file_name = file.split('/')[-1]  # Extract the file name
        prefix = file_name.split('_')[0]  # Extract the prefix before the first underscore
        if prefix in file_groups:
            file_groups[prefix].append(file)
        else:
            file_groups[prefix] = [file]

    return file_groups

def buscar_archivos(path):
    
    fastq_files = glob.glob(f'{path}/*.fastq',recursive=True)  # This pattern assumes the files are in subdirectories, adjust it as needed

    return fastq_files

def buscar_archivos_fastq(path):
    
    fastq_files = glob.glob(f'{path}/*.fastq',recursive=True)  # This pattern assumes the files are in subdirectories, adjust it as needed

    return fastq_files

def obtener_archivos():
    vc= ver_carpetas()
    folders_path="../tutorialM/datos/sets2"
    #folders_path="test"

    nombres=vc.ver_carpetas(folders_path)
    print(f"numero carpetas:{len(nombres)}")
    paths=[]
    for nombre in nombres:
        paths.append(folders_path+"/"+nombre)
    print(f"ejemplo {paths[0]}")
    print(buscar_archivos(paths[0]))
    print(f"largo de paths: {len(paths)}")
    
    return paths

def process_paired_fastq_files(file1, file2,modelo):
    sequences_r1 = []
    sequences_r2 = []
    qualities_f = []
    qualities_r= []
    aux=[]

    aux2=0
    aux3=0

    with open(file1, "r") as handle1, open(file2, "r") as handle2:
        for record1, record2 in zip(SeqIO.parse(handle1, "fastq"), SeqIO.parse(handle2, "fastq")):
            assert record1.id.split()[0] == record2.id.split()[0], "Mismatch in paired reads"
            R1_id_mod= record1.id.split()[0].replace(":", "_")
            # Append sequences from both files separately
            seq1 = str(record1.seq)
            seq2 = str(record2.seq)
            aux2+=1
            max_len = max(len(seq1), len(seq2))
            if len(seq1) < max_len:
                seq1 += 'N' * (max_len - len(seq1))
            else:
                seq2 += 'N' * (max_len - len(seq2))
            
            
            len_diff1 = len(seq1) - len(record1.letter_annotations["phred_quality"])
            if len_diff1 > 0:
                record1.letter_annotations["phred_quality"].extend([0] * len_diff1)
            len_diff2 = len(seq2) - len(record2.letter_annotations["phred_quality"])
            if len_diff2 > 0:
                record2.letter_annotations["phred_quality"].extend([0] * len_diff2)
            
            datos=discriminar_secuencia(record1.letter_annotations["phred_quality"],record2.letter_annotations["phred_quality"],modelo)
            existe = modelo.predict(datos)
            
            if int(existe[0])==1:
                aux3=aux3+1
                aux.append(R1_id_mod)
                sequences_r1.append(seq1)
                qualities_f.append(record1.letter_annotations["phred_quality"])
                sequences_r2.append(seq2)
                qualities_r.append(record2.letter_annotations["phred_quality"])
    print(aux2)
    return np.array(sequences_r1),np.array(sequences_r2),qualities_f,qualities_r,aux

def encode_sequence_with_quality(sequence, quality_scores):
    mapping = {
            'A': [1, 0, 0, 0],
            'C': [0, 1, 0, 0],
            'G': [0, 0, 1, 0],
            'T': [0, 0, 0, 1],
            'M': [0.5, 0.5, 0, 0],
            'R': [0.5, 0, 0.5, 0],
            'W': [0.5, 0, 0, 0.5],
            'S': [0, 0.5, 0.5, 0],
            'Y': [0, 0.5, 0, 0.5],
            'K': [0, 0, 0.5, 0.5],
            'V': [0.33, 0.33, 0, 0.33],
            'H': [0.33, 0.33, 0.33, 0],
            'D': [0.33, 0, 0.33, 0.33],
            'B': [0, 0.33, 0.33, 0.33],
            'N': [0.25, 0.25, 0.25, 0.25],
        }

    encoded_sequence = []
    norm_quality=[]
    for i, base in enumerate(sequence):
        base_encoding =  mapping.get(base)
        if(quality_scores[i]):
            quality = quality_scores[i]

        else:
                quality=0
        normalized_quality = 1.0 if quality >= 50 else (quality - 30) / 20 if quality > 30 else 0.0

        encoded_sequence.append(base_encoding)
        norm_quality.append(normalized_quality)
        
    return np.array(encoded_sequence),np.array(norm_quality)

def encode_fastq(sequences,quality,max_sequence_length=253):
    encoded_sequences = []
    normal_qualities=[]
    for qual,seq in zip(quality,sequences):
        if len(seq) < max_sequence_length:
            seq += 'N' * (max_sequence_length - len(seq))
            qual.extend([0] * len(seq))# Pad sequence with 'N' to reach max length
        encoded_seq,norm_qual = encode_sequence_with_quality(seq[:max_sequence_length],qual)  # Truncate or pad to fixed length
        encoded_sequences.append(encoded_seq)
        normal_qualities.append(norm_qual)
    return np.array(encoded_sequences),np.array(normal_qualities)

def contar_calidades2(calidades):
    qual1=0
    qual2=0
    for cal in calidades:
        
        if cal < 30:
            qual1=qual1+1
        else:
            qual2=qual2+1# Si el número es mayor que 50, devolver 1
    return qual1,qual2

def procesar_calidades(calidad):

    sum_cal_buenas,sum_cal_malas=contar_calidades2(calidad)
    promedio_cal=promediar_cal(calidad)
        
    return sum_cal_buenas,sum_cal_malas,promedio_cal


def promediar_cal(calidad):
    cal=np.array(calidad)
    suma=np.sum(cal)
    return round(suma/len(cal), 2)


def formar_datos(cal_fr,cal_rv):
    
    atributos_fr=procesar_calidades(cal_fr)
    atributos_rv=procesar_calidades(cal_rv)
    datos_para_modelo=np.concatenate((atributos_fr,atributos_rv),axis=0)
    return datos_para_modelo
    
def discriminar_secuencia(cal_fr,cal_rv,modelo):
    datos=formar_datos(cal_fr,cal_rv)
    #print(datos.shape)
    datos=datos.reshape(1, -1)

    return datos
    
def decode(valor):
    mapping = {
        'A': [1, 0, 0, 0],
        'C': [0, 1, 0, 0],
        'G': [0, 0, 1, 0],
        'T': [0, 0, 0, 1],
        'M': [0.5, 0.5, 0, 0],
        'R': [0.5, 0, 0.5, 0],
        'W': [0.5, 0, 0, 0.5],
        'S': [0, 0.5, 0.5, 0],
        'Y': [0, 0.5, 0, 0.5],
        'K': [0, 0, 0.5, 0.5],
        'V': [0.33, 0.33, 0, 0.33],
        'H': [0.33, 0.33, 0.33, 0],
        'D': [0.33, 0, 0.33, 0.33],
        'B': [0, 0.33, 0.33, 0.33],
        'N': [0.25, 0.25, 0.25, 0.25],
    }

    for key, value in mapping.items():
        if all(abs(v - vi) <= 0.15 for v, vi in zip(value, valor)):
            return key
    return 'N'
    

def guardar_secuencias(items_seqs,modelo,inicio,path):
    
    
    encoded_fr,qual_fr=encode_fastq(items_seqs[0],items_seqs[2])
    encoded_rv,qual_rv=encode_fastq(items_seqs[1],items_seqs[3])
    prediccion=modelo.predict(x=[encoded_fr,encoded_rv,qual_fr,qual_rv])
        
    fin=time.time()
    print(fin-inicio)
    with open(f"{path}/secuencia.fasta", "w") as output_handle:
        for i in range(0,len(encoded_fr)):
            #print(encoded_fr[0][i])
            #print((encoded_fr[i]).shape)
            #prediccion=modelo.predict(x=[encoded_fr[i],encoded_rv[i],qual_fr[i],qual_rv[i]])
            
            aux=[]
            #print(">>",i)
            #print(prediccion[i])
            for item in prediccion[i]:
                #print(item)
                aux.append(decode(item))
            #print(aux)
            aux = ''.join(aux)
            seq = Seq(aux)
            record = SeqRecord(seq, id=items_seqs[4][i],name=items_seqs[4][i],description='')
            #print(seq)
            
            #print(record)

            # Escribir el archivo FASTA
            SeqIO.write(record, output_handle, "fasta")

def main():
    

    modelo_seleccion=joblib.load(f'rl_m_{554}.joblib')
    modelo_cnn_seleccionado= tf.keras.models.load_model('elegidos/elegidos/cnn_nolstm_4i29.keras')   
    inicio = time.time()
    #path='test4'
    path='test4'
    aux=get_fastq_files(path)
    #print(aux)
    
    aux1=[]
    aux2=[]
    aux3=[]
    aux4=[]
    aux5=[]
    
    for key in aux:
        #print(aux[key][0], aux[key][1])
        items_seqs=process_paired_fastq_files(aux[key][0], aux[key][1],modelo_seleccion)
        aux1.extend(items_seqs[0])
        aux2.extend(items_seqs[1])
        aux3.extend(items_seqs[2])
        aux4.extend(items_seqs[3])
        aux5.extend(items_seqs[4])
    print(len(aux2))
    guardar_secuencias([aux1,aux2,aux3,aux4,aux5],modelo_cnn_seleccionado,inicio,path)
    



if __name__ == "__main__":
    main()