# wordler
Provides help with solving a popular word puzzle. Not for cheating, but just for fun.

Allows the position of known (green) letters to be specified. Also accepts a list of patterns for the known letters in the wrong positions (yellow), and which characters are not in the word (grey).

All possible permutations are created, with locked letters in place. Known letters are included, excluding positions they're known to not be in, while excluding patterns with any letters that are known to be absent.

Words that match the patterns are returned from a dictionary, letting you drive your next guess from a valid set of potential words.

## config

| Parameter | meaning | example | notes |
|-----------|---------|---------|-------|
|`locked_pattern`| String specifying the known locked letters in the answer (green) | `'r__l_'` | `r` and `l` are locked into positions `1` and `4` and are correct |
|`floating_patterns` | Specify the patterns of known letters in the wrong position (yellow) |`['_a___', '__a__', '____a']` | `a` is in the word, but not in position `2`, `3` or `5` |
|`excluded_letters`| String containing the letters known not to be in the answer (grey) |`'qwuin'`| None of `q`, `w`, `u`, `i` and n appear in the answer

## `floating_patterns` and `locked_pattern` overlaps
If `floating_patterns` contains a letter that's already locked in place in a different position, processing will assume that there are multiple instances of that letter in the solution.

However, if all positions for that letter except the locked one have been used, and if that letter is locked to that remaining position in `locked_pattern`, it will be assumed that locked is the only instance of that letter present.
    