int number_of_vehicles = 3;
range VEHICLE = 1..number_of_vehicles;
int number_of_stops = 13;
range STOP =  1..number_of_stops;
range CUSTOMER =  2..number_of_stops;
int DEPOT = 1;

int distance[STOP, STOP] =
    [[0,2457,712,1433,66,2141,1616,635,2407,1104,644,1167,1057],
    [2457,0,1752,1374,2409,365,851,1853,958,2339,1817,1688,1775],
    [712,1752,0,954,672,1452,906,275,1737,1195,167,838,778],
    [1433,1374,954,0,1368,1010,871,829,1891,967,878,336,445],
    [66,2409,672,1368,0,2090,1572,577,2383,1047,593,1101,991],
    [2141,365,1452,1010,2090,0,593,1522,1111,1974,1498,1324,1412],
    [1616,851,906,871,1572,593,0,1039,1033,1710,987,1078,1124],
    [635,1853,275,829,577,1522,1039,0,1956,920,108,633,550],
    [2407,958,1737,1891,2383,1111,1033,1956,0,2732,1874,2110,2151],
    [1104,2339,1195,967,1047,1974,1710,920,2732,0,1028,654,587],
    [644,1817,167,878,593,1498,987,108,1874,1028,0,713,640],
    [1167,1688,838,336,1101,1324,1078,633,2110,654,713,0,117],
    [1057,1775,778,445,991,1412,1124,550,2151,587,640,117,0]];

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

    // Each vehicle visits exactly two customers.
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
                for (var s in thisOplModel.STOP) {
                    for (var d in thisOplModel.STOP) {
                        if (thisOplModel.traversed[s][d][v] >= 0.99) {
                            writeln("(" + s + ", " + d + "), distance = "
                                + thisOplModel.distance[s][d]);
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
