import numpy as np
import scipy.special
import csv
import sys


# input: train_image.csv train_label.csv test_image.csv
class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.learning_rate = 0.2
        self.sigmoid_function = lambda x: scipy.special.expit(x)
        self.softmax_function = lambda x: np.exp(x)/sum(np.exp(x))
        self.weight_input_hidden = np.random.rand(self.hidden_nodes, self.input_nodes) - 0.5
        self.weight_hidden_output = np.random.rand(self.output_nodes, self.hidden_nodes) - 0.5

        pass

    def train(self, train_list, correct_labels):
        inputs = np.array(train_list, ndmin=2).T    # 784 x 1
        labels = np.array(correct_labels, ndmin=2).T

        hidden_input = np.dot(self.weight_input_hidden, inputs)
        hidden_output = self.sigmoid_function(hidden_input)

        result_input = np.dot(self.weight_hidden_output, hidden_output)
        result_output_softmax = self.softmax_function(result_input)

        output_error = result_output_softmax - labels
        hidden_error = np.dot(self.weight_hidden_output.T, output_error)
        result_sigmoid_deri = result_output_softmax * (1 - result_output_softmax)
        hidden_sigmoid_deri = hidden_output * (1 - hidden_output)
        red = output_error * result_sigmoid_deri
        hed = hidden_error * hidden_sigmoid_deri

        self.weight_hidden_output -= self.learning_rate * np.dot(red, np.transpose(hidden_output))
        self.weight_input_hidden -= self.learning_rate * np.dot(hed, np.transpose(inputs))

        pass

    def query(self, query_list):
        queries = np.array(query_list, ndmin=2).T

        hidden_input = np.dot(self.weight_input_hidden, queries)
        hidden_output = self.sigmoid_function(hidden_input)
        final_input = np.dot(self.weight_hidden_output, hidden_output)
        final_output_activation = self.softmax_function(final_input)

        return final_output_activation


def make_prediction():
    training_image_file = open(sys.argv[1], 'r')
    training_label_file = open(sys.argv[2], 'r')
    training_image_lists = training_image_file.readlines()
    training_label_lists = training_label_file.readlines()
    training_image_file.close()
    training_label_file.close()

    input_nodes = 784
    hidden_nodes = 200
    output_nodes = 10
    n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes)

    epochs = 10
    for e in range(epochs):
        print('Epoch: ', e + 1)
        for index in range(len(training_image_lists)):
            values_in_str = training_image_lists[index].split(',')
            # normalize all input values
            query_list = (np.asfarray(values_in_str) / 255)

            correct_labels = np.zeros(output_nodes) + 0.0
            correct_labels[int(training_label_lists[index])] = 1.0
            n.train(query_list, correct_labels)

    # start querying
    test_image_file = open(sys.argv[3], 'r')
    test_image_lists = test_image_file.readlines()
    test_image_file.close()

    prediction = []
    for image in test_image_lists:
        image_str = image.split(',')
        test_image = (np.asfarray(image_str) / 255.0)
        output_list = n.query(test_image)

        result = np.argmax(output_list)
        prediction.append(result)

    with open('test_predictions.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in prediction:
            csvwriter.writerow([i])


def accuracy_check():
    count = 0
    validation_file = open('test_predictions.csv', 'r')
    validation_array = validation_file.readlines()
    validation_file.close()
    test_label_file = open('test_label.csv', 'r')
    correct_array = test_label_file.readlines()
    test_label_file.close()

    for index, result in enumerate(validation_array):
        if int(result) == int(correct_array[index]):
            count += 1
        # else:
        #     print('Index: ', index+1, result, correct_array[index])
    accuracy = count / len(validation_array)
    print('Accuracy: ', accuracy * 100, '%')


if __name__ == "__main__":
    make_prediction()
    accuracy_check()
