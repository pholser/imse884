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

solve satisfy;

% Each team role satisfied by a player.
constraint
    forall (r in TEAM_ROLE) (
        sum (p in PLAYER) (team[p, r]) == 1
    );

% No player satisfies more than one team role.
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
