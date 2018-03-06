import math
import sys
def make_dictionaries(dictionary,trainin_set_attributes,training_set,classifier):
    if classifier == None:
        column = 0
        for attribute_list in trainin_set_attributes:
            attr_dict = {}
            for attribute in attribute_list:
                attr_dict[attribute] = calculate_general_probability(attribute, column, training_set)
            dictionary[column] = attr_dict
            column += 1
    else:
        column = 0
        for attribute_list in trainin_set_attributes:
            attr_dict = {}
            for attribute in attribute_list:
                attr_dict[attribute] = calculate_probability(attribute,classifier,column,training_set)
            dictionary[column] = attr_dict
            column += 1
    return dictionary

def partition(training_set, training_set_attributes):
    p_dict = {}
    e_dict = {}
    general_probability_dictionary = {}

    p_dict = make_dictionaries(p_dict,training_set_attributes,training_set,"p")
    e_dict = make_dictionaries(e_dict,training_set_attributes,training_set,"e")
    general_probability_dictionary = make_dictionaries(general_probability_dictionary,training_set_attributes,training_set,None)
    dictionary_list = []
    dictionary_list.append(p_dict)
    dictionary_list.append(e_dict)
    dictionary_list.append(general_probability_dictionary)
    return dictionary_list
def calculate_general_probability(attribute, column, training_set):
    count = 0
    for line in training_set:
        if line[column] == attribute:
            count += 1
    return count / len(training_set)

def calculate_probability(attribute, classifier,column, training_set):
    count = 0
    for line in training_set:
        if line[column] == attribute and line[0] == classifier:
            count += 1
    classifier_count = 0
    for line in training_set:
        if line[0] == classifier:
            classifier_count += 1
    return count / classifier_count


def run_bayes(training, testing, output):

    p_dict = {}
    e_dict = {}
    general_probability_dict = {}

    data = open(training)
    training_set = []
    training_set_attributes = []
    for line in data:
        training_set += [line.split()]

    columns = len(training_set[0])

    for i in range(0, columns):
        temp_set = []
        for line in training_set:
            if line[i] not in temp_set:
                temp_set.append((line[i]))
        training_set_attributes.append(temp_set)
    dictionary_list = partition(training_set,training_set_attributes)
    p_dict = dictionary_list[0]
    e_dict = dictionary_list[1]
    general_probability_dict = dictionary_list [2]

    test_set = test_data(p_dict,e_dict,general_probability_dict,testing)

    test_bayes_data = open(testing)
    accuracy_test_set = []
    for line in test_bayes_data:
        accuracy_test_set += [line.split()]

    accuracy_percentage = compare(test_set,accuracy_test_set)

    output_results(accuracy_percentage,test_set,output)

def output_results(accuracy_percentage, test_set, output):
    out = open(output, "w+")
    out.write("Using the given test file we have " + str(accuracy_percentage) + "% accuracy\n")
    index = 1
    for line in test_set:
        predicted_label = line[0]
        out.write(
            "Predicted label for row " + str(index) + " is: " + predicted_label + ". The whole line is: " + str(line))
        out.write("\n")
        index += 1
def test_data(p_dict, e_dict,general_probability_dict, testing):
    test_bayes_data = open(testing)
    test_set = []
    accuracy_test_set = []
    for line in test_bayes_data:
        accuracy_test_set += [line.split()]
    for line in accuracy_test_set:
        test_set += [line[1:]]
    test_set = test(p_dict,e_dict,general_probability_dict,test_set)
    return test_set

def test(p_dict,e_dict,general_probability_dict,test_set):


    for line in test_set:
        p_probability = 1
        e_probability = 1
        general_probability = 1
        for column in range(0,len(line)):
            attribute = line[column]
            p_probability *= extract_probability(p_dict,attribute,column+1)
            e_probability *= extract_probability(e_dict,attribute,column+1)
            general_probability *= extract_probability(general_probability_dict,attribute,column+1)
        if (p_probability / general_probability) > (e_probability / general_probability):
            line.insert(0,"p")
        else:
            line.insert(0,"e")
    return test_set

def compare(test_set,accuracy_set):
    count = 0
    for i in range(len(test_set)):
        if test_set[i][0] == accuracy_set[i][0]:
            count+=1
    return 100 * (count / len(test_set))

def extract_probability(dictionary, attribute, column):
    Attribute_dict = dictionary[column]

    probability = Attribute_dict[attribute]
    return probability

if __name__ == '__main__':
    training_data = sys.argv[1]
    testing_data = sys.argv[2]
    output_file = sys.argv[3]

    run_bayes(training_data,testing_data,output_file)