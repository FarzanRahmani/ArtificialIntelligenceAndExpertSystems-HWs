import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

def print_result(accuracy , x_test_data , y_predict , y_test_data):
    print("$-------------------------------------------$")
    print("scikit-learn Naive Bayes accuracy is " + str(accuracy*100) + "%")
    print("number of mislabeled points out of a total %d points : %d" % (x_test_data.count()[0], int((x_test_data.count()[0] - accuracy * x_test_data.count()[0]))))
    print("number of correct answers is : " + str(int(accuracy * x_test_data.count()[0])))
    # print("Predicted species_kind is : " + str(y_predict))
    # print("Real species_kind is : " + str(y_test_data))
    print("$-------------------------------------------$")
    # save result in a txt file
    file = open("scikit_learn_result.txt" , "w")
    # clear file content
    file.truncate(0)
    # write new content
    file.write("$-------------------------------------------$\n")
    file.write("scikit-learn Naive Bayes accuracy is " + str(accuracy *100) + "% \n")
    file.write("number of mislabeled points out of a total %d points : %d" % (x_test_data.count()[0], int((x_test_data.count()[0] - accuracy * x_test_data.count()[0]))) + " \n")
    file.write("number of correct answers is : " + str(int(accuracy * x_test_data.count()[0])) + " \n")
    file.write("$-------------------------------------------$")
    file.close()

def main():
    # Read iris data set and extract it 
    iris_dataset = pd.read_csv("iris.data" , names=['feature_0' , 'feature_1' , 'feature_2' , 'feature_3' , 'species_kind'])

    # Split data set into training data and test data
    x = iris_dataset[['feature_0' , 'feature_1' , 'feature_2' , 'feature_3']]
    y = iris_dataset['species_kind']
    x_training_data , x_test_data , y_training_data , y_test_data = train_test_split(x , y , test_size=0.2) # 80% training and 20% test

    # Create Gaussian Naive Bayes model and train it
    model = GaussianNB()
    y_predict = model.fit(x_training_data , y_training_data).predict(x_test_data) # predict test data

    # Calculate accuracy
    accuracy = accuracy_score(y_test_data , y_predict)
    print_result(accuracy , x_test_data , y_predict , y_test_data)

if __name__ == "__main__":
    main()