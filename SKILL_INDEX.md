# Skill Index

ScholarFlow Skills 的可安装 skill 索引。每个条目都是独立工作流，可以按任务单独安装，也可以按产品线成套安装。

当前发布包包含 230 个 skill。

## Nature Research Suite

| Skill | 用途 |
|---|---|
| `nature-academic-search` | Multi-source literature search, citation verification, MeSH search strategy, citation file management (.nbib/.ris/.bib conversion), and reference management (BibTeX, related art... |
| `nature-citation` | Add strict Nature/CNS citations to manuscript text by splitting long passages into citable segments, searching only accepted flagship and subjournal titles from Nature Portfolio... |
| `nature-data` | Prepare, audit, or revise Nature-ready Data Availability statements, data repository plans, dataset citations, and FAIR metadata checklists for manuscripts. Use when the user as... |
| `nature-downloader` | Use this skill whenever the user wants to configure school/library access, reuse a logged-in Chrome institutional session, search library databases, download legitimate open-acc... |
| `nature-experiment-log` | 标准化实验日志记录——接收原始材料（图/语音/文字），产出带 YAML frontmatter 的标准日志到 Obsidian vault。需配合飞书 CLI 或手动输入使用。 |
| `nature-figure` | Submission-grade Nature/high-impact journal figure workflow for Python or R. Use whenever the user asks to create, revise, audit, or polish manuscript figures, multi-panel scien... |
| `nature-literature-pipeline` | Complete automated literature discovery pipeline: multi-source search → six-dimension scoring → fine reading → formatted delivery → archival. Combines a configurable engine with... |
| `nature-paper-to-patent` | Convert scientific papers, theses, technical reports, source code, figures, or research manuscripts into evidence-grounded Chinese invention patent drafts. Use when an AI agent... |
| `nature-paper2ppt` | Build a complete but efficient Nature-style Chinese PPTX presentation from a scientific paper, preprint, PDF, article text, abstract, figure legends, or reading notes. Use this... |
| `nature-polishing` | Polish, restructure, or translate academic prose into Nature-leaning English using writing-strategy principles, curated Nature/Nature Communications article patterns, and phrase... |
| `nature-reader` | Build full-paper Chinese-English side-by-side, figure/table-aware, source-grounded Markdown readers for journal or conference papers from PDF, DOI, arXiv, publisher HTML, or pas... |
| `nature-response` | Draft, audit, or revise point-by-point reviewer response letters for Nature-family manuscript revisions. Use when the user provides reviewer comments, editor decision letters, r... |
| `nature-reviewer` | Simulate a Nature-style reviewer assessment from the referee perspective rather than an author rebuttal. Use when the user wants a pre-submission review, reviewer report, peer-r... |
| `nature-writing` | Draft, restructure, or plan Nature-style manuscript sections from author-provided claims, results, figures, notes, or Chinese drafts. Use when the user wants to write or rebuild... |

## PaperSpine & Literature Ops

| Skill | 用途 |
|---|---|
| `paper-harbor` | 文献港。自动化检索、筛选并把文献元数据保存到 Zotero。适用于用户要从 ScienceDirect 或中国知网按关键词、影响因子、出版时间和数量生成候选清单、优先级清单、Zotero 入库清单和可追踪输出目录。默认不下载 PDF/HTML 全文，禁止绕过登录、付费墙、验证码或机构权限限制。 |
| `paper-spine` | End-to-end research manuscript workflow that turns materials, target venue, literature evidence, motivation, outline, drafting, rewriting, translation, humanization, LaTeX, and... |
| `paper-spine-audit` | Audits PaperSpine outputs for missing artifacts, shallow revisions, logic transfer, unsupported claims, and translation coverage. |
| `paper-spine-build` | Builds a paper or report from materials using the shared PaperSpine research, motivation, and rationale workflow. |
| `paper-spine-citation` | Builds a citation support bank for Introduction, Discussion, and background claims. |
| `paper-spine-humanize` | Reduces AI detection rates via tiered stylistic constraints mapped to real AIGC detection dimensions. Produces a teaching humanize_matrix.md. |
| `paper-spine-intake` | Collects PaperSpine workflow options and writes config for flash/pro, scene, language, and inputs. |
| `paper-spine-latex` | Handles LaTeX project assembly, figure placement, citations, labels, and compile-safe cleanup. |
| `paper-spine-research` | Researches target requirements, downloads reference materials, learns strong examples, and prepares motivation options. |
| `paper-spine-rewrite` | Rewrites an existing manuscript from confirmed motivation, research, paragraph-level rationale, and evidence. |
| `paper-spine-translate` | Produces the complete translation_zh/ package with row-by-row translation of all required artifacts and full-paper translation. |
| `paper-spine-ui` | Launches the PaperSpine external terminal configuration UI for Codex and Claude Code. |

## Academic Writing & Integrity

| Skill | 用途 |
|---|---|
| `academic-paper` | Route academic paper outlining, drafting, abstract writing, revision, citation formatting, AI disclosure, LaTeX/DOCX/PDF formatting guidance, and manuscript improvement to Paper... |
| `academic-pipeline` | End-to-end research-to-paper pipeline routing: question refinement, deep research, outline, drafting, citation/integrity gates, reviewer simulation, revision, figures, data chec... |
| `ai-check` | Audit academic text for AI-like patterns, disclosure needs, citation integrity, unsupported claims, writing artifacts, and manuscript quality risks. Route to PaperSpine humaniza... |
| `aigc-down-skill` | Reduce AIGC-like writing artifacts in academic text by routing to paper-spine-humanize and nature-polishing, with a change matrix and preservation of scientific meaning. |
| `deep-research` | Route deep research, literature review, systematic review, meta-analysis, fact-checking, research question refinement, and evidence mapping requests to ScholarFlow literature, r... |
| `deep-research-review` | Review, audit, and stress-test deep research outputs, literature reviews, evidence maps, systematic review drafts, and research claims with ScholarFlow reviewer, citation, and i... |
| `humanize` | Humanize academic or professional writing by reducing formulaic AI-like patterns while preserving meaning, evidence, tone, and citation integrity. Alias for paper-spine-humanize... |
| `journal-selection-advisor` | Help users choose suitable Chinese or English journals for a manuscript through guided intake, manuscript-journal fit analysis, tiered journal recommendations, JCR/CAS/disciplin... |
| `journal-submission-normalizer` | Find official Chinese or English journal author instructions, extract submission and formatting requirements, and normalize manuscripts before submission. Use when the user asks... |
| `manuscript-writing` | Route manuscript drafting, restructuring, abstract writing, results narration, discussion framing, cover letters, and journal-style polishing to PaperSpine, Nature writing, Natu... |
| `omics-analysis` | Route omics analysis planning, QC, bioinformatics workflow design, multi-omics data interpretation, figures, reproducibility checks, and manuscript-ready reporting across instal... |
| `paper-self-review` | This skill should be used when the user asks to "review paper quality", "check paper completeness", "validate paper structure", "self-review before submission", "audit claims",... |
| `peer-review` | Structured manuscript/grant review with checklist-based evaluation. Use when writing formal peer reviews with specific criteria methodology assessment, statistical validity, rep... |
| `reference-checker` | Exhaustively verify English and Chinese manuscript references before journal submission. Use when checking whether references are real, accurate, complete, traceable, and format... |
| `research-integrity-guardrail` | Research-paper integrity and quality guardrail for academic manuscripts, AutoResearch-style outputs, literature reviews, methods/results sections, appendices, rebuttals, grant t... |
| `research-paper-writing` | Improve academic paper writing quality for ML/CV/NLP-style papers with clear section structure, paragraph flow, and reviewer-facing presentation. Use when drafting or revising A... |
| `review-response` | Systematic review response workflow from comment analysis to professional rebuttal writing. Use when the user asks to "write rebuttal", "respond to reviewers", "draft review res... |

## Bio & Omics Toolkit

| Skill | 用途 |
|---|---|
| `bakta-genome-annotation` | Annotate bacterial and archaeal genomes and plasmids with Bakta's Prodigal/HMM/diamond pipeline. Identifies CDS, ncRNA, tRNA, rRNA, tmRNA, sORFs, CRISPR arrays, oriC/oriV/oriT,... |
| `bcftools-variant-manipulation` | CLI for VCF/BCF: filter, merge, annotate, query, normalize, compute stats. Core post-variant-calling: quality filtering, multi-sample merging, rsID annotation, genotype extracti... |
| `bio-alignment-filtering` | Filter alignments by flags, mapping quality, and regions using samtools view and pysam. Use when extracting specific reads, removing low-quality alignments, or subsetting to tar... |
| `bio-alignment-indexing` | Create and use BAI/CSI indices for BAM/CRAM files using samtools and pysam. Use when enabling random access to alignment files or fetching specific genomic regions. |
| `bio-alignment-sorting` | Sort alignment files by coordinate or read name using samtools and pysam. Use when preparing BAM files for indexing, variant calling, or paired-end analysis. |
| `bio-alignment-validation` | Validate alignment quality with insert size distribution, proper pairing rates, GC bias, strand balance, and other post-alignment metrics. Use when verifying alignment data qual... |
| `bio-bam-statistics` | Generate alignment statistics using samtools flagstat, stats, depth, coverage, and mosdepth. Use when assessing alignment quality, calculating coverage, or generating QC reports. |
| `bio-basecalling` | Convert raw Nanopore signal data (FAST5/POD5) to nucleotide sequences using Dorado basecaller. Covers model selection, GPU acceleration, modified base detection, and quality fil... |
| `bio-batch-downloads` | Download large datasets from NCBI efficiently using EPost, history server, batching, rate limiting, and retry logic. Use when bulk-fetching tens of thousands of sequences, pulli... |
| `bio-batch-processing` | Process multiple sequence files in batch using Biopython. Use when working with many files, merging/splitting sequences, or automating file operations across directories. |
| `bio-blast-searches` | Run remote BLAST searches against NCBI servers using Biopython Bio.Blast.NCBIWWW. Use when identifying unknown sequences, finding homologs, picking the correct BLAST program (bl... |
| `bio-codon-usage` | Analyze codon usage, calculate CAI (Codon Adaptation Index), and examine synonymous codon bias using Biopython. Use when analyzing coding sequences for expression optimization o... |
| `bio-comparative-genomics-genome-distance-and-species-delineation` | Compute genome-to-genome distances (ANI, AAI, dDDH, k-mer Mash) and assign taxonomic classifications using skani (Shaw 2023), FastANI (Jain 2018), pyani / pyANI ANIb / ANIm, Ort... |
| `bio-comparative-genomics-hgt-detection` | Detect horizontal gene transfer (HGT / LGT) using compositional methods (GC%, codon usage, tetranucleotide z-scores via SIGI-HMM, AlienHunter, IslandViewer 4, IslandPath-DIMOB),... |
| `bio-comparative-genomics-ortholog-inference` | Infer orthologous genes and gene families across species using OrthoFinder3 (HOG-based phylogenetic orthology), SonicParanoid2, Broccoli, ProteinOrtho, OMA / FastOMA hierarchica... |
| `bio-comparative-genomics-pangenome-analysis` | Build and analyze pangenomes for prokaryotes (Panaroo, PPanGGOLiN, PEPPAN, GET_HOMOLOGUES, anvi'o pangenomics) and eukaryotes (Minigraph-Cactus, PGGB, vg pangenome graphs). Impl... |
| `bio-comparative-genomics-synteny-analysis` | Detect syntenic blocks and structural rearrangements between genomes using MCScanX (Wang 2012), JCVI/MCScan (Tang 2008 Python), GENESPACE (Lovell 2022) for orthology-anchored ri... |
| `bio-comparative-genomics-whole-genome-alignment` | Build whole-genome alignments using Progressive Cactus (Armstrong 2020 reference-free clade-level WGA), Minigraph-Cactus (Hickey 2024 pangenome-aware), LASTZ chain/net (UCSC pip... |
| `bio-compressed-files` | Read and write compressed sequence files (gzip, bzip2, BGZF) using Biopython. Use when working with .gz or .bz2 sequence files. Use BGZF for indexable compressed files. |
| `bio-consensus-sequences` | Generate consensus FASTA sequences by applying VCF variants to a reference using bcftools consensus. Use when creating sample-specific reference sequences or reconstructing hapl... |
| `bio-data-visualization-circos-plots` | Build circular genome visualizations using circlize (R), pyCirclize (Python), or Circos (Perl CLI) with ideogram tracks, multi-data tracks (scatter, histogram, heatmap), chord/l... |
| `bio-data-visualization-genome-tracks` | Build genome-browser-style multi-track figures with pyGenomeTracks (config-driven), Gviz (R), and IGV batch screenshotting. Covers BigWig coverage tracks, BED/peak overlays, gen... |
| `bio-data-visualization-heatmaps-clustering` | Build clustered heatmaps for expression matrices and other features-by-samples data with rigorous distance/linkage/scaling choices, robust color mapping, optimal leaf ordering,... |
| `bio-data-visualization-multipanel-figures` | Compose multi-panel publication figures with patchwork, cowplot, gridExtra (R), or matplotlib GridSpec/subfigures (Python) including shared axes/legends/guides collection, panel... |
| `bio-data-visualization-network-visualization` | Visualize biological networks (PPI, gene-regulatory, co-expression, pathway) with layout algorithm choice (ForceAtlas2, Fruchterman-Reingold, Kamada-Kawai, hive plots), edge bun... |
| `bio-data-visualization-sequence-logos` | Build sequence logos from aligned DNA, RNA, or protein motifs using ggseqlogo (R), Logomaker (Python), or WebLogo with explicit bits vs probability encoding, background-frequenc... |
| `bio-data-visualization-statistical-annotation` | Add p-value brackets, significance asterisks, and effect-size annotations to distribution plots using ggpubr, ggsignif, and statannotations with correct test selection (parametr... |
| `bio-duplicate-handling` | Mark and remove PCR/optical duplicates using samtools fixmate and markdup. Use when preparing alignments for variant calling or when duplicate reads would bias analysis. |
| `bio-entrez-fetch` | Retrieve records from NCBI databases using Biopython Bio.Entrez (EFetch, ESummary). Use when downloading sequences, fetching GenBank/GenPept records, getting document summaries,... |
| `bio-entrez-search` | Search NCBI databases using Biopython Bio.Entrez (ESearch, EInfo, EGQuery, ESpell). Use when finding records by keyword, building reproducible field-qualified queries, navigatin... |
| `bio-epidemiological-genomics-amr-surveillance` | Detects acquired antimicrobial-resistance determinants and chromosomal point-mutation resistance in bacterial assemblies using AMRFinderPlus, ResFinder 4.0 (acquired + PointFind... |
| `bio-epidemiological-genomics-pathogen-typing` | Assigns isolate identity at the right resolution for the question -- ANI / Mash species triage, 7-locus MLST historical comparability, cgMLST / wgMLST outbreak resolution (chewB... |
| `bio-epidemiological-genomics-phylodynamics` | Estimates time-scaled phylogenies, molecular clock rates, effective reproduction number R_e (or R_t), and population dynamics from dated pathogen genomes using TreeTime (maximum... |
| `bio-epidemiological-genomics-transmission-inference` | Infers person-to-person transmission from pathogen genomes using outbreaker2 (Campbell 2018), TransPhylo (Didelot 2017), phybreak (Klinkenberg 2017), BadTrIP (De Maio 2018), SCO... |
| `bio-epidemiological-genomics-variant-surveillance` | Assigns pathogen lineages (SARS-CoV-2 Pangolin via UShER mode; Nextclade clade + QC; pango-designation alias_key.json resolution) and tracks variant frequencies over time using... |
| `bio-experimental-design-batch-design` | Designs genomics experiments so technical nuisance variation (batch, lane, plate, flow cell, operator, reagent lot, processing day) is balanced against the biological variable o... |
| `bio-experimental-design-multiple-testing` | Controls error rates across thousands of simultaneous tests in genomics discovery using false-discovery-rate methods (Benjamini-Hochberg 1995; Benjamini-Yekutieli 2001 for arbit... |
| `bio-experimental-design-power-analysis` | Calculates statistical power for high-dimensional genomics experiments (bulk RNA-seq, scRNA-seq, ATAC-seq, ChIP-seq, methylation, proteomics) under negative-binomial count model... |
| `bio-experimental-design-randomization-blocking` | Structures biological experiments so inference is valid by construction, covering Fisher's principles (randomization, replication, local control), the experimental-vs-observatio... |
| `bio-experimental-design-sample-size` | Estimates the minimum biological replicates (or cells/events) for a target power at a target FDR in genomics experiments using ssizeRNA, PROPER, powsimR for scRNA-seq, and pilot... |
| `bio-fastq-quality` | Work with FASTQ quality scores using Biopython. Use when analyzing read quality, filtering by quality, trimming low-quality bases, or generating quality reports. |
| `bio-filter-sequences` | Filter and select sequences by criteria (length, ID, GC content, patterns) using Biopython. Use when subsetting sequences, removing unwanted records, or selecting by specific cr... |
| `bio-format-conversion` | Convert between sequence file formats (FASTA, FASTQ, GenBank, EMBL) using Biopython Bio.SeqIO. Use when changing file formats or preparing data for different tools. |
| `bio-genome-annotation-annotation-qc` | Assesses the quality and completeness of a genome annotation with BUSCO (conserved single-copy ortholog recovery), OMArk (proteome completeness, consistency, and contamination),... |
| `bio-genome-annotation-annotation-transfer` | Transfers gene annotations between genome assemblies via coordinate liftover (UCSC liftOver, CrossMap for same-species version updates) or feature/sequence projection (Liftoff f... |
| `bio-genome-annotation-functional-annotation` | Assigns GO terms, Pfam/InterPro domains, KEGG orthologs, EC numbers, and product names to predicted proteins using eggNOG-mapper (orthology), InterProScan (domain signatures), a... |
| `bio-genome-annotation-ncrna-annotation` | Identifies non-coding RNAs (tRNA, rRNA, snoRNA, snRNA, riboswitches, sRNAs) using Infernal covariance-model search against Rfam, tRNAscan-SE 2.0 for tRNA, barrnap for rRNA, and... |
| `bio-genome-annotation-prokaryotic-annotation` | Annotates bacterial and archaeal genomes (isolates, MAGs, plasmids) with Bakta (active versioned databases, NCBI-compliant output) or Prokka (legacy), producing GFF3/GenBank/EMB... |
| `bio-genome-assembly-assembly-polishing` | Decides whether and how to polish a draft genome assembly to raise consensus accuracy (QV) with read-type-matched tools - Racon and medaka (ONT consensus), dorado polish, Polypo... |
| `bio-genome-assembly-assembly-qc` | Evaluates genome assembly quality across the three orthogonal axes - contiguity (QUAST auN/NG50/NGx, not bare N50), completeness (BUSCO/compleasm gene-space plus Merqury k-mer c... |
| `bio-genome-assembly-contamination-detection` | Detects and removes contamination in genome assemblies via two disjoint workflows - foreign-sequence screening of a single-organism (eukaryote/isolate) assembly with NCBI FCS-GX... |
| `bio-genome-assembly-genome-profiling` | Profiles a genome from raw reads BEFORE assembly with a k-mer spectrum (KMC or Jellyfish histogram), then models it with GenomeScope2 to estimate genome size, heterozygosity, re... |
| `bio-genome-assembly-hifi-assembly` | Assembles haplotype-resolved diploid and telomere-to-telomere (T2T) genomes from PacBio HiFi reads with hifiasm (HiFi-only, Hi-C, or trio phasing) and verkko (HiFi + ultralong O... |
| `bio-genome-assembly-long-read-assembly` | Assembles genomes de novo from noisy long reads (Oxford Nanopore R9/R10/Dorado, PacBio CLR) with Flye (repeat graph), Canu (correct-trim-assemble OLC), NextDenovo, Shasta, Raven... |
| `bio-genome-assembly-metagenome-assembly` | Assembles microbial-community sequencing into metagenome-assembled genomes (MAGs) with metaFlye (ONT), metaSPAdes/MEGAHIT (Illumina), and hifiasm-meta/metaMDBG (PacBio HiFi), th... |
| `bio-genome-assembly-scaffolding` | Orders and orients assembled contigs into chromosome-scale scaffolds from long-range linking data, inserting N-gap spacers (adds no sequence). Covers Hi-C/Omni-C scaffolding (Ya... |
| `bio-genome-assembly-short-read-assembly` | Assembles a genome de novo from Illumina short reads with SPAdes (isolate/careful/sc/meta/plasmid/rna modes), MEGAHIT (low-memory, huge datasets), Unicycler (bacterial finishing... |
| `bio-local-blast` | Build local BLAST databases and run searches using NCBI BLAST+ command-line tools. Use when running >50 queries, building custom databases with -parse_seqids and -taxid, downloa... |
| `bio-long-read-sequencing-clair3-variants` | Deep learning-based variant calling from long reads using Clair3 for SNPs and small indels. Use when calling germline variants from ONT or PacBio alignments, particularly when h... |
| `bio-long-read-sequencing-nanopore-methylation` | Calls DNA methylation from Oxford Nanopore sequencing data using signal-level analysis. Use when detecting 5mC or 6mA modifications directly from nanopore reads without bisulfit... |
| `bio-longread-alignment` | Align long reads using minimap2 for Oxford Nanopore and PacBio data. Supports various presets for different read types and applications. Use when aligning ONT or PacBio reads to... |
| `bio-longread-medaka` | Polish assemblies and call variants from Oxford Nanopore data using medaka. Uses neural networks trained on specific basecaller versions. Use when improving ONT-only assemblies... |
| `bio-longread-qc` | Quality control for long-read sequencing data using NanoPlot, NanoStat, and chopper. Generate QC reports, filter reads by length and quality, and visualize read characteristics.... |
| `bio-longread-structural-variants` | Detect structural variants from long-read alignments using Sniffles, cuteSV, and SVIM. Use when detecting deletions, insertions, inversions, translocations, or complex rearrange... |
| `bio-metagenomics-abundance` | Species abundance estimation using Bracken with Kraken2 output. Redistributes reads from higher taxonomic levels to species for more accurate estimates. Use when accurate specie... |
| `bio-metagenomics-amr-detection` | Detect antimicrobial resistance genes using AMRFinderPlus, ResFinder, and CARD. Screen isolates and metagenomes for resistance determinants. Use when characterizing resistance p... |
| `bio-metagenomics-functional-profiling` | Profile functional potential of metagenomes using HUMAnN3 and similar tools. Use when obtaining pathway abundances, gene family counts, or functional annotations from metagenomi... |
| `bio-metagenomics-kraken` | Taxonomic classification of metagenomic reads using Kraken2. Fast k-mer based classification against RefSeq database. Use when performing initial taxonomic classification of sho... |
| `bio-metagenomics-metaphlan` | Marker gene-based taxonomic profiling using MetaPhlAn 4. Provides accurate species-level relative abundances using clade-specific markers. Use when accurate taxonomic profiling... |
| `bio-metagenomics-strain-tracking` | Track bacterial strains using MASH, sourmash, fastANI, and inStrain. Compare genomes, detect contamination, and monitor strain-level variation. Use when needing sub-species reso... |
| `bio-metagenomics-visualization` | Visualize metagenomic profiles using R (phyloseq, microbiome) and Python (matplotlib, seaborn). Create stacked bar plots, heatmaps, PCA plots, and diversity analyses. Use when c... |
| `bio-microbiome-amplicon-processing` | Amplicon sequence variant (ASV) inference from 16S rRNA or ITS amplicon sequencing using DADA2. Covers quality filtering, error learning, denoising, and chimera removal. Use whe... |
| `bio-microbiome-differential-abundance` | Differential abundance testing for microbiome data using compositionally-aware methods like ALDEx2, ANCOM-BC2, and MaAsLin2. Use when identifying taxa that differ between experi... |
| `bio-microbiome-diversity-analysis` | Alpha and beta diversity analysis for microbiome data. Calculate within-sample richness, evenness, and between-sample dissimilarity with phyloseq and vegan. Use when comparing c... |
| `bio-microbiome-functional-prediction` | Predict metagenome functional content from 16S rRNA marker gene data using PICRUSt2. Infer KEGG, MetaCyc, and EC abundances from ASV tables. Use when functional profiling is nee... |
| `bio-microbiome-qiime2-workflow` | QIIME2 command-line workflow for 16S/ITS amplicon analysis. Alternative to DADA2/phyloseq R workflow with built-in provenance tracking. Use when preferring CLI over R, needing r... |
| `bio-microbiome-taxonomy-assignment` | Taxonomic classification of ASVs using reference databases like SILVA, GTDB, or UNITE. Covers naive Bayes classifiers (DADA2, IDTAXA) and exact matching approaches. Use when ass... |
| `bio-motif-search` | Find patterns, motifs, and subsequences in biological sequences using Biopython. Use when searching for transcription factor binding sites, regulatory elements, or any sequence... |
| `bio-ncbi-datasets-cli` | Download genome assemblies, gene records, and ortholog data from NCBI using the modern Datasets v2 CLI (replaces assembly_summary.txt scraping and many EFetch workflows). Use wh... |
| `bio-paired-end-fastq` | Handle paired-end FASTQ files (R1/R2) using Biopython. Use when working with Illumina paired reads, synchronizing pairs, interleaving/deinterleaving, or filtering paired data. |
| `bio-phylo-distance-calculations` | Compute evolutionary distances and build phylogenetic trees using Biopython Bio.Phylo.TreeConstruction. Use when creating distance matrices from alignments, building NJ/UPGMA tr... |
| `bio-phylo-divergence-dating` | Estimate divergence times using molecular clock models with BEAST2, MCMCTree, and TreePL. Use when dating speciation events, calibrating phylogenies with fossils, choosing betwe... |
| `bio-phylo-modern-tree-inference` | Build maximum likelihood phylogenetic trees using IQ-TREE2 and RAxML-NG with expert model selection, branch support assessment, and topology testing. Use when inferring publicat... |
| `bio-phylo-species-trees` | Estimate species trees using coalescent methods including ASTRAL-III, wASTRAL, ASTRAL-Pro, SVDQuartets, and BPP. Use when multi-locus data shows gene tree discordance from incom... |
| `bio-phylo-tree-io` | Read, write, and convert phylogenetic tree files using Biopython Bio.Phylo. Use when parsing Newick, Nexus, PhyloXML, or NeXML tree formats, converting between formats, or handl... |
| `bio-phylo-tree-manipulation` | Modify phylogenetic tree structure using Biopython Bio.Phylo. Use when rooting trees with outgroups, midpoint, or MAD methods, pruning taxa, collapsing clades, ladderizing branc... |
| `bio-phylo-tree-visualization` | Draw and export phylogenetic trees using Biopython Bio.Phylo with matplotlib and modern alternatives. Use when creating tree figures, customizing colors and labels, exporting to... |
| `bio-pileup-generation` | Generate pileup data for variant calling using samtools mpileup and pysam. Use when preparing data for variant calling, analyzing per-position read data, or calculating allele f... |
| `bio-primer-design-primer-basics` | Design PCR primers for a target sequence using primer3-py. Specify target regions, product size, melting temperature, and other constraints. Returns ranked primer pairs with qua... |
| `bio-primer-design-primer-validation` | Validate PCR primers for specificity, dimers, hairpins, and secondary structures using primer3-py thermodynamic calculations. Check self-complementarity, heterodimer formation,... |
| `bio-primer-design-qpcr-primers` | Design qPCR primers and TaqMan/molecular beacon probes using primer3-py. Configure probe Tm, primer-probe spacing, and hydrolysis probe constraints for real-time PCR assays. Use... |
| `bio-read-alignment-bowtie2-alignment` | Align short reads using Bowtie2 with local or end-to-end modes. Supports gapped alignment. Use when aligning ChIP-seq, ATAC-seq, or when flexible alignment modes are needed. |
| `bio-read-alignment-bwa-alignment` | Align DNA short reads to reference genomes using bwa-mem2, the faster successor to BWA-MEM. Use when aligning DNA short reads to a reference genome. |
| `bio-read-qc-adapter-trimming` | Remove sequencing adapters from FASTQ files using Cutadapt and Trimmomatic. Supports single-end and paired-end reads, Illumina TruSeq, Nextera, and custom adapter sequences. Use... |
| `bio-read-qc-contamination-screening` | Detect sample contamination and cross-species reads using FastQ Screen. Screen reads against multiple reference genomes to identify bacterial, viral, adapter, or sample swap con... |
| `bio-read-qc-fastp-workflow` | All-in-one read preprocessing with fastp including adapter trimming, quality filtering, deduplication, base correction, and HTML report generation. Use when preprocessing Illumi... |
| `bio-read-qc-quality-filtering` | Filter reads by quality scores, length, and N content using Trimmomatic and fastp. Apply sliding window trimming, remove low-quality bases from read ends, and discard reads belo... |
| `bio-read-qc-quality-reports` | Generate and interpret quality reports from FASTQ files using FastQC and MultiQC. Assess per-base quality, adapter content, GC bias, duplication levels, and overrepresented sequ... |
| `bio-read-sequences` | Read biological sequence files (FASTA, FASTQ, GenBank, EMBL, ABI, SFF) using Biopython Bio.SeqIO. Use when parsing sequence files, iterating multi-sequence files, random access... |
| `bio-reference-operations` | Generate consensus sequences and manage reference files using samtools. Use when creating consensus from alignments, indexing references, or creating sequence dictionaries. |
| `bio-reporting-automated-qc-reports` | Generates standardized quality control reports by aggregating metrics from FastQC, alignment, and other tools using MultiQC. Use when summarizing QC metrics across samples, crea... |
| `bio-reporting-figure-export` | Exports publication-ready figures in various formats with proper resolution, sizing, and typography. Use when preparing figures for journal submission, creating vector graphics... |
| `bio-reporting-jupyter-reports` | Creates reproducible Jupyter notebooks for bioinformatics analysis with parameterization using papermill. Use when generating automated analysis reports, running notebook-based... |
| `bio-reporting-quarto-reports` | Build reproducible scientific documents, presentations, and websites with Quarto supporting R, Python, Julia, and Observable JS. Use when creating reproducible reports with Quarto. |
| `bio-reverse-complement` | Generate reverse complements and complements of DNA/RNA sequences using Biopython. Use when working with opposite strands, primer design, or converting between template and codi... |
| `bio-sam-bam-basics` | View, convert, and understand SAM/BAM/CRAM alignment files using samtools and pysam. Use when inspecting alignments, converting between formats, or understanding alignment file... |
| `bio-seq-objects` | Create and manipulate Seq, MutableSeq, and SeqRecord objects using Biopython. Use when creating sequences from strings, modifying sequence data in-place, or building annotated s... |
| `bio-sequence-properties` | Calculate sequence properties like GC content, molecular weight, isoelectric point, and GC skew using Biopython. Use when analyzing sequence composition, computing physical prop... |
| `bio-sequence-slicing` | Slice, extract, and concatenate biological sequences using Biopython. Use when extracting subsequences, joining sequences, or manipulating sequence regions by position. |
| `bio-sequence-statistics` | Calculate sequence statistics (N50, length distribution, GC content, summary reports) using Biopython. Use when analyzing sequence datasets, generating QC reports, or comparing... |
| `bio-sra-data` | Download raw sequencing reads from NCBI SRA using sra-tools (prefetch, fasterq-dump, vdb-validate) or the ENA mirror. Use when pulling FASTQ for SRR/ERR/DRR accessions, deciding... |
| `bio-transcription-translation` | Transcribe DNA to RNA and translate to protein using Biopython. Use when converting between DNA, RNA, and protein sequences, finding ORFs, or using alternative codon tables. |
| `bio-uniprot-access` | Query UniProt's REST API (post-2022 endpoint at rest.uniprot.org) for protein sequences, annotations, GO terms, cross-references, ID mappings, and proteomes. Use when fetching U... |
| `bio-variant-annotation` | Comprehensive variant annotation using bcftools annotate/csq, VEP, SnpEff, and ANNOVAR. Add database annotations, predict functional consequences, and assess clinical significan... |
| `bio-variant-calling` | Call SNPs and indels from aligned reads using bcftools mpileup and call. Use when detecting variants from BAM files or generating VCF from alignments. |
| `bio-variant-calling-deepvariant` | Deep learning-based variant calling with Google DeepVariant. Provides high accuracy for germline SNPs and indels from Illumina, PacBio, and ONT data. Use when calling variants w... |
| `bio-variant-calling-filtering-best-practices` | Comprehensive variant filtering including GATK VQSR, hard filters, bcftools expressions, and quality metric interpretation for SNPs and indels. Use when filtering variants using... |
| `bio-variant-calling-structural-variant-calling` | Call structural variants (SVs) from sequencing data using Manta, Delly, GRIDSS, and LUMPY. Detects deletions, insertions, inversions, duplications, and translocations too large... |
| `bio-variant-normalization` | Normalize indel representation, decompose MNPs, and split multiallelic variants using bcftools norm. Use when comparing variants from different callers, preparing VCF for databa... |
| `bio-vcf-basics` | View, query, and understand VCF/BCF variant files using bcftools and cyvcf2. Use when inspecting variants, extracting specific fields, or understanding VCF format structure. |
| `bio-vcf-manipulation` | Merge, concatenate, sort, intersect, and subset VCF files using bcftools. Use when combining variant files, comparing call sets, or restructuring VCF data. |
| `bio-vcf-statistics` | Generate variant statistics, sample concordance, and quality metrics using bcftools stats and gtcheck. Use when evaluating variant quality, comparing samples, or summarizing VCF... |
| `bio-workflow-management-nextflow-pipelines` | Create scalable, containerized bioinformatics pipelines with Nextflow DSL2 supporting Docker, Singularity, and cloud execution. Use when building portable pipelines with contain... |
| `bio-workflow-management-snakemake-workflows` | Build reproducible bioinformatics pipelines with Snakemake using rules, wildcards, and automatic dependency resolution. Use when creating Python-based workflows, automating mult... |
| `bio-workflows-fastq-to-variants` | End-to-end DNA sequencing workflow from FASTQ files to variant calls. Covers QC, alignment with BWA, BAM processing, and variant calling with bcftools or GATK HaplotypeCaller. U... |
| `bio-workflows-genome-annotation-pipeline` | End-to-end genome annotation pipeline from assembled contigs to functional annotation, covering repeat masking, gene prediction, and functional assignment for both prokaryotic a... |
| `bio-workflows-genome-assembly-pipeline` | Orchestrates an end-to-end de novo genome assembly project, routing each step to the right genome-assembly skill rather than restating it. Profiles the genome first (k-mer spect... |
| `bio-workflows-longread-sv-pipeline` | End-to-end workflow for detecting structural variants from long-read sequencing data. Covers ONT/PacBio alignment with minimap2 and SV calling with Sniffles or cuteSV. Use when... |
| `bio-workflows-metagenomics-pipeline` | End-to-end metagenomics workflow from FASTQ to taxonomic and functional profiles. Covers Kraken2 classification, Bracken abundance estimation, and HUMAnN functional profiling. U... |
| `bio-workflows-microbiome-pipeline` | End-to-end 16S amplicon workflow from FASTQ reads to differential abundance. Orchestrates DADA2 ASV inference, taxonomy assignment, diversity analysis, and compositional testing... |
| `bio-workflows-outbreak-pipeline` | End-to-end outbreak investigation from pathogen isolates to transmission networks. Orchestrates MLST typing, AMR surveillance, phylodynamic dating, and transmission inference wi... |
| `bio-write-sequences` | Write biological sequences to files (FASTA, FASTQ, GenBank, EMBL) using Biopython Bio.SeqIO. Use when saving sequences, creating new sequence files, or outputting modified records. |
| `biopython-molecular-biology` | Molecular biology toolkit: sequence manipulation, FASTA/GenBank/PDB I/O, NCBI Entrez, BLAST automation, pairwise/MSA alignment, Bio.PDB, phylogenetic trees. Use for batch proces... |
| `biopython-sequence-analysis` | Biopython sequence analysis: parse FASTA/FASTQ/GenBank/GFF (SeqIO), NCBI Entrez (esearch/efetch/elink), remote/local BLAST, pairwise/MSA alignment (PairwiseAligner, MUSCLE/Clust... |
| `busco-status-interpretation` | Guide to interpreting BUSCO completeness statuses: why Duplicated BUSCOs count as complete, parsing output files, computing/comparing completeness across proteomes/genomes, comm... |
| `bwa-mem2-dna-aligner` | Fast short-read DNA aligner for WGS/WES/ChIP-seq. 2× faster BWA-MEM successor; outputs SAM/BAM with read group headers for GATK. Primary plus supplementary records for chimeric... |
| `cobrapy-metabolic-modeling` | Constraint-based (COBRA) analysis of genome-scale metabolic models: FBA, FVA, knockouts, flux sampling, production envelopes, gapfilling, media optimization. Use for strain desi... |
| `ena-database` | ENA REST API for sequences, reads, assemblies, and annotations. Portal API search, Browser API retrieval (XML/FASTA/EMBL), file reports for FASTQ/BAM URLs, taxonomy, cross-refs.... |
| `fastp-fastq-preprocessing` | All-in-one FASTQ QC and adapter trimming. Auto-detects Illumina adapters, filters low-quality reads, corrects paired-end overlaps, emits HTML+JSON QC in one pass. 3-10x faster t... |
| `gget-genomic-databases` | Unified CLI/Python interface to 20+ genomic databases. Gene lookups (Ensembl search/info/seq), BLAST/BLAT, AlphaFold, Enrichr enrichment, OpenTargets disease/drug, CELLxGENE sin... |
| `kegg-database` | KEGG REST API (academic only). Pathways, genes, compounds, enzymes, diseases, drugs via 7 ops (info/list/find/get/conv/link/ddi). ID conversion (NCBI/UniProt/PubChem). Use biose... |
| `kegg-pathway-analysis` | Guide to KEGG pathway enrichment for DEG results. Covers ORA vs GSEA, mandatory directionality splitting, KEGG organism codes, API failure handling with offline fallbacks, cross... |
| `molecular-docking-md-mmpbsa-pymol` | Automate small molecule-target protein docking, MD, MM-PBSA/MM-GBSA, and visualization. Default system is one or more protein receptor chains plus an organic small-molecule liga... |
| `multiqc-qc-reports` | Aggregates QC from 150+ bioinformatics tools into one interactive HTML report. Scans FastQC, samtools, STAR, HISAT2, Trim Galore, featureCounts, Kallisto, Salmon, Picard, GATK l... |
| `plannotate-plasmid-annotation` | Auto-annotate plasmids with features (promoters, terminators, resistance, origins, tags, fluorescent proteins) via BLAST against curated DBs (Addgene, fpbase, SnapGene). FASTA o... |
| `prokka-genome-annotation` | Annotate prokaryotic genomes (bacteria, archaea, viruses) via Prokka's BLAST/HMM pipeline. Identifies CDS, rRNA, tRNA, tmRNA, signal peptides against Pfam, TIGRFAMs, RefSeq. Out... |
| `pysam-genomic-files` | Read/write SAM/BAM/CRAM, VCF/BCF, FASTA/FASTQ. Region queries, pileup, variant filtering, read groups. Python htslib wrapper exposing samtools/bcftools CLI. Use STAR/BWA for ali... |
| `roary-pangenome` | Compute the bacterial pan-genome from Prokka/Bakta GFF3 annotations with Roary's CD-HIT + BLAST + MCL clustering pipeline. Builds gene presence/absence matrices, core/soft-core/... |
| `samtools-bam-processing` | CLI toolkit for SAM/BAM/CRAM: sort, index, convert, filter, QC alignments. Core commands: view, sort, index, flagstat, stats, depth, markdup, merge. Required between alignment a... |
| `sgrna-design-guide` | Three-tiered sgRNA design guide using validated Addgene sequences, CRISPick pre-computed datasets, or de novo design rules for CRISPR experiments |
| `snpeff-variant-annotation` | Annotate and filter VCF variants with SnpEff and SnpSift. SnpEff predicts functional effects (HIGH/MODERATE/LOW/MODIFIER), genes, transcripts, AA changes, HGVS; SnpSift filters... |
| `vcf-variant-filtering` | Guide to quality filtering raw VCF files before computing summary stats (Ts/Tv ratio, variant counts, AF distributions). Covers detecting raw VCFs via FILTER column and QUAL ins... |

## Delivery Stack

| Skill | 用途 |
|---|---|
| `local-md-mermaid-pdf` | Converts Markdown files with Mermaid diagrams to PDF using local tools (mmdc, md-to-pdf, Puppeteer) with CSS styling and page numbers. Use when the user asks to export markdown... |
| `markitdown` | Use when converting files such as PDF, DOCX, PPTX, XLSX, HTML, images, audio, or video into Markdown using Microsoft MarkItDown. Trigger when the user asks to extract file conte... |
| `pdf` | Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such a... |
| `pdf-guide` | Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such a... |
| `ppt` | Build PPT / PowerPoint / 演示文稿 / slide decks end-to-end via a .pptwork/<deck>/ filesystem contract. Use when the user wants to plan, author, screenshot, or export a slide deck. P... |
| `ppt-html-authoring` | Author a single PPT slide as a self-contained slide.html + design.md, given one outline entry. Use when the user asks to design, draft, or rewrite an individual slide page (KPI... |
| `screenshot-docs` | Capture screenshots of a running app and embed them into README.md and docs/ to make GitHub landing pages novice-friendly. Classifies the app as PySide6 GUI, Swift GUI, terminal... |

## Agent Ops & Governance

| Skill | 用途 |
|---|---|
| `artifact-staging-and-render-qa` | Stage external files into a writable workspace, normalize fragile paths, check local toolchain readiness, and render-verify deliverables before handoff. Use when users provide f... |
| `format-basic-norms` | Universal baseline academic formatting and reference-integrity standard. Use automatically for every conversation involving drafting, rewriting, translation, polishing, review,... |
| `planning-with-files` | Manus-style persistent file-based planning for AI coding agents: keeps task_plan.md, findings.md, and progress.md on disk so work survives context loss and /clear. Use when aske... |
| `securityauditor` | Static security audit workflow for Codex skills, agent skills, SKILL.md files, bundled scripts, hooks, shell snippets, suspicious file operations, prompt-injection instructions,... |
| `session-handoff` | Creates a safe en-US handoff markdown file from the current session, including the session timestamp, status, objective, expected result, work done, wins, failures, blockers, re... |
| `skill-writing-guide` | Guide for authoring Agent Skills (SKILL.md). Covers the open standard format, required frontmatter, directory layout, progressive disclosure, description writing, and best pract... |
| `storage-analyzer` | macOS / Windows 只读存储分析助手（自动识别系统）。扫描整机磁盘占用，找出 占空间大户，把每一项分成 🟢可自动清理 / 🟡需人工判断 / 🔴谨慎清理 三级并给出 可执行处置方案，生成排版精美、可折叠、命令可一键复制的交互式 HTML 报告，并可 起本地服务在网页上一键删除（移废纸篓/直接删）。扫描全程只读。务必在以下场景 使用：用户说"存... |

## Content & Knowledge Work

| Skill | 用途 |
|---|---|
| `content-research-writer` | Assists in writing high-quality content by conducting research, adding citations, improving hooks, iterating on outlines, and providing real-time feedback on each section. Trans... |
| `hv-analysis` | 横纵分析法（Horizontal-Vertical Analysis）深度研究Skill。由数字生命卡兹克提出，融合了索绪尔的历时-共时分析、社会科学的纵向-横截面研究设计、商学院案例研究法与竞争战略分析的核心思想。 当用户想要系统性研究一个产品、公司、概念、技术或人物时使用。核心是双轴分析：纵轴追踪从诞生到当下的完整生命历程（以叙事故事呈现），横轴在... |
| `neat-freak` | End-of-session knowledge cleanup with OCD-level rigor — reconciles project docs (CLAUDE.md, README.md, docs/) and agent memory against the code so nothing rots. 会话结束后对项目文档和记忆进行洁... |
| `notebooklm` | Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini. Browser automation, library manageme... |
| `zotero-lit-fetch` | 全自动抓取中英文文献到 Zotero，优先获取 PDF，跨 Windows / macOS。当用户想把 知网(CNKI)、万方(Wanfang)、维普(VIP)、PubMed、Web of Science、Google Scholar、 Scopus、CrossRef、bioRxiv、Semantic Scholar 等数据库的检索结果或单篇文章导入... |
