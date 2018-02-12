set of int: EMPLOYEE;
set of int: JOB;
array[EMPLOYEE, JOB] of int: expected_benefit;
array[JOB] of int: number_of_required_people;


% Is an employee assigned a particular job?
array[EMPLOYEE, JOB] of var 0..1: assigned;


% Every employee must perform at least one job.
% No one employee can perform four or more jobs.
constraint
    forall (e in EMPLOYEE) (
        sum (j in JOB) (assigned[e, j]) >= 1
        /\
        sum (j in JOB) (assigned[e, j]) <= 4
    );

% Each job requires a certain number of people to complete.
% Every job must be done.
constraint
    forall (j in JOB) (
        sum (e in EMPLOYEE) (assigned[e, j])
        ==
        number_of_required_people[j]
    );

% Anyone doing job 5 cannot do job 2, 7, or 9.
% Treating the four jobs as a four-digit binary number here;
% if the most significant bit is set, the other bits must not
% be set.
constraint
    forall (e in EMPLOYEE) (
        8 * assigned[e, 5]
            + 4 * assigned[e, 2]
            + 2 * assigned[e, 7]
            + assigned[e, 9]
        <= 8
    );


var int: obj =
    sum (e in EMPLOYEE, j in JOB) (
        assigned[e, j] * expected_benefit[e, j]
    );

solve maximize obj;


output([
    "assigned =\n" ++ show2d(assigned) ++ "\n",
    "obj = \(obj)\n"
]);
