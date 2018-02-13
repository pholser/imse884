int number_of_machines = ...;
range MACHINE = 1..number_of_machines;
int number_of_jobs = ...;
range JOB = 1..number_of_jobs;
int processing_time[JOB] = ...;


// Is a given job assigned to a given machine?
dvar int+ job_assigned_to_machine[JOB, MACHINE] in (0..1);

// Last completion time of a job at a machine.
// We're solving for max last completion time; sequence of jobs
// does not matter.
dvar int+ last_completion_time[MACHINE];

dvar int+ max_last_completion_time;


minimize max_last_completion_time;


subject to {
    // Every job assigned to exactly one machine.
    forall (j in JOB) (
        sum (m in MACHINE) (job_assigned_to_machine[j, m]) == 1
    );

    // Definition of last completion time on a machine.
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
            for (var m in thisOplModel.MACHINE) {
                writeln("Machine " + m + ":");
                for (var j in thisOplModel.JOB) {
                    if (thisOplModel.job_assigned_to_machine[j][m] > 0.99) {
                        writeln(
                            "Job " + j + ", duration = "
                                + thisOplModel.processing_time[j]);
                    }
                }
                writeln("Last completion time: " + thisOplModel.last_completion_time[m]);
            }
            writeln("Max completion time = " + cplex.getObjValue());
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem");
    }
}
