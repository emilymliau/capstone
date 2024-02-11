install.packages("remotes")

# Load the remotes package
library(remotes)

# Install devtools version 2.4.2 (replace with the version you want)
remotes::install_version("devtools", version = "2.4.2")

# install.packages("devtools")
library(devtools)
devtools::install_github("cran/mvpart")
library(mvpart)
devtools::install_github("asthakhatiwada/multiGPATree")
library(multiGPATree)

load("simdata.RData")
data("simdata")
class(simdata)
names(simdata)
dim(simdata$gwasPval)
dim(simdata$annMat)
head(simdata$gwasPval)
head(simdata$annMat)
View(simdata)
library(dplyr)

realData <- read.csv('AMR_data.csv')
class(realData)

annot <- select(realData, -CIGDAY, -DRNKWK, -RSID, -X, -Unnamed..0)
pval <- select(realData, CIGDAY, DRNKWK)

fit.mGPATree <- multiGPATree(gwasPval = pval,
                             annMat = annot,
                             initAlpha = 0.1,
                             cpTry = 0.005,
                             ncore = 3)
fit.mGPATree
class(fit.mGPATree)
#head(fit.mGPATree$gwasPval)
#head(fit.mGPATree$annMat)
names(fit.mGPATree@fit)

fit.mGPATree.pruned.p1p2 <- prune(fit.mGPATree@fit$P1_P2, cp = 0.20)
fit.mGPATree.pruned.p1p2

plot(fit.mGPATree@fit$P1_P2)
