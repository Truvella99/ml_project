import kfold
import parameter_tuning
import lr
import constants
import plot
import parameter_tuning
import numpy
import pickle
import kfold
import gmm

def trainGenerative(DTR_RAND,LTR_RAND):
    # ---------------   GENERATIVE MODELS   -----------------------

    print("RAW (No PCA No Z_Norm)")
    print("Prior = 0.5")
    kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.5)
    print("Prior = 0.1")
    kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.1)
    print("Prior = 0.9")
    kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.9)
    
    # print("\nZ_Norm\n")
    # print("Prior = 0.5")
    # kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=0.5)
    # print("Prior = 0.1")
    # kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=0.1)
    # print("Prior = 0.9")
    # kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=0.9)

    for m in range(10,4,-1):
        print("RAW + PCA with M = " + str(m) + "\n")
        print("Prior = 0.5")
        kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=True,M=m,Z_Norm_Flag=None,Dcf_Prior=0.5)
        print("Prior = 0.1")
        kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=True,M=m,Z_Norm_Flag=None,Dcf_Prior=0.1)
        print("Prior = 0.9")
        kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=True,M=m,Z_Norm_Flag=None,Dcf_Prior=0.9)

        # print("\nZ_Norm + PCA with M = " + str(m) + "\n")
        # print("Prior = 0.5")
        # kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=True,M=m,Z_Norm_Flag=True,Dcf_Prior=0.5)
        # print("Prior = 0.1")
        # kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=True,M=m,Z_Norm_Flag=True,Dcf_Prior=0.1)
        # print("Prior = 0.9")
        # kfold.K_Fold_Generative(DTR_RAND,LTR_RAND,K=constants.K,PCA_Flag=True,M=m,Z_Norm_Flag=True,Dcf_Prior=0.9)

