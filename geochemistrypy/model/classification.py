# -*- coding: utf-8 -*-
# import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import classification_report, plot_confusion_matrix, confusion_matrix
from utils.base import save_fig
from global_variable import MODEL_OUTPUT_IMAGE_PATH
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
# sys.path.append("..")


class ClassificationWorkflowBase(object):

    X = None
    y = None
    name = None
    common_function = ["Model Score", "Confusion Matrix"]
    special_function = None

    @classmethod
    def show_info(cls):
        print("*-*" * 2, cls.name, "is running ...", "*-*" * 2)
        print("Expected Functionality:")
        function = cls.common_function + cls.special_function
        for i in range(len(function)):
            print("+ ", function[i])

    def __init__(self, random_state: int = 42) -> None:
        self.random_state = random_state
        self.model = None
        self.naming = None

    @staticmethod
    def data_split(X_data, y_data, test_size=0.2, random_state=42):
        ClassificationWorkflowBase.X = X_data
        ClassificationWorkflowBase.y = y_data
        X_train, X_test, y_train, y_test = train_test_split(ClassificationWorkflowBase.X,
                                                            ClassificationWorkflowBase.y,
                                                            test_size=test_size,
                                                            random_state=random_state)
        return X_train, X_test, y_train, y_test

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        y_test_prediction = self.model.predict(X_test)
        return y_test_prediction

    @staticmethod
    def score(y_test, y_test_prediction):
        print("-----* Model Score *-----")
        print(classification_report(y_test, y_test_prediction))

    def confusion_matrix_plot(self, X_test, y_test, y_test_prediction):
        print("-----* Confusion Matrix *-----")
        print(confusion_matrix(y_test, y_test_prediction))
        plot_confusion_matrix(self.model, X_test, y_test)
        plt.show()
        save_fig(f"Confusion Matrix - {self.naming}", MODEL_OUTPUT_IMAGE_PATH)


class SVMClassification(ClassificationWorkflowBase):

    name = "Support Vector Machine"
    special_function = ['Two-dimensional Decision Boundary Diagram']

    def __init__(
            self,
            C=1.0,
            kernel='rbf',
            degree=3,
            gamma="scale",
            coef0=0.0,
            shrinking=True,
            probability=False,
            tol=1e-3,
            cache_size=200,
            class_weight=None,
            verbose=False,
            max_iter=-1,
            decision_function_shape="ovr",
            break_ties=False,
            random_state=None
    ):
        ##############################################################
        #Support vector machine is used to classify the data
        ##############################################################
        """
        :param C:float, default=1.0 Regularization parameter. The strength of the regularization is inversely proportional to C. Must be strictly positive. The penalty is a squared l2 penalty.
        :param kernel:Specifies the kernel type to be used in the algorithm
        :param degree:Degree of the polynomial kernel function (‘poly’). Ignored by all other kernels.
        :param gamma:Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’.
        :param coef0:Independent term in kernel function. It is only significant in ‘poly’ and ‘sigmoid’.
        :param shrinking:Whether to use the shrinking heuristic. See the User Guide
        :param probability:Whether to enable probability estimates. This must be enabled prior to calling , will slow down that method as it internally uses 5-fold cross-validation, and may be inconsistent with .
        :param tol:Whether to enable probability estimates. This must be enabled prior to calling , will slow down that method as it internally uses 5-fold cross-validation, and may be inconsistent with .
        :param cache_size:Specify the size of the kernel cache (in MB).
        :param class_weight:Set the parameter C of class i to class_weight[i]*C for SVC.
        :param verbose:Enable verbose output. Note that this setting takes advantage of a per-process runtime setting in libsvm that, if enabled, may not work properly in a multithreaded context.
        :param max_iter:Hard limit on iterations within solver, or -1 for no limit.
        :param decision_function_shape:Whether to return a one-vs-rest (‘ovr’) decision function of shape (n_samples, n_classes) as all other classifiers, or the original one-vs-one (‘ovo’) decision function of libsvm which has shape (n_samples, n_classes * (n_classes - 1) / 2). However, note that internally, one-vs-one (‘ovo’) is always used as a multi-class strategy to train models; an ovr matrix is only constructed from the ovo matrix. The parameter is ignored for binary classification.
        :param break_ties:If true, , and number of classes > 2, predict will break ties according to the confidence values of decision_function; otherwise the first class among the tied classes is returned. Please note that breaking ties comes at a relatively high computational cost compared to a simple predict
        :param random_state:Controls the pseudo random number generation for shuffling the data for probability estimates. Ignored when is False. Pass an int for reproducible output across multiple function calls. See Glossary.

        References
        ----------------------------------------
        API design for machine learning software: experiences from the scikit-learn project.Buitinck, LarLouppe, GillesBlondel, MathieuPedregosa, FabianMueller, AndreasGrise, Olivierculae, VladPrettenhofer, PeterGramfort, AlexandreGrobler, JaquesLayton, RobertVanderplas, JakeJoly, ArnaudHolt, BrianVaroquaux, Gaël
        http://arxiv.org/abs/1309.0238
        """
        super().__init__(random_state)
        self.C = C
        self.kernel = kernel
        self.degree = degree
        self.gamma = gamma
        self.coef0 = coef0
        self.shrinking = shrinking
        self.probability = probability
        self.tol = tol
        self.cache_size = cache_size
        self.class_weight = class_weight
        self.verbose = verbose
        self.max_iter = max_iter
        self.decision_function_shape = decision_function_shape
        self.break_ties = break_ties
        self.random_state = random_state

        self.model = SVC(C=self.C,
                         kernel=self.kernel,
                         degree=self.degree,
                         gamma=self.gamma,
                         coef0=self.coef0,
                         shrinking=self.shrinking,
                         probability=self.probability,
                         tol=self.tol,
                         cache_size=self.cache_size,
                         class_weight=self.class_weight,
                         verbose=self.verbose,
                         max_iter=self.max_iter,
                         decision_function_shape=self.decision_function_shape,
                         break_ties=self.break_ties,
                         random_state=self.random_state)
        self.naming = SVMClassification.name


    def plot_svc_function(self):
        """
        Dichotomize the two selected elements and draw an image

        """
        print("PLot_SVC_Function")
        y = np.array(ClassificationWorkflowBase().y)
        X = np.array(ClassificationWorkflowBase().X)
        y = np.squeeze(y)
        clf = self.model.fit(X,y)
        plt.scatter(X[:, 0], X[:, 1], c=y, s=50, edgecolors='k',cmap="rainbow")
        ax = plt.gca()
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        x = np.linspace(xlim[0], xlim[1], 30)
        y = np.linspace(ylim[0], ylim[1], 30)
        Y, X = np.meshgrid(y, x)
        xy = np.vstack([X.ravel(), Y.ravel()]).T
        P = clf.decision_function(xy).reshape(X.shape)
        ax.contour(X, Y, P, colors="k", levels=[-1, 0, 1], alpha=0.5, linestyles=["--", "-", "--"])
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        save_fig('plot_svc', MODEL_OUTPUT_IMAGE_PATH)
        plt.show()

    def special_components(self):
        self.plot_svc_function()


