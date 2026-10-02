
library(ggplot2)

# read in AF.txt
af_exercise4 <- read.table("AF.txt", header = TRUE, sep = "\t")

# histogram

plot1 <- ggplot(af_exercise4, aes( x = AF)) +
  geom_histogram( bins = 11 ) +
  labs(x = "Allele Frequency", y = 
         "Count")

ggsave("AF.png", plot = p)