def trainLR(DTR_RAND,LTR_RAND,Load_Data=False):
    # ---------------   LR MODELS   -----------------------
    lambda_values = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
    classifier = [(lr.LogisticRegressionWeighted, "Logistic Regression Weighted"),(lr.LogisticRegressionWeightedQuadratic, "Logistic Regression Weighted Quadratic")]
    
    for prior in constants.DCFS_PRIORS:
        # ------ LR_LINEAR ------
        if not Load_Data:
            print("Prior = " + str(prior) + "\n")
            print("RAW (No PCA No Z_Norm)\n")
            raw_linear,raw_quadratic = parameter_tuning.lr_lambda_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,lambda_values=lambda_values,classifier=classifier,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/raw_linear_lr" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_linear, f)
            # Save the list of objects to a file
            with open("modelData/raw_quadratic_lr" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_quadratic, f)
            print("Z_Norm\n")
            zNorm_linear,zNorm_quadratic = parameter_tuning.lr_lambda_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,lambda_values=lambda_values,classifier=classifier,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/zNorm_linear_lr" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_linear, f)
            # Save the list of objects to a file
            with open("modelData/zNorm_quadratic_lr" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_quadratic, f)
            m = 8
            print("RAW + PCA with M = " + str(m) + "\n")
            rawPca_linear,rawPca_quadratic = parameter_tuning.lr_lambda_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,lambda_values=lambda_values,classifier=classifier,PCA_Flag=True,M=m,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/rawPca_linear_lr" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(rawPca_linear, f)
            # Save the list of objects to a file
            with open("modelData/rawPca_quadratic_lr" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(rawPca_quadratic, f)
            print("Z_Norm + PCA with M = " + str(m) + "\n")
            zNormPca_linear,zNormPca_quadratic = parameter_tuning.lr_lambda_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,lambda_values=lambda_values,classifier=classifier,PCA_Flag=True,M=m,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/zNormPca_linear_lr" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_linear, f)
            # Save the list of objects to a file
            with open("modelData/zNormPca_quadratic_lr" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_quadratic, f)

        if Load_Data:
            # Retrieve the list of objects from the file
            with open("modelData/raw_linear_lr" + str(prior) + ".pkl", "rb") as f:
                raw_linear = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/raw_quadratic_lr" + str(prior) + ".pkl", "rb") as f:
                raw_quadratic = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_linear_lr" + str(prior) + ".pkl", "rb") as f:
                zNorm_linear = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_quadratic_lr" + str(prior) + ".pkl", "rb") as f:
                zNorm_quadratic = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/rawPca_linear_lr" + str(prior) + ".pkl", "rb") as f:
                rawPca_linear = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/rawPca_quadratic_lr" + str(prior) + ".pkl", "rb") as f:
                rawPca_quadratic = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_linear_lr" + str(prior) + ".pkl", "rb") as f:
                zNormPca_linear = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_quadratic_lr" + str(prior) + ".pkl", "rb") as f:
                zNormPca_quadratic = pickle.load(f)
        
        m = 8
        # ------ PLOT LR_LINEAR ------
        labels = ['minDCF no PCA no Znorm','minDCF no PCA Znorm','minDCF PCA=' + str(m) + ' no Znorm','minDCF PCA=' + str(m) + ' Znorm']
        colors = ['b','r','g','y']
        # array of lambda values (for linear) and corresponding mindcfs
        plot.plotDCF([lambda_values,lambda_values,lambda_values,lambda_values],[raw_linear,zNorm_linear,rawPca_linear,zNormPca_linear],labels,colors,xlabel='lambda',title='Linear Logistic Regression')

        # ------ PLOT LR_QUADRATIC ------
        labels = ['minDCF no PCA no Znorm','minDCF no PCA Znorm','minDCF PCA=' + str(m) + ' no Znorm','minDCF PCA=' + str(m) + ' Znorm']
        colors = ['b','r','g','y']
        # array of lambda values (for linear) and corresponding mindcfs
        plot.plotDCF([lambda_values,lambda_values,lambda_values,lambda_values],[raw_quadratic,zNorm_quadratic,rawPca_quadratic,zNormPca_quadratic],labels,colors,'lambda',title='Quadratic Logistic Regression')

    m = 8
    # linear
    # lambda 10^-1 PCA=8 no Znorm (0.1 and 0.9)
    # print("Training Prior: Effective Prior")
    # classifier = [(lr.LogisticRegressionWeighted, "Logistic Regression Weighted")]
    # print("DcfPrior: 0.5")
    # kfold.K_Fold_LR(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,lambd=0.1,PCA_Flag=True,M=m,Z_Norm_Flag=False,Dcf_Prior=0.5,Calibration_Flag=False)
    # print("DcfPrior: 0.1")
    # kfold.K_Fold_LR(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,lambd=0.1,PCA_Flag=True,M=m,Z_Norm_Flag=False,Dcf_Prior=0.1,Calibration_Flag=False)
    # print("DcfPrior: 0.9")
    # kfold.K_Fold_LR(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,lambd=0.1,PCA_Flag=True,M=m,Z_Norm_Flag=False,Dcf_Prior=0.9,Calibration_Flag=False)
    # quadratic
    # lambda = 10^-3 no PCA zNorm
    # print("Training Prior: Effective Prior")
    # classifier = [(lr.LogisticRegressionWeightedQuadratic, "Logistic Regression Weighted Quadratic")]
    # print("DcfPrior: 0.5")
    # kfold.K_Fold_LR(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,lambd=0.001,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=0.5,Calibration_Flag=False)
    # print("DcfPrior: 0.1")
    # kfold.K_Fold_LR(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,lambd=0.001,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=0.1,Calibration_Flag=False)
    # print("DcfPrior: 0.9")
    # kfold.K_Fold_LR(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,lambd=0.001,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=0.9,Calibration_Flag=False)


def trainLinearSVM(DTR_RAND,LTR_RAND,Load_Data=False):
    # ---------------   LINEAR SVM   -----------------------
    print("SVM LINEAR HYPERPARAMETERS K AND C TRAINING:")
    K_values = [1, 10] # K=10 migliore ma tutor ha detto valore lab 1 vedere, al max 1,10 
    C_values = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0]

    for prior in constants.DCFS_PRIORS:
        if not Load_Data:
            print("Prior = " + str(prior) + "\n")

            print("RAW (No PCA No Z_Norm)\n")
            raw_linear = parameter_tuning.svm_linear_K_C_parameters_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/raw_linear_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_linear, f)
            print("Z_Norm\n")
            zNorm_linear = parameter_tuning.svm_linear_K_C_parameters_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/zNorm_linear_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_linear, f)
            m = 8
            print("RAW + PCA with M = " + str(m) + "\n")
            pca_linear = parameter_tuning.svm_linear_K_C_parameters_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,PCA_Flag=True,M=m,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/rawPca_linear_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_linear, f)
            print("Z_Norm + PCA with M = " + str(m) + "\n")
            zNormPca_linear = parameter_tuning.svm_linear_K_C_parameters_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,PCA_Flag=True,M=m,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/zNormPca_linear_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_linear, f)

        if Load_Data:
            # Retrieve the list of objects from the file
            with open("modelData/raw_linear_svm" + str(prior) + ".pkl", "rb") as f:
                raw_linear = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_linear_svm" + str(prior) + ".pkl", "rb") as f:
                zNorm_linear = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/rawPca_linear_svm" + str(prior) + ".pkl", "rb") as f:
                pca_linear = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_linear_svm" + str(prior) + ".pkl", "rb") as f:
                zNormPca_linear = pickle.load(f)
        
        m = 8
        # ----  SINGLE PLOT FOR prior, K = 1  -----
        raw_linear_k_1 = list(filter(lambda PlotElement: PlotElement.is_k(1), raw_linear))
        minDcfs_raw_linear_k_1 = [PlotElement.getminDcf() for PlotElement in raw_linear_k_1]
        C_values_raw_linear_k_1 = [PlotElement.getC() for PlotElement in raw_linear_k_1]

        zNorm_linear_k_1 = list(filter(lambda PlotElement: PlotElement.is_k(1), zNorm_linear))
        minDcfs_zNorm_linear_k_1 = [PlotElement.getminDcf() for PlotElement in zNorm_linear_k_1]
        C_values_zNorm_linear_k_1 = [PlotElement.getC() for PlotElement in zNorm_linear_k_1]

        pca_linear_k_1 = list(filter(lambda PlotElement: PlotElement.is_k(1), pca_linear))
        minDcfs_pca_linear_k_1 = [PlotElement.getminDcf() for PlotElement in pca_linear_k_1]
        C_values_pca_linear_k_1 = [PlotElement.getC() for PlotElement in pca_linear_k_1]

        zNormPca_linear_k_1 = list(filter(lambda PlotElement: PlotElement.is_k(1), zNormPca_linear))
        minDcfs_zNormPca_linear_k_1 = [PlotElement.getminDcf() for PlotElement in zNormPca_linear_k_1]
        C_values_zNormPca_linear_k_1 = [PlotElement.getC() for PlotElement in zNormPca_linear_k_1]

        labels = ['minDCF K = 1 no PCA no Znorm','minDCF K = 1 no PCA Znorm','minDCF K = 1 PCA=' + str(m) + ' no Znorm','minDCF K = 1 PCA=' + str(m) + ' Znorm']
        colors = ['b','r','g','y']
        #base colors: r, g, b, m, y, c, k, w
        plot.plotDCF([C_values_raw_linear_k_1,C_values_zNorm_linear_k_1,C_values_pca_linear_k_1,C_values_zNormPca_linear_k_1],[minDcfs_raw_linear_k_1,minDcfs_zNorm_linear_k_1,minDcfs_pca_linear_k_1,minDcfs_zNormPca_linear_k_1],labels,colors,xlabel='C',title='Linear SVM')

        # ----  SINGLE PLOT FOR prior, K = 10  -----
        raw_linear_k_10 = list(filter(lambda PlotElement: PlotElement.is_k(10), raw_linear))
        minDcfs_raw_linear_k_10 = [PlotElement.getminDcf() for PlotElement in raw_linear_k_10]
        C_values_raw_linear_k_10 = [PlotElement.getC() for PlotElement in raw_linear_k_10]

        zNorm_linear_k_10 = list(filter(lambda PlotElement: PlotElement.is_k(10), zNorm_linear))
        minDcfs_zNorm_linear_k_10 = [PlotElement.getminDcf() for PlotElement in zNorm_linear_k_10]
        C_values_zNorm_linear_k_10 = [PlotElement.getC() for PlotElement in zNorm_linear_k_10]

        pca_linear_k_10 = list(filter(lambda PlotElement: PlotElement.is_k(10), pca_linear))
        minDcfs_pca_linear_k_10 = [PlotElement.getminDcf() for PlotElement in pca_linear_k_10]
        C_values_pca_linear_k_10 = [PlotElement.getC() for PlotElement in pca_linear_k_10]

        zNormPca_linear_k_10 = list(filter(lambda PlotElement: PlotElement.is_k(10), zNormPca_linear))
        minDcfs_zNormPca_linear_k_10 = [PlotElement.getminDcf() for PlotElement in zNormPca_linear_k_10]
        C_values_zNormPca_linear_k_10 = [PlotElement.getC() for PlotElement in zNormPca_linear_k_10]

        labels = ['minDCF K = 10 no PCA no Znorm','minDCF K = 10 no PCA Znorm','minDCF K = 10 PCA=' + str(m) + ' no Znorm','minDCF K = 10 PCA=' + str(m) + ' Znorm']
        colors = ['b','r','g','y']
        #base colors: r, g, b, m, y, c, k, w
        plot.plotDCF([C_values_raw_linear_k_10,C_values_zNorm_linear_k_10,C_values_pca_linear_k_10,C_values_zNormPca_linear_k_10],[minDcfs_raw_linear_k_10,minDcfs_zNorm_linear_k_10,minDcfs_pca_linear_k_10,minDcfs_zNormPca_linear_k_10],labels,colors,xlabel='C',title='Linear SVM')


