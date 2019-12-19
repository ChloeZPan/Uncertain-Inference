## Project 3: Uncertain Inference

In this project, we implemented some of the algorithms of uncertain inference. We parsed .xml files and represented Bayesian networks with tree structure. For exact inference, we implemented the “inference by enumeration” algorithm. For approximate inference, we implemented the rejection sampling algorithm. In addition, we used three sample networks to test our code.

# 1 Architecture
![image](https://github.com/ChloeZPan/Uncertain-Inference/blob/master/image/figure1.PNG)
Figure 1: Architecture of the program

# 2 XMLBIF Parsing and Network Representation
The main two function to parse the .xml files and present bayesian networks are build_bn() and dog_build_bn(). For dog_problem.xml is slightly different to the other 2 .xml file, we use dog_build_bn() to parse the file and build the networks. In particular, when passing the element from xml to the Bayesian networks, variables will be in topological order which means the parents nodes should be entered before their children nodes.

We represent the Bayesian networks as a tree. A BayesianNet class has nodes, variables, variable_values and two methods variable_node() and add(). Nodes are represented using a class named BayesNode. Variable_values are set to a list [True, False] in this project. variable_node() is a method to get the node of a specific variable. add() is a method to add node to the tree. The networks presentation of the three testing cases are as below.

(1) aima-alarm
![image](https://github.com/ChloeZPan/Uncertain-Inference/blob/master/image/figure2.PNG)
Figure 2: Representation of AIAM-Alarm Networks
(2) wet-grass
![image](https://github.com/ChloeZPan/Uncertain-Inference/blob/master/image/figure3.PNG)
Figure 3: Representation of Wet-grass Networks
(3) dog-problem
![image](https://github.com/ChloeZPan/Uncertain-Inference/blob/master/image/figure4.PNG)
Figure 4: Representation of Dog-problem Networks

## 3 Exact Inference
In this part, we implement the “inference by enumeration” algorithm described in AIMA Section 14.4. In file InferenceByEnum.py, class ProbDist is used to present a discrete probability distribution. Enumeration_ask and enumeration_all will return the conditional probability distribution of a variable given evidences. The results of testing the three files are below:

(1) When test ﬁle is aima-alarm.xml, the query variable is B, and the evidence variables are J with value true and M also with value true.
(2) When test ﬁle is aima-wet-grass.xml, the query variable is R, and the evidence variables are S with value true.
(3) When test ﬁle is dog-problem.xml, the query variable is hear-bark, and the evidence variables are family-out with value true and bowel-problem with value true.

## 4 Approximate Inference
We implement an approximate inferencer using rejection sampling algorithm. Function prior_sample generates events from a given Bayesian network. Each variable is sampled at random according with the conditional probability given the parents. Function rejection_sampling generates number of samples specified in the command line using function prior_sample and only calculated the number of samples that is consistent with the given evidences. Finally, function rejection_sampling returns the conditional probability of the query variables in the form of {True : p1, False : p2}.
The implementation is based on the pseudocode of rejection sampling in figure 14.14 of AIMA.
