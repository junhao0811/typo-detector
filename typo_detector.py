from collections import deque


# %% Node data structure
class Node:
    """
    This class represents a single node in the trie data structure, containing an array of links to child nodes, a data payload, and metadata about the node's level and size.
    """

    def __init__(self, data=None, level=None, size=27):
        """
        Function description: Initializes a new trie node with a link array for all possible characters and optional metadata.

        Input:
            data: any data type to store as payload (typically used at terminal nodes)
            level: integer representing the depth level of this node in the trie
            size: integer representing the size of the link array (default 27 for terminal + 26 letters)

        Time complexity: O(1)

        Space complexity: O(1) - creates a fixed-size array regardless of input
        """
        # terminal $ at index 0
        self.link = [None] * size
        # data payload
        self.data = data
        # level of node
        self.level = level
        # size of node
        self.size = size


# %% The Trie data structure
class TypoDetector:
    """
    This class implements a trie data structure to efficiently store and search for words with a Levenshtein distance of 1 from a given suspicious word.
    """

    def __init__(self, list_words):
        """
        Function description: This function initializes the TypoDetector typo detection system by creating multiple trie data structures organized by word length and inserting all dictionary words into their respective tries.

        Approach description:
        1. Store the input word list and find the maximum word length to determine the size of the tries array.
        2. Create an array of tries where each index corresponds to a specific word length.
        3. For each word in list_words, determine its length and check if a trie exists for that length.
        4. If no trie exists for that word length, create a new trie root node at the corresponding index.
        5. Insert each word into its appropriate trie using the word as the key and its index in list_words as the payload.
        6. Each trie uses a 27-element link array where index 0 represents the terminal character '$' and indices 1-26 represent letters 'a'-'z'.

        Input:
            list_words: a list of N words (all lowercase letters)

        Time complexity: O(C), where C is the total number of characters across all words in list_words

        Time complexity analysis: Inserting all words costs O(C) since each character is processed exactly once.

        Space complexity: O(C), where C is the total number of characters across all words in list_words

        Space complexity analysis: Each character in each word requires one node in the trie structure, plus terminal nodes.
        """
        self.list_words = list_words

        # find longest word length
        max_size = max((len(word) for word in list_words), default=0)

        # create an array of tries, categorized by different word length
        self.trie_collection = [None] * (max_size + 1)

        # for each word, check if trie exists before insert
        for i in range(len(list_words)):
            word = list_words[i]
            length = len(word)
            # if trie doesn't exist, create it
            if self.trie_collection[length] is None:
                self.trie_collection[length] = Node(level=0)
            # insert the word as the key and the index of the word from list_words as its payload
            self.insert(trie=self.trie_collection[length], key=word, data=i)

    def insert(self, trie, key, data=None):
        """
        Function description: This function inserts a word into the specified trie data structure with the given data as payload, creating new nodes as necessary along the path.

        Input:
            trie: a Node object representing the root of the trie
            key: a string representing the word to insert (all lowercase letters)
            data: any data type to store as payload at the terminal node (typically an integer index)

        Time complexity: O(M), where M is the length of the key string

        Time complexity analysis: Given M is the length of the key string,
            Processing each character in the key costs O(1) per character,
            Creating the terminal node costs O(1),
            Total: O(M) + O(1) = O(M)

        Space complexity: O(M), where M is the length of the key string

        Space complexity analysis: In the worst case, all M characters require new nodes to be created.
        """
        count_level = 1
        # begin from root
        current: Node = trie
        # go through the key 1 by 1
        for char in key:
            # calculate index
            # $ = 0, a = 1, b = 2, c = 3 ...
            index = ord(char) - 97 + 1
            # if path exist
            if current.link[index] is not None:
                current = current.link[index]
            # if path doesn't exist
            else:
                # create a new node
                current.link[index] = Node(level=count_level)
                current = current.link[index]
            count_level += 1

        # go through the terminal $, index = 0
        index = 0
        if current.link[index] is not None:
            current = current.link[index]
        # if path doesn't exist
        else:
            # create a new node
            current.link[index] = Node(level=count_level)
            current = current.link[index]
        # add in the payload
        current.data = data

    def check_word(self, sus_word):
        """
        Function description: This function identifies all dictionary words that have exactly one character substitution (Levenshtein distance of 1) from the given suspicious word using BFS traversal on the appropriate trie.

        Approach description:
        1. Get the length of the suspicious word and validate that a trie exists for words of this length.
        2. Model the problem as a graph traversal where each node represents a position in both the suspicious word and a dictionary word path.
        3. Use BFS with a queue storing tuples of (current_trie_node, levenshtein_distance, character_position).
        4. For each character position, explore all possible characters (a-z) in the current trie node's children.
        5. If the explored character matches the expected character from sus_word, continue without increasing distance.
        6. If the explored character differs from the expected character, increment the Levenshtein distance by 1 (substitution).
        7. Only continue paths where the Levenshtein distance remains <= 1 to prune invalid paths early.
        8. When all characters are processed, check if we reached a terminal node with exactly distance 1.
        9. Collect the original dictionary words corresponding to valid terminal nodes and return them.

        Input:
            sus_word: a string representing the suspicious word to check (all lowercase letters)

        Output: a list of strings containing all dictionary words with exactly one character substitution from sus_word

        Time complexity: O(J*N) + O(X), where J is the length of sus_word, N is the number of dictionary words of length J, and X is the total characters in the result

        Time complexity analysis: Given J is the length of sus_word, N is the number of dictionary words of length J, and X is the total characters in the result,
            BFS explores at most 26^1 * N paths since we limit Levenshtein distance to 1,
            Each path has exactly J character positions to process,
            Processing each character position costs O(26) = O(1) to check all possible characters,
            Total BFS cost: O(J * N * 1) = O(J * N),
            Building the result list costs O(X) to copy all result strings,
            Overall: O(J * N) + O(X)

        Space complexity: O(X), where X is the total number of characters in the result

        Space complexity analysis: The space is dominated by O(X) which includes the actual result strings that need to be stored and returned.
        """
        # get sus_word length
        sus_word_length = len(sus_word)

        # if there is no such word length in our trie collection
        if sus_word_length >= len(self.trie_collection):
            return []

        # get the correct trie based on the length of the word
        current: Node = self.trie_collection[sus_word_length]

        # if there is no such word
        if current is None:
            return []

        # to store words from list_words with edit distance 1 to sus_word
        result = []

        # to store candidate nodes
        dq = deque()

        # begin from root
        dq.append((current, 0, 0))

        # go through each character 1 by 1
        while dq:
            current, levenshtein_distance, sus_char_pos = dq.popleft()

            # check whether we've processed all the characters from sus_word
            if sus_word_length == sus_char_pos:
                index = 0
                if current.link[index] is not None and levenshtein_distance == 1:
                    current = current.link[index]
                    result.append(self.list_words[current.data])
                continue

            # calculate index
            # $ = 0, a = 1, b = 2, c = 3 ...
            index = ord(sus_word[sus_char_pos]) - 97 + 1
            # iterate through the node's link, which is an array, and check for possible edits
            for i in range(1, current.size):
                if current.link[i] is not None:
                    if i == index:
                        # no edit, just move to the next character
                        dq.append(
                            (current.link[i], levenshtein_distance, sus_char_pos + 1)
                        )
                    else:
                        # edit distance 1, increment the levenshtein distance
                        new_levenshtein_distance = levenshtein_distance + 1
                        if new_levenshtein_distance <= 1:
                            dq.append(
                                (
                                    current.link[i],
                                    new_levenshtein_distance,
                                    sus_char_pos + 1,
                                )
                            )

        return result
