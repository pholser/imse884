int number_of_machines = ...;
range MACHINE = 1..number_of_machines;
int number_of_jobs = ...;
range JOB = 1..number_of_jobs;
int processing_time[JOB] = ...;

dvar int+ job_assigned_to_machine[JOB, MACHINE] in (0..1);
dvar int+ last_completion_time[MACHINE];
dvar int+ max_last_completion_time;

minimize max_last_completion_time;

subject to {
    // Every job assigned to exactly one machine.
    forall (j in JOB) (
        sum (m in MACHINE) (job_assigned_to_machine[j, m]) == 1
    );

    forall (m in MACHINE) (
        last_completion_time[m] ==
            sum (j in JOB) (
                job_assigned_to_machine[j, m] * processing_time[j]
            )
    );

    // Choice of max last completion time obeys the maximization property.
    forall (m in MACHINE) (
        max_last_completion_time >= last_completion_time[m]
    );
}

main {
    if (!thisOplModel.generate()) {
        if (cplex.solve()) {
            for (var j in thisOplModel.JOB) {
                for (var m in thisOplModel.MACHINE) {
                    if (thisOplModel.job_assigned_to_machine[j][m] > 0.99) {
                        writeln(
                            "Job " + j + " assigned to machine " + m
                                + ", duration = "
                                + thisOplModel.processing_time[j]);
                    }
                }
            }
            writeln("Max completion time = "
                + thisOplModel.max_last_completion_time);
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem");
    }
}
