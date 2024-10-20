# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data
data = pd.read_csv('assignment5.csv')

data = np.array(data)
m, n = data.shape 
np.random.shuffle(data)

train_size = int(0.7 * m)
test_size = int(0.2 * m)

data_train = data[:train_size].T
Y_train = data_train[0]
X_train = data_train[1:n]
X_train = X_train / 255.

data_val = data[train_size:train_size+test_size].T
Y_val = data_val[0]
X_val = data_val[1:n]
X_val = X_val / 255.

data_test = data[train_size+test_size:].T
Y_test = data_test[0]
X_test = data_test[1:n]
X_test = X_test / 255.
    
# Main Functions
def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
    A1 = np.maximum(Z1, 0) # ReLu

    Z2 = W2.dot(A1) + b2
    A2 = np.exp(Z2) / sum(np.exp(Z2)) # Softmax

    return Z1, A1, Z2, A2

def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):

    one_hot_Y = np.zeros((Y.size, Y.max() + 1))
    one_hot_Y[np.arange(Y.size), Y] = 1
    one_hot_Y = one_hot_Y.T

    dZ2 = A2 - one_hot_Y
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2)

    dZ1 = W2.T.dot(dZ2) * (Z1 > 0)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1)
    
    return dW1, db1, dW2, db2

def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1    
    W2 = W2 - alpha * dW2  
    b2 = b2 - alpha * db2    
    return W1, b1, W2, b2

def train_model(X, Y, alpha, iterations):
    
    W1 = np.random.rand(10, 784) - 0.5 
    b1 = np.random.rand(10, 1) - 0.5

    W2 = np.random.rand(10, 10) - 0.5 
    b2 = np.random.rand(10, 1) - 0.5

    best_val_acc = 0
    best_params = (W1, b1, W2, b2)

    val_accs = []  # to store validation accuracies at each iteration

    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)

        # Evaluate performance on training set
        train_predictions = np.argmax(A2, 0)
        train_acc = np.sum(train_predictions == Y_train) / Y_train.size

        # Evaluate performance on validation set
        Z1_val, A1_val, Z2_val, A2_val = forward_prop(W1, b1, W2, b2, X_val)
        val_predictions = np.argmax(A2_val, 0)
        val_acc = np.sum(val_predictions == Y_val) / Y_val.size
        val_accs.append(val_acc)  # store validation accuracy at each iteration

        # Print progress and update best parameters if validation accuracy improves
        if i % 10 == 0:
            print("Training accuracy: ", train_acc)
            print("Validation accuracy: ", val_acc)
            print("_________________________________")
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_params = (W1, b1, W2, b2)

    # Plot validation accuracy vs. iterations
    plt.plot(np.arange(iterations), val_accs)
    plt.xlabel('Iterations')
    plt.ylabel('Accuracy')
    plt.title('Changing Accuracy In Validation Set')
    plt.show()

    return W1, b1, W2, b2

def test_model(X_test, Y_test, W1, b1, W2, b2):
    Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X_test)
    predictions = np.argmax(A2, axis=0)
    accuracy = np.sum(predictions == Y_test) / Y_test.size

    # Calculate percentage of correctness for each class
    classes = np.unique(Y_test)
    correct_percents = []
    for cls in classes:
        idx = np.where(Y_test == cls)[0]
        correct_idx = np.where(predictions[idx] == cls)[0]
        correct_percent = 100 * len(correct_idx) / len(idx)
        correct_percents.append(correct_percent)

    # Plot bar chart
    for i in range(len(correct_percents)):
        print(i, correct_percents[i])
    plt.bar(classes, correct_percents)
    plt.xlabel('Classes')
    plt.ylabel('Percentage Accuracy')
    plt.title('Correctness of trained ANN')
    plt.show()

    return accuracy


# Driver Code
W1, b1, W2, b2 = train_model(X_train, Y_train, 0.10, 1000)
test_accuracy = test_model(X_test, Y_test, W1, b1, W2, b2)
print(test_accuracy*100)
