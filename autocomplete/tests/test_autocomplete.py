"""Test Autocomplete System."""
from unittest import TestCase
from autocomplete import Autocompleter

class TestAutocompleter(TestCase):
    def setUp(self):
        self.autocompleter = Autocompleter([
            'WhatsApp Messenger',
            'Facebook',
            'Facebook Lite'
        ])

    def test_can_suggest(self):
        """Test can suggest all words starting with a given prefix."""
        suggestions = self.autocompleter.suggest('Fac')
        expected_suggestions = [
            'Facebook',
            'Facebook Lite'
        ]
        self.assertListEqual(list(suggestions), expected_suggestions)

    def test_can_suggest_no_words(self):
        """Test can doesn't suggest any word when none starts with the given prefix"""
        suggestions = self.autocompleter.suggest('PrefixForNothing')
        expected_suggestions = []
        self.assertListEqual(list(suggestions), expected_suggestions)

    def test_can_suggest_for_empty_prefix(self):
        """Test can suggest when the prefix is empty, returning all words."""
        suggestions = self.autocompleter.suggest('')
        expected_suggestions = [
            'WhatsApp Messenger',
            'Facebook',
            'Facebook Lite'
        ]
        self.assertListEqual(list(suggestions), expected_suggestions)
