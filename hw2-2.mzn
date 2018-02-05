set of int: PLAYER;
array[PLAYER] of string: player_names;
array[PLAYER] of int: player_salaries;
array[PLAYER] of float: player_avg_points;

enum POSITION = {PG, SG, PF, SF, C};
enum TEAM_ROLE = {
    POINT_GUARD,
    SHOOTING_GUARD,
    OTHER_GUARD,
    POWER_FORWARD,
    SMALL_FORWARD,
    OTHER_FORWARD,
    CENTER,
    UTILITY
};
array[PLAYER, POSITION] of 0..1: position_eligible;
array[POSITION, TEAM_ROLE] of 0..1: team_role_fulfillable =
    array2d(
        POSITION,
        TEAM_ROLE,
        [|1, 0, 1, 0, 0, 0, 0, 1
         |0, 1, 1, 0, 0, 0, 0, 1
         |0, 0, 0, 1, 0, 1, 0, 1
         |0, 0, 0, 0, 1, 1, 0, 1
         |0, 0, 0, 0, 0, 0, 1, 1
         |]);
int: salary_cap;

array[PLAYER, TEAM_ROLE] of var 0..1: team;

var float: obj =
    sum (p in PLAYER, r in TEAM_ROLE) (
        team[p, r] * player_avg_points[p]
    );
solve maximize obj;
% solve satisfy;

% Each team role filled by a player.
constraint
    forall (r in TEAM_ROLE) (
        sum (p in PLAYER) (team[p, r]) == 1
    );

% No player fills more than one team role.
constraint
    forall (p in PLAYER) (
        sum (r in TEAM_ROLE) (team[p, r]) <= 1
    );

% No player fills a team role for which they are position-ineligible.
constraint
    forall (p in PLAYER, r in TEAM_ROLE) (
        (team[p, r] == 1)
        ->
        (sum (s in POSITION) (
            position_eligible[p, s]
            *
            team_role_fulfillable[s, r]
        ) >= 1)
    );

% Salary cap obeyed.
constraint
    sum (p in PLAYER, r in TEAM_ROLE) (
        team[p, r] * player_salaries[p]
    ) <= salary_cap;

output(
    [
        player_names[p]
            ++ " "
            ++ show([s | s in POSITION where position_eligible[p, s] == 1])
            ++ " plays "
            ++ show(r)
            ++ ", avg points = "
            ++ show(player_avg_points[p])
            ++ ", salary = "
            ++ show(player_salaries[p])
            ++ "\n"
        | p in PLAYER, r in TEAM_ROLE where fix(team[p, r]) == 1
    ]
    ++
    ["salary spent = "
        ++ show(sum (p in PLAYER, r in TEAM_ROLE) (
            fix(team[p, r]) * player_salaries[p]
        ))
        ++ "\n"]
    ++
    ["obj = \(obj)\n"]
);
