enum CHEMICAL;
int: number_of_pipelines;
set of int: PIPELINE = 1..number_of_pipelines;
array[PIPELINE, CHEMICAL] of float: average_grade;
array[CHEMICAL] of float: epa_max;
array[CHEMICAL] of float: epa_min;
float: max_pipeline_supply;
float: production_requirement;
enum CONTRACT_TIER = {LOW, MEDIUM, HIGH};
enum CONTRACT_TIER_BOUNDARY = {LOW_MEDIUM, MEDIUM_HIGH};
array[PIPELINE, CONTRACT_TIER] of float: contract_cost_per_barrel;
array[PIPELINE, CONTRACT_TIER_BOUNDARY] of float: contract_threshold;


% How many barrels should we purchase from each pipeline per day?
array[PIPELINE] of var float: barrels_purchased;

array[PIPELINE] of var float: cost
    = [(
        (barrels_purchased[p] < contract_threshold[p, LOW_MEDIUM])
            * contract_cost_per_barrel[p, LOW]
        + (barrels_purchased[p] >= contract_threshold[p, LOW_MEDIUM]
            /\ barrels_purchased[p] < contract_threshold[p, MEDIUM_HIGH])
            * contract_cost_per_barrel[p, MEDIUM]
        + (barrels_purchased[p] > contract_threshold[p, LOW_MEDIUM])
            * contract_cost_per_barrel[p, HIGH]
       )
       * barrels_purchased[p]    
       | p in PIPELINE];

% Must meet production demand.
constraint
    sum (p in PIPELINE) (barrels_purchased[p]) == production_requirement;

% Constraints on purchases from pipelines.
constraint
    forall (p in PIPELINE) (
        barrels_purchased[p] >= 0
        /\
        barrels_purchased[p] <= max_pipeline_supply
    );

% Chemical levels of blend within EPA regulations.
constraint
    forall (c in CHEMICAL) (
        sum (p in PIPELINE) (average_grade[p, c] * barrels_purchased[p])
        >=
        epa_min[c] * sum (p in PIPELINE) (barrels_purchased[p])
        /\
        sum (p in PIPELINE) (average_grade[p, c] * barrels_purchased[p])
        <=
        epa_max[c] * sum (p in PIPELINE) (barrels_purchased[p])
    );

solve satisfy;
