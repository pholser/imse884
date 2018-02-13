int number_of_players = ...;
range PLAYER = 1..number_of_players;
string player_names[PLAYER] = ...;
int player_salaries[PLAYER] = ...;
float player_avg_points[PLAYER] = ...;

{string} POSITION = {"PG", "SG", "PF", "SF", "C"};
{string} TEAM_ROLE = {
    "POINT_GUARD",
    "SHOOTING_GUARD",
    "OTHER_GUARD",
    "POWER_FORWARD",
    "SMALL_FORWARD",
    "OTHER_FORWARD",
    "CENTER",
    "UTILITY"
};

// Tells whether a player may play a given position.
int position_eligible[PLAYER, POSITION] = ...;

// Tells whether a role on the fantasy team may be filled by
// a player playing a given position.
int team_role_fulfillable[POSITION, TEAM_ROLE] =
    [
        [1, 0, 1, 0, 0, 0, 0, 1],
        [0, 1, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 1]
    ];
int salary_cap = ...;


// What players fill what roles on the fantasy team?
dvar int+ team[PLAYER, TEAM_ROLE] in (0..1);


maximize
    sum (p in PLAYER, r in TEAM_ROLE) (
        team[p, r] * player_avg_points[p]
    );


subject to {
    // Each team role filled by a player.
    forall (r in TEAM_ROLE) (
        sum (p in PLAYER) (team[p, r]) == 1
    );

    // No player fills more than one team role.
    forall (p in PLAYER) (
        sum (r in TEAM_ROLE) (team[p, r]) <= 1
    );

    // No player fills a team role for which they are position-ineligible.
    forall (p in PLAYER, r in TEAM_ROLE) (
        (team[p, r] == 1)
        =>
        (sum (s in POSITION) (
            position_eligible[p, s]
            *
            team_role_fulfillable[s, r]
        ) >= 1)
    );

    // Salary cap obeyed.
    sum (p in PLAYER, r in TEAM_ROLE) (
        team[p, r] * player_salaries[p]
    ) <= salary_cap;
}

main {
    if (!thisOplModel.generate()) {
        if (cplex.solve()) {
            for (var p in thisOplModel.PLAYER) {
                for (var r in thisOplModel.TEAM_ROLE) {
                    if (thisOplModel.team[p][r] > 0.99) {
                        write(
                            thisOplModel.player_names[p]
                            + " [");
                        for (var s in thisOplModel.POSITION) {
                            if (thisOplModel.position_eligible[p][s] == 1) {
                                write(s + " ");
                            }
                        }
                        write("] plays " + r + ", ");
                        write("average points = "
                            + thisOplModel.player_avg_points[p]);
                        writeln(", salary = "
                            + thisOplModel.player_salaries[p]);
                    }
                }
            }
            writeln("Fantasy points expected = " + cplex.getObjValue());
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem");
    }
}
