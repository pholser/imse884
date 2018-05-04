/* Parameters */

int: number_of_employees;
set of int: EMPLOYEE = 1..number_of_employees;
int: number_of_hours_in_workday;
set of int: WORKHOUR = 1..number_of_hours_in_workday;
int: regular_hourly_wage;
int: overtime_hourly_wage;
int: offhours_hourly_wage_bump;
int: factory_employee_capacity;
int: daily_labor_hours_requirement;
int: fulltime_daily_hours_min;
int: fulltime_daily_hours_max;
int: parttime_daily_hours_min;
int: parttime_daily_hours_max;

array[EMPLOYEE] of 0..1: is_full_time;
array[WORKHOUR] of 0..1: offhours;


/* Decision variables */

array[EMPLOYEE, WORKHOUR] of var 0..1: working;
array[EMPLOYEE, WORKHOUR] of var int: regular_wages;
array[EMPLOYEE, WORKHOUR] of var int: offhours_wages;
array[EMPLOYEE, WORKHOUR] of var int: overtime_wages;


/* Objective */

var int: obj =
    sum (e in EMPLOYEE, h in WORKHOUR) (
        regular_wages[e, h]
        +
        offhours_wages[e, h]
        +
        overtime_wages[e, h]
    );
solve minimize obj;


/* Constraints */

% Definition of wages paid.
constraint
    forall (e in EMPLOYEE, h in WORKHOUR) (
        regular_wages[e, h] == regular_hourly_wage * working[e, h]
    );
constraint
    forall (e in EMPLOYEE, h in WORKHOUR) (
        offhours_wages[e, h]
        ==
        ((1 - is_full_time[e]) * offhours[h] * offhours_hourly_wage_bump * working[e, h])
    );
constraint
    forall (e in EMPLOYEE, h in WORKHOUR) (
        overtime_wages[e, h]
        ==
        is_full_time[e]
        *
        (overtime_hourly_wage - regular_hourly_wage)
        * max(0, sum (w in WORKHOUR where w <= h) (working[e, h]) - fulltime_daily_hours_min)
        * working[e, h] 
    );

% Full-time employees work at minimum and at most a certain number of hours each day.
constraint
    forall (e in EMPLOYEE) (
        is_full_time[e] == 1
        ->
        (sum (h in WORKHOUR) (working[e, h]) >= fulltime_daily_hours_min
            /\
            sum (h in WORKHOUR) (working[e, h]) <= fulltime_daily_hours_max)
    );

% Part-time employees work at minimum and at most a certain number of hours each day.
constraint
    forall (e in EMPLOYEE) (
        is_full_time[e] == 0
        ->
        (sum (h in WORKHOUR) (working[e, h]) >= parttime_daily_hours_min
            /\
            sum (h in WORKHOUR) (working[e, h]) <= parttime_daily_hours_max)
    );


% At most a certain number of employees may be working at a time.
constraint
    forall (h in WORKHOUR) (
        sum (e in EMPLOYEE) (working[e, h]) <= factory_employee_capacity
    );


% Each employee's work time must be consecutive.
constraint
    forall (e in EMPLOYEE,
        start in 1..(number_of_hours_in_workday - 2),
        end in (start + 2)..number_of_hours_in_workday) (
        
        (working[e, start] == 1 /\ working[e, end] == 1)
        ->
        sum (h in start..end) (working[e, h]) == end - start + 1
    );

% Need a certain number of total hours worked each day.
constraint
    sum (e in EMPLOYEE, h in WORKHOUR) (working[e, h])
    >=
    daily_labor_hours_requirement;

/*
Employee 1: 0 + 25 + 25 + 25 + 25 + 25  + 25 + 25 + 25 + 40 + 40 + 0
Employee 2: 0 + 25 + 25 + 25 + 25 + 25  + 25 + 25 + 25 + 40 + 40 + 0
Employee 3: 0 + 25 + 25 + 25 + 25 + 25  + 25 + 25 + 25 + 40 + 40 + 0
Employee 4: 0 + 25 + 25 + 25 + 25 + 25  + 25 + 25 + 25 + 40 + 40 + 0
Employee 5: 0 + 0 + 25 + 25 + 25 + 25   + 25 + 25 + 25 + 25 + 40 + 0
Employee 6: 0 + 0 + 25 + 25 + 25 + 25   + 25 + 25 + 25 + 25 + 40 + 40
Employee 7: 0 + 0 + 25 + 25 + 25 + 25   + 25 + 25 + 25 + 25 + 40 + 40
Employee 8: 0 + 25 + 25 + 25 + 25 + 25  + 25 + 25 + 25 + 40 + 40 + 0
Employee 9: 0 + 0 + 25 + 25 + 25 + 25   + 25 + 25 + 25 + 25 + 40 + 40
Employee10: 25 + 25 + 25 + 25 + 25 + 25 + 25 + 25 + 40 + 40 + 0 + 0
Employee11: 0 + 0 + 25 + 25 + 25 + 25   + 25 + 0  + 0  + 0  + 0 + 0
Employee12: 0 + 0 + 0 + 0 + 0 + 0       + 25 + 25 + 25 + 0  + 0 + 0
Employee13: 0 + 0 + 25 + 25 + 25 + 0    + 0 + 0 + 0 + 0 + 0 + 0
Employee14: 0 + 0 + 0 + 0 + 0 + 0       + 0 + 25 + 25 + 25 + 30 + 0
Employee15: 0 + 0 + 25 + 25 + 25 + 0    + 0 + 0 + 0 + 0 + 0 + 0
Employee16: 0 + 0 + 0 + 0 + 0 + 25      + 25 + 25 + 0 + 0 + 0 + 0

wages[e]
==

/* Output */

output(
    [if e == 1
     then "Employee:  "
     else
         if e <= 10 then "  " else " " endif
     endif
     ++ show(e) | e in EMPLOYEE]
     ++ ["\n----------------------------------------------------------\n"]
);
output([
    (if h + 6 <= 12
    then (show(h + 6) ++ (if h + 6 == 12 then "n" else "am" endif))
    else (show((h + 6) mod 12) ++ "pm")
    endif)
    ++
    (if h + 6 >= 10 /\ h + 6 <= 11
    then "       "
    else "        "
    endif)
    ++ concat([
        if fix(working[e, h]) == 1
        then "*  "
        else "   "
        endif | e in EMPLOYEE
    ])
    ++ "\n" | h in WORKHOUR]);
output([show2d(regular_wages) ++ "\n"]);
output([show2d(offhours_wages) ++ "\n"]);
output([show2d(overtime_wages) ++ "\n"]);
output(["obj = \(obj)\n"]);
