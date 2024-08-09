

def read_image(image_filename):
    """
    Reads an image from a file.
    
    :param image_filename: String representing the name of the file.
    :return: 2D list of integers representing an image.
    """
    with open(image_filename,"r") as image_file:
        image = []
        for line in image_file:
            y = []
            for x_i in line.strip():
                y.append(int(x_i))
            image.append(y)
    return image


def linear(x, w, b):
    """
    Input: A list of inputs (x), a list of weights (w) and a bias (b).
    Output: A single number corresponding to the value of f(x) in Equation 1.

    >>> x = [1.0, 3.5]
    >>> w = [3.8, 1.5]
    >>> b = -1.7
    >>> round(linear(x, w, b),6) #linear(x, w, b)
    7.35
    """

    return sum(w[j]*x[j] for j in range(len(w))) + b


def linear_layer(x, w, b):
    """
    Input: A list of inputs (x), a table of weights (w) and a list of
           biases (b).
    Output: A list of numbers corresponding to the values of f(x) in
            Equation 2.
    
    >>> x = [1.0, 3.5]
    >>> w = [[3.8, 1.5], [-1.2, 1.1]]
    >>> b = [-1.7, 2.5]
    >>> y = linear_layer(x, w, b)
    >>> [round(y_i,6) for y_i in y] #linear_layer(x, w, b)
    [7.35, 5.15]
    """

    return [linear(x, w[i], b[i]) for i in range(len(w))]


def relu_layer(x, w, b):
    """
    Input: A list of inputs (x), a table of weights (w) and a
           list of biases (b).
    Output: A list of numbers corresponding to the values of f(x) in
            Equation 4.

    >>> x = [1, 0]
    >>> w = [[2.1, -3.1], [-0.7, 4.1]]
    >>> b = [-1.1, 4.2]
    >>> y = relu_layer(x, w, b)
    >>> [round(y_i,6) for y_i in y] #relu_layer(x, w, b)
    [1.0, 3.5]
    >>> x = [0, 1]
    >>> y = relu_layer(x, w, b)
    >>> [round(y_i,6) for y_i in y] #relu_layer(x, w, b)
    [0.0, 8.3]
    """

    return [max(linear(x, w[i], b[i]), 0.0) for i in range(len(w))]


def inference(x, w, b):
    """
    Input: A list of inputs (x), a list of tables of weights (w) and a table
           of biases (b).
    Output: A list of numbers corresponding to output of the ANN.
    
    >>> x = [1, 0]
    >>> w = [[[2.1, -3.1], [-0.7, 4.1]], [[3.8, 1.5], [-1.2, 1.1]]]
    >>> b = [[-1.1, 4.2], [-1.7, 2.5]]
    >>> y = inference(x, w, b)
    >>> [round(y_i,6) for y_i in y] #inference(x, w, b)
    [7.35, 5.15]
    """

    num_layers = len(w)
    
    for l in range(num_layers-1):
        x = relu_layer(x, w[l], b[l])
        
    return linear_layer(x, w[num_layers-1], b[num_layers-1])


def read_weights(file_name):
    """
    Input: A string (file_name) that corresponds to the name of the file
           that contains the weights of the ANN.
    Output: A list of tables of numbers corresponding to the weights of
            the ANN.
    
    >>> w_example = read_weights('example_weights.txt')
    >>> w_example
    [[[2.1, -3.1], [-0.7, 4.1]], [[3.8, 1.5], [-1.2, 1.1]]]
    >>> w = read_weights('weights.txt')
    >>> len(w)
    3
    >>> len(w[2])
    10
    >>> len(w[2][0])
    16
    """

    # weights_file = open(file_name,"r")
    # w = []
    # for line in weights_file:
    #     if "#" == line[0]:
    #         w.append([])
    #     else:
    #         w[-1].append([float(w_ij) for w_ij in line.strip().split(",")])
    
    # return w

    with open(file_name,"r") as weights_file:
        w = []
        for line in weights_file:
            if "#" == line[0]:
                w.append([])
            else:
                w[-1].append([float(w_ij) for w_ij in line.strip().split(",")])
    return w


def read_biases(file_name):
    """
    Input: A string (file_name), that corresponds to the name of the file
           that contains the biases of the ANN.
    Output: A table of numbers corresponding to the biases of the ANN.
    
    >>> b_example = read_biases('example_biases.txt')
    >>> b_example
    [[-1.1, 4.2], [-1.7, 2.5]]
    >>> b = read_biases('biases.txt')
    >>> len(b)
    3
    >>> len(b[0])
    16
    """

    # biases_file = open(file_name,"r")
    # b = []
    # for line in biases_file:
    #     if not "#" == line[0]:
    #         b.append([float(b_j) for b_j in line.strip().split(",")])
    
    # return b

    with open(file_name,"r") as biases_file:
        b = []
        for line in biases_file:
            if not "#" == line[0]:
                b.append([float(b_j) for b_j in line.strip().split(",")])
    
    return b


def argmax(x):
    """
    Input: A list of numbers (i.e., x) that can represent the scores
           computed by the ANN.
    Output: A number representing the index of an element with the maximum
            value, the function should return the minimum index.
    
    >>> x = [1.3, -1.52, 3.9, 0.1, 3.9]
    >>> argmax(x)
    2
    """

    num_inputs = len(x)
    max_index = 0
    
    for i in range(1,num_inputs):
        if x[max_index] < x[i]:
            max_index = i
            
    return  max_index


def predict_number(image):
    """
    Input: A list of lists of numbers (i.e., image) that corresponds to the image.
    Output: The number predicted in the image by the ANN.

    >>> i = predict_number(image)
    >>> print('The image is number ' + str(i))
    The image is number 4
    """
    
    x = [pixel for row in image for pixel in row]
    w = read_weights('./weights.txt')
    b = read_biases('./biases.txt')
    
    y = inference(x, w, b)
    return argmax(y)