class DecisionTreeClassification(ClassificationWorkflowBase):

    name = "DecisionTree"
    special_function = ["DecisionTree Tree Plot Function"]

    def __init__(
            self,
            criterion='gini',
            splitter='best',
            max_depth=3,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0.0,
            max_features=None,
            random_state=None,
            max_leaf_nodes=None,
            min_impurity_decrease=0.0,
            class_weight=None,
            ccp_alpha=0.0
    ):
        ##############################################################################
        #Classification of data using machine learning models with decision trees
        ##############################################################################
        """
        :param criterion:The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “log_loss” and “entropy” both for the Shannon information gain
        :param splitter:The strategy used to choose the split at each node. Supported strategies are “best” to choose the best split and “random” to choose the best random split.
        :param max_depth:The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.
        :param min_samples_split:The minimum number of samples required to split an internal node
        :param min_samples_leaf:The minimum number of samples required to be at a leaf node. A split point at any depth will only be considered if it leaves at least min_samples_leaf training samples in each of the left and right branches. This may have the effect of smoothing the model, especially in regression.
        :param min_weight_fraction_leaf:The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node. Samples have equal weight when sample_weight is not provided.
        :param max_features:The number of features to consider when looking for the best split
        :param random_state:Controls the randomness of the estimator.
        :param max_leaf_nodes:Grow a tree with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes.
        :param min_impurity_decrease:A node will be split if this split induces a decrease of the impurity greater than or equal to this value.
        :param class_weight:Weights associated with classes in the form {class_label: weight}.
        :param ccp_alpha:Complexity parameter used for Minimal Cost-Complexity Pruning.

        References
        ----------------------------------------
        API design for machine learning software: experiences from the scikit-learn project.Buitinck, LarLouppe, GillesBlondel, MathieuPedregosa, FabianMueller, AndreasGrise, Olivierculae, VladPrettenhofer, PeterGramfort, AlexandreGrobler, JaquesLayton, RobertVanderplas, JakeJoly, ArnaudHolt, BrianVaroquaux, Gaël
        http://arxiv.org/abs/1309.0238
        """
        super().__init__(random_state)
        self.criterion = criterion
        self.splitter = splitter
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        self.class_weight = class_weight
        self.ccp_alpha = ccp_alpha
        self.model = DecisionTreeClassifier(criterion=self.criterion,
                                            splitter=self.splitter,
                                            max_depth=self.max_depth,
                                            min_samples_split=self.min_samples_split,
                                            min_samples_leaf=self.min_samples_leaf,
                                            min_weight_fraction_leaf=self.min_weight_fraction_leaf,
                                            max_features=self.max_features,
                                            random_state=self.random_state,
                                            max_leaf_nodes=self.max_leaf_nodes,
                                            min_impurity_decrease=self.min_impurity_decrease,
                                            class_weight=self.class_weight,
                                            ccp_alpha=self.ccp_alpha)
        self.naming = DecisionTreeClassification.name

    def plot_tree_function(self):
        ###################################################
        #Drawing decision tree diagrams
        ###################################################
        print("Plot_Tree_Function")
        y = ClassificationWorkflowBase().y
        X = ClassificationWorkflowBase().X
        clf = self.model.fit(X,y)
        tree.plot_tree(clf, filled=True)
        save_fig('plot_decisiontree', MODEL_OUTPUT_IMAGE_PATH)
        plt.show()

    def special_components(self):
        self.plot_tree_function()