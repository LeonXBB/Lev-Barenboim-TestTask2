# BT exercice

# This implementation is strictly defined by the conditions in the __init__
# A valid array: [10, 3, 15, 1, None, 9]

from math import ceil

from localization import *


class BinaryTree():
    @staticmethod
    def is_valid_array(bt_array):
        '''First, let's check if the elements in the bt_array are of valid types. Then, let's check the conditions. I have split this function into two mono-purposed ones because, in good design, every function should have exactly one goal.'''

        def check_type(node, invalid_elements=[]):

            # Cashing for performance
            if node in invalid_elements:
                return False

            else:
                if node is not None and type(node) is not int:
                    invalid_elements.append(node)
                    return False

            return True

        def check_conditions():

            # Basically, we have two similar conditions here, with the differences of the indexes (offset of one) and, the operations (greater than and less than). So, instead of repeating the same code twise, I came up with this for loop:

            for condition_set in ((2*i + 1, "__ge__"), (2*i + 2, "__le__")):  # index, operation

                try:
                    bt_array[condition_set[0]]
                    is_index_error = False
                except IndexError:
                    is_index_error = True
                except:
                    raise Exception(GENERAL_EXCEPTION)  # Just in case

                is_none = False if is_index_error else bt_array[condition_set[0]] is None

                # We cannot compare with None, so let's write an extra line to be able to check for the return type
                operation_result = False if is_index_error or is_none else getattr(
                    node, condition_set[1])(bt_array[condition_set[0]])

                is_condition = False if is_index_error or is_none or type(
                    operation_result) is not bool else operation_result

                if is_index_error or is_none or is_condition:
                    continue
                else:
                    return False

            return True

        def check_duplicates():

            if len(set(bt_array)) != len(bt_array):
                return False

            return True

        for i, node in enumerate(bt_array):

            # First, let's quickly check whether our data is correct...
            if not check_type(node):
                return False

            # Now, let's check the conditions
            if not check_conditions():
                return False

            # Finally, let's check for duplicates
            if not check_duplicates():
                return False

        return True

    def __init__(self, bt_array):
        """
        Initialise a bt with an array that satisfies the following conditions
        1. bt[2*i + 1] === (None or IndexError) or bt[i] >= bt[2*i + 1]
        2. bt[2*i + 2] === (None or IndexError) or bt[i] <= bt[2*i + 2]
        """
        if not self.is_valid_array(bt_array):
            raise ValueError(INVALID_TREE)

        # This should be the only internal structure used
        self.internal_array = bt_array

    def exists(self, value):

        # Alright, so a few words here (for the reviewer, I suppose). I understand that finding whether an element exists in a binary tree is an operation for a BST, not a BT. Thus, I would need to sort this tree to correctly design this function. However, when I contacted the HR person with some questions about this task, they told me that contacting technical team would be unlikely. Given that, and the fact that the description of the task does not include mandatory sorting (in this function), I have decided to play it safe and implement the function for the unsorted tree. This applies also for the other functions below (excluding 'sorted_array', obviously).

        # Should I have been designing the function to be used with sorting, instead of traversing / cashing the whole tree O(n), I would have made it based on direction (whether value is < or > that current node's value)

        def check_node(node_index, checked_nodes=[]):

            if node_index in checked_nodes:  # Using cashing again to improve performance
                return False

            # If this is what we are looking for, return true
            if self.internal_array[node_index] == value:
                return True

            # Getting the coordinates for left and right child notes
            left_child = None if len(
                self.internal_array) <= 2*node_index + 1 else 2*node_index + 1
            right_child = None if len(
                self.internal_array) <= 2*node_index + 2 else 2*node_index + 2

            for child in (left_child, right_child):
                if child is not None:
                    # and value < (or >) self.internal_array[node_index]: # As our array is not sorted, we cannot simplify like this, thus increasing execution time
                    if check_node(child):
                        return True

            checked_nodes.append(node_index)  # Cashing for performance

            return False

        # if we do not have a root, we do not have anything to check
        if not len(self.internal_array):
            return False

        if value is None:
            return None in self.internal_array

        if type(value) is not int:
            raise TypeError(INVALID_TYPE)

        rv = check_node(0)  # start from the root and go recursively
        return rv

    def add(self, value):

        # This function exists to auto fill the internal array with null values so we have enough indexes to insert a new node
        def increase_internal_array(up_to):
            while len(self.internal_array) <= up_to:
                self.internal_array.append(None)

        def add_node(insert_index):  # This function adds a new node to a tree
            increase_internal_array(insert_index)
            self.internal_array[insert_index] = value
            return

        def traverse_node(node_index):

            # Getting the value of the node
            node_value = self.internal_array[node_index]

            # Getting child nodes
            left_child = None if len(self.internal_array) <= 2*node_index + \
                1 or self.internal_array[2*node_index + 1] is None else 2*node_index + 1
            right_child = None if len(self.internal_array) <= 2*node_index + \
                2 or self.internal_array[2*node_index + 2] is None else 2*node_index + 2

            # At this point, we basically need to either traverse a node one level lower or add a new one. We can do something like that (the same for loop like in the array check, instead of repeating code twice):

            comparison_sets = (("__le__", left_child, 2*node_index + 1), ("__gt__",
                               right_child, 2*node_index + 2))  # method, child, insert_index

            for set_ in comparison_sets:
                # If the value is smaller than the node, we traverse the left child. And the opposite
                if getattr(value, set_[0])(node_value):
                    if set_[1] is not None:
                        traverse_node(set_[1])
                    else:
                        add_node(set_[2])
                        return

        if len(self.internal_array) == 0:  # If we do not have a root, we need to add it
            self.internal_array.append(value)
            return

        if self.exists(value):  # Bts cannot have duplicates
            raise ValueError("Duplicate value")

        if value is None:
            return

        if type(value) is not int:
            raise TypeError(INVALID_TYPE)

        traverse_node(0)  # start from the root and go recursively

    def smallest(self):

        # Please, look at the "exists" function for the explanation why I don't sort

        def traverse_node(node_index, min_value=None):

            left_child = None if len(
                self.internal_array) <= 2*node_index + 1 else 2*node_index + 1
            right_child = None if len(
                self.internal_array) <= 2*node_index + 2 else 2*node_index + 2

            if self.internal_array[node_index] is not None and (min_value is None or self.internal_array[node_index] < min_value):
                min_value = self.internal_array[node_index]

            # Basically, we could go one direction only... Left for the smallest and right for the biggest
            for child in (left_child, right_child):
                if child is not None:
                    min_value = traverse_node(child, min_value)

            return min_value

        if len(self.internal_array) == 0:  # If we do not have a root, we do not have anything to check
            return None

        return traverse_node(0)

    def biggest(self):

        # Please, look at the "exists" function for the explanation why I don't sort

        def traverse_node(node_index, max_value=None):

            left_child = None if len(
                self.internal_array) <= 2*node_index + 1 else 2*node_index + 1
            right_child = None if len(
                self.internal_array) <= 2*node_index + 2 else 2*node_index + 2

            if self.internal_array[node_index] is not None and (max_value is None or self.internal_array[node_index] > max_value):
                max_value = self.internal_array[node_index]

            # Basically, we could go one direction only... Left for the smallest and right for the biggest. (Yes, I copied this function from above)
            for child in (left_child, right_child):
                if child is not None:
                    max_value = traverse_node(child, max_value)

            return max_value

        if len(self.internal_array) == 0:  # If we do not have a root, we do not have anything to check
            return None

        return traverse_node(0)

    def sorted_array(self):
        # TODO: should return a sorted array

        # My favourite way to sort a binary tree is to use double in-order traversal (see below)

        def traverse_node(node_index, results=[]):

            left_child = None if len(
                self.internal_array) <= 2*node_index + 1 else 2*node_index + 1
            right_child = None if len(
                self.internal_array) <= 2*node_index + 2 else 2*node_index + 2

            if left_child is not None:
                traverse_node(left_child)

            results.append(self.internal_array[node_index])

            if right_child is not None:
                traverse_node(right_child)

            return results

        def build_node(node_index, array, rv=[]):

            middle_index = ceil(len(array) // 2)
            middle_element = array[middle_index]

            while len(rv) <= node_index:
                rv.append(None)

            rv[node_index] = middle_element

            if len(array) >= 2:
                left_array = array[:middle_index]
                right_array = array[middle_index + 1:]

                left_index = 2*node_index + 1
                right_index = 2*node_index + 2

                for array, index in ((left_array, left_index), (right_array, right_index)):
                    if len(array):
                        rv = build_node(index, array)

            return rv

        if len(self.internal_array) == 0:
            return []

        # First, we get in-order model of the tree
        unsorted_array = traverse_node(0)

        # Now, we sort it
        unsorted_array = [x for x in unsorted_array if x is not None]
        sorted_array = sorted(unsorted_array)

        # Finally, we can rebuld the tree using the sorted array
        # (I'm sorry, language of the task is not exactly clear to me, I'm not sure if the last part is necessary or not)
        self.internal_array = build_node(0, sorted_array)
        return self.internal_array


# How would you optimise this tree ?
# TODO: answer in text, code is not required

# Well, first of all, I would sort the tree before each call. That would improve performance as well as memory usage.
# Also, I would use modern OOP approach instead of the procedural one.
# Finally, I'd make the unit tests deeper: more edge cases, non-leaf positions for add functions, test for whether the tree is searchable or not etc.


if __name__ == "__main__":
    test = BinaryTree([10, 3, 15, 1, None, 9])
