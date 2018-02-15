# Paul Holser, IMSE 884, HW 2

Included in this distribution:

## hw2-1.xlsx

Excel workbook, with solution to problem 1.

## hw2-1.mzn, hw1-2.dzn

MiniZinc model and data file for problem 1. Using COIN-OR as the backing
solver in MiniZinc IDE, I confirmed the Excel solution.

## DraftKingsData.csv

This is the Excel workbook for problem 2 saved to CSV, with the Unicode BOM
(byte order mark) removed. This helped the Ruby program I wrote (see below)
to churn out a OPL data file from the DraftKings data.

## hw2-2-data-gen.rb

Ruby script to read in the DraftKings CSV and produce an OPL data file on the
standard output.

## hw2-2.mod, hw2-2.dat, hw2-2.mod.out

OPL model, data file, and captured output for solution to problem 2.

## hw2-3a.py

Python program to solve problem 3 part a (for minimizing customer completion
time). Sorts the jobs in ascending order of processing time, and iterates over
the sorted list, adding the job to the machine that will minimize that job's
completion time (based on what's ahead of it in the machine queues).
This guarantees an optimal solution.

## hw2-3.dat

OPL data for problems 3a and 3b.

## hw2-3a.mod, hw2-3a.mod.out

OPL model and data file for problem 3 part a. This model confirmed another
solution with the same optimal objective, not including solutions that are
symmetric to the one the Python program found (given the machines are
interchangeable).

## hw2-3b.mod, hw2-3b.mod.out

OPL model and captured output for problem 3 part b (for minimizing go-home
time).

## hw2-4.mod, hw2-4.mod.out

OPL model and data file for problem 4.

## hw2-5a.mod, hw2-5a.dat, hw2-5a.mod.out

OPL model, data file, and captured output for problem 5a (six vehicles,
each vehicle visits exactly two customers).

## hw2-5b.mod, hw2-5b.dat, hw2-5b.mod.out

OPL model, data file, and captured output for problem 5b (three vehicles,
each vehicle visits at least two customers).
