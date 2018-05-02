/* Parameters */

int: number_of_employees;
set of int: EMPLOYEE = 1..number_of_employees;
int: number_of_hours_in_workday;
set of int: WORKHOUR = 1..number_of_hours_in_workday;
int: regular_hourly_wage;
int: overtime_hourly_wage;
int: offhours_hourly_wage_bump;
int: daily_overtime_hours_cap;
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


/* Objective */

var int: obj =
    sum (e in EMPLOYEE, h in WORKHOUR) (
        regular_hourly_wage * working[e, h]
    );
solve minimize obj;


/* Constraints */

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
    