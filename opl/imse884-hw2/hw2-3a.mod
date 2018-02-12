int number_of_machines = ...;
range MACHINE = 1..number_of_machines;
int number_of_jobs = ...;
range JOB = 1..number_of_jobs;
range POSITION = 1..number_of_jobs;
int processing_time[JOB] = ...;


// Is a given job assigned to a given machine at a given position?
dvar int+ job_assigned_to_machine[JOB, POSITION, MACHINE] in (0..1);
// The completion time of the job at a given position
dvar int+ completion_time[POSITION, MACHINE];


minimize
    sum (p in POSITION, m in MACHINE) (completion_time[p, m]);


subject to {
    // Definition of completion time of a job at a given position.
    forall (p in POSITION, m in MACHINE) (
        completion_time[p, m]
        ==
        sum (j in JOB, p1 in POSITION : p1 <= p) (
            job_assigned_to_machine[j, p1, m]
            *
            processing_time[j]
        )
    );

    // Every job assigned to exactly one position at one machine.
    forall (j in JOB) (
        sum (p in POSITION, m in MACHINE) (
            job_assigned_to_machine[j, p, m]
        ) == 1
    );

    // No position at a machine occupied by more than one job.
    forall (p in POSITION, m in MACHINE) (
        sum (j in JOB) (
            job_assigned_to_machine[j, p, m]
        ) <= 1
    );
}


main {
    if (!thisOplModel.generate()) {
        if (cplex.solve()) {
            for (var m in thisOplModel.MACHINE) {
                writeln("Machine " + m + ":");
                for (var p in thisOplModel.POSITION) {
                    for (var j in thisOplModel.JOB) {
                        if (thisOplModel.job_assigned_to_machine[j][p][m] > 0.99) {
                            writeln(
                                "Job " + j + ", duration = "
                                    + thisOplModel.processing_time[j]
                                    + ", completion time = "
                                    + thisOplModel.completion_time[p][m]);
                        }
                    }
                }
            }

            writeln("Total completion time = " + cplex.getObjValue());
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem");
    }
}
