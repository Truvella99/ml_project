import numpy
import scipy
import matplotlib.pyplot as plt
import constants
import main 
import os
import optimal_decision
import constants

def plot_hist(DTR,L):
    # 'spoofed-fingerprint' : name = 0 'authentic-fingerprint' : name = 1 
    spoofed_mask = (L == 0)
    authentic_mask = (L == 1)

    data_spoofed = DTR[:, spoofed_mask]
    data_authentic = DTR[:, authentic_mask]

    for i in range(0,constants.NUM_FEATURES):
        plt.figure(i)
        plt.xlabel("Feature" + str(i+1))
        plt.hist(data_spoofed[i, :], bins = 50, density = True, alpha = 0.4, label = 'Spoofed', edgecolor = 'black')
        plt.hist(data_authentic[i, :], bins = 50, density = True, alpha = 0.4, label = 'Authentic', edgecolor = 'black')
        plt.legend()
        plt.tight_layout()
    
    plt.show()

def plot_scatter(DTR,L):
    # 'spoofed-fingerprint' : name = 0 'authentic-fingerprint' : name = 1 
    spoofed_mask = (L == 0)
    authentic_mask = (L == 1)

    data_spoofed = DTR[:, spoofed_mask]
    data_authentic = DTR[:, authentic_mask]

    # plot only the unique combinations of the different features (we will have 45 only without dimensionality reduction)
    list_combination = []
    figure_id = 0
    for x in range(0,constants.NUM_FEATURES):
        for y in range(0,constants.NUM_FEATURES):
            if x == y:
                continue
            list_combination.append(str(y)+str(x))
            current_element = str(x)+str(y)
            if current_element in list_combination:
                continue
            figure_id+=1
            plt.figure(figure_id)
            plt.xlabel("Feature" + str(x+1))
            plt.ylabel("Feature" + str(y+1))
            plt.scatter(data_spoofed[x,:], data_spoofed[y,:], label = 'Spoofed')
            plt.scatter(data_authentic[x,:], data_authentic[y,:], label = 'Authentic')
            plt.legend()
            plt.tight_layout()
        plt.show()


def plot_scatter_projected_data_pca(DP,L):
    
    DP0,DP1 = main.getClassMatrix(DP,L)  
    
    # 2-D plot: regardless of the value of m, we can plot only for m = 2
    # for m=2 DPi[m-2: ], DPi[m-1 : ]
    plt.scatter(DP0[0, :], DP0[1, :], label = 'Spoofed')   
    plt.scatter(DP1[0, :], DP1[1, :], label = 'Authentic')  
 
    plt.legend()
    plt.show()

def plot_hist_projected_data_lda(DP,L):
    
    DP0,DP1 = main.getClassMatrix(DP,L)  
    
    # 1-D plot: 2 classes - 1 = 1
    plt.hist(DP0[0, :], bins = 50, density = True, alpha = 0.4, label = 'Spoofed', edgecolor = 'black')
    plt.hist(DP1[0, :], bins = 50, density = True, alpha = 0.4, label = 'Authentic', edgecolor = 'black')
    
    plt.legend()
    plt.show()

def plot_fraction_explained_variance_pca(DTR):
    # Apply PCA to get s eigenvalues and sort them to compute variance percentage 
    _, C = main.computeMeanCovMatrix(DTR)

    s, U = numpy.linalg.eigh(C)

    sorted_eigenvalues = s[::-1]
    total_variance = numpy.sum(sorted_eigenvalues)
    explained_variance_ratio = numpy.cumsum(sorted_eigenvalues / total_variance)
    plt.plot(range(1, constants.NUM_FEATURES + 1), explained_variance_ratio, marker='o')
    plt.xlabel('PCA dimensions')
    plt.ylabel('Fraction of explained variance')
    plt.title("PCA - Explained Variance")
    plt.show()
    plt.close()

# ------    PEARSON CORRELATION PLOTS   ----------

# pearson for the whole dataset

def plot_Heatmap_Whole_Dataset(DTR):
    heatmap = numpy.zeros((DTR.shape[0],DTR.shape[0]))
    for f1 in range(DTR.shape[0]):
        for f2 in range(DTR.shape[0]):
                if f2 <= f1:
                    heatmap[f1][f2] = abs(scipy.stats.pearsonr(DTR[f1, :], DTR[f2, :])[0])
                    heatmap[f2][f1] = heatmap[f1][f2]
    plt.figure() 
    plt.title('Heatmap of the Whole Dataset')
    plt.xticks(numpy.arange(0,constants.NUM_FEATURES),numpy.arange(1,constants.NUM_FEATURES + 1))  
    plt.yticks(numpy.arange(0,constants.NUM_FEATURES),numpy.arange(1,constants.NUM_FEATURES + 1))              
    plt.imshow(heatmap, cmap='Greys')
    plt.colorbar()
    plt.show()

