int: number_of_vertices;
set of int: VERTEX = 1..number_of_vertices;
array[VERTEX, VERTEX] of 0..1: edge;
int: number_of_colors = number_of_vertices;
set of int: COLOR = 1..number_of_colors;


array[VERTEX, COLOR] of var float: x;
array[COLOR] of var float: u;
constraint forall (v in VERTEX, k in COLOR) (x[v, k] >= 0 /\ x[v, k] <= 1);
constraint forall (k in COLOR) (u[k] >= 0 /\ u[k] <= 1);


var float: obj = sum (k in COLOR) ( u[k] );
solve minimize obj;


% Every vertex gets exactly one color.
constraint
    forall (v in VERTEX) (
        sum (k in COLOR) ( x[v, k] ) == 1
    );

% Adjacent nodes get different colors.
constraint
    forall (
        v1 in VERTEX,
        v2 in VERTEX,
        k in COLOR
        where edge[v1, v2] == 1) (

        x[v1, k] + x[v2, k] <= u[k]
    );

% A node can get a particular color only if that color is in fact used.
constraint
    forall (v in VERTEX, k in COLOR) (
        x[v, k] <= u[k]
    );

% Sample clique constraint
% constraint
%     forall (k in COLOR) (
%         x[1, k] + x[3, k] + x[4, k] <= u[k]
%    );
    
% constraint
%     forall (k in COLOR) (
%         x[2, k] + x[4, k] <= u[k]
%     );

% Symmetry-breaking: color used only if some nodes get it.
% constraint
%     forall (k in COLOR) (
%         u[k] <= sum (v in VERTEX) ( x[v, k] )
%     );

% Symmetry-breaking: use lesser-numbered colors first.
% constraint
%     forall (k in 1..(number_of_colors - 1)) (
%         u[k] >= u[k + 1]
%     );


output(
    [if fix(x[v, k]) == 1
     then "Vertex \(v) gets color \(k)\n"
     else ""
     endif | v in VERTEX, k in COLOR]
    ++
    ["# of colors used = \(obj)\n"]
    ++
    [show2d(x), "\n", show(u)]
);