def trainPolynomialSVM(DTR_RAND,LTR_RAND,Load_Data=False):
    print("SVM POLYNOMIAL K,C,c,d TRAINING:")
    K_values = [1]
    C_values = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0] # for C <= 10^-6 there is a significative worsening in performance 
    c_values = [0, 1]
    d_values = [2.0]

    for prior in constants.DCFS_PRIORS:
        if not Load_Data:
            print("Prior = " + str(prior) + "\n")

            print("RAW (No PCA No Z_Norm)\n")
            raw_polynomial = parameter_tuning.svm_kernel_polynomial_K_C_c_d_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,c_values=c_values,d_values=d_values,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/raw_polynomial_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_polynomial, f)
            print("Z_Norm\n")
            zNorm_polynomial = parameter_tuning.svm_kernel_polynomial_K_C_c_d_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,c_values=c_values,d_values=d_values,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/zNorm_polynomial_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_polynomial, f)
            m = 8
            print("RAW + PCA with M = " + str(m) + "\n")
            pca_polynomial = parameter_tuning.svm_kernel_polynomial_K_C_c_d_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,c_values=c_values,d_values=d_values,PCA_Flag=True,M=m,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/pca_polynomial_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_polynomial, f)
            print("Z_Norm + PCA with M = " + str(m) + "\n")
            zNormPca_polynomial = parameter_tuning.svm_kernel_polynomial_K_C_c_d_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,c_values=c_values,d_values=d_values,PCA_Flag=True,M=m,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/zNormPca_polynomial_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_polynomial, f)
        
        if Load_Data:
            # Retrieve the list of objects from the file
            with open("modelData/raw_polynomial_svm" + str(prior) + ".pkl", "rb") as f:
                raw_polynomial = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_polynomial_svm" + str(prior) + ".pkl", "rb") as f:
                zNorm_polynomial = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/pca_polynomial_svm" + str(prior) + ".pkl", "rb") as f:
                pca_polynomial = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_polynomial_svm" + str(prior) + ".pkl", "rb") as f:
                zNormPca_polynomial = pickle.load(f)

        m = 8
        # ----- PLOT FOR c = 0 ------
        raw_polynomial_c0 = list(filter(lambda PlotElement: PlotElement.is_c(0), raw_polynomial))
        minDcfs_raw_polynomial_c0 = [PlotElement.getminDcf() for PlotElement in raw_polynomial_c0]
        C_values_raw_polynomial_c0 = [PlotElement.getC() for PlotElement in raw_polynomial_c0]

        zNorm_polynomial_c0 = list(filter(lambda PlotElement: PlotElement.is_c(0), zNorm_polynomial))
        minDcfs_zNorm_polynomial_c0 = [PlotElement.getminDcf() for PlotElement in zNorm_polynomial_c0]
        C_values_zNorm_polynomial_c0 = [PlotElement.getC() for PlotElement in zNorm_polynomial_c0]

        pca_polynomial_c0 = list(filter(lambda PlotElement: PlotElement.is_c(0), pca_polynomial))
        minDcfs_pca_polynomial_c0 = [PlotElement.getminDcf() for PlotElement in pca_polynomial_c0]
        C_values_pca_polynomial_c0 = [PlotElement.getC() for PlotElement in pca_polynomial_c0]

        zNormPca_polynomial_c0 = list(filter(lambda PlotElement: PlotElement.is_c(0), zNormPca_polynomial))
        minDcfs_zNormPca_polynomial_c0 = [PlotElement.getminDcf() for PlotElement in zNormPca_polynomial_c0]
        C_values_zNormPca_polynomial_c0 = [PlotElement.getC() for PlotElement in zNormPca_polynomial_c0]

        labels = ['minDCF c = 0 no PCA no Znorm','minDCF c = 0 no PCA Znorm','minDCF c = 0 PCA=' + str(m) + ' no Znorm','minDCF c = 0 PCA=' + str(m) + ' Znorm']
        colors = ['b','r','g','y']
        #base colors: r, g, b, m, y, c, k, w
        plot.plotDCF([C_values_raw_polynomial_c0,C_values_zNorm_polynomial_c0,C_values_pca_polynomial_c0,C_values_zNormPca_polynomial_c0],[minDcfs_raw_polynomial_c0,minDcfs_zNorm_polynomial_c0,minDcfs_pca_polynomial_c0,minDcfs_zNormPca_polynomial_c0],labels,colors,xlabel='C',title='Polynomial SVM')


        # ----- PLOT FOR c = 1 ------
        raw_polynomial_c1 = list(filter(lambda PlotElement: PlotElement.is_c(1), raw_polynomial))
        minDcfs_raw_polynomial_c1 = [PlotElement.getminDcf() for PlotElement in raw_polynomial_c1]
        C_values_raw_polynomial_c1 = [PlotElement.getC() for PlotElement in raw_polynomial_c1]

        zNorm_polynomial_c1 = list(filter(lambda PlotElement: PlotElement.is_c(1), zNorm_polynomial))
        minDcfs_zNorm_polynomial_c1 = [PlotElement.getminDcf() for PlotElement in zNorm_polynomial_c1]
        C_values_zNorm_polynomial_c1 = [PlotElement.getC() for PlotElement in zNorm_polynomial_c1]

        pca_polynomial_c1 = list(filter(lambda PlotElement: PlotElement.is_c(1), pca_polynomial))
        minDcfs_pca_polynomial_c1 = [PlotElement.getminDcf() for PlotElement in pca_polynomial_c1]
        C_values_pca_polynomial_c1 = [PlotElement.getC() for PlotElement in pca_polynomial_c1]

        zNormPca_polynomial_c1 = list(filter(lambda PlotElement: PlotElement.is_c(1), zNormPca_polynomial))
        minDcfs_zNormPca_polynomial_c1 = [PlotElement.getminDcf() for PlotElement in zNormPca_polynomial_c1]
        C_values_zNormPca_polynomial_c1 = [PlotElement.getC() for PlotElement in zNormPca_polynomial_c1]

        labels = ['minDCF c = 1 no PCA no Znorm','minDCF c = 1 no PCA Znorm','minDCF c = 1 PCA=' + str(m) + ' no Znorm','minDCF c = 1 PCA=' + str(m) + ' Znorm']
        colors = ['b','r','g','y']
        #base colors: r, g, b, m, y, c, k, w
        plot.plotDCF([C_values_raw_polynomial_c1,C_values_zNorm_polynomial_c1,C_values_pca_polynomial_c1,C_values_zNormPca_polynomial_c1],[minDcfs_raw_polynomial_c1,minDcfs_zNorm_polynomial_c1,minDcfs_pca_polynomial_c1,minDcfs_zNormPca_polynomial_c1],labels,colors,xlabel='C',title='Polynomial SVM')

    # K = 1     d = 2
    # c = 1     C = 10^-2
    # PCA = 8 ZNorm
    # m = 8
    # print("Training Prior: Effective Prior")
    # print("DcfPrior: 0.5")
    # kfold.K_Fold_SVM_kernel_polynomial(DTR_RAND,LTR_RAND,constants.K,hyperParameter_K = 1,hyperParameter_C = 0.01, hyperParameter_c = 1, hyperParameter_d = 2, PCA_Flag = True, M = m, Z_Norm_Flag = True, Dcf_Prior = 0.5, Calibration_Flag = False)
    # print("DcfPrior: 0.1")
    # kfold.K_Fold_SVM_kernel_polynomial(DTR_RAND,LTR_RAND,constants.K,hyperParameter_K = 1,hyperParameter_C = 0.01, hyperParameter_c = 1, hyperParameter_d = 2, PCA_Flag = True, M = m, Z_Norm_Flag = True, Dcf_Prior = 0.1, Calibration_Flag = False)
    # print("DcfPrior: 0.9")
    # kfold.K_Fold_SVM_kernel_polynomial(DTR_RAND,LTR_RAND,constants.K,hyperParameter_K = 1,hyperParameter_C = 0.01, hyperParameter_c = 1, hyperParameter_d = 2, PCA_Flag = True, M = m, Z_Norm_Flag = True, Dcf_Prior = 0.9, Calibration_Flag = False)