# pearson for single class
# 'spoofed-fingerprint' : L = 0 (Red Color)
# 'authentic-fingerprint' : L = 1 (Blue Color)

def plot_Heatmap_Spoofed_Authentic(DTR, LTR, Class_Label):   
    heatmap = numpy.zeros((DTR.shape[0],DTR.shape[0]))
    for f1 in range(DTR.shape[0]):
        for f2 in range(DTR.shape[0]):
                if f2 <= f1:
                    heatmap[f1][f2] = abs(scipy.stats.pearsonr(DTR[:,LTR==Class_Label][f1, :], DTR[:,LTR==Class_Label][f2, :])[0])
                    heatmap[f2][f1] = heatmap[f1][f2]
    plt.figure()              
    plt.xticks(numpy.arange(0,constants.NUM_FEATURES),numpy.arange(1,constants.NUM_FEATURES + 1))  
    plt.yticks(numpy.arange(0,constants.NUM_FEATURES),numpy.arange(1,constants.NUM_FEATURES + 1))
    color = ''
    title = ''
    if Class_Label == 0:
        title = 'Heatmap of the spoofed-fingerprint class' 
        color = 'Reds'
    else:
        title = 'Heatmap of the authentic-fingerprint class' 
        color = 'Blues'
    plt.title(title)
    plt.imshow(heatmap, cmap=color )
    plt.colorbar()
    plt.show()

# -------   DCF PLOT    --------------

plot_index = 0

def plotDCF(x, y, labels, colors, xlabel, title):   
    global plot_index
    plt.figure()
    for i in range(0,len(x)):
        plt.plot(x[i], y[i], label=labels[i], color=colors[i])
        plt.xlim([min(x[i]), max(x[i])])
        #plt.ylim([0,max(y[i])+1])
    plt.title(title)
    plt.xscale("log")    
    plt.legend()
    plt.xlabel(xlabel)    
    plt.ylabel("min DCF")
    plt.savefig(os.path.join('output_plot_folder','plot_' + str(plot_index) + '.png'))
    plot_index+=1
    #plt.show()


# -------- GMM DCF PLOT  ---------------
def gmm_dcf_plot(raw_minDCFs, zNorm_minDCFs, pca_minDCFs, zNormPca_minDCFs, gmmComponents, gmm_model_name, m_pca):
    global plot_index
    plt.figure()
    plt.title(gmm_model_name)
    plt.xlabel("GMM components")
    plt.ylabel("minDCF values")
    x_axis = numpy.arange(len(gmmComponents))
    gmmComponents = numpy.array(gmmComponents)
    plt.bar(x_axis + 0.10 , raw_minDCFs, width = 0.125,linewidth = 1.0, edgecolor='black', color="Red", label = 'RAW')
    plt.bar(x_axis + 0.225 , zNorm_minDCFs, width = 0.125,linewidth = 1.0, edgecolor='black', color="Yellow", label = 'zNorm')
    plt.bar(x_axis + 0.35 , pca_minDCFs, width = 0.125,linewidth = 1.0, edgecolor='black', color="Green", label = 'PCA m = ' + str(m_pca))
    plt.bar(x_axis + 0.475 , zNormPca_minDCFs, width = 0.125,linewidth = 1.0, edgecolor='black', color="Blue", label = 'PCA m = ' + str(m_pca) + ' + zNorm')
    plt.xticks([r + 0.3 for r in range(len(gmmComponents))],gmmComponents)
    plt.legend()
    plt.savefig(os.path.join('output_plot_folder','plot_' + str(plot_index) + '.png'))
    plot_index+=1
    #plt.show()

def gmm_plot_all_component_combinations(x, y, labels, colors, gmm_model_name):
    global plot_index
    plt.figure()
    for i in range(0,len(x)):
        plt.plot(x[i], y[i], label=labels[i], color=colors[i])
        plt.xlim([min(x[i]), max(x[i])])
        #plt.ylim([0,max(y[i])+1])
    #plt.xscale("log")    
    plt.legend()
    plt.xlabel("GMM components class 1")    
    plt.ylabel("minDCF")
    plt.title(gmm_model_name)
    plt.savefig(os.path.join('output_plot_folder','plot_' + str(plot_index) + '.png'))
    plot_index+=1
    #plt.legend()
    #plt.show()

