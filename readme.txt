connectZ file includes multiple functions. 

The function named 'outputFinalCodes' functions as a platform to proceed with the game play and it links all game checking functions wherever applicable.

The game checking functions basically map the output codes. The function names are intuitive enough so no elaborate explanations are provided here.

The most challenging bit is how to check a 'win'. The procedure is given as below.
Firstly, create two seperate grid histories for the two players.
Secondly, list all newly-generated winning combinations (in the sense that all of which includes the current grid) when there is a current grid.
Lastly, check if any of the newly-generated winning combinations is a sublist of the grid history. If so, a 'win' is identified.

In addition, it is worth to notice that there are four types of winning combinations, i.e. vertical (below the current grid only), horizontal, main diagonal and anti diagonal. After careful calculations, only those valid winning combinations are checked. That is to say, these winning combinations shouldn't be outside of the board.

Another noteworthy part is that I created two lists of pair tuples for grid history. In this way, space and time could be saved in case of a very sparse game play, namely a very large board with only a few plays. It is for the same reason that I created a dictionary of height history rather than a matrix.

The last part to be noticed is cleaning data. The blank lines are not treated as file error here and are needed to be removed. It is especially crucial for illegal continue checking. For example, after a 'win' is identified, the program could possibly miss the illegal continue if there is a blank line and a number after; or the program could errorneously identify a illegal continue if there are some blank lines. Since blank lines needs to be removed both in normal cases and in illegal continue checking case, a helper function named 'nonblank_lines' are created.