def trainRadialBasisFunctionSVM(DTR_RAND,LTR_RAND,Load_Data=False):
    print("SVM RADIAL BASIS FUNCTION (RBF) K,C,gamma TRAINING:")
    K_values = [1.0]
    C_values = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0, 100000.0]
    # we want log(gamma), so we pass gamma value for which log(gamma) = -3,-4,-5
    gamma_values = [1.0/numpy.exp(3), 1.0/numpy.exp(4), 1.0/numpy.exp(5)] #hyper-parameter
    
    for prior in constants.DCFS_PRIORS:
        if not Load_Data:
            print("Prior = " + str(prior) + "\n")

            print("RAW (No PCA No Z_Norm)\n")
            raw_rbf = parameter_tuning.svm_kernel_rbf_K_C_gamma_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,gamma_values=gamma_values,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/raw_rbf_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_rbf, f)
            print("Z_Norm\n")
            zNorm_rbf = parameter_tuning.svm_kernel_rbf_K_C_gamma_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,gamma_values=gamma_values,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/zNorm_rbf_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_rbf, f)
            m = 8
            print("RAW + PCA with M = " + str(m) + "\n")
            pca_rbf = parameter_tuning.svm_kernel_rbf_K_C_gamma_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,gamma_values=gamma_values,PCA_Flag=True,M=m,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/pca_rbf_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_rbf, f)
            print("Z_Norm + PCA with M = " + str(m) + "\n")
            zNormPca_rbf = parameter_tuning.svm_kernel_rbf_K_C_gamma_parameter_testing(DTR_RAND,LTR_RAND,K=constants.K,k_values=K_values,C_values=C_values,gamma_values=gamma_values,PCA_Flag=True,M=m,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
            # Save the list of objects to a file
            with open("modelData/zNormPca_rbf_svm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_rbf, f)

        if Load_Data:
            # Retrieve the list of objects from the file
            with open("modelData/raw_rbf_svm" + str(prior) + ".pkl", "rb") as f:
                raw_rbf = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_rbf_svm" + str(prior) + ".pkl", "rb") as f:
                zNorm_rbf = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/pca_rbf_svm" + str(prior) + ".pkl", "rb") as f:
                pca_rbf = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_rbf_svm" + str(prior) + ".pkl", "rb") as f:
                zNormPca_rbf = pickle.load(f)
        
        m = 8
        # ---- PLOT FOR log(gamma) = -3 -----
        raw_gamma_1e3 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(3)), raw_rbf))
        minDcfs_raw_gamma_1e3 = [PlotElement.getminDcf() for PlotElement in raw_gamma_1e3]
        C_values_raw_gamma_1e3 = [PlotElement.getC() for PlotElement in raw_gamma_1e3]

        zNorm_gamma_1e3 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(3)), zNorm_rbf))
        minDcfs_zNorm_gamma_1e3 = [PlotElement.getminDcf() for PlotElement in zNorm_gamma_1e3]
        C_values_zNorm_gamma_1e3 = [PlotElement.getC() for PlotElement in zNorm_gamma_1e3]

        pca_gamma_1e3 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(3)), pca_rbf))
        minDcfs_pca_gamma_1e3 = [PlotElement.getminDcf() for PlotElement in pca_gamma_1e3]
        C_values_pca_gamma_1e3 = [PlotElement.getC() for PlotElement in pca_gamma_1e3]

        zNormPca_gamma_1e3 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(3)), zNormPca_rbf))
        minDcfs_zNormPca_gamma_1e3 = [PlotElement.getminDcf() for PlotElement in zNormPca_gamma_1e3]
        C_values_zNormPca_gamma_1e3 = [PlotElement.getC() for PlotElement in zNormPca_gamma_1e3]

        labels = ['minDCF log(γ) = -3 no PCA no Znorm','minDCF log(γ) = -3 no PCA Znorm','minDCF log(γ) = -3 PCA=' + str(m) + ' no Znorm','minDCF log(γ) = -3 PCA=' + str(m) + ' Znorm']
        colors = ['b','g','y','c','r']
        #base colors: r, g, b, m, y, c, k, w
        plot.plotDCF([C_values_raw_gamma_1e3,C_values_zNorm_gamma_1e3,C_values_pca_gamma_1e3,C_values_zNormPca_gamma_1e3],[minDcfs_raw_gamma_1e3,minDcfs_zNorm_gamma_1e3,minDcfs_pca_gamma_1e3,minDcfs_zNormPca_gamma_1e3],labels,colors,xlabel='C',title='Radial Basis Function SVM')


        # ---- PLOT FOR log(gamma) = -4 -----
        raw_gamma_1e4 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(4)), raw_rbf))
        minDcfs_raw_gamma_1e4 = [PlotElement.getminDcf() for PlotElement in raw_gamma_1e4]
        C_values_raw_gamma_1e4 = [PlotElement.getC() for PlotElement in raw_gamma_1e4]

        zNorm_gamma_1e4 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(4)), zNorm_rbf))
        minDcfs_zNorm_gamma_1e4 = [PlotElement.getminDcf() for PlotElement in zNorm_gamma_1e4]
        C_values_zNorm_gamma_1e4 = [PlotElement.getC() for PlotElement in zNorm_gamma_1e4]

        pca_gamma_1e4 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(4)), pca_rbf))
        minDcfs_pca_gamma_1e4 = [PlotElement.getminDcf() for PlotElement in pca_gamma_1e4]
        C_values_pca_gamma_1e4 = [PlotElement.getC() for PlotElement in pca_gamma_1e4]

        zNormPca_gamma_1e4 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(4)), zNormPca_rbf))
        minDcfs_zNormPca_gamma_1e4 = [PlotElement.getminDcf() for PlotElement in zNormPca_gamma_1e4]
        C_values_zNormPca_gamma_1e4 = [PlotElement.getC() for PlotElement in zNormPca_gamma_1e4]

        labels = ['minDCF log(γ) = -4 no PCA no Znorm','minDCF log(γ) = -4 no PCA Znorm','minDCF log(γ) = -4 PCA=' + str(m) + ' no Znorm','minDCF log(γ) = -4 PCA=' + str(m) + ' Znorm']
        colors = ['b','g','y','c','r']
        #base colors: r, g, b, m, y, c, k, w
        plot.plotDCF([C_values_raw_gamma_1e4,C_values_zNorm_gamma_1e4,C_values_pca_gamma_1e4,C_values_zNormPca_gamma_1e4],[minDcfs_raw_gamma_1e4,minDcfs_zNorm_gamma_1e4,minDcfs_pca_gamma_1e4,minDcfs_zNormPca_gamma_1e4],labels,colors,xlabel='C',title='Radial Basis Function SVM')


        # ---- PLOT FOR log(gamma) = -5 -----
        raw_gamma_1e5 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(5)), raw_rbf))
        minDcfs_raw_gamma_1e5 = [PlotElement.getminDcf() for PlotElement in raw_gamma_1e5]
        C_values_raw_gamma_1e5 = [PlotElement.getC() for PlotElement in raw_gamma_1e5]

        zNorm_gamma_1e5 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(5)), zNorm_rbf))
        minDcfs_zNorm_gamma_1e5 = [PlotElement.getminDcf() for PlotElement in zNorm_gamma_1e5]
        C_values_zNorm_gamma_1e5 = [PlotElement.getC() for PlotElement in zNorm_gamma_1e5]

        pca_gamma_1e5 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(5)), pca_rbf))
        minDcfs_pca_gamma_1e5 = [PlotElement.getminDcf() for PlotElement in pca_gamma_1e5]
        C_values_pca_gamma_1e5 = [PlotElement.getC() for PlotElement in pca_gamma_1e5]

        zNormPca_gamma_1e5 = list(filter(lambda PlotElement: PlotElement.is_gamma(1/numpy.exp(5)), zNormPca_rbf))
        minDcfs_zNormPca_gamma_1e5 = [PlotElement.getminDcf() for PlotElement in zNormPca_gamma_1e5]
        C_values_zNormPca_gamma_1e5 = [PlotElement.getC() for PlotElement in zNormPca_gamma_1e5]

        labels = ['minDCF log(γ) = -5 no PCA no Znorm','minDCF log(γ) = -5 no PCA Znorm','minDCF log(γ) = -5 PCA=' + str(m) + ' no Znorm','minDCF log(γ) = -5 PCA=' + str(m) + ' Znorm']
        colors = ['b','g','y','c','r']
        #base colors: r, g, b, m, y, c, k, w
        plot.plotDCF([C_values_raw_gamma_1e5,C_values_zNorm_gamma_1e5,C_values_pca_gamma_1e5,C_values_zNormPca_gamma_1e5],[minDcfs_raw_gamma_1e5,minDcfs_zNorm_gamma_1e5,minDcfs_pca_gamma_1e5,minDcfs_zNormPca_gamma_1e5],labels,colors,xlabel='C',title='Radial Basis Function SVM')
    
    # K = 1     gamma = 1/e^5     C = 10^2
    # PCA = 8 ZNorm
    # m = 8
    # print("Training Prior: Effective Prior")
    # print("DcfPrior: 0.5")
    # kfold.K_Fold_SVM_kernel_rbf(DTR_RAND,LTR_RAND,constants.K,hyperParameter_K = 1,hyperParameter_C = 100.0, hyperParameter_gamma = 1.0/numpy.exp(5),PCA_Flag = True, M = m, Z_Norm_Flag = True, Dcf_Prior = 0.5, Calibration_Flag = False)
    # print("DcfPrior: 0.1")
    # kfold.K_Fold_SVM_kernel_rbf(DTR_RAND,LTR_RAND,constants.K,hyperParameter_K = 1,hyperParameter_C = 100.0, hyperParameter_gamma = 1.0/numpy.exp(5),PCA_Flag = True, M = m, Z_Norm_Flag = True, Dcf_Prior = 0.1, Calibration_Flag = False)
    # print("DcfPrior: 0.9")
    # kfold.K_Fold_SVM_kernel_rbf(DTR_RAND,LTR_RAND,constants.K,hyperParameter_K = 1,hyperParameter_C = 100.0, hyperParameter_gamma = 1.0/numpy.exp(5),PCA_Flag = True, M = m, Z_Norm_Flag = True, Dcf_Prior = 0.9, Calibration_Flag = False)

