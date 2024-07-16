# This repo has sample codes that can be used in different projects.

## ORTools to solve TSP

- Works with asymmeytric costs
- Does not work with negative edge weights

Test Matrix
data['distance_matrix'] = [
        [0,1,10000,2],
        [3,0,1,10000],
        [10000,-2,0,1],
        [1,100000,2,0]]


Test Matrix
data['distance_matrix'] = [
        [0,1,10000,2],
        [3,0,1,10000],
        [10000,3,0,1],
        [1,100000,2,0]]

## LKH3 to solve TSP

- Download LKH3 from here: http://webhotel4.ruc.dk/~keld/research/LKH-3/
- Install on a Unix/Linux machine execute the following commands:
`tar xvfz LKH-3.0.10.tgz`
`cd LKH-3.0.10`
`make`
-
