"""Autocomplete system. Suggests word completitions from a preconfigured corpus."""
from pygtrie import CharTrie

class Autocompleter():
    """Autocomple Sytems.

    Maintains a trie with keys from a given corpus of words.
    Gives autocompletion suggestions by retrieving all keys for a give prefix.
    """ 

    def __init__(self, words):
        """Initialize a autocompleter with a given set of words."""
        self.trie = CharTrie((word, True) for word in words)
        
    def suggest(self, prefix):
        """Return all words in the corpus starting with a givne prefix."""
        try:
            return self.trie.keys(prefix=prefix)
        except KeyError:
            return []