def compute_bayes_error_plot(llrs,labels,plt_title):
    n_points = 100
    effPriorLogOdds = numpy.linspace(-5, 5, n_points)

    # COMPUTE effpriorlogodds FOR THESE W.P.
    CFN = 1
    CFP = 10
    PRIOR_PROBABILITY = 0.5

    EFFECTIVE_PRIOR = (PRIOR_PROBABILITY * CFN)/((PRIOR_PROBABILITY * CFN) + (1-PRIOR_PROBABILITY) * CFP) 

    target = numpy.log(EFFECTIVE_PRIOR/(1-EFFECTIVE_PRIOR))

    PRIOR_PROBABILITY = 0.1
    EFFECTIVE_PRIOR = (PRIOR_PROBABILITY * CFN)/((PRIOR_PROBABILITY * CFN) + (1-PRIOR_PROBABILITY) * CFP) 

    unbalanced_01 = numpy.log(EFFECTIVE_PRIOR/(1-EFFECTIVE_PRIOR))

    PRIOR_PROBABILITY = 0.9
    EFFECTIVE_PRIOR = (PRIOR_PROBABILITY * CFN)/((PRIOR_PROBABILITY * CFN) + (1-PRIOR_PROBABILITY) * CFP) 

    unbalanced_09 = numpy.log(EFFECTIVE_PRIOR/(1-EFFECTIVE_PRIOR))

    # ADD THEM TO EFFPRIORLOGODDS LIST
    effPriorLogOdds = numpy.insert(effPriorLogOdds,numpy.abs(effPriorLogOdds - target).argmin(),target)
    effPriorLogOdds = numpy.insert(effPriorLogOdds,numpy.abs(effPriorLogOdds - unbalanced_01).argmin(),unbalanced_01)
    effPriorLogOdds = numpy.insert(effPriorLogOdds,numpy.abs(effPriorLogOdds - unbalanced_09).argmin(),unbalanced_09)
    target_index = numpy.abs(effPriorLogOdds - target).argmin()
    unbalanced_01_index = numpy.abs(effPriorLogOdds - unbalanced_01).argmin()
    unbalanced_09_index = numpy.abs(effPriorLogOdds - unbalanced_09).argmin()

    n_points += 3

    DCFs = [None] * n_points
    MIN_DCFs = [None] * n_points
    for i in range(0,n_points):
        pi_t = 1/(1+numpy.exp(-effPriorLogOdds[i]))
        DCFs[i],_,_ = optimal_decision.computeOptimalDecisionBinaryBayesPlot(pi_t,1,1,llrs,labels)
        MIN_DCFs[i] = optimal_decision.computeMinDCF(pi_t,1,1,llrs,labels)
    
    print("Target Working Point:\n")
    print("ActDCF: " + str(DCFs[target_index]))
    print("MinDCF: " + str(MIN_DCFs[target_index]) + "\n")
    print("Unbalanced 0.1 Working Point:\n")
    print("ActDCF: " + str(DCFs[unbalanced_01_index]))
    print("MinDCF: " + str(MIN_DCFs[unbalanced_01_index]) + "\n")
    print("Unbalanced 0.9 Working Point:\n")
    print("ActDCF: " + str(DCFs[unbalanced_09_index]))
    print("MinDCF: " + str(MIN_DCFs[unbalanced_09_index]) + "\n")
    # pass priorlogodd value
    bayesErrorPlot(DCFs,MIN_DCFs,effPriorLogOdds,plt_title,priorlogodd=[effPriorLogOdds[target_index],effPriorLogOdds[unbalanced_01_index],effPriorLogOdds[unbalanced_09_index]])

#The normalized Bayes error plot allows assessing the performance of the
#recognizer as we vary the application, i.e. as a function of prior log-odds ptilde
def bayesErrorPlot(dcf, mindcf, effPriorLogOdds, plt_title, priorlogodd=None): #dcf is the array containing the DCF values, and mindcf is the array containing the minimum DCF values
    global plot_index
    plt.figure()
    plt.plot(effPriorLogOdds, dcf, label='actDCF', color='b')
    plt.plot(effPriorLogOdds, mindcf, label='minDCF', linestyle='dashed' , color='r')
    colors = ['yellow','cyan','green']
    # priorlogodd: working points of 0.5,0.1,0.9
    for i in range(0,len(colors)):
        plt.plot([priorlogodd[i], priorlogodd[i]], [0, 1], colors[i])
    #plt.plot([-4, priorlogodd], [mindcflogodd, mindcflogodd], 'g', linestyle='dashed')
    plt.xlabel("$log \\frac{ \\tilde{\pi}}{1-\\tilde{\pi}}$")
    plt.ylabel("DCF")
    plt.legend(loc='upper right')
    plt.title(plt_title)
    plt.ylim([0, 1.0])
    plt.xlim([-5, 5])
    plt.savefig(os.path.join('output_plot_folder','plot_' + str(plot_index) + '.png'))
    plot_index+=1
    #plt.show()