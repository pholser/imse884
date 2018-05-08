/* Parameters */

int number_of_employees = 16;
range EMPLOYEE = 1..number_of_employees;
int number_of_hours_in_workday = 12;
range WORKHOUR = 1..number_of_hours_in_workday;
string WORKHOUR_LABELS[WORKHOUR] = [
    "7am", "8am", "9am", "10am", "11am", "12n",
    "1pm", "2pm", "3pm", "4pm", "5pm", "6pm"
];
int regular_hourly_wage = 25;
int overtime_hourly_wage_increase = 15;
int offhours_hourly_wage_increase = 5;
int factory_employee_capacity = 13;
int daily_labor_hours_requirement = 120;
int full_time_daily_hours_min = 8;
int full_time_daily_hours_max = 10;
int part_time_daily_hours_min = 3;
int part_time_daily_hours_max = 5;

// Arbitrarily choosing employees 1-10 as full-timers,
// employees 11-16 as part-timers.
int is_full_time[EMPLOYEE] = [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0];
int offhours[WORKHOUR] = [
    1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1];


/* Decision variables */

// Does a given employee work the given hour?
dvar int+ working[EMPLOYEE, WORKHOUR] in (0..1);

// How much regular wage is an employee paid for this hour?
dvar int+ regular_wages[EMPLOYEE, WORKHOUR];
// How much regular wage is an employee paid for the day?
dvar int+ employee_regular_wages[EMPLOYEE];

// How much offhours wage bump is an employee eligible for this hour,
// disregarding whether employee is working overtime?
dvar int+ offhours_wages[EMPLOYEE, WORKHOUR];
// How much offhours wage bump is an employee eligible for this day,
// disregarding whether employee is working overtime?
dvar int+ employee_offhours_wages[EMPLOYEE];

// How many hours of overtime does the employee work for the day?
dvar int+ employee_overtime_hours[EMPLOYEE];
// How much overtime wage increase is an employee eligible for this day
// because of the overtime hours worked?
dvar int+ employee_overtime_wages[EMPLOYEE];

// Total hours worked for each employee?
dvar int+ employee_total_hours[EMPLOYEE];
// Total daily wage for each employee?
dvar int+ employee_total_wages[EMPLOYEE];


/* Objective */

minimize
    sum (e in EMPLOYEE) (
        employee_total_wages[e]
    );


/* Constraints */

subject to {
    // Definition of regular wages paid.
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

    // Definition of eligible offhour wage bumps.
    forall (e in EMPLOYEE, h in WORKHOUR) (
        offhours_wages[e, h]
        ==
        offhours[h]
        *
        offhours_hourly_wage_increase
        *
        working[e, h]
    );

    forall (e in EMPLOYEE) (
        employee_offhours_wages[e]
        ==
        sum (h in WORKHOUR) (offhours_wages[e, h])
    );

    // Definition of overtime hours.
    forall (e in EMPLOYEE) (
        employee_overtime_hours[e]
        ==
        maxl(
            0,
            employee_total_hours[e] - full_time_daily_hours_min
        )
    );

    // Definition of eligible overtime wage increases.
    forall (e in EMPLOYEE) (
        employee_overtime_wages[e]
        ==
        employee_overtime_hours[e]
        *
        overtime_hourly_wage_increase
    );

    // Definition of employee's hours worked in a day.
    forall (e in EMPLOYEE) (
        employee_total_hours[e]
        ==
        sum (h in WORKHOUR) (working[e, h])
    );

    /*
        Definition of employee's total daily wages.

        An employee that works overtime should not get the offhours
        wage bump for those offhours worked.

        One hour of overtime worked would result in a $15 increase,
        which would beat out even a $10 increase for a 2-hour
        offhours period covered; and if an employee managed to work
        some of both 2-hour offhours periods, they would be working
        overtime anyway because of the 9am-5pm "core hours" period.

        Therefore, to implement the requirement regarding overtime
        taking precedence over offhours incentive, we take the maximum
        of the eligible offhours and overtime wage increases
        to count toward the employee's daily pay.

        If the overtime or offhours pay incentives change,
        or the lengths or layout of the offhour periods change,
        we will need to rethink this part of the formulation.
    */
    forall (e in EMPLOYEE) (
        employee_total_wages[e]
        ==
        employee_regular_wages[e]
        +
        maxl(
            employee_offhours_wages[e],
            employee_overtime_wages[e]
        )
    );

    // Employees work at minimum/at most a certain number of hours each day.
    // The ceiling on hours per day for full-timers accounts for
    // the overtime limit of no more than 2 hours per day.
    forall (e in EMPLOYEE) (
        employee_total_hours[e]
        >=
        is_full_time[e] * full_time_daily_hours_min
        +
        (1 - is_full_time[e]) * part_time_daily_hours_min
        &&
        employee_total_hours[e]
        <=
        is_full_time[e] * full_time_daily_hours_max
        +
        (1 - is_full_time[e]) * part_time_daily_hours_max
    );

    // At most a certain number of employees may be working at a time.
    forall (h in WORKHOUR) (
        sum (e in EMPLOYEE) (working[e, h]) <= factory_employee_capacity
    );

    // Each employee's work time must be consecutive.
    // That is, if an employee is scheduled to work hour A and hour B > A,
    // they must be scheduled to work all hours in between A and B.
    forall (e in EMPLOYEE,
        start in 1..(number_of_hours_in_workday - 2),
        end in (start + 2)..number_of_hours_in_workday) (
        
        (working[e, start] == 1 && working[e, end] == 1)
        =>
        sum (h in start..end) (working[e, h]) == end - start + 1
    );

    // Need a certain number of total hours worked each day.
    sum (e in EMPLOYEE) (employee_total_hours[e])
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
                write("    " + e
                    + pad.substring(
                        0,
                        e >= 10 ? pad.length - 1 : pad.length));

                for (var h in thisOplModel.WORKHOUR) {
                    write(thisOplModel.working[e][h] >= 0.99
                        ? " *   "
                        : " -   ");
                }
                writeln();
            }
            writeln();

            writeln("Daily Wages Paid:");
            writeln("===========");
            
            for (var e in thisOplModel.EMPLOYEE) {
                write("Employee " + e + ": regular $"
                    + thisOplModel.employee_regular_wages[e]);
                if (thisOplModel.employee_offhours_wages[e] > 0
                    || thisOplModel.employee_overtime_wages[e] > 0) {

                    if (thisOplModel.employee_offhours_wages[e]
                        > thisOplModel.employee_overtime_wages[e]) {

                        write(", offhours $"
                            + thisOplModel.employee_offhours_wages[e]);
                    } else {
                        write(", overtime $"
                            + thisOplModel.employee_overtime_wages[e]);
                    }
                }

                writeln(" --> total $" + thisOplModel.employee_total_wages[e]);
            }

            writeln("Total Daily Wages Paid: $" + cplex.getObjValue());
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem");
    }
}
