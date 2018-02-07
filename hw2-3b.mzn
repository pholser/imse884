int: number_of_machines;
set of int: MACHINE = 1..number_of_machines;
int: number_of_jobs;
set of int: JOB = 1..number_of_jobs;
array[JOB] of int: processing_time;

array[JOB, MACHINE] of var 0..1: job_assigned_to_machine;
array[MACHINE] of var int: last_completion_time =
    [sum (j in JOB) (
         job_assigned_to_machine[j, m] * processing_time[j]
     ) | m in MACHINE];
var int: max_last_completion_time;

solve minimize max_last_completion_time;


% Every job assigned to exactly one machine.
constraint
    forall (j in JOB) (
        sum (m in MACHINE) (job_assigned_to_machine[j, m]) == 1
    );

% Choice of max last completion time obeys the maximization property.
constraint
    forall (m in MACHINE) (
        max_last_completion_time >= last_completion_time[m]
    );

output(
    [
        "Job \(j) assigned to machine \(m), duration = \(processing_time[j])\n"
        | j in JOB, m in MACHINE where fix(job_assigned_to_machine[j, m]) == 1
    ]
    ++
    ["Max completion time = \(max_last_completion_time)\n"]
);
