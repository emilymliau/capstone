#####################################
##    multiGPATree, Sample Data    ##
#####################################

#install.packages("devtools")
library(devtools)
install_github("cran/mvpart")
library(mvpart)
install_github("asthakhatiwada/multiGPATree")
library(multiGPATree)
package?multiGPATree

load("C:/Users/emily/Downloads/simdata.RData")
data(simdata)
class(simdata)
names(simdata)
dim(simdata$gwasPval)
dim(simdata$annMat)
head(simdata$gwasPval)
head(simdata$annMat)

fit.mGPATree <- multiGPATree(gwasPval = simdata$gwasPval,
                             annMat = simdata$annMat,
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
# fit.mGPATree.pruned.p1p3 <- prune(fit.mGPATree@fit$P1_P3, cp = 0.20) #  PRUNING THE MULTIGPATREE MODEL RESULT FOR PHENOTYPES P1 AND P3
# fit.mGPATree.pruned.p1p3
# fit.mGPATree.pruned.p2p3 <- prune(fit.mGPATree@fit$P2_P3, cp = 0.20) #  PRUNING THE MULTIGPATREE MODEL RESULT FOR PHENOTYPES P2 AND P3
# fit.mGPATree.pruned.p2p3

plot(fit.mGPATree@fit$P1_P2)
# plot(fit.mGPATree@fit$P1_P3) #  MULTIGPATREE MODEL PLOT FOR PHENOTYPES P1 AND P3
# plot(fit.mGPATree@fit$P2_P3) #  MULTIGPATREE MODEL PLOT FOR PHENOTYPES P2 AND P3

leaf(fit.mGPATree@fit$P1_P2)
# leaf(fit.mGPATree@fit$P1_P3) #  LEAF RELATED INFORMATION FOR PHENOTYPES P1 AND P3
# leaf(fit.mGPATree@fit$P2_P3) #  LEAF RELATED INFORMATION FOR PHENOTYPES P2 AND P3

assoc.mGPATree.p1p2 <- assoc(fit.mGPATree@fit$P1_P2,
                             FDR = 0.01,
                             fdrControl="global")
head(assoc.mGPATree.p1p2)
table(assoc.mGPATree.p1p2$P1_P2)
table(assoc.mGPATree.p1p2$P1_P2, assoc.mGPATree.p1p2$leaf)
table(assoc.mGPATree.p1p2$P1)
table(assoc.mGPATree.p1p2$P1, assoc.mGPATree.p1p2$leaf)
table(assoc.mGPATree.p1p2$P2)
table(assoc.mGPATree.p1p2$P2, assoc.mGPATree.p1p2$leaf)