def trainGMMSameComponents(DTR_RAND,LTR_RAND,Load_Data=False):
    # BUILD INITIAL GMM (NON DOVREBBE SERVIRCI) 
    # get dataset split by class
    # DP0_RAND,DP1_RAND = getClassMatrix(DTR_RAND,LTR_RAND)
    # weight of classes for the gmm
    # we compute each weight by using the formula : num_sample_class/num_sample_whole_dataset
    # gmm_weights = [DP0_RAND.shape[1]/DTR_RAND.shape[1],DP1_RAND.shape[1]/DTR_RAND.shape[1]]
    # print(gmm_weights)
    # compute mean and covariance matrix for each class
    # mu_DP0,cov_DP0 = computeMeanCovMatrix(DP0_RAND)
    # mu_DP1,cov_DP1 = computeMeanCovMatrix(DP1_RAND)
    # build the gmm
    # GMM = [[gmm_weights[0],mu_DP0,cov_DP0],[gmm_weights[1],mu_DP1,cov_DP1]]
    # ------------- GMM WITH SAME PER-CLASS COMPONENTS ----------------
    classifiers = [(gmm.LBGalgorithm,gmm.constraintSigma,"Full Covariance (standard)"), (gmm.DiagLBGalgorithm,gmm.DiagConstraintSigma,"Diagonal Covariance"), (gmm.TiedLBGalgorithm, gmm.constraintSigma, "Tied Covariance"),(gmm.TiedDiagLBGalgorithm,gmm.DiagConstraintSigma,"Tied Diagonal Covariance")]
    for prior in constants.DCFS_PRIORS:
        if not Load_Data:
            print("GMM WITH SAME PER-CLASS COMPONENTS")
            gmm_components = []
            # mindcfs of Full Covariance, of Diagonal Covariance, of Tied Covariance, of Tied Diagonal Covariance
            raw_full_min_dcfs = []
            raw_diag_min_dcfs = []
            raw_tied_min_dcfs = []
            raw_tied_diag_min_dcfs = []

            zNorm_full_min_dcfs = []
            zNorm_diag_min_dcfs = []
            zNorm_tied_min_dcfs = []
            zNorm_tied_diag_min_dcfs = []

            pca_full_min_dcfs = []
            pca_diag_min_dcfs = []
            pca_tied_min_dcfs = []
            pca_tied_diag_min_dcfs = []

            zNormPca_full_min_dcfs = []
            zNormPca_diag_min_dcfs = []
            zNormPca_tied_min_dcfs = []
            zNormPca_tied_diag_min_dcfs = []

            for nSplit in range(0,11):
                # from 2 to 1024 components
                print("Number of GMM Components: " + str(2**nSplit) + "\n")
                gmm_components.append(2**nSplit)
                print("Prior = " + str(prior) + "\n")

                print("RAW (No PCA No Z_Norm)\n")
                # minDcfs[0] mindcfs of Full Covariance, minDcfs[1] of Diagonal Covariance, minDcfs[2] of Tied Covariance, minDcfs[3] of Tied Diagonal Covariance
                raw_minDcfs,_,_ = kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifiers,nSplit0=nSplit,nSplit1=None,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
                raw_full_min_dcfs.append(raw_minDcfs[0])
                raw_diag_min_dcfs.append(raw_minDcfs[1])
                raw_tied_min_dcfs.append(raw_minDcfs[2])
                raw_tied_diag_min_dcfs.append(raw_minDcfs[3]) 

                print("Z_Norm\n")
                zNorm_minDcfs,_,_ = kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifiers,nSplit0=nSplit,nSplit1=None,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
                zNorm_full_min_dcfs.append(zNorm_minDcfs[0])
                zNorm_diag_min_dcfs.append(zNorm_minDcfs[1])
                zNorm_tied_min_dcfs.append(zNorm_minDcfs[2])
                zNorm_tied_diag_min_dcfs.append(zNorm_minDcfs[3]) 
                
                m = 8
                print("RAW + PCA with M = " + str(m) + "\n")
                pca_minDcfs,_,_ = kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifiers,nSplit0=nSplit,nSplit1=None,PCA_Flag=True,M=m,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
                pca_full_min_dcfs.append(pca_minDcfs[0])
                pca_diag_min_dcfs.append(pca_minDcfs[1])
                pca_tied_min_dcfs.append(pca_minDcfs[2])
                pca_tied_diag_min_dcfs.append(pca_minDcfs[3])

                print("Z_Norm + PCA with M = " + str(m) + "\n")
                zNormPca_minDcfs,_,_ = kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifiers,nSplit0=nSplit,nSplit1=None,PCA_Flag=True,M=m,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
                zNormPca_full_min_dcfs.append(zNormPca_minDcfs[0])
                zNormPca_diag_min_dcfs.append(zNormPca_minDcfs[1])
                zNormPca_tied_min_dcfs.append(zNormPca_minDcfs[2])
                zNormPca_tied_diag_min_dcfs.append(zNormPca_minDcfs[3])
            
            # Save gmm components
            # Save the list of objects to a file
            with open("modelData/components_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(gmm_components, f)

            # Save All Combinations for This Prior
            # Save the list of objects to a file
            with open("modelData/raw_full_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_full_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/raw_diag_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_diag_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/raw_tied_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_tied_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/raw_tied_diag_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_tied_diag_min_dcfs, f)
            
            # Save the list of objects to a file
            with open("modelData/zNorm_full_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_full_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNorm_diag_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_diag_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNorm_tied_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_tied_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNorm_tied_diag_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_tied_diag_min_dcfs, f)
            
            # Save the list of objects to a file
            with open("modelData/pca_full_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_full_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/pca_diag_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_diag_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/pca_tied_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_tied_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/pca_tied_diag_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_tied_diag_min_dcfs, f)
            
            # Save the list of objects to a file
            with open("modelData/zNormPca_full_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_full_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNormPca_diag_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_diag_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNormPca_tied_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_tied_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNormPca_tied_diag_gmm" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_tied_diag_min_dcfs, f)

        if Load_Data:
            # Retrieve data for plotting
            # Retrieve the list of objects from the file
            with open("modelData/components_gmm" + str(prior) + ".pkl", "rb") as f:
                gmm_components = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/raw_full_gmm" + str(prior) + ".pkl", "rb") as f:
                raw_full_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/raw_diag_gmm" + str(prior) + ".pkl", "rb") as f:
                raw_diag_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/raw_tied_gmm" + str(prior) + ".pkl", "rb") as f:
                raw_tied_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/raw_tied_diag_gmm" + str(prior) + ".pkl", "rb") as f:
                raw_tied_diag_min_dcfs = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_full_gmm" + str(prior) + ".pkl", "rb") as f:
                zNorm_full_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_diag_gmm" + str(prior) + ".pkl", "rb") as f:
                zNorm_diag_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_tied_gmm" + str(prior) + ".pkl", "rb") as f:
                zNorm_tied_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_tied_diag_gmm" + str(prior) + ".pkl", "rb") as f:
                zNorm_tied_diag_min_dcfs = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/pca_full_gmm" + str(prior) + ".pkl", "rb") as f:
                pca_full_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/pca_diag_gmm" + str(prior) + ".pkl", "rb") as f:
                pca_diag_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/pca_tied_gmm" + str(prior) + ".pkl", "rb") as f:
                pca_tied_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/pca_tied_diag_gmm" + str(prior) + ".pkl", "rb") as f:
                pca_tied_diag_min_dcfs = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_full_gmm" + str(prior) + ".pkl", "rb") as f:
                zNormPca_full_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_diag_gmm" + str(prior) + ".pkl", "rb") as f:
                zNormPca_diag_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_tied_gmm" + str(prior) + ".pkl", "rb") as f:
                zNormPca_tied_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_tied_diag_gmm" + str(prior) + ".pkl", "rb") as f:
                zNormPca_tied_diag_min_dcfs = pickle.load(f)


        m = 8
        # ----- PLOT GMMS   ------
        plot.gmm_dcf_plot(raw_full_min_dcfs,zNorm_full_min_dcfs,pca_full_min_dcfs,zNormPca_full_min_dcfs,gmm_components,"Full Covariance (standard)",m_pca=m)
        
        plot.gmm_dcf_plot(raw_diag_min_dcfs,zNorm_diag_min_dcfs,pca_diag_min_dcfs,zNormPca_diag_min_dcfs,gmm_components,"Diagonal Covariance",m_pca=m)
        
        plot.gmm_dcf_plot(raw_tied_diag_min_dcfs,zNorm_tied_min_dcfs,pca_tied_min_dcfs,zNormPca_tied_min_dcfs,gmm_components,"Tied Covariance",m_pca=m)
        
        plot.gmm_dcf_plot(raw_tied_diag_min_dcfs,zNorm_tied_diag_min_dcfs,pca_tied_diag_min_dcfs,zNormPca_tied_diag_min_dcfs,gmm_components,"Tied Diagonal Covariance",m_pca=m)


def trainGMMAllCombinations(DTR_RAND,LTR_RAND,Load_Data=False):
    # ---------- GMM WITH ALL POSSIBLE COMPONENTS COMBINATION -----------
    # classifier = [(gmm.LBGalgorithm,gmm.constraintSigma,"Full Covariance (standard)")]
    # print("Raw Full Cov G0=4 G1=1")
    # print("DcfPrior: 0.5")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=2,nSplit1=0,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.5,Calibration_Flag=None)
    # print("DcfPrior: 0.1")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=2,nSplit1=0,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.1,Calibration_Flag=None)
    # print("DcfPrior: 0.9")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=2,nSplit1=0,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.9,Calibration_Flag=None)
    # classifier = [(gmm.DiagLBGalgorithm,gmm.DiagConstraintSigma,"Diagonal Covariance")]
    # print("Raw Diag Cov G0=8 G1=2")
    # print("DcfPrior: 0.5")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=3,nSplit1=1,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.5,Calibration_Flag=None)
    # print("DcfPrior: 0.1")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=3,nSplit1=1,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.1,Calibration_Flag=None)
    # print("DcfPrior: 0.9")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=3,nSplit1=1,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.9,Calibration_Flag=None)
    # classifier = [(gmm.TiedLBGalgorithm, gmm.constraintSigma, "Tied Covariance")]
    # print("Raw Tied Cov G0=8 G1=8")
    # print("DcfPrior: 0.5")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=3,nSplit1=3,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.5,Calibration_Flag=None)
    # print("DcfPrior: 0.1")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=3,nSplit1=3,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.1,Calibration_Flag=None)
    # print("DcfPrior: 0.9")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=3,nSplit1=3,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.9,Calibration_Flag=None)
    # classifier = [(gmm.TiedDiagLBGalgorithm,gmm.DiagConstraintSigma,"Tied Diagonal Covariance")]
    # print("Raw Tied Diag Cov G0=8 G1=2")
    # print("DcfPrior: 0.5")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=3,nSplit1=1,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.5,Calibration_Flag=None)
    # print("DcfPrior: 0.1")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=3,nSplit1=1,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.1,Calibration_Flag=None)
    # print("DcfPrior: 0.9")
    # kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifier,nSplit0=3,nSplit1=1,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=0.9,Calibration_Flag=None)

    classifiers = [(gmm.LBGalgorithm,gmm.constraintSigma,"Full Covariance (standard)"), (gmm.DiagLBGalgorithm,gmm.DiagConstraintSigma,"Diagonal Covariance"), (gmm.TiedLBGalgorithm, gmm.constraintSigma, "Tied Covariance"),(gmm.TiedDiagLBGalgorithm,gmm.DiagConstraintSigma,"Tied Diagonal Covariance")]
    for prior in constants.DCFS_PRIORS:
        if not Load_Data:
            print("Prior = " + str(prior) + "\n")
            colors = {
                0 : 'blue',
                1 : 'red',
                2 : 'green',
                3 : 'yellow',
                4 : 'magenta',
                5 : 'cyan',
                6 : 'black',
                7 : 'white'
            }
            print("GMM WITH ALL POSSIBLE COMPONENTS COMBINATION")
            labels = []
            plot_colors = []
            gmm_components_class_1 = []
            # mindcfs of Full Covariance, of Diagonal Covariance, of Tied Covariance, of Tied Diagonal Covariance
            raw_full_min_dcfs = []
            raw_diag_min_dcfs = []
            raw_tied_min_dcfs = []
            raw_tied_diag_min_dcfs = []

            zNorm_full_min_dcfs = []
            zNorm_diag_min_dcfs = []
            zNorm_tied_min_dcfs = []
            zNorm_tied_diag_min_dcfs = []

            pca_full_min_dcfs = []
            pca_diag_min_dcfs = []
            pca_tied_min_dcfs = []
            pca_tied_diag_min_dcfs = []

            zNormPca_full_min_dcfs = []
            zNormPca_diag_min_dcfs = []
            zNormPca_tied_min_dcfs = []
            zNormPca_tied_diag_min_dcfs = []

            for nSplit0 in range(0,4):
                print("Number of GMM Components of Class 0: " + str(2**nSplit0))
                labels.append("minDCF G0 = " + str(2**nSplit0))
                plot_colors.append(colors[nSplit0])
                gmm_components_class_1_single = []

                raw_full_min_dcfs_single = []
                raw_diag_min_dcfs_single = []
                raw_tied_min_dcfs_single = []
                raw_tied_diag_min_dcfs_single = []

                zNorm_full_min_dcfs_single = []
                zNorm_diag_min_dcfs_single = []
                zNorm_tied_min_dcfs_single = []
                zNorm_tied_diag_min_dcfs_single = []

                pca_full_min_dcfs_single = []
                pca_diag_min_dcfs_single = []
                pca_tied_min_dcfs_single = []
                pca_tied_diag_min_dcfs_single = []

                zNormPca_full_min_dcfs_single = []
                zNormPca_diag_min_dcfs_single = []
                zNormPca_tied_min_dcfs_single = []
                zNormPca_tied_diag_min_dcfs_single = []
                for nSplit1 in range(0,4):
                    # from 2 to 1024 components
                    print("Number of GMM Components of Class 1: " + str(2**nSplit1))
                    gmm_components_class_1_single.append(2**nSplit1)
                    # minDcfs[0] mindcfs of Full Covariance, minDcfs[1] of Diagonal Covariance, minDcfs[2] of Tied Covariance, minDcfs[3] of Tied Diagonal Covariance

                    print("RAW (No PCA No Z_Norm)\n")
                    raw_minDcfs,_,_ = kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifiers,nSplit0=nSplit0,nSplit1=nSplit1,PCA_Flag=None,M=None,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
                    
                    raw_full_min_dcfs_single.append(raw_minDcfs[0])
                    raw_diag_min_dcfs_single.append(raw_minDcfs[1])
                    raw_tied_min_dcfs_single.append(raw_minDcfs[2])
                    raw_tied_diag_min_dcfs_single.append(raw_minDcfs[3]) 

                    print("Z_Norm\n")
                    zNorm_minDcfs,_,_ = kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifiers,nSplit0=nSplit0,nSplit1=nSplit1,PCA_Flag=None,M=None,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
                    
                    zNorm_full_min_dcfs_single.append(zNorm_minDcfs[0])
                    zNorm_diag_min_dcfs_single.append(zNorm_minDcfs[1])
                    zNorm_tied_min_dcfs_single.append(zNorm_minDcfs[2])
                    zNorm_tied_diag_min_dcfs_single.append(zNorm_minDcfs[3]) 
                    
                    m = 8
                    print("RAW + PCA with M = " + str(m) + "\n")
                    pca_minDcfs,_,_ = kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifiers,nSplit0=nSplit0,nSplit1=nSplit1,PCA_Flag=True,M=m,Z_Norm_Flag=None,Dcf_Prior=prior,Calibration_Flag=None)
                    
                    pca_full_min_dcfs_single.append(pca_minDcfs[0])
                    pca_diag_min_dcfs_single.append(pca_minDcfs[1])
                    pca_tied_min_dcfs_single.append(pca_minDcfs[2])
                    pca_tied_diag_min_dcfs_single.append(pca_minDcfs[3]) 
                    
                    print("Z_Norm + PCA with M = " + str(m) + "\n")
                    zNormPca_minDcfs,_,_ = kfold.K_Fold_GMM(DTR_RAND,LTR_RAND,K=constants.K,classifiers=classifiers,nSplit0=nSplit0,nSplit1=nSplit1,PCA_Flag=True,M=m,Z_Norm_Flag=True,Dcf_Prior=prior,Calibration_Flag=None)
                    
                    zNormPca_full_min_dcfs_single.append(zNormPca_minDcfs[0])
                    zNormPca_diag_min_dcfs_single.append(zNormPca_minDcfs[1])
                    zNormPca_tied_min_dcfs_single.append(zNormPca_minDcfs[2])
                    zNormPca_tied_diag_min_dcfs_single.append(zNormPca_minDcfs[3]) 

                gmm_components_class_1.append(gmm_components_class_1_single)
                
                raw_full_min_dcfs.append(raw_full_min_dcfs_single)
                raw_diag_min_dcfs.append(raw_diag_min_dcfs_single)
                raw_tied_min_dcfs.append(raw_tied_min_dcfs_single)
                raw_tied_diag_min_dcfs.append(raw_tied_diag_min_dcfs_single)

                zNorm_full_min_dcfs.append(zNorm_full_min_dcfs_single)
                zNorm_diag_min_dcfs.append(zNorm_diag_min_dcfs_single)
                zNorm_tied_min_dcfs.append(zNorm_tied_min_dcfs_single)
                zNorm_tied_diag_min_dcfs.append(zNorm_tied_diag_min_dcfs_single)

                pca_full_min_dcfs.append(pca_full_min_dcfs_single)
                pca_diag_min_dcfs.append(pca_diag_min_dcfs_single)
                pca_tied_min_dcfs.append(pca_tied_min_dcfs_single)
                pca_tied_diag_min_dcfs.append(pca_tied_diag_min_dcfs_single)

                zNormPca_full_min_dcfs.append(zNormPca_full_min_dcfs_single)
                zNormPca_diag_min_dcfs.append(zNormPca_diag_min_dcfs_single)
                zNormPca_tied_min_dcfs.append(zNormPca_tied_min_dcfs_single)
                zNormPca_tied_diag_min_dcfs.append(zNormPca_tied_diag_min_dcfs_single)
            
            # Save Data

            # Save the list of objects to a file
            with open("modelData/labels_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(labels, f)
            
            # Save the list of objects to a file
            with open("modelData/colors_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(plot_colors, f)
            
            # Save the list of objects to a file
            with open("modelData/components_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(gmm_components_class_1, f)

            # Save the list of objects to a file
            with open("modelData/raw_full_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_full_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/raw_diag_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_diag_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/raw_tied_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_tied_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/raw_tied_diag_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(raw_tied_diag_min_dcfs, f)
            
            # Save the list of objects to a file
            with open("modelData/zNorm_full_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_full_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNorm_diag_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_diag_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNorm_tied_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_tied_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNorm_tied_diag_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNorm_tied_diag_min_dcfs, f)
            
            # Save the list of objects to a file
            with open("modelData/pca_full_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_full_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/pca_diag_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_diag_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/pca_tied_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_tied_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/pca_tied_diag_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(pca_tied_diag_min_dcfs, f)
            
            # Save the list of objects to a file
            with open("modelData/zNormPca_full_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_full_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNormPca_diag_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_diag_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNormPca_tied_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_tied_min_dcfs, f)
            # Save the list of objects to a file
            with open("modelData/zNormPca_tied_diag_gmm_allComb" + str(prior) + ".pkl", "wb") as f:
                pickle.dump(zNormPca_tied_diag_min_dcfs, f)

        if Load_Data:
            # Retrieve data for plotting

            # Retrieve the list of objects from the file
            with open("modelData/labels_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                labels = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/colors_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                plot_colors = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/components_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                gmm_components_class_1 = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/raw_full_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                raw_full_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/raw_diag_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                raw_diag_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/raw_tied_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                raw_tied_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/raw_tied_diag_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                raw_tied_diag_min_dcfs = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_full_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                zNorm_full_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_diag_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                zNorm_diag_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_tied_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                zNorm_tied_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNorm_tied_diag_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                zNorm_tied_diag_min_dcfs = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/pca_full_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                pca_full_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/pca_diag_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                pca_diag_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/pca_tied_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                pca_tied_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/pca_tied_diag_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                pca_tied_diag_min_dcfs = pickle.load(f)
            
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_full_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                zNormPca_full_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_diag_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                zNormPca_diag_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_tied_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                zNormPca_tied_min_dcfs = pickle.load(f)
            # Retrieve the list of objects from the file
            with open("modelData/zNormPca_tied_diag_gmm_allComb" + str(prior) + ".pkl", "rb") as f:
                zNormPca_tied_diag_min_dcfs = pickle.load(f)


        # ----- PLOT GMMS ALL COMBINATIONS  ------
        m = 8

        # ----- RAW -------
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,raw_full_min_dcfs,labels,plot_colors,"Full Covariance (standard) no PCA no Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,raw_diag_min_dcfs,labels,plot_colors,"Diagonal Covariance no PCA no Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,raw_tied_min_dcfs,labels,plot_colors,"Tied Covariance no PCA no Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,raw_tied_diag_min_dcfs,labels,plot_colors,"Tied Diagonal Covariance no PCA no Znorm")

        # ----- zNorm -------
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,zNorm_full_min_dcfs,labels,plot_colors,"Full Covariance (standard) no PCA Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,zNorm_diag_min_dcfs,labels,plot_colors,"Diagonal Covariance no PCA Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,zNorm_tied_min_dcfs,labels,plot_colors,"Tied Covariance no PCA Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,zNorm_tied_diag_min_dcfs,labels,plot_colors,"Tied Diagonal Covariance no PCA Znorm")

        # ----- PCA -------
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,pca_full_min_dcfs,labels,plot_colors,"Full Covariance (standard) PCA=" + str(m) + " no Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,pca_diag_min_dcfs,labels,plot_colors,"Diagonal Covariance PCA=" + str(m) + " no Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,pca_tied_min_dcfs,labels,plot_colors,"Tied Covariance PCA=" + str(m) + " no Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,pca_tied_diag_min_dcfs,labels,plot_colors,"Tied Diagonal Covariance PCA=" + str(m) + " no Znorm")

        # ----- zNorm PCA -------
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,pca_full_min_dcfs,labels,plot_colors,"Full Covariance (standard) PCA=" + str(m) + " Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,pca_diag_min_dcfs,labels,plot_colors,"Diagonal Covariance PCA=" + str(m) + " Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,pca_tied_min_dcfs,labels,plot_colors,"Tied Covariance PCA=" + str(m) + " Znorm")
        plot.gmm_plot_all_component_combinations(gmm_components_class_1,pca_tied_diag_min_dcfs,labels,plot_colors,"Tied Diagonal Covariance PCA=" + str(m) + " Znorm")

