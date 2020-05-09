# Computing Project 1: Function Descriptions
### Q1: First-past-the-post
A function `first_past_the_post(votes)` that returns the outcome of an election for a given list of votes using the First Past the Post voting scheme.

The parameters to this function are:

`votes` is a list of two or more strings, where each string corresponds to a vote for the candidate whose name is in the string.
`first_past_the_post` returns a string containing either the name of the candidate with the most votes using First Past the Post voting, or the string 'tie' if there is a tie.

Assumptions:

There is no candidate with the name “tie”.
There are at least two different candidates receiving votes.

```
>>> v1 = ["chris", "marion", "marion", "nic", "marion", "nic", "nic", "chris", "marion"]
>>> first_past_the_post(v1)
'marion'
>>> v2 = ["chris", "chris", "marion", "nic", "chris", "nic", "nic", "nic", "chris"]
>>> first_past_the_post(v2)
'tie'
```

### Q2: Second-preference
A function `second_preference(votes)` that returns the outcome of an election for a given list of votes using the Second Preference voting scheme.

The parameters to this function are:

`votes` is a list of votes, where each vote is a list that contains two strings, such that the first string is the name of the first preference candidate and the second string is the name of that second preference candidate for that vote.
`second_preference` function returns a string containing either the name of the candidate with the most votes using Second Preference voting scheme, or the string 'tie' if there is a tie.

Assumptions:

There is no candidate with the name “tie”.
All votes contain two preferences, and that the two preferences are different.

Example output:

```
>>> v1 = [["chris", "nic"], ["marion", "nic"], ["marion", "chris"], ["nic", "chris"], ["marion", "nic"], ["nic", "chris"], ["nic", "chris"], ["chris", "nic"], ["marion", "nic"]]
>>> second_preference(v1)
'nic'
>>> v2 = [["chris", "nic"], ["marion", "nic"], ["marion", "chris"], ["nic", "chris"], ["chris", "marion"], ["nic", "chris"]]
>>> second_preference(v2)
'tie'
>>> v3 = [["chris", "mini"], ["marion", "nic"], ["marion", "chris"], ["nic", "chris"], ["marion", "nic"], ["nic", "chris"], ["nic", "chris"], ["chris", "mini"], ["marion", "nic"]]
>>> second_preference(v3)
'marion'
```
### Q3: Multiple-preference
A function `multiple_preference(votes)` that returns the outcome of an election for a given list of votes using the Multiple Preference voting scheme.

`votes` is a list of votes where each vote is a list of strings corresponding to the candidates in decreasing order of preference. Returns a string containing either the name of the candidate with the most votes using Preferences voting, or the string “tie” if there is a tie.
`multiple_preference` function returns a string containing either the name of the candidate with the most votes using Multiple Preference voting scheme, or the string 'tie' if there is a tie.

Assumptions:

There is no candidate with the name “tie”.
Each vote contains all candidates, and that each candidate appears only once in each vote.

Example output:
```
>>> v1 = [["a", "b", "c", "d", "e"], ["b", "e", "d", "c", "a"], ["c", "d", "e", "b", "a"], ["d", "b", "a", "c", "e"], ["e", "a", "c", "b", "d"]]
>>> multiple_preference(v1)
'b'
>>> v2 = [["a", "b", "c", "d", "e"], ["b", "e", "d", "c", "a"], ["c", "d", "e", "b", "a"], ["d", "b", "a", "c", "e"], ["d", "a", "b", "c", "e"], ["e", "a", "c", "b", "d"]]
>>> multiple_preference(v2)
'tie'
```