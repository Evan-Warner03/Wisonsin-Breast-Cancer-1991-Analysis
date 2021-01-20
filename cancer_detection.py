# Program which is primarily used to analyze breast cancer data from wisconsin
# Created by Evan Warner, January 10, 2021

# data obtained from: https://wisostat.uni-koeln.de/fileadmin/sites/statistik/Datenportal/data_descriptions/Breast_cancer_Wisconsin.pdf

class Node():
    
    """
    A Node is an object which is primarily used to build the decision tree. Each
    Node has a value, and a left and right, which are either boolean values or
    Nodes.
    """
    
    def __init__(self, value=None, left=None, right=None):
        
        # if values are not specified, simply create an empty Node
        self.value = value
        self.left = left
        self.right = right
    
    
    def __str__(self):
        # return a formatted string which illustrates the shape of the
        # decision tree
        return "<{}> {} <{}>".format(str(self.left), self.value, str(self.right))



def get_characteristics():
    """
    get_characteristics() -> List
    
    Retrieves the data from "breast-cancer-wisconsin.txt", classifies it, and
    returns the data as a list of tumours
    """
    
    # open the file
    in_file = open("breast-cancer-wisconsin.txt")
    
    tumours = []
    for line in in_file:
        # split the csv's and remove the id tag which is arbitrarily assigned
        line = line.strip()
        line = line.split(",")
        line = line[1:]
        
        # handle unknown data
        for i in range(len(line)):
            if line[i] != '?':
                line[i] = int(line[i])
            
        tumours.append(line)
    
    # create labels to categorize the given data, which is typically 1-10
    classifiers = [
        ["small_clump", "moderate_clump", "large_clump"], 
        ["csize_not_uniform", "csize_moderately_uniform", "csize_very_uniform"], 
        ["cshape_not_uniform", "cshape_moderately_uniform", "cshape_very_uniform"], 
        ["not_very_adhesive", "moderately_adhesive", "very_adhesive"], 
        ["small_sec_size", "moderate_sec_size", "large_sec_size"], 
        ["few_bare_nuclei", "some_bare_nuclei", "many_bare_nuclei"], 
        ["few_bland_chromatin", "some_bland_chromatin", "many_bland_chromatin"],
        ["few_normal_nucleoli", "some_normal_nucleoli", "many_normal_nucleoli"],
        ["little_mitosis", "some_mitosis", "much_mitosis"]
        ]
    classifier_ints = [3,7,10]  
    
    # iterate through the data, and replace it with the above classifiers
    for i in range(len(tumours)):
        new_tumour = []
        for ii in range(len(tumours[i])-1):
            if tumours[i][ii] != "?":
                for iii in range(len(classifier_ints)):
                    if tumours[i][ii] <= classifier_ints[iii] and len(new_tumour)-1 != ii:
                        new_tumour.append(classifiers[ii][iii])
                        
        tumours[i] = [tumours[i][-1], new_tumour]
    
    return tumours



def get_attributes(tumours):
    """
    get_attributes(List) -> List
    
    Given a list of tumours, returns a list of attributes the tumours have,
    with no duplicates
    """
    
    attributes = []
    
    # iterate through each tumour
    for t in tumours:
        for att in t[1]:
            
            # check if it is already in the list of attributes
            if att not in attributes:
                attributes.append(att)
                
    return attributes



def split_attributes(tumours, attribute, ben_mal=False):
    """
    split_attributes(List, Any, Bool) -> List
    
    Splits the given tumours by the given attribute, will split the tumours
    by characteristics if ben_mal is False, or by whether or not the tumour is
    Malignant or Benign otherwise
    """
    
    with_att = []
    without_att = []
    
    for t in tumours:
        
        # check if the attribute is a feature of this tumour
        if ben_mal and attribute == t[0]:
            with_att.append(t)
        
        # check if this tumour is Benign or Malignant
        elif attribute in t[1]:
            with_att.append(t)
        
        # otherwise the tumour must be without the attribute
        else:
            without_att.append(t)
    
    return with_att, without_att



def decision_tree(tumours):
    """
    decision_tree(List) -> Leaf
    
    Given a list of tumours, creates and returns a decision tree which can be
    used to best predict whether unknown tumours are Benign or Malignant
    """
    
    # get the attributes from all the tumours
    atts = get_attributes(tumours)
    
    # find how many in the list of tumours are Malignant, and how
    # many are Benign
    ben, mal = split_attributes(tumours, 2, True)
    
    # if the list of attributes is empty, there is nothing left to
    # distinguish the tumours, therefore return the most likely answer,
    # based on the given tumours
    if atts == []:
        return mal > ben
    
    # otherwise, split the tumours into two lists, by checking if they
    # have the first attribute in the list of all attributes
    att = atts[0]
    with_att, without_att = split_attributes(tumours, att)
    
    # if every tumour is Benign, it must be that this branch is always False
    if mal == []:
        return False
    
    # if every tumour is Malignant, it must be that this branch is always True
    elif ben == []:
        return True
    
    # otherwise, remove the attribute used to split the list from the tumours
    else:
        for i in range(len(with_att)):
            if att in with_att[i][1]:
                with_att[i][1].remove(att)
                
        # crate a Leaf, with the left value of the Leaf being the branch to 
        # follow if the tumour does have that initial attribute, and the 
        # right value being the branch to follow if the tumour does not
        # have the attribute
        return Node(att, decision_tree(with_att), decision_tree(without_att))



def predict(dtree, tumour):
    """
    predict(Leaf, List) -> Bool
    
    Given a decision tree and a single tumour, uses the decision tree to
    predict whether or not the tumour is Malignant (True), or Benign (False)
    """
    
    # if the Leaf is just a boolean, we have arrived at a prediction
    if dtree == True or dtree == False:
        return dtree
    
    # if the attribute is in tumour, take the left branch
    elif dtree.value in tumour:
        return predict(dtree.left, tumour)
    
    # otherwise take the right branch
    else:
        return predict(dtree.right, tumour)



def test(dtree, tumours):
    """
    test(Leaf, List) -> Str
    
    Outputs the percentage accuracy of the tree, following the results of
    testing the tree with each tumour in tumours
    """
    
    # track score
    score = 0
    
    # iterate through every tumour
    for t in tumours:
        
        # make a prediction
        pred = predict(dtree, tumours)
        
        # check if the prediction matches the expected output, 
        # add a point if so
        
        if pred and t[0] == 4:
            score += 1
        
        elif not pred and t[0] == 2:
            score += 1
    
    # output a well formatted message describing the accuracy of the decision
    # tree, and the number of tests conducted
    print("the decision tree was accurate {:.2f}% of the time, over {} test cases".format(score/len(tumours)*100, len(tumours)))



if __name__ == "__main__":
    # --- default creation and testing of decision tree --- #
    # retrieve the information from the file
    tumours = get_characteristics()
    
    # create a tree using 619 cases, and allow the tree to be tested
    # on the last 80 (by default)
    tree = decision_tree(tumours[:619])
    test(tree, tumours[619:])
