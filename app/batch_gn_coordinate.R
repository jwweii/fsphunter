library(ensembldb)
library(AnnotationHub)
library(stringr)
library(dplyr)

#load correct version of ensembl cache (v93) from the hub
ah <- AnnotationHub()
qr <- query(ah, c("EnsDb", "v93", "Homo sapiens"))
edb = qr[[1]]

#read tsv file
tx_coordinate <- read.table("path/to/tsv", header = TRUE, sep = "\t")


#extract tx coordinates 
tx_coordinate$tx_coordinate_n <- lapply(tx_coordinate$tx_coordinate, function(x) {
    as.numeric(unlist(str_extract_all(x, "(\\d+)")))
  })

# define a function to return a start list fits format
start_to_rngtx <- function(tx_corordinate, tx_id){
  start <- c()
  for (i in 1:length(tx_corordinate)){
    if (i %% 2 == 1){
      start <- append(start, tx_corordinate[i])
    }
  }
  return(start)
}

# define a function to return a width list fits format
width_to_rngtx <- function(tx_corordinate, tx_id){
  width <- c()
  for (i in 1:length(tx_corordinate)){
    if (i %% 2 == 1){
      width <- append(width, 27)
    }
  }
  return(width)
}

# define a function to return a name list fits format
names_to_rngtx <- function(tx_corordinate, tx_id){
  names <- c()
  for (i in 1:length(tx_corordinate)){
    if (i %% 2 == 1){
      names <- append(names, tx_id)
    }
  }
  return(names)
}

# define a function to return genome coordinates
get_gn_coordinate <- function(test_n, test_id){
  start <- as.numeric(start_to_rngtx(test_n, test_id))
  width <- as.numeric(width_to_rngtx(test_n, test_id))
  names <- names_to_rngtx(test_n, test_id)
  if (is.na(start[1])){
    output <- NA
  } else{
    rng_tx <- IRanges(start = start, width = width, names = c(names))
    rng_gnm <- transcriptToGenome(rng_tx, edb)
    chr <- rng_gnm[[1]]@seqinfo@seqnames
    gn_start <- c()
    for (j in 1:length(names)){
      end <- c(rng_gnm[[j]]@ranges@start + 26)
      gn_start <- append(gn_start, rng_gnm[[j]]@ranges@start)
      gn_start <- append(gn_start, end)
    }
    output <- c(chr, gn_start)
  }
  return(output)
}

# Create a for loop to getting the genome coordinates on each row
for (i in 1:nrow(tx_coordinate)){
  test_n <- tx_coordinate$tx_coordinate_n[[i]]
  test_id <- tx_coordinate$longest_cds[[i]]
  gn_cor <- get_gn_coordinate(test_n, test_id)
  tx_coordinate$gn_cor[[i]] <- gn_cor
}


