int number_of_vehicles = ...;
range VEHICLE = 1..number_of_vehicles;
int number_of_stops = ...;
range STOP =  1..number_of_stops;
range CUSTOMER =  2..number_of_stops;
int DEPOT = ...;
int distance[STOP, STOP] = ...;


// Does a vehicle traverse an arc from stop A to stop B?
dvar int+ traversed[STOP, STOP, VEHICLE] in (0..1);

// Variables used in the Miller-Tucker-Zemlin subtour elimination constraints
dvar float+ u[CUSTOMER];


minimize
    sum (s1 in STOP, s2 in STOP, v in VEHICLE) (
        traversed[s1, s2, v] * distance[s1, s2]
    );


subject to {
    // No self-arcs traversed.
    forall (s in STOP) (
        sum (v in VEHICLE) (traversed[s, s, v]) == 0
    );

    // Each customer visited exactly once.
    forall (c in CUSTOMER) (
        sum (source in STOP, v in VEHICLE) (
            traversed[source, c, v]
        ) == 1
    );

    // If a vehicle visits a stop, it leaves it too.
    // If a vehicle does not visit a stop, it does not leave it.
    forall (v in VEHICLE, s in STOP) (
        sum (source in STOP) (traversed[source, s, v])
        -
        sum (destination in STOP) (
            traversed[s, destination, v]
        ) == 0
    );

    // All vehicles leave the depot.
    forall (v in VEHICLE) (
        sum (c in CUSTOMER) (traversed[DEPOT, c, v]) == 1
    );

    // All vehicles come back to the depot.
    forall (v in VEHICLE) (
        sum (c in CUSTOMER) (traversed[c, DEPOT, v]) == 1
    );

    // Each vehicle visits at least two customers.
    forall (v in VEHICLE) (
        sum (c in CUSTOMER, s in STOP) (traversed[s, c, v]) >= 2
    );

    // Disregard subtours. These are Miller-Tucker-Zemlin
    // subtour elimination constraints.
    forall (c1 in CUSTOMER, c2 in CUSTOMER : c1 != c2) (
        u[c1]
        -
        u[c2]
        + number_of_stops * sum (v in VEHICLE) (
            traversed[c1, c2, v]
        )
        <=
        number_of_stops - 1
    );
}


main {
    if (!thisOplModel.generate()) {
        if (cplex.solve()) {
            for (var v in thisOplModel.VEHICLE) {
                writeln("Vehicle " + v + " traverses:");
                writeln("===========================");
                
                var tour_complete = false;
                var s = thisOplModel.DEPOT;
                while (!tour_complete) {
                    for (var d in thisOplModel.STOP) {
                        if (thisOplModel.traversed[s][d][v] >= 0.99) {
                            writeln("(" + s + ", " + d + "), distance = "
                                + thisOplModel.distance[s][d]);
                            s = d;
                            if (d == thisOplModel.DEPOT) {
                                tour_complete = true;
                                break;
                            }
                        }
                    }
                }

                writeln("");
            }
            writeln("Total distance covered = " + cplex.getObjValue());
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem");
    }
}
