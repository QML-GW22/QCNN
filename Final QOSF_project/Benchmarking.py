import data
import Training
import QCNN_circuit
import Hierarchical_circuit
import numpy as np

def accuracy_test(predictions, labels, binary = True):
    if binary == True:
        acc = 0
        for l, p in zip(labels, predictions):
            if np.abs(l - p) < 1:
                acc = acc + 1
        return acc / len(labels)

    else:
        acc = 0
        for l, p in zip(labels, predictions):
            if np.abs(l - p) < 0.5:
                acc = acc + 1
        return acc / len(labels)

def Encoding_to_Embedding(Encoding):
    if Encoding == 'resize256':
        Embedding = 'Amplitude'
    elif Encoding == 'pca8':
        Embedding = 'Angle'
    elif Encoding == 'autoencoder8':
        Embedding = 'Angle'

    # Amplitude Hybrid Embedding
    elif Encoding == 'pca32':
        Embedding = 'Amplitude-Hybrid4'
    elif Encoding == 'autoencoder32':
        Embedding = 'Amplitude-Hybrid4'

    elif Encoding == 'pca16':
        Embedding = 'Amplitude-Hybrid2'
    elif Encoding == 'autoencoder16':
        Embedding = 'Amplitude-Hybrid2'

    # Angular HybridEmbedding
    elif Encoding == 'pca30':
        Embedding = 'Angular-Hybrid4'
    elif Encoding == 'autoencoder30':
        Embedding = 'Angular-Hybrid4'
    elif Encoding == 'pca6':
        Embedding = 'Angular-Hybrid2'
    elif Encoding == 'autoencoder6':
        Embedding = 'Angular-Hybrid2'
    return Embedding


def Benchmarking(dataset, classes, Unitaries, U_num_params, Encodings, circuit, binary=True):
    I = len(Unitaries)
    J = len(Encodings)

    # save the result in the result.txt file
    f = open('Result/result.txt', 'w')

    for i in range(I):
        for j in range(J):
            U = Unitaries[i]
            U_params = U_num_params[i]
            Encoding = Encodings[j]
            Embedding = Encoding_to_Embedding(Encoding)

            X_train, X_test, Y_train, Y_test = data.data_load_and_process(dataset, classes=classes,
                                                                          feature_reduction=Encoding, binary=binary)

            print("\n")
            print("Loss History for " + circuit + " circuits, " + U + " " + Encoding)
            loss_history, trained_params = Training.circuit_training(X_train, Y_train, U, U_params, Embedding, circuit)

            if circuit == 'QCNN':
                predictions = [QCNN_circuit.QCNN(x, trained_params, U, U_params, Embedding) for x in X_test]
            elif circuit == 'Hierarchical':
                predictions = [Hierarchical_circuit.Hierarchical_classifier(x, trained_params, U, U_params, Embedding) for x in X_test]

            accuracy = accuracy_test(predictions, Y_test, binary)
            print("Accuracy for " + U + " " + Encoding + " :" + str(accuracy))

            f.write("Loss History for " + circuit + " circuits, " + U + " " + Encoding)
            f.write("\n")
            f.write(str(loss_history))
            f.write("\n")
            f.write("Accuracy for " + U + " " + Encoding + " :" + str(accuracy))
            f.write("\n")
            f.write("\n")
    f.close()

def Data_norm(dataset, classes, Encodings, binary=True):
    J = len(Encodings)
    Num_data = 1000

    f = open('Result/data_norm.txt', 'w')

    for j in range(J):
        Encoding = Encodings[j]

        X_train, X_test, Y_train, Y_test = data.data_load_and_process(dataset, classes=classes,
                                                                          feature_reduction=Encoding, binary=binary)

        if Encoding == 'pca32' or Encoding == 'autoencoder32':
            norms_X1 = []
            norms_X2 = []
            for i in range(Num_data):
                index = np.random.randint(0, len(X_train))
                X = X_train[index]

                X1 = X[:2 ** 4]
                X2 = X[2 ** 4:2 ** 5]
                norm_X1, norm_X2 = np.linalg.norm(X1), np.linalg.norm(X2)
                norms_X1.append(norm_X1)
                norms_X2.append(norm_X2)

            norms_X1, norms_X2 = np.array(norms_X1), np.array(norms_X2)
            mean_X1, stdev_X1 = np.mean(norms_X1), np.std(norms_X1)
            mean_X2, stdev_X2 = np.mean(norms_X2), np.std(norms_X2)

            if Encoding == 'pca32':
                f.write("PCA32 Encoding\n")
            elif Encoding == 'autoencoder32':
                f.write("autoencoder32 Encoding\n")
            f.write("mean of X1: " + str(mean_X1) + " standard deviation of X1: " + str(stdev_X1))
            f.write("\n")
            f.write("mean of X2: " + str(mean_X2) + " standard deviation of X2: " + str(stdev_X2))
            f.write("\n")

        elif Encoding == 'pca16' or Encoding == 'autoencoder16':
            norms_X1 = []
            norms_X2 = []
            norms_X3 = []
            norms_X4 = []
            for i in range(Num_data):
                index = np.random.randint(0, len(X_train))
                X = X_train[index]

                X1 = X[:4]
                X2 = X[4:8]
                X3 = X[8:12]
                X4 = X[12:16]
                norm_X1, norm_X2, norm_X3, norm_X4 = np.linalg.norm(X1), np.linalg.norm(X2), np.linalg.norm(
                    X3), np.linalg.norm(X4)

                norms_X1.append(norm_X1)
                norms_X2.append(norm_X2)
                norms_X3.append(norm_X3)
                norms_X4.append(norm_X4)

            norms_X1, norms_X2, norms_X3, norms_X4 = np.array(norms_X1), np.array(norms_X2), np.array(norms_X3), np.array(norms_X4)

            mean_X1, stdev_X1 = np.mean(norms_X1), np.std(norms_X1)
            mean_X2, stdev_X2 = np.mean(norms_X2), np.std(norms_X2)
            mean_X3, stdev_X3 = np.mean(norms_X3), np.std(norms_X3)
            mean_X4, stdev_X4 = np.mean(norms_X4), np.std(norms_X4)

            if Encoding == 'pca16':
                f.write("PCA16 Encoding\n")
            elif Encoding == 'autoencoder16':
                f.write("autoencoder16 Encoding\n")
            f.write("mean of X1: " + str(mean_X1) + " standard deviation of X1: " + str(stdev_X1))
            f.write("\n")
            f.write("mean of X2: " + str(mean_X2) + " standard deviation of X2: " + str(stdev_X2))
            f.write("\n")
            f.write("mean of X3: " + str(mean_X3) + " standard deviation of X3: " + str(stdev_X3))
            f.write("\n")
            f.write("mean of X4: " + str(mean_X4) + " standard deviation of X4: " + str(stdev_X4))
            f.write("\n")

    f.close()
