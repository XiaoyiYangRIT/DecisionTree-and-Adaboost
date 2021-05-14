from Models import features as fe
import math

def learn(trainset, times = 10):
    """
    The adaboost Learning function
    :param trainset: All datas for the training
    :return: The ensemble dictionary for weight of all decision stump
    """
    # Initialize the ensemble and weight
    ensemble = {}
    weight = []
    size = len(trainset)
    for i in range(size):
        weight.append(1 / size) 
    
    attrs = fe.features
    
    # Iterate all features
    # Repeat the boosting to increase the accuracy
    for time in range(times):
        for i in range(fe.NUM_FEATURES):
            # Initialize the error to 0
            error = 0

            # Find the incorrectly predicted data and sum up the error weight
            for j in range(size):
                # All the true expect the positive, which is "nl". Otherwise, "en"
                if(trainset[j][i] and trainset[j][-1] == fe.negative) or ((not trainset[j][i]) and trainset[j][-1] == fe.positive):
                    error = error + weight[j]

            # Update the weight of correctly predicted data
            for j in range(size):
                if(trainset[j][i] and trainset[j][-1] == fe.positive) or ((not trainset[j][i]) and trainset[j][-1] == fe.negative):
                    weight[j] = weight[j] * error / (1 - error)

            # Normalize all weights
            weight = normalize(weight)

            # Calculate the weight of the current stump
            ensemble[i] = math.log((1 - error) / error)
    return ensemble
            
def predict(example, hypo):
    """
    The adaboost predict function
    print out the predict outcome
    :param example: One data to be predicted
    :param hypo: The generated emsemble
    """
    weight = 0
    for i in range(fe.NUM_FEATURES):
        if example[i]:
            weight = weight + hypo[i]
        else:
            weight = weight - hypo[i]
    if(weight >= 0):
        print(fe.positive)
    else:
        print(fe.negative)
    
def normalize(weights):
    """
    Normalize the weight of all hypothesis by adjust the sum to 1
    :param weights: Weights of all hypothesis
    :return: The updated weights
    """
    result = []
    Sum = sum(weights)
    result = []
    time = 1 / Sum
    for weight in weights:
        weight = weight * time
        result.append(weight)
    return result