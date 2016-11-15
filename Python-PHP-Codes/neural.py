# Package imports
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import sklearn.datasets
import sklearn.linear_model
import matplotlib
import json


'''
Training data
'''
with open('../Output-files/features.json','r') as features_file:
	data=json.load(features_file)
y=[]
data= data['Stock Features']
ll=[]
for i in range((7*len(data))/10):
	l=[]
	l.append(data[i]['On Balance Volume'])
	# l.append(data[i]['Price Momentum Oscillator'])
	# l.append(data[i]['Moving Average'])
	# l.append(data[i]['Stochastic Oscillator'])
	# l.append(data[i]['Relative Strength Index'])
	ll.append(l)
	if(data[i]['Target']==1):
		y.append(1)
	else:
		y.append(0)
X=np.array(ll)


num_examples = len(X) # training set size
nn_input_dim = 1 # input layer dimensionality
nn_output_dim = 2 # output layer dimensionality

# Gradient descent parameters (I picked these by hand)
epsilon = 0.01 # learning rate for gradient descent
reg_lambda = 0.01 # regularization strength


# Helper function to evaluate the total loss on the dataset
def calculate_loss(model):
    W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
    # Forward propagation to calculate our predictions
    z1 = X.dot(W1) + b1
    a1 = np.tanh(z1)
    z2 = a1.dot(W2) + b2
    exp_scores = np.exp(z2)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    # Calculating the loss
    corect_logprobs = -np.log(probs[range(num_examples), y])
    data_loss = np.sum(corect_logprobs)
    # Add regulatization term to loss (optional)
    data_loss += reg_lambda/2 * (np.sum(np.square(W1)) + np.sum(np.square(W2)))
    return 1./num_examples * data_loss

# Helper function to predict an output (0 or 1)
def predict(model, x):
    W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
    # Forward propagation
    # print "in predict function"
    # print type(x)
    # print x
    # print len(x)
    # print len(W1)
    # print len(b1)
    z1 = x.dot(W1) + b1

    # print "z1 "
    # print z1
    # print len(z1)

    a1 = np.tanh(z1)
    z2 = a1.dot(W2) + b2
    
    # print len(b2)
    # print len(z2)

    exp_scores = np.exp(z2)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    # print "probs is "
    # print len(probs)
    # print probs
    print "returning this"
    print np.argmax(probs, axis=1)
    return np.argmax(probs, axis=1)
    # return probs
# This function learns parameters for the neural network and returns the model.
# - nn_hdim: Number of nodes in the hidden layer
# - num_passes: Number of passes through the training data for gradient descent
# - print_loss: If True, print the loss every 1000 iterations
def build_model(nn_hdim, num_passes=20000, print_loss=False):
    
    # Initialize the parameters to random values. We need to learn these.
    global epsilon
    np.random.seed(0)
    W1 = np.random.randn(nn_input_dim, nn_hdim) / np.sqrt(nn_input_dim)
    b1 = np.zeros((1, nn_hdim))
    W2 = np.random.randn(nn_hdim, nn_output_dim) / np.sqrt(nn_hdim)
    b2 = np.zeros((1, nn_output_dim))

    # This is what we return at the end
    model = {}
    # Gradient descent. For each batch...
    for i in xrange(0, num_passes):
    	
        # Forward propagation
        z1 = X.dot(W1) + b1
        a1 = np.tanh(z1)
        z2 = a1.dot(W2) + b2
        exp_scores = np.exp(z2)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        # print "below are the probabilities"
        # print probs[0],
        # print probs[1]
        # Backpropagation
        delta3 = probs
        delta3[range(num_examples), y] -= 1
        dW2 = (a1.T).dot(delta3)
        db2 = np.sum(delta3, axis=0, keepdims=True)
        delta2 = delta3.dot(W2.T) * (1 - np.power(a1, 2))
        dW1 = np.dot(X.T, delta2)
        db1 = np.sum(delta2, axis=0)

        # Add regularization terms (b1 and b2 don't have regularization terms)
        dW2 += reg_lambda * W2
        dW1 += reg_lambda * W1

        # Gradient descent parameter update
        W1 += -epsilon * dW1
        b1 += -epsilon * db1
        W2 += -epsilon * dW2
        b2 += -epsilon * db2
        
        # Assign new parameters to the model
        model = { 'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
        
        # Optionally print the loss.
        # This is expensive because it uses the whole dataset, so we don't want to do it too often.
        if print_loss and i % 1000 == 0:
          print "Loss after iteration %i: %f" %(i, calculate_loss(model))
    
    return model




o=[]
model = build_model(200, print_loss=True)

'''
Testing data
'''

ll=[]
for i in range((7*len(data))/10,len(data)):
	l=[]
	l.append(data[i]['On Balance Volume'])
	# l.append(data[i]['Price Momentum Oscillator'])
	# l.append(data[i]['Moving Average'])
	# l.append(data[i]['Stochastic Oscillator'])
	# l.append(data[i]['Relative Strength Index'])
	ll.append(l)
	if(data[i]['Target']==1):
		o.append(1)
	else:
		o.append(0)
z=np.array(ll)
print 'predicted this '
pre= predict(model,z)

print 'actual output is '
print o

cnt=0
for i in range(len(o)):
	if(o[i]==pre[i]):
		cnt+=1
print "accuracy is "+str(float(cnt)/len(o))