# wordler
Small Python script to help with solving word puzzles. Not for cheating, but just for fun.

Allows the position of known (green) letters to be specified. Also accepts a list of patterns for the known letters in the wrong positions (yellow).

Finally, it will take the characters that are known to not occur in the word (grey).

All possible permutations are created, including known letters, and removing invalid ones according to letters known to not occur, plus those present but in the wrong place.

Words that match these patterns are returned from a dictionary, showing a valid set of words to choose from for the next guess.

## config

| Parameter | meaning | example | notes |
|-----------|---------|---------|-------|
|`locked letters`| String specifying the known locked letters in the answer (green) | `'r__l_'` | `r` and `l` are locked into positions `1` and `4` and are correct |
|`floating_patterns` | Specify the patterns of known letters in the wrong position (yellow) |`['_a___', '__a__', '____a']` | `a` is in the word, but not in position `2`, `3` or `5` |
|`excluded_letters`| String containing the letters known not to be in the answer (grey) |`'qwuin'`| None of `q`, `w`, `u`, `i` and n appear in the answer
    