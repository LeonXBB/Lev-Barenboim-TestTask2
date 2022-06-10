import unittest
import random

from binary_tree import BinaryTree


class TestTree(unittest.TestCase):

    # empty tree

    def test_empty_tree_creation(self):

        tree = BinaryTree([])

        self.assertEqual(len(tree.internal_array), 0)
        self.assertEqual(tree.exists(1), False)

    def test_one_nod_tree_creation(self):

        random_int = random.randint(0, 100)

        tree = BinaryTree([random_int])

        self.assertEqual(len(tree.internal_array), 1)
        self.assertEqual(tree.exists(random_int), True)

    def test_multiple_nodes_tree_creation(self):

        random_ints = [10, 3, 15, 1, None, 9]

        tree = BinaryTree(random_ints)

        for i in random_ints:
            self.assertEqual(tree.exists(i), True)

    def test_incorrect_array(self):

        # wrong_type

        with self.assertRaises(ValueError):
            tree = BinaryTree(["a", False, 3.15, (None,)])

        # duplicate_values

        with self.assertRaises(ValueError):
            tree = BinaryTree([1, 1, 1])

        # incorrect_indexes

        with self.assertRaises(Exception) as context:
            tree = BinaryTree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertTrue("Invalid tree!" in str(context.exception))

    def test_exist(self):

        # correct call with rv = True

        tree = BinaryTree([5])
        self.assertEqual(tree.exists(5), True)

        # correct call with rv = False

        tree = BinaryTree([5])
        self.assertEqual(tree.exists(6), False)

        # empty tree

        tree = BinaryTree([])
        self.assertEqual(tree.exists(5), False)

        # wrong_type

        with self.assertRaises(TypeError):
            tree = BinaryTree([2, 1, 3])
            tree.exists(False)

        # None

        tree = BinaryTree([1, None, 3])
        self.assertEqual(tree.exists(None), True)

        # root

        tree = BinaryTree([2, 1, 3])
        self.assertEqual(tree.exists(2), True)

        # non-root

        tree = BinaryTree([2, 1, 3])
        self.assertEqual(tree.exists(1), True)

    def test_add(self):

        # correct call

        tree = BinaryTree([2, 1, 3])

        # right-side leaf
        tree.add(4)
        self.assertEqual(tree.exists(4), True)
        self.assertEqual(tree.internal_array, [2, 1, 3, None, None, None, 4])

        # left-side leaf
        tree.add(0)
        self.assertEqual(tree.exists(0), True)
        self.assertEqual(tree.internal_array, [2, 1, 3, 0, None, None, 4])

        # duplicate_values

        with self.assertRaises(ValueError):
            tree = BinaryTree([2, 1, 3])
            tree.add(2)

        # wrong_type

        with self.assertRaises(TypeError):
            tree = BinaryTree([2, 1, 3])
            tree.add(False)

        # None

        tree = BinaryTree([2, 1, 3])
        tree.add(None)
        self.assertEqual(tree.exists(None), False)

        # root

        tree = BinaryTree([2, 1, 3])
        tree.add(0)
        self.assertEqual(tree.exists(0), True)

        # non-root

        tree = BinaryTree([2, 1, 3])
        tree.add(4)
        self.assertEqual(tree.exists(4), True)

    def test_smallest(self):

        # correct call

        tree = BinaryTree([2, 1, 3])
        self.assertEqual(tree.smallest(), 1)

        # empty tree

        tree = BinaryTree([])
        self.assertEqual(tree.smallest(), None)

    def test_biggest(self):

        # correct call

        tree = BinaryTree([2, 1, 3])
        self.assertEqual(tree.biggest(), 3)

        # empty tree

        tree = BinaryTree([])
        self.assertEqual(tree.biggest(), None)

    def test_sort(self):

        # correct call

        tree = BinaryTree([10, 3, 15, 1, None, 9])
        self.assertEqual(tree.sorted_array(), [9, 3, 15, 1, None, 10])

        # empty tree

        tree = BinaryTree([])
        self.assertEqual(tree.sorted_array(), [])


if __name__ == '__main__':
    unittest.main()
