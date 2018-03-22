"""logistic model class for binary classification."""
import tensorflow as tf
import numpy as np


class LogisticModel_TF(object):

    def __init__(self, ndims, W_init='zeros'):
        """Initialize a logistic model.

        This function prepares an initialized logistic model.
        It will initialize the weight vector, self.W, based on the method
        specified in W_init.

        We assume that the FIRST index of Weight is the bias term,
            Weight = [Bias, W1, W2, W3, ...]
            where Wi correspnds to each feature dimension

        W_init needs to support:
          'zeros': initialize self.W with all zeros.
          'ones': initialze self.W with all ones.
          'uniform': initialize self.W with uniform random number between [0,1)
          'gaussian': initialize self.W with gaussion distribution (0, 0.1)

        Args:
            ndims(int): feature dimension
            W_init(str): types of initialization.
        """
        self.ndims = ndims
        self.W_init = W_init
        self.W0 = None
        ###############################################################
        # Fill your code below
        ###############################################################
        if W_init == 'zeros':
            self.W0 = tf.zeros([self.ndims+1,1],dtype=tf.float64)

        elif W_init == 'ones':
            self.W0 = tf.ones([self.ndims+1,1],dtype=tf.float64)

        elif W_init == 'uniform':
            self.W0 = tf.random_uniform([self.ndims+1,1],0,1,dtype=tf.float64)

        elif W_init == 'gaussian':
            self.W0 = tf.random_normal([self.ndims+1,1],0,1,dtype=tf.float64)
        else:
            print ('Unknown W_init ', W_init)


    def build_graph(self, learn_rate):
        """ build tensorflow training graph for logistic model.
        Args:
            learn_rate: learn rate for gradient descent
            ......: append as many arguments as you want
        """
        ###############################################################
        # Fill your code in this function
        ###############################################################
        self.W = tf.Variable(self.W0)
        self.Y = tf.placeholder(tf.float64, shape=(None,1))
        self.X = tf.placeholder(tf.float64, shape=(None, self.ndims+1))
        # loss = tf.matmul(tf.transpose(self.Y - (1 / (1 + tf.exp( tf.matmul( -self.X,self.W))))), self.Y - (1 / (1+ tf.exp(tf.matmul( -self.X, self.W)))))
        loss = tf.reduce_sum(tf.square(self.Y - (1/(1+tf.exp(-1*tf.matmul(self.X,self.W)))) ))
        self.optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(loss)


    def fit(self, Y_true, X, max_iters):
        """ train model with input dataset using gradient descent.
        Args:
            Y_true(numpy.ndarray): dataset labels with a dimension of (# of samples,1)
            X(numpy.ndarray): input dataset with a dimension of (# of samples, ndims+1)
            max_iters: maximal number of training iterations
            ......: append as many arguments as you want
        Returns:
            (numpy.ndarray): sigmoid output from well trained logistic model, used for classification
                             with a dimension of (# of samples, 1)
        """
        ###############################################################
        # Fill your code in this function
        ###############################################################
        init = tf.global_variables_initializer()
        sess = tf.Session()
        sess.run(init)
        print(type(X),type(Y_true))
        for itr in range(max_iters):
            sess.run(self.optimizer, feed_dict={self.X: X, self.Y : Y_true})
            prob = sess.run(1 / (1 + tf.exp(tf.matmul(-X, self.W))))
            val = prob
            val[val>=0.5] = 1
            val[val<0.5] = 0
            y_predict = np.array(val)

            s = np.sum(Y_true == y_predict)

            acc = s / len(Y_true)
            #print('Iteration : ',itr,'Accuracy : ', acc)

        #print('Finished')

        return prob



