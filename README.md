# wordler
Small Python script to help with solving word puzzles. Not for cheating, but just for fun.

Allows the position of known (green) letters to be specified. Also accepts a list of patterns for the known letters in the wrong positions (yellow).

Finally, it will take the characters that are known to not occur in the word (grey).

All possible permutations are created, including known letters, and removing invalid ones according to letters known to not occur, plus those present but in the wrong place.

Words that match these patterns are returned from a dictionary, showing a valid set of words to choose from for the next guess.
