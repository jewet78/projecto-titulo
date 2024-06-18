class comandos:

    def pcr_seqs(fasta, keepdots="F", start=11894, end=25319,inputdir="",outputdir=""):
        command= f"pcr.seqs(fasta={fasta}.fasta, start={start}, end={end}, keepdots={keepdots},inputdir={inputdir},outputdir={outputdir})"
        return command

    def rename_file(input_file, new_name,inputdir="",outputdir=""):
        command= f"rename.file(input={input_file}.pcr.fasta, new={new_name},inputdir={inputdir},outputdir={outputdir})"
        return command

    def make_file(inputdir, prefix, type="fastq",outputdir=""):
        command= f"make.file(inputdir={inputdir}, type={type}, prefix={prefix},outputdir={outputdir})"
        return command

    def make_contigs(file, maxambig=0, maxlength=275, maxhomop=8,inputdir="",outputdir=""):
        command= f"make.contigs(file={file}, maxambig={maxambig}, maxlength={maxlength}, maxhomop={maxhomop},inputdir={inputdir},outputdir={outputdir})"
        return command

    def unique_seqs(fasta, count,inputdir="",outputdir=""):
        command= f"unique.seqs(fasta={fasta}.trim.contigs.fasta, count={count}.contigs.count_table,inputdir={inputdir},outputdir={outputdir})"
        return command

    def align_seqs(fasta, reference,inputdir="",outputdir=""):
        command= f"align.seqs(fasta={fasta}, reference={reference},inputdir={inputdir},outputdir={outputdir})"
        return command
    
    def screen_seqs_uno(fasta, count, maxambig=0, maxlength=275, maxhomop=8,inputdir="",outputdir=""):
        command= f"screen.seqs(fasta={fasta}, count={count}, maxambig={maxambig}, maxlength={maxlength}, maxhomop={maxhomop},inputdir={inputdir},outputdir={outputdir})"
        return command
    
    def screen_seqs(fasta, count, start=1969, end=11551,inputdir="",outputdir=""):
        command= f"screen.seqs(fasta={fasta}, count={count}, start={start}, end={end},inputdir={inputdir},outputdir={outputdir})"
        return command

    def filter_seqs(fasta, vertical="T", trump=".",inputdir="",outputdir=""):
        command= f"filter.seqs(fasta={fasta}, vertical={vertical}, trump={trump},inputdir={inputdir},outputdir={outputdir})"
        return command

    def unique_seqs(fasta, count,inputdir="",outputdir=""):
        command= f"unique.seqs(fasta={fasta}, count={count},inputdir={inputdir},outputdir={outputdir})"
        return command

    def pre_cluster(fasta, count, diffs=2,inputdir="",outputdir=""):
        command= f"pre.cluster(fasta={fasta}, count={count}, diffs={diffs},inputdir={inputdir},outputdir={outputdir})"
        return command

    def chimera_vsearch(fasta, count, dereplicate="t",inputdir="",outputdir=""):
        command= f"chimera.vsearch(fasta={fasta}, count={count}, dereplicate={dereplicate},inputdir={inputdir},outputdir={outputdir})"
        return command

    def classify_seqs(fasta, count, reference, taxonomy,inputdir="",outputdir=""):
        command= f"classify.seqs(fasta={fasta}, count={count}, reference={reference}, taxonomy={taxonomy},inputdir={inputdir},outputdir={outputdir})"
        return command

    def remove_lineage(fasta, count, taxonomy, taxon="Chloroplast-Mitochondria-unknown-Archaea-Eukaryota",inputdir="",outputdir=""):
        command= f"remove.lineage(fasta={fasta}, count={count}, taxonomy={taxonomy}, taxon={taxon},inputdir={inputdir},outputdir={outputdir})"
        return command

    def remove_groups(count, fasta, taxonomy, groups='Mock',inputdir="",outputdir=""):
        command= f"remove.groups(count={count}, fasta={fasta}, taxonomy={taxonomy}, groups={groups},inputdir={inputdir},outputdir={outputdir})"
        return command

    def cluster_split(fasta, count, taxonomy, taxlevel=4, cutoff=0.03,inputdir="",outputdir=""):
        command= f"cluster.split(fasta={fasta}, count={count}, taxonomy={taxonomy}, taxlevel={taxlevel}, cutoff={cutoff},inputdir={inputdir},outputdir={outputdir})"
        return command

    def make_shared(list, count, label=0.03,inputdir="",outputdir=""):
        command= f"make.shared(list={list}, count={count}, label={label},inputdir={inputdir},outputdir={outputdir})"
        return command

    def classify_otu(list, count, taxonomy, label=0.03,inputdir="",outputdir=""):
        command= f"classify.otu(list={list}, count={count}, taxonomy={taxonomy}, label={label},inputdir={inputdir},outputdir={outputdir})"
        return command

    def phylotype(taxonomy,inputdir="",outputdir=""):
        command= f"phylotype(taxonomy={taxonomy},inputdir={inputdir},outputdir={outputdir})"
        return command

    def make_shared_label_one(list, count,inputdir="",outputdir=""):
        command= f"make.shared(list={list}, count={count}, label=1,inputdir={inputdir},outputdir={outputdir})"
        return command

    def classify_otu_label_one(list, count, taxonomy,inputdir="",outputdir=""):
        command= f"classify.otu(list={list}, count={count}, taxonomy={taxonomy}, label=1,inputdir={inputdir},outputdir={outputdir})"
        return command

    def make_shared_count_current(count,inputdir="",outputdir=""):
        command= f"make.shared(count={count},inputdir={inputdir},outputdir={outputdir})"
        return command

    def classify_otu_label_asv(list, count, taxonomy,inputdir="",outputdir=""):
        command= f"classify.otu(list={list}, count={count}, taxonomy={taxonomy}, label=ASV,inputdir={inputdir},outputdir={outputdir})"
        return command

    def dist_seqs_lt(fasta, output='lt',inputdir="",outputdir=""):
        command= f"dist.seqs(fasta={fasta}, output={output},inputdir={inputdir},outputdir={outputdir})"
        return command

    def clearcut(phylip,inputdir="",outputdir=""):
        command= f"clearcut(phylip={phylip},inputdir={inputdir},outputdir={outputdir})"
        return command

    def summary_seqs():
        command="summary.seqs(fasta=current)"
        return command
