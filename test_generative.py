from __future__ import annotations
import unittest
from generative import flatten_image, unflatten_image, check_adjacent_for_one, pixel_flip, write_image, generate_new_images
from ai import read_image


class TestGenerative(unittest.TestCase):
    """Unit tests for the module generative.py"""

    def test_flatten_image(self) -> None:
        """
        Verify output of flatten_image for at least three different sizes of images.
        """
        #case 1: size 1×1
        unflat_image1 = [
            [1]
        ]
        flat_image1 = [1]
        assert flat_image1 == flatten_image(unflat_image1),"Failed converting 1-1 sized 2D list to 1D list" 

        #case 2: size 3×3
        unflat_image2 = [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
        ]
        flat_image2 = [1, 0, 0, 1, 0, 0, 1, 1, 1]
        assert flat_image2 == flatten_image(unflat_image2),"Failed converting 3-3 sized 2D list to 1D list"    

        #case 3: size 5×5 
        unflat_image3 = [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1]
        ]
        flat_image3 = [1, 0, 0, 0, 1,0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1]
        assert flat_image3 == flatten_image(unflat_image3),"Failed converting 5-5 sized 2D list to 1D list"
        

    def test_unflatten_image(self) -> None:
        """
        Verify output of unflatten_image for at least three different sizes of flattened images.
        """
        #case 2: size 1×1
        unflat_image1 = [
            [0]
        ]
        flat_image1 = [0]
        assert unflat_image1 == unflatten_image(flat_image1),"Failed converting 1-1 sized 1D list to 2D list"

        #case 2: size 3×3
        unflat_image2 = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 1, 1]
        ]
        flat_image2 = [1, 1, 1, 1, 1, 0, 1, 1, 1]
        assert unflat_image2 == unflatten_image(flat_image2),"Failed converting 3-3 sized 1D list to 2D list"      
        #case 3: size 5×5 
        unflat_image3 = [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 1, 0, 1, 1]
        ]
        flat_image3 =[1, 0, 0, 0, 1,0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1]
        assert unflat_image3 == unflatten_image(flat_image3),"Failed converting 5-5 sized 1D list to 2D list" 



    def test_check_adjacent_for_one(self) -> None:
        """
        Verify output of check_adjacent_for_one for three different pixel indexes of an image representing different scenarios.
        """
        unflat_image = [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0]
        ]
        unflat_image = flatten_image(unflat_image)

        #case 1(have adjacent)
        assert check_adjacent_for_one(unflat_image, 1) == True ,"Pxicel 1 must have adjacent 1"
        #case 2(in the middle, no adjacent)
        assert check_adjacent_for_one(unflat_image, 12) == False,"Pxicel 12 must not have adjacent 1"
        #case 3(edge, no adjacent)
        assert check_adjacent_for_one(unflat_image, 9) == False,"Pxicel 9 must not have adjacent 1"
        #case 4(corner, have adjacent)
        assert check_adjacent_for_one(unflat_image, 24) == True,"Pxicel 24 must have adjacent 1"


    def test_pixel_flip(self) -> None:
        """
        Verify output of pixel_flip for a 5x5 image with a budget of 2.
        """

        """ Ex.)Mathmatical ecxplanation of The nature of the sum after adding all combination(in this case)
        [                               
        [1, (0), (0), 1, (0)],
        [1, (0),  0, (0), 0 ],
        [1, (0),  0,  0,  0 ],         
        [1, (0),  0,  0,  0 ],
        [1,  1,   1,  1,  1 ]
        ]
        () is the number where is likely to be flipped(from condition of the adjacent for one)
        each sum of each () will be the same value after adding all possibilities
        -each of all () 's sum will be 10 after adding all possible 55 combinations(for the case of list above)
        -0 or 1(when flipped) will be added every time one posssible list
        Therfore, this works af all possibilities are correct
        """
        # case: possible locations are 10
        image = [  #  5x5  
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1]
        ]
        assert len(image) == 5,"Vertical length is not 5"
        for row in image:
            assert len(row) == 5, "Horozontal length is not 5"
        
        results = []
        pixel_flip(flatten_image(image), flatten_image(image),2, results)
        sum_lst = [] # list of all sum of each index where is likely to be flipped

        for i in [1,2,4,6,8,11,16,17,18,19]:# index of possible flip place(in flatten images) in other words, index of () according to the explanation above
            total = 0
            for each_possible_lst in results:
                total+= each_possible_lst[i]
            sum_lst.append(total)
        for each in sum_lst:
            assert sum_lst[0] == each, "All possiblities are not in the list"
        
        #make sure diffrence is 2 or less since budget = 2, but not 0, which is unflipped.
        for each_possible_lst in results:
            difference = 0
            for i in range(len(flatten_image(image))):
                if flatten_image(image)[i] != each_possible_lst[i]:
                    #checks flipped pixcel had adjacent value of 1.
                    assert check_adjacent_for_one(each_possible_lst, i) == True
                    difference +=1
                
            assert not difference >= 3, "The number of flip over budget"
            assert not difference <=0,"There is a list none of Pxicel is flipped"


    def test_generate_new_images(self) -> None:
        """
        Verify generate_new_images with image.txt and for each image of the generated images verify that:
        - image is of size 28x28,
        - all values in the generated image are either 1s or 0s,
        - the number of pixels flipped from original image are within budget,
        - all pixels flipped from the original image had an adjacent value of 1.
        """
        
        image = read_image("image.txt")
        new_images = generate_new_images(image, 2)
        for each_image in new_images: #check every possible image
            #Varify size 28x28
            assert len(each_image) == 28,"Vertical length is not 28"
            for i in range(28):
                assert len(each_image[i]) == 28, "Horozontal length is not 28"
        
            #all values are 1s or 0s for all num in the image
            for row in each_image:
                for num in row:
                    assert num == 0 or 1, "The image contains the number other than 0 and 1"

            #make sure diffrence is 2 or less since budget = 2, but not 0, which is unflipped.
            difference = 0
            for i in range(len(flatten_image(image))):
                if flatten_image(image)[i] != flatten_image(each_image)[i]:#where flipped pixcels are
                    difference +=1
                    #checks flipped pixcel had adjacent value of 1.
                    assert check_adjacent_for_one(flatten_image(each_image), i) == True
                
            assert not difference >= 3, "The number of flip over budget"
            assert not difference <=0,"There is a list none of Pxicel is flipped"


if __name__ == "__main__":
    unittest.main()
