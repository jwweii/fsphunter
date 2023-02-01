#install the ensembldb package
#if (!require("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")
#BiocManager::install("ensembldb")
#BiocManager::install("AnnotationHub")

library(jsonlite)
library(ensembldb)
library(AnnotationHub)

#load correct version of ensembl cache (v93) from the hub
ah <- AnnotationHub()
qr <- query(ah, c("EnsDb", "v93", "Homo sapiens"))

edb = qr[[1]]

# Read the input file
args <- commandArgs(trailingOnly=TRUE)
input_file <- args[1]
python_list <- as.list(fromJSON(readLines(input_file)))

tx = python_list[[1]]
p_start = as.numeric(python_list[[2]])
p_width = as.numeric(python_list[[3]])

rng_tx <- IRanges(start = c(p_start), width = c(p_width), names = c(tx))
rng_gnm <- transcriptToGenome(rng_tx, edb)

r_seqnames = rng_gnm@listData[[tx]]@seqnames@values
r_ranges = rng_gnm@listData[[tx]]@ranges@start

output_lst <- list(r_seqnames, r_ranges)
output_str <- toJSON(output_lst)
cat(output_str)

