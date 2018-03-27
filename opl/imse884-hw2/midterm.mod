/* Parameters */

{string} CHEMICAL = ...;
int number_of_pipelines = ...;
range PIPELINE = 1..number_of_pipelines;
float average_grade[PIPELINE, CHEMICAL] = ...;
float epa_min[CHEMICAL] = ...;
float epa_max[CHEMICAL] = ...;
float max_pipeline_supply = ...;
float production_requirement = ...;
int number_of_contract_tiers = ...;
range CONTRACT_TIER = 1..number_of_contract_tiers;
range CONTRACT_TIER_BOUNDARY = 0..number_of_contract_tiers;
float contract_cost_per_barrel[PIPELINE, CONTRACT_TIER] = ...;
float contract_threshold[PIPELINE, CONTRACT_TIER_BOUNDARY] = ...;


/* Decision variables */

// How many barrels should we purchase from each pipeline per day?
dvar float+ barrels_purchased[PIPELINE];
// What is the total content of each chemical in the resulting blend?
dvar float+ chemical_content[CHEMICAL];
// How much will we have spent sourcing from a given pipeline?
dvar float+ contract_cost[PIPELINE];
// What contract tier is in force for each pipeline?
dvar int+ contract_tier_chosen[PIPELINE, CONTRACT_TIER] in (0..1);

// These represent coefficients of a convex combination of
// endpoints of a contract tier; more on this below.
dvar float+ lambda[PIPELINE, CONTRACT_TIER];
dvar float+ mu[PIPELINE, CONTRACT_TIER];


/* Objective */

minimize
    sum (p in PIPELINE) (contract_cost[p]);


/* Constraints */

subject to {
    // Exactly one contract tier in force per pipeline.
    forall (p in PIPELINE) (
        sum (t in CONTRACT_TIER) (contract_tier_chosen[p, t]) == 1
    );

    // Limit the convex combination choices.
    // If a contract tier is in force for a pipeline, then the
    // number of barrels purchased for that pipeline and the cost
    // incurred is a convex combination of the endpoints of that
    // contract tier, since the piecewise cost function is linear
    // in each tier.
    // If a contract tier is not in force, lambda and mu will be
    // forced to zero.
    forall (p in PIPELINE, t in CONTRACT_TIER) (
        lambda[p, t] + mu[p, t] == contract_tier_chosen[p, t]
    );

    // Enforce the definition of contract cost per pipeline.
    forall (p in PIPELINE) (
        contract_cost[p]
        ==
        sum (t in CONTRACT_TIER) (
            lambda[p, t]
                * contract_threshold[p, t - 1]
                * contract_cost_per_barrel[p, t]
            +
            mu[p, t]
                * contract_threshold[p, t]
                * contract_cost_per_barrel[p, t]
        )
    );

    // Enforce the definition of barrels purchased.
    forall (p in PIPELINE) (
        barrels_purchased[p]
        ==
        sum (t in CONTRACT_TIER) (
            lambda[p, t] * contract_threshold[p, t - 1]
            +
            mu[p, t] * contract_threshold[p, t]
        )
    );

    // Must meet production demand.
    sum (p in PIPELINE) (barrels_purchased[p]) == production_requirement;

    // Cap on amount purchased from a given pipeline.
    forall (p in PIPELINE) (
        barrels_purchased[p] <= max_pipeline_supply
    );

    // Enforce the definition of total chemical content in blend.
    forall (c in CHEMICAL) (
        chemical_content[c]
        ==
        sum (p in PIPELINE) (average_grade[p, c] * barrels_purchased[p])
    );

    // Chemical levels of blend within EPA regulations.
    //
    // Typical linearization of "average" constraints here:
    // instead of saying:
    //     sum[p](avg_grade[p, c] * barrels_purchased[p]
    //         / sum[p](barrels_purchased[p])
    //         >= epa_min[c]
    //     sum[p](avg_grade[p, c] * barrels_purchased[p]
    //         / sum[p](barrels_purchased[p])
    //         <= epa_max[c]
    // we have to do algebra to make the constraints linear.
    forall (c in CHEMICAL) (
        chemical_content[c]
        >=
        epa_min[c] * sum (p in PIPELINE) (barrels_purchased[p])
        &&
        chemical_content[c]
        <=
        epa_max[c] * sum (p in PIPELINE) (barrels_purchased[p])
    );
}


main {
    if (!thisOplModel.generate()) {
        if (cplex.solve()) {
            for (var p in thisOplModel.PIPELINE) {
                writeln("Purchase " + thisOplModel.barrels_purchased[p]
                    + " barrels from pipeline " + p
                    + ", cost = $"
                    + thisOplModel.contract_cost[p]);
            }
            writeln("Total cost = $" + cplex.getObjValue());

            for (var c in thisOplModel.CHEMICAL) {
                writeln("Grade of " + c + ": "
                    + thisOplModel.epa_min[c]
                    + " <= "
                    + (thisOplModel.chemical_content[c]
                        / thisOplModel.production_requirement)
                    + " <= "
                    + thisOplModel.epa_max[c]);
            }
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem");
    }
}
