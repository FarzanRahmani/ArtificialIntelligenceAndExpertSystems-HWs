import pandas as pd
import math

# since features are continuous we need to calculate mean and variance for each feature
possiblity ={}
means = {}
variances = {}

# Calculate possiblity for each species_kind and return the species_kind with maximum possiblity
def calculate_possiblity(row):
    probability = possiblity.copy()
    for feature in row.index:
        if feature != 'species_kind':
            for species_kind in probability.keys():
                probability[species_kind] *= condition_probability(species_kind , feature , row[feature])
    return max(probability , key= probability.get)

# Calculate condition probability for each feature given species_kind (P(feature|species_kind)) and return the probability using Gaussian Naive Bayes formula 
def condition_probability(species_kind , feature , number):
    answer = (1 / math.sqrt(2 * math.pi * variances[(feature , species_kind)]))* math.exp(((-(number - means[(feature , species_kind)])**2))/ (2 * variances[(feature , species_kind)]))
    return answer

def print_result(accuracy, right_answer, test):
    print("$-------------------------------------------$")
    print("My Naive Bayes Implementation accuracy is " + str(accuracy) + "%")
    print("number of mislabeled points out of a total %d points : %d" % (test.count()[0], (test.count()[0] - right_answer)))
    print("number of correct answers is : " + str(right_answer))
    print("$-------------------------------------------$")
    # save result in a txt file
    file = open("NavieBayesOutPut.txt", "w")
    # clear file content
    file.truncate(0)
    # write new content
    file.write("$-------------------------------------------$\n")
    file.write("My Naive Bayes Implementation accuracy is " + str(accuracy) + "% \n")
    file.write("number of mislabeled points out of a total %d points : %d \n" % (test.count()[0], (test.count()[0] - right_answer)))
    file.write("number of correct answers is : " + str(right_answer) + " \n")
    file.write("$-------------------------------------------$")
    file.close()

def main():
    # Read iris data set and extract it 
    iris_dataset = pd.read_csv("iris.data" , names=['feature_0' , 'feature_1' , 'feature_2' , 'feature_3' , 'species_kind'])

    # Split data set into training data and test data
    training_data = iris_dataset.sample(n = int(iris_dataset.count()[0] * 0.8)) # 80% training and 20% test
    test_data = iris_dataset[~iris_dataset.index.isin(training_data.index)]
    test_data = test_data.reset_index(drop = True)
    training_data = training_data.reset_index(drop = True)

    # calculate possiblity for each species_kind
    for i in range(training_data['species_kind'].nunique()):
        possiblity[training_data['species_kind'].value_counts().index[i]] = training_data['species_kind'].value_counts()[i] / training_data['species_kind'].count()

    # Calculate mean and variance for each feature beacause we need it for Gaussian Naive Bayes
    for feature in training_data.columns :
        if feature != 'species_kind':
            for species_kind in training_data['species_kind'].unique():
                means[(feature , species_kind)] = training_data.groupby(by = ['species_kind']).describe()[feature]['mean'][species_kind]
                variances[(feature , species_kind)] = math.pow(training_data.groupby(by = ['species_kind']).describe()[feature]['std'][species_kind], 2)    


    # Calculate possiblity for each species_kind for each row in test data set and compare it with the real species_kind and calculate accuracy
    correct_answers = 0
    for index , row in test_data.iterrows():
        possible_answer = calculate_possiblity(row)
        if row['species_kind'] == possible_answer:
            correct_answers += 1
    accuracy_rate = (correct_answers / test_data.count()[0]) * 100

    print_result(accuracy_rate, correct_answers, test_data)

if __name__ == "__main__":
    main()