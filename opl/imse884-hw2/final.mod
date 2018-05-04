/* Parameters */

int number_of_employees = ...;
range EMPLOYEE = 1..number_of_employees;
int number_of_hours_in_workday = ...;
range WORKHOUR = 1..number_of_hours_in_workday;
string WORKHOUR_LABELS[WORKHOUR] = ...;
int regular_hourly_wage = ...;
int overtime_hourly_wage_increase = ...;
int offhours_hourly_wage_bump =...;
int factory_employee_capacity = ...;
int daily_labor_hours_requirement = ...;
int fulltime_daily_hours_min = ...;
int fulltime_daily_hours_max = ...;
int parttime_daily_hours_min = ...;
int parttime_daily_hours_max = ...;

int is_full_time[EMPLOYEE] = ...;
int offhours[WORKHOUR] = ...;


/* Decision variables */

// Does a given employee work the given hour?
dvar int+ working[EMPLOYEE, WORKHOUR] in (0..1);

// How much regular wage is an employee paid for this hour?
dvar int+ regular_wages[EMPLOYEE, WORKHOUR];
dvar int+ employee_regular_wages[EMPLOYEE];

// How much offhours wage bump does an employee get for this hour?
dvar int+ offhours_wages[EMPLOYEE, WORKHOUR];
dvar int+ employee_offhours_wages[EMPLOYEE];

// How much overtime wage increase does an employee get for the day?
dvar int+ employee_works_overtime[EMPLOYEE] in (0..1);
dvar int+ employee_overtime_hours[EMPLOYEE];
dvar int+ employee_overtime_wages[EMPLOYEE];

// Total daily wage for each employee?
dvar int+ employee_total_wages[EMPLOYEE];


/* Objective */

minimize
    sum (e in EMPLOYEE) (
        employee_total_wages[e]
    );


/* Constraints */

subject to {
    // Definitions of wages paid.
    forall (e in EMPLOYEE, h in WORKHOUR) (
        regular_wages[e, h]
        ==
        regular_hourly_wage * working[e, h]
    );
    forall (e in EMPLOYEE) (
        employee_regular_wages[e]
        ==
        sum (h in WORKHOUR) (regular_wages[e, h])
    );

    forall (e in EMPLOYEE, h in WORKHOUR) (
        offhours_wages[e, h]
        ==
        (1 - is_full_time[e])
        *
        offhours[h]
        *
        offhours_hourly_wage_bump
        *
        working[e, h]
    );

    forall (e in EMPLOYEE) (
        employee_offhours_wages[e]
        ==
        sum (h in WORKHOUR) (offhours_wages[e, h])
    );

//    forall (e in EMPLOYEE) (
//        employee_works_overtime == 0
//        =>
//        employee_overtime_hours[e] == 0
//    );

    forall (e in EMPLOYEE) (
        employee_overtime_hours[e]
        ==
        maxl(
            0,
            sum (h in WORKHOUR) (working[e, h]) - fulltime_daily_hours_min
        )
    );

    forall (e in EMPLOYEE) (
        employee_overtime_wages[e]
        ==
        is_full_time[e]
        *
        employee_overtime_hours[e]
        *
        overtime_hourly_wage_increase
    );

    forall (e in EMPLOYEE) (
        employee_total_wages[e]
        ==
        employee_regular_wages[e]
        +
        employee_offhours_wages[e]
        +
        employee_overtime_wages[e]
    );

//    forall (e in EMPLOYEE) (
//        employee_works_overtime[e]
//        ==
//        
//    );

    // Full-time employees work at minimum/at most
    // a certain number of hours each day.
    // The ceiling on hours per day accounts for the overtime limit.
    forall (e in EMPLOYEE) (
        is_full_time[e] == 1
        =>
        (sum (h in WORKHOUR) (working[e, h]) >= fulltime_daily_hours_min
            &&
            sum (h in WORKHOUR) (working[e, h]) <= fulltime_daily_hours_max)
    );

    // Part-time employees work at minimum/at most
    // a certain number of hours each day.
    forall (e in EMPLOYEE) (
        is_full_time[e] == 0
        =>
        (sum (h in WORKHOUR) (working[e, h]) >= parttime_daily_hours_min
            &&
            sum (h in WORKHOUR) (working[e, h]) <= parttime_daily_hours_max)
    );

    // At most a certain number of employees may be working at a time.
    forall (h in WORKHOUR) (
        sum (e in EMPLOYEE) (working[e, h]) <= factory_employee_capacity
    );

    // Each employee's work time must be consecutive.
    forall (e in EMPLOYEE,
        start in 1..(number_of_hours_in_workday - 2),
        end in (start + 2)..number_of_hours_in_workday) (
        
        (working[e, start] == 1 && working[e, end] == 1)
        =>
        sum (h in start..end) (working[e, h]) == end - start + 1
    );

    // Need a certain number of total hours worked each day.
    sum (e in EMPLOYEE, h in WORKHOUR) (working[e, h])
    >=
    daily_labor_hours_requirement;
}


main {
    if (!thisOplModel.generate()) {
        if (cplex.solve()) {
            writeln("Daily Schedule (* = working, - = not working)");
            writeln("=============================================");

            write("Employee    ");
            for (var h in thisOplModel.WORKHOUR) {
                var label = thisOplModel.WORKHOUR_LABELS[h];
                var pad = "     ";
                write(label + pad.substring(0, pad.length - label.length));
            }
            writeln();

            for (var e in thisOplModel.EMPLOYEE) {
                var pad = "       ";
                write("    " + e + pad.substring(0, e >= 10 ? pad.length - 1 : pad.length));

                for (var h in thisOplModel.WORKHOUR) {
                    write(thisOplModel.working[e][h] > 0 ? " *   " : " -   ");
                }
                writeln();
            }
            writeln();

            writeln("Daily Wages Paid:");
            writeln("===========");
            
            for (var e in thisOplModel.EMPLOYEE) {
                write("Employee " + e + ": regular $"
                    + thisOplModel.employee_regular_wages[e]
                    + ", offhours $"
                    + thisOplModel.employee_offhours_wages[e]
                    + ", overtime $"
                    + thisOplModel.employee_overtime_wages[e]
                    + ", total $"
                    + thisOplModel.employee_total_wages[e]
                );
                writeln();
            }

            writeln("Total Daily Wages Paid: $" + cplex.getObjValue());
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem");
    }
}
