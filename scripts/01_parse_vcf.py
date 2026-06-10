# scripts/01_parse_vcf.py
# =========================================================================
# PURPOSE: Parse the 1000 Genomes Phase 1 chromosome 22 VCF,
# build a genotype matrix, add population labels, write to CSV
# for downstream PCA and visualization.
# =========================================================================

from pysam import VariantFile # reads the compressed VCF
import numpy as np
import pandas as pd

# ---- CONFIGURATION ----
VCF_PATH = '/Users/tim/bioinformatics-portfolio/01b-genes-and-geography/data/raw/ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz'
PANEL_PATH = '/Users/tim/bioinformatics-portfolio/01b-genes-and-geography/data/raw/phase1_integrated_calls.20101123.ALL.panel'
OUTPUT_PATH = '/Users/tim/bioinformatics-portfolio/01b-genes-and-geography/data/processed/matrix.csv'

# keep every Nth variant. 100 gives ~5000 variants from chr22 -- 
# enough for clear structure, fast enough to finish in minutes.
SAMPLE_EVERY_N = 100

# Approximate total variants in chr22 Phase 1 (for progress %)
TOTAL_VARIANTS = 494328

print('=== Step 1: Parsing VCF ===')

genotypes = [] # will hold allele-count tuples per sampled variant
samples = [] # will hold sample IDs from the VCF header
variant_ids = [] # will hold sample variants IDs

with VariantFile(VCF_PATH) as vcf:
    counter = 0

    for record in vcf:
        counter += 1

        # Print progress every 1% of the file
        if counter % (TOTAL_VARIANTS // 100) == 0:
            pct = round(100 * counter / TOTAL_VARIANTS)
            print(f' {pct}%({counter}/{TOTAL_VARIANTS})')

        # Sub-samsple: keep only every Nth variant.
        # 'continue' skips the rest of the loop for this variant.
        if counter % SAMPLE_EVERY_N!=0:
            continue

        # For each sample, grab its (allele1, allele2) tuple.
        # 0 = reference allele, 1 = first alternate allele.
        alleles = [
            record.samples[s].allele_indices 
            for s in record.samples
        ]

        # Capture sample names ONCE (same for every variant).
        if not samples:
            samples = list(record.samples)

        # Store this variant's alleles and its ID
        genotypes.append(alleles)
        variant_ids.append(record.id if record.id else f'{record.chrom}:{record.pos}')

print(f'\nDone. Sampled {len(genotypes)} variants from {counter} total.')

# ---- BUILD THE NUMPY MATRIX ----
print('\n=== Step 2: Buildign genotype matrix ===')

# Convert the nested list into a numpy array.
# Shape: (n_variants, n_samples, 2) == the 2 is the two alleles.
genotypes_np = np.array(genotypes)
print(f'Raw shape (variants x samples x alleles): {genotypes_np.shape}')

# Count non-zero alleles per sample per variant
# This collapses the allele dimension:
# (0,0) -> 0 homozygous reference
# (0,1) -> 1 heterozygous
# (1,1) -> 2 homozygous alternate

matrix = np.count_nonzero(genotypes_np, axis=2)
print(f' After collapse(variants x samples): {matrix.shape}')

# Transpose so rows = samples, columns = variants as this is the orientation scikit-learn PCA expects
matrix = matrix.T
print(f' After transpose (samples x variants): {matrix.shape}')

# ---- LOAD POPULATION LABELS ----
print('\n=== Step 3: Loading population labels ===')

# Build a dictionary: sample_id -> population_code
labels = {}
with open(PANEL_PATH) as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 2 and parts [0] != 'sample': # skip header
            labels[parts[0]] = parts[1]

print(f' Loaded labels for {len(labels)} samples.')

# --- BUILD DATAFRAME AND WRITE CSV ----
print('\n=== Step 4: Building DataFrame and writing CSV ===')

# Each row = one sample; columns = variant IDs.
df = pd.DataFrame(matrix, columns=variant_ids, index=samples)

# Add the population code by looking up each sample in our dictionary.
df['Population code'] = df.index.map(labels)

# Make the sample index into a normal column called 'Sample'
df.index.name = 'Sample'
df.reset_index(inplace=True)

print(f' DataFrame shape: {df.shape}')

# Write to CSV for the visualization notebook.
df.to_csv(OUTPUT_PATH, index=False)
print(f'\nMatrix written to {OUTPUT_PATH}')

