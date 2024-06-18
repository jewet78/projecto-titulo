import re
import subprocess
from os import cpu_count
from mothur import comandos as co
import asyncio
from correr_comandos import run_commands
from nombreCarpetas import ver_carpetas 
#import threading
#import pexpect
#import  time
# Usage example:
#illumnia bacteria v3-v4


def main():

    mothur_init ="./mothur/mothur"
    vc= ver_carpetas()
    variables={
        "filesDir":"./datos/MiSeq",
        "fileVar":"stability.files",
        "prefix":"stability",
        "newFiles":"test5",
        "silvadir":"./datos/silva.bacteria/silva.bacteria/",
        "silva_file":"silva.bacteria",
        "new_name_silva":"silva.v4",
        "procesadores":"auto"
    }
    """
    nombres=vc.ver_carpetas(variables["newFiles"])
    
    aux=variables["newFiles"]

    for nombre in nombres:
        
        variables["newFiles"]=aux+f"/{nombre}"
        print(variables["newFiles"])
        first_pass(mothur_init,variables)
    """
    first_pass(mothur_init,variables)
    #first_pass(mothur_init,variables)

    #p = subprocess.Popen([initMothur], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    
    #monitor_thread = threading.Thread(target=monitor_input, args=(p,))
    #monitor_thread.start()

    # Wait for the monitoring thread to finish or the subprocess to terminate
    #monitor_thread.join()
    #response, error = p.communicate()
    #print(response)
    # p.interact()
    """
    The valid parameters are: fasta, oligos, name, count, group, taxonomy,
    checkorient, ecoli, start, end, nomatch, pdiffs, rdiffs, processors, keepprimer, 
    keepdots, seed, inputdir, and outputdir.
    
    """
    #p.kill()


def first_pass(mothur_init,va):
    rc=run_commands()
    """
    commands=[co.pcr_seqs(va["silva_file"],inputdir=va["silvadir"],outputdir=va["filesDir"]),
            co.rename_file(va["silva_file"],va["new_name_silva"],inputdir=va["filesDir"],outputdir=va["filesDir"]),
            co.make_file(va["filesDir"],va["prefix"],outputdir=va["filesDir"]),
            [co.make_contigs(va["fileVar"],inputdir=va["filesDir"],outputdir=va["filesDir"]),co.summary_seqs()],
            [co.unique_seqs(va["prefix"]+".trim.contigs.fasta",count=va["prefix"]+".contigs.count_table", inputdir=va["filesDir"],outputdir=va["filesDir"]),co.summary_seqs()],
            [co.align_seqs(va["prefix"]+".trim.contigs.fasta",va["new_name_silva"],va["filesDir"],va["filesDir"]),co.summary_seqs()],
            [co.screen_seqs(va["prefix"]+".trim.contigs.fasta",va["prefix"]+".contigs.count_table",inputdir=va["filesDir"],outputdir=va["filesDir"]),co.summary_seqs()],
            [co.filter_seqs(va["prefix"]+".trim.contigs.fasta",inputdir=va["filesDir"],outputdir=va["filesDir"]),co.unique_seqs("current","current",va["filesDir"],va["filesDir"]),co.pre_cluster("current","current",inputdir=va["filesDir"],outputdir=va["filesDir"])],
        ]
    """
    commands=[
        co.make_file(va["newFiles"],va["prefix"],outputdir=va["newFiles"]),
        co.make_contigs(va["fileVar"],inputdir=va["newFiles"],outputdir=va["newFiles"]),
        [co.screen_seqs_uno(va["prefix"]+".trim.contigs.fasta",va["prefix"]+".contigs.count_table",inputdir=va["newFiles"],outputdir=va["newFiles"]), co.summary_seqs()]
    ]
    
    asyncio.run(rc.run_mothur_commands(commands,mothur_init))


if __name__ == "__main__":
    main()