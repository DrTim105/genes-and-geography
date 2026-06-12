
# Data Download Instructions

Raw data is NOT included in this repo (files are too large for GitHub).
All data is freely available. Place downloaded files in `data/raw/`.

--- 

## Paper being replicated
Novembre J et al. "Genes mirror geography within Europe."
Nature 456:98-101 (2008). https://www.nature.com/articles/nature07331

--- 

## Required files

### 1. Chromosome 22 VCF + index (1000 Genomes Phase 1)
```bash
curl -O "https://42basepairs.com/download/s3/1000genomes/release/20110521/ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz"

curl -O "https://42basepairs.com/download/s3/1000genomes/release/20110521/ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz.tbi"
```

Backup source (official EBI FTP, slower):
```bash
wget "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz"

wget "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20110521/ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz.tbi"
```

### 2. Sample panel file (maps sample ID to population code)
```bash
curl -O "https://42basepairs.com/download/s3/1000genomes/release/20110521/phase1_integrated_calls.20101123.ALL.panel"
```

### 3. Population descriptions
Download `igsr_populations.tsv` from:
https://www.internationalgenome.org/data-portal/population
Click "Download the list" and save as `igsr_populations.tsv` in `data/raw/`.

If you don't have curl, replace `curl -O` with `wget` for each command.

--- 

## Directory structure after download
- data/raw/ 

- ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz

- ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz.tbi

- phase1_integrated_calls.20101123.ALL.panel

- igsr_populations.tsv

All four files must be present before running scripts/01_parse_vcf.py.
--- 

## Note on the tabix index 
The .tbi file must have exactly the same base name as the .vcf.gz file 
and must be in the same directory. 
If pysam reports a missing index, you can regenerate it with: 

```bash
tabix -p vcf ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz 
```
--- 

## Data citation An integrated map of genetic variation from 1,092 human genomes. Nature 491:56-65 (2012). DOI: 10.1038/nature11632 
https://www.nature.com/articles/nature11632

