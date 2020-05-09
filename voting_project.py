
######################################################
# Function 1
def first_past_the_post(votes):
    ''' Count the votes for each candidate and return the winner.
    
    Takes a list of strings, with one instance of candidate's name as
    a vote. NOT case-sensitive. Returns tie if winning votes are equal.'''

    # First, build a tally of the candidates and their votes:
    tally = {}
    for candidate in votes:
        if candidate in tally:
            tally[candidate] += 1
        else:
            tally[candidate] = 1
            
    # Then, filter through the dictionary for the candidate(s) with max votes:
    winner = []    
    max_votes = max(tally.values())
    
    for i in tally.keys():
        if tally[i] == max_votes:
            winner.append(i)
            
    # Finally, check if there is more than one winner:
    if len(winner) > 1:
        return 'tie'
    else:
        return winner[0]
        
        
#############################################################
# Function 2

def second_preference(votes):
    ''' Count second preference voting and return the winner.
    
    Takes a list of lists. One instance of candidate's name (as str) is
    a preference, and a total list is a vote. NOT case-sensitive.
    Returns tie if winning votes are equal.'''
    
    
    # Collect first pref votes:
    tally = {}
    for i in votes:
        if i[0] in tally:
            tally[i[0]] += 1
        else:
            tally[i[0]] = 1
    
    # Calculate the FPTP winner by first preference:
    FPTP_winner = []    
    max_votes = max(tally.values())
    
    for i in tally.keys():
        if tally[i] == max_votes:
            FPTP_winner.append(i)
    
    turnout = len(votes)
    if (len(FPTP_winner) == 1) and ((max_votes / turnout) >= 0.5):
        return FPTP_winner[0]
    
    # If there's no absolute majority, we calculate second preference.
    # Find the losing candidates by first preference:
    
    loser = []
    for i in tally:
        if tally[i] == min(tally.values()):
            loser.append(i)

    # Get string value for the loser, tiebreaking multiple losers by name:
    if len(loser) > 1:
        loser = sorted(loser)[0]
    else:
        loser = loser[0]

    # Remove loser from tally, and allocate loser's second preference votes:
    tally.pop(loser)
    for i in votes:
        if i[0] == loser:
            if i[1] in tally:
                tally[i[1]] += 1
            else:
                tally[i[1]] = 1
    
    # Evaluate the new vote totals
    max_votes = max(tally.values())
    winner = []
    for i in tally.keys():
        if tally[i] == max_votes:
            winner.append(i)
    
    # Return winner
    if len(winner) > 1:
        return 'tie'
    else:
        return winner[0]
#############################################################
# Function 3
def multiple_preference(votes):
    ''' Count multiple preference votes and return the winner.
    
    Takes a list of ordered lists. One instance of candidate's name (as str) is
    a preference, and an ordered list is a vote. NOT case-sensitive.
    Returns tie if winning votes are equal.'''

    # Build dictionary of full-preference votes. Updates with re-allocations;
    # includes empty entries for candidates with no firstpref votes.
    tally = {}
    for vote in votes:
        if vote[0] in tally:
            tally[vote[0]].append(vote)
        else:
            tally[vote[0]] = [vote, ]
        for pref in vote:
            if pref not in tally:
                tally[pref] = []

    winner = []
    eliminated = []
    turnout = len(votes)
    
    
    while not winner:    
        
        # Count votes for each remaining candidate
        vote_count = {}
        for candidate in tally:
            vote_count[candidate] = len(tally[candidate])
        
        max_votes = max(vote_count.values())
        
        # If there's more than 2 candidates left and no majority, reallocate
        if (len(tally) > 2) and max_votes / turnout <= 0.5:
            
            # Find the loser in this round, and add them to those eliminated
            roundloser = []
            for candidate in vote_count:
                if vote_count[candidate] == min(vote_count.values()):
                    roundloser.append(candidate)

            roundloser = sorted(roundloser)[0]
            eliminated.append(roundloser)
            
            # For each of the loser's votes: extract prefs only for those
            # not yet eliminated & add them to the next-preferred's tally entry
            
            for vote in tally[roundloser]:
                extracted_vote = []
                for pref in vote:
                    if pref not in eliminated:
                        extracted_vote.append(pref)

                if len(extracted_vote) > 0: 
                    tally[extracted_vote[0]].append(extracted_vote)

            # Remove roundloser's now-redundant tally entry and go back up
            # to `vote_count` to evaluate our new tally for a potential winner
            
            tally.pop(roundloser)
    
        # We now have winning candidate(s), so can break out of our loop
        else:
            for candidate in vote_count:
                if vote_count[candidate] == max_votes:
                    winner.append(candidate)
             
    if len(winner) == 1:
        return winner[0]
    else:
        return 'tie'