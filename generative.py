"""


It contains methods for generating new images from existing images.

@file generative.py
@author Ryuta Minami
"""
from __future__ import annotations
from ai import predict_number, read_image # functions
"""
accepts as an argument a 2D list of integers representing an image 
returns an integer for the number it predicts the image represents.
Ex.) Ai recognized as 4, 4

"""

def flatten_image(image: list[list[int]]) -> list[int]:
    """
    Flattens a 2D list into a 1D list.
    
    :param image: 2D list of integers representing an image.
    :return: 1D list of integers representing a flattened image.
    """
    return [pixel for row in image for pixel in row]
    
            
def unflatten_image(flat_image: list[int]) -> list[list[int]]:
    """
    Unflattens a 1D list into a 2D list.
        
    :param flat_image: 1D list of integers representing a flattened image.
    :return: 2D list of integers.
    """
    length_of_side = int(len(flat_image) ** 0.5) 
    outer_list = []
    for i in range(length_of_side): # length_of_side-> num of element in each row
        outer_list.append(flat_image[0 + i * length_of_side : length_of_side + i * length_of_side])
        #slice every "length_of_side" element and put each into outer list
    return outer_list

def check_adjacent_for_one(flat_image: list[int], flat_pixel: int) -> bool:
    """
    Checks if a pixel has an adjacent pixel with the value of 1.
    
    :param flat_image: 1D list of integers representing a flattened image.
    :param flat_pixel: Integer representing the index of the pixel in question.
    :return: Boolean.
    """
    length_of_side = len(flat_image) ** 0.5 
    length_of_side= int(length_of_side) 
    unflat_image = unflatten_image(flat_image) #judge with unflatten_image is eaiser
    #convert index of flatten_image(flat_pixel) to unflatten_image ver. (row_num, col_num)
    row_num = flat_pixel // length_of_side 
    col_num = flat_pixel % length_of_side
  
    try:
        if unflat_image[row_num][col_num + 1] == 1: # checking right (0, 1)
            return True
    except: # handle the case index out of range: don't check if checking number is not exist 
        pass
    try:
        if unflat_image[row_num][col_num - 1] == 1: # left (0, -1)
            assert col_num - 1 != -1 #prevent index to be negative : this cause unexpected operation
            return True
    except:
        pass
    try: 
        if unflat_image[row_num - 1][col_num] == 1:#up(-1, 0)
            assert row_num - 1 != -1
            return True  
    except:
        pass
    try:
        if unflat_image[row_num + 1][col_num] == 1: #down(1,0)
            return True
    except:
        pass
    return False #if none of 4 condition is true, false


def pixel_flip(lst: list[int], orig_lst: list[int], budget: int, results: list, i: int = 0) -> None:
    """
    Uses recursion to generate all possibilities of flipped arrays where
    a pixel was a 0 and there was an adjacent pixel with the value of 1.

    :param lst: 1D list of integers representing a flattened image.
    :param orig_lst: 1D list of integers representing the original flattened image.
    :param budget: Integer representing the number of pixels that can be flipped.
    :param results: List of 1D lists of integers representing all possibilities of flipped arrays, initially empty.
    :param i: Integer representing the index of the pixel in question.
    :return: None.
    """
    orig_lst = orig_lst[:]   
    if i >= len(orig_lst): # index length even if buget still not 0, halt 
        return None
    if budget <= 0:
        return None
    if check_adjacent_for_one(orig_lst, i) and lst[i]!= 1: #check_adjacent function not covering the case 1 so added
        lst[i]= 1        
        results.append(lst[:])
        pixel_flip(lst, orig_lst, budget-1, results, i+1)
        lst[i]= 0  #undo
    pixel_flip(lst, orig_lst, budget, results, i+1) # go to next pixcel to check if pixcel doesn't have adjacent for one


def write_image(orig_image: list[list[int]], new_image: list[list[int]], file_name: str) -> None:
    """
    Writes a newly generated image into a file where the modified pixels are marked as 'X'.
    
    :param orig_image: 2D list of integers representing the original image.
    :param new_image: 2D list of integers representing a newly generated image.
    :param file_name: String representing the name of the file.
    :return: None.
    """
    for row in range(len(orig_image)): 
        for col in range(len(new_image[0])): 
            if orig_image[row][col] != new_image[row][col]:# only flipped part is different from original
                new_image[row][col] = "X" 
    with open(file_name, "w") as fileref: 
        for row in range(len(new_image)):
            for col in range(len(new_image[0])):
                fileref.write(str(new_image[row][col]))
            fileref.write("\n") # go to the next row after done writing one row



def generate_new_images(image: list[list[int]], budget: int) -> list[list[int]]:
    """
    Generates all possible new images that can be generated within the budget.
    
    :param image: 2D list of integers representing an image.
    :param budget: Integer representing the number of pixels that can be flipped.
    :return: List of 2D lists of integers representing all possible new images.
    """
    results = [] # will have list of list of flatten images
    flat_image = flatten_image(image)
    pixel_flip(flat_image, flat_image,budget,results, i=0) #results has list of unflatten all possiblities
    new_results = [] # will have all possible 2D lists
    for possibility in results:#add all possible 1D lists(based on prediction)
        unflattened_possibility = unflatten_image(possibility)
        if predict_number(image) == predict_number(unflattened_possibility): 
            new_results.append(unflattened_possibility)
    return new_results


if __name__ == "__main__":
    image = read_image("image.txt")
    new_images = generate_new_images(image, 2)
    print(f"Number of new images generated: {len(new_images)}")
    # Write first image to test generation
    write_image(image, new_images[0], "new_image_1.txt") 

