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
range CONTRACT_TIER_BOUNDARY = 1..(number_of_contract_tiers - 1);
float contract_cost_per_barrel[PIPELINE, CONTRACT_TIER] = ...;
float contract_threshold[PIPELINE, CONTRACT_TIER_BOUNDARY] = ...;


// How many barrels should we purchase from each pipeline per day?
dvar float+ barrels_purchased[PIPELINE];
dvar float+ chemical_content[CHEMICAL];


minimize
    sum (p in PIPELINE) (
        piecewise (b in CONTRACT_TIER_BOUNDARY) {
            contract_cost_per_barrel[p, b] -> contract_threshold[p, b];
            contract_cost_per_barrel[p, number_of_contract_tiers]
        } barrels_purchased[p]
    );


subject to {
    // Must meet production demand.
    sum (p in PIPELINE) (barrels_purchased[p]) == production_requirement;

    // Constraints on purchases from pipelines.
    forall (p in PIPELINE) (
        barrels_purchased[p] <= max_pipeline_supply
    );

    // Chemical levels of blend within EPA regulations.
    forall (c in CHEMICAL) (
        chemical_content[c]
        ==
        sum (p in PIPELINE) (average_grade[p, c] * barrels_purchased[p])
    );

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
                    + " barrels from pipeline " + p);
            }
            for (var c in thisOplModel.CHEMICAL) {
                writeln("Grade of " + c + ": "
                    + (thisOplModel.chemical_content[c]
                        / thisOplModel.production_requirement));
            }

            writeln("Total cost = " + cplex.getObjValue());
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem");
    }
}
