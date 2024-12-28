from Bio.Seq import Seq
from Bio import SeqIO
from Bio import pairwise2
from Bio.SeqUtils import MeltingTemp as mt
import re

# Constants
PAM_SEQUENCE = "NGG"  # PAM sequence for Streptococcus pyogenes Cas9
GUIDE_RNA_LENGTH = 20  # Length of the guide RNA

def find_pam_sites(dna_sequence, pam_sequence=PAM_SEQUENCE):
    """
    Find all potential PAM sites in a DNA sequence.
    """
    # Regular expression for PAM sequence
    pam_regex = pam_sequence.replace("N", ".")
    target_sites = []
    
    # Search for PAM sites
    for match in re.finditer(f"(?=({pam_regex}))", dna_sequence):
        pam_start = match.start()
        pam_site = match.group(1)
        guide_rna_start = pam_start - GUIDE_RNA_LENGTH
        if guide_rna_start >= 0:
            guide_rna = dna_sequence[guide_rna_start:pam_start]
            target_sites.append((guide_rna_start, guide_rna, pam_site))

def dna_polymerase(template_strand):
    """
    Simulate DNA polymerase activity by synthesizing a complementary DNA strand.
    
    Parameters:
    template_strand (str): The template strand of DNA to be replicated.

    Returns:
    str: The newly synthesized complementary DNA strand.
    """
    # DNA base pairing rules
    base_pairing = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    
    # Initialize the new strand
    new_strand = ""
    
    # Synthesize the new strand based on the template strand
    for base in template_strand:
        new_strand += base_pairing[base]
    
    return new_strand

# Example usage
template_strand = "ATCGGCTA"
new_strand = dna_polymerase(template_strand)
print("Template Strand: ", template_strand)
print("New Strand:      ", new_strand)

# Constants
PAM_SEQUENCE = "NGG"  # Typical PAM sequence for Cas9
GUIDE_RNA_LENGTH = 20

def find_target_sites(dna_sequence, pam_sequence=PAM_SEQUENCE):
    """
    Find all potential CRISPR-Cas9 target sites in a DNA sequence.
    """
    target_sites = []
    for match in re.finditer(f"(?=([ATCG]{{{GUIDE_RNA_LENGTH}}}{pam_sequence}))", dna_sequence):
        target_sites.append((match.start(), match.group(1)))
    return target_sites

def design_guide_rna(target_site):
    """
    Design a guide RNA for a given target site.
    """
    return target_site[:GUIDE_RNA_LENGTH]

def find_off_target_sites(dna_sequence, guide_rna, max_mismatches=3):
    """
    Find potential off-target sites for a given guide RNA in a DNA sequence.
    """
    off_target_sites = []
    for i in range(len(dna_sequence) - GUIDE_RNA_LENGTH + 1):
        segment = dna_sequence[i:i + GUIDE_RNA_LENGTH]
        mismatches = sum(1 for a, b in zip(segment, guide_rna) if a != b)
        if mismatches <= max_mismatches:
            off_target_sites.append((i, segment, mismatches))
    return off_target_sites

def calculate_melting_temperature(seq):
    """
    Calculate the melting temperature of a DNA sequence.
    """
    return mt.Tm_NN(seq)

def main():
    # Load a DNA sequence (example sequence)
    dna_sequence = "AGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCT"

    # Find target sites
    target_sites = find_target_sites(dna_sequence)
    print("Potential CRISPR-Cas9 Target Sites:")
    for start, site in target_sites:
        print(f"Position: {start}, Site: {site}")
    
    # Design guide RNAs for each target site
    guide_rnas = [design_guide_rna(site) for _, site in target_sites]
    print("\nDesigned Guide RNAs:")
    for gRNA in guide_rnas:
        print(f"Guide RNA: {gRNA}, Melting Temperature: {calculate_melting_temperature(gRNA):.2f} °C")
    
    # Find off-target sites for each guide RNA
    for gRNA in guide_rnas:
        off_target_sites = find_off_target_sites(dna_sequence, gRNA)
        print(f"\nOff-Target Sites for Guide RNA {gRNA}:")
        for pos, seq, mismatches in off_target_sites:
            print(f"Position: {pos}, Sequence: {seq}, Mismatches: {mismatches}")

if __name__ == "__main__":
    main()
