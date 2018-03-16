/* Parameters */

enum CHEMICAL;
int: number_of_pipelines;
set of int: PIPELINE = 1..number_of_pipelines;
array[PIPELINE, CHEMICAL] of float: average_grade;
array[CHEMICAL] of float: epa_max;
array[CHEMICAL] of float: epa_min;
float: max_pipeline_supply;
float: production_requirement;
int: number_of_contract_tiers;
set of int: CONTRACT_TIER = 1..number_of_contract_tiers;
set of int: CONTRACT_TIER_BOUNDARY = 1..number_of_contract_tiers+1;
array[PIPELINE, CONTRACT_TIER] of float: contract_cost_per_barrel;
array[PIPELINE, CONTRACT_TIER_BOUNDARY] of float: contract_threshold;


/* Decision variables */

% How many barrels should we purchase from each pipeline per day?
array[PIPELINE] of var float: barrels_purchased;
% What is the total content of each chemical in the resulting blend?
array[CHEMICAL] of var float: chemical_content;
% How much will we have spent sourcing from a given pipeline?
array[PIPELINE] of var float: contract_cost;
% What contract tier is in force for each pipeline?
array[PIPELINE, CONTRACT_TIER] of var 0..1: contract_tier_chosen;

% These represent coefficients of a convex combination of
% endpoints of a contract tier; more on this below.
array[PIPELINE, CONTRACT_TIER] of var float: lambda;
array[PIPELINE, CONTRACT_TIER] of var float: mu;


/* Objective */

var float: obj =
    sum (p in PIPELINE) (contract_cost[p]);
solve minimize obj;


/* Constraints */

% Exactly one contract tier in force per pipeline.
constraint
    forall (p in PIPELINE) (
        sum (t in CONTRACT_TIER) (contract_tier_chosen[p, t]) == 1
    );

% Limit the convex combination choices.
% If a contract tier is in force for a pipeline, then the
% number of barrels purchased for that pipeline and the cost
% incurred is a convex combination of the endpoints of that
% contract tier, since the piecewise cost function is linear
% in each tier.
% If a contract tier is not in force, lambda and mu will be
% forced to zero.
constraint
    forall (p in PIPELINE, t in CONTRACT_TIER) (
        lambda[p, t] >= 0
        /\
        mu[p, t] >= 0
        /\
        lambda[p, t] + mu[p, t] == contract_tier_chosen[p, t]
    );

% Enforce the definition of contract cost per pipeline.
constraint
    forall (p in PIPELINE) (
        contract_cost[p]
        ==
        sum (t in CONTRACT_TIER) (
            lambda[p, t]
            *
            contract_threshold[p, t]
            *
            contract_cost_per_barrel[p, t]
            +
            mu[p, t]
            *
            contract_threshold[p, t + 1]
            *
            contract_cost_per_barrel[p, t]
        )
    );

% Enforce the definition of barrels purchased.
constraint
    forall (p in PIPELINE) (
        barrels_purchased[p]
        ==
        sum (t in CONTRACT_TIER) (
            lambda[p, t] * contract_threshold[p, t]
            +
            mu[p, t] * contract_threshold[p, t + 1]
        )
    );

% Must meet production demand.
constraint
    sum (p in PIPELINE) (barrels_purchased[p]) == production_requirement;

% Cap on amount purchased from a given pipeline.
constraint
    forall (p in PIPELINE) (
        barrels_purchased[p] <= max_pipeline_supply
    );

% Enforce the definition of total chemical content in blend.
constraint
    forall (c in CHEMICAL) (
        chemical_content[c]
        ==
        sum (p in PIPELINE) (average_grade[p, c] * barrels_purchased[p])
    );

% Chemical levels of blend within EPA regulations.
%
% Typical linearization of "average" constraints here:
% instead of saying:
%    sum[p](avg_grade[p, c] * barrels_purchased[p]
%        / sum[p](barrels_purchased[p])
%        >= epa_min[c]
%    sum[p](avg_grade[p, c] * barrels_purchased[p]
%        / sum[p](barrels_purchased[p])
%        <= epa_max[c]
% we have to do algebra to make the constraints linear.
constraint
    forall (c in CHEMICAL) (
        chemical_content[c]
        >=
        epa_min[c] * sum (p in PIPELINE) (barrels_purchased[p])
        /\
        chemical_content[c]
        <=
        epa_max[c] * sum (p in PIPELINE) (barrels_purchased[p])
    );
