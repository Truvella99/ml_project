import numpy
import scipy
import main
import constants

def computeSw(D,L):
    data_list = main.getClassMatrix(D,L)
    Sw = 0
    for i in range(0,constants.NUM_CLASSES):
        _,CVi = main.computeMeanCovMatrix(data_list[i])
        Sw += data_list[i].shape[1] * CVi 

    Sw = Sw/D.shape[1]
    
    return Sw

def computeSb(D,L):
    data_list = main.getClassMatrix(D,L)
    Sb = 0
    mu_all = main.vcol(D.mean(1))

    for i in range(0,constants.NUM_CLASSES):
        mu = main.vcol(data_list[i].mean(1))
        diff = mu - mu_all
        product = numpy.dot(diff,diff.T)
        Sb+=(product * data_list[i].shape[1])
    
    Sb = Sb/D.shape[1]

    return Sb

def LDA1(m,Sb,Sw,D):
    #m = Num of Classes - 1
    s, U = scipy.linalg.eigh(Sb, Sw)
    W = U[:, ::-1][:, 0:m] # autovettori associati agli m autovalori più grandi, m direzioni (come file IRIS_LDA_matrix_m2.numpy)
    # project the dataset on these directions
    DP = numpy.dot(W.T,D)
    return DP

# Other LDA Alternative (careful to add the projection if needed)
def LDA2(m,Sw,Sb):
    U, s, _ = numpy.linalg.svd(Sw)
    P1 = numpy.dot(U, main.vcol(1.0/s**0.5)*U.T)
    SBTilde = numpy.dot(P1, numpy.dot(Sb,P1.T))
    U, _, _ = numpy.linalg.svd(SBTilde)
    P2 = U[:, 0:m]
    return numpy.dot(P1.T,P2)