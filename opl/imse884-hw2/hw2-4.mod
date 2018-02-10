{string} LOAN = {"Student", "Car", "Credit Card"};
float initial_balance[LOAN] = [30000, 8000, 12000];
float interest_rate_per_month[LOAN] = [0.0075, 0.005, 0.01];
float minimum_monthly_payment[LOAN] = [300, 50, 125];
float monthly_debt_retirement_budget = 800;
int max_month = 180;
range MONTH_0 = 0..max_month;
range MONTH = 1..max_month;
float over_minimum = 50;

dvar float monthly_balance[LOAN, MONTH_0];
dvar float monthly_interest_charge[LOAN, MONTH_0];
dvar float monthly_payment[LOAN, MONTH];
dvar int+ pay_over_minimum[LOAN, MONTH] in (0..1);
dvar int paid[LOAN, MONTH] in (0..1);

minimize
    sum (loan in LOAN, m in MONTH_0) (
        monthly_interest_charge[loan, m]
    );

subject to {
    // Initial balances.
    forall (loan in LOAN)
        monthly_balance[loan, 0] == initial_balance[loan];

    // Month-over-month interest.
    forall (loan in LOAN, m in MONTH_0)
        monthly_interest_charge[loan, m]
        ==
        monthly_balance[loan, m] * interest_rate_per_month[loan];

    // Pay over the minimum on at least two loans each month.
    forall (m in MONTH) (
        sum (loan in LOAN) (
            pay_over_minimum[loan, m]
        ) >= 2
    );

    // Pay at least the minimum plus any overage each month.
    forall (loan in LOAN, m in MONTH) (
        monthly_payment[loan, m]
        >=
        (
            minimum_monthly_payment[loan]
            +
            (pay_over_minimum[loan, m] * over_minimum)
        )
    );

    // Pay no more than your budget each month.
    forall (m in MONTH) (
        sum (loan in LOAN) (monthly_payment[loan, m])
        <=
        monthly_debt_retirement_budget
    );

    // Month-over-month balances.
    forall (loan in LOAN, m in MONTH) (
        monthly_balance[loan, m]
        ==
        maxl(
            0,
            monthly_balance[loan, m - 1]
                + monthly_interest_charge[loan, m - 1]
                - monthly_payment[loan, m]
        )
    );
}


main {
    if (!thisOplModel.generate()) {
        if (cplex.solve()) {
            writeln("Monthly payments");
            writeln("================");
            writeln("Month\tStudent\t\tCar\t\tCredit Card");
            for (var m in thisOplModel.MONTH) {
                writeln(m
                    + "\t" + thisOplModel.monthly_payment["Student"][m]
                    + "\t" + thisOplModel.monthly_payment["Car"][m]
                    + "\t" + thisOplModel.monthly_payment["Credit Card"][m]
                );
            }
            writeln("");
            writeln("Monthly interest");
            writeln("================");
            writeln("Month\tStudent\t\tCar\t\tCredit Card");
            for (var m in thisOplModel.MONTH) {
                writeln(m
                    + "\t" + thisOplModel.monthly_interest_charge["Student"][m]
                    + "\t" + thisOplModel.monthly_interest_charge["Car"][m]
                    + "\t" + thisOplModel.monthly_interest_charge["Credit Card"][m]
                );
            }
            writeln("");
            writeln("Monthly balances");
            writeln("================");
            writeln("Month\tStudent\t\tCar\t\tCredit Card");
            for (var m in thisOplModel.MONTH) {
                writeln(m
                    + "\t" + thisOplModel.monthly_balance["Student"][m]
                    + "\t" + thisOplModel.monthly_balance["Car"][m]
                    + "\t" + thisOplModel.monthly_balance["Credit Card"][m]
                );
            }
            writeln("");
            writeln("Payoff months:")
            writeln("================");
            write("Student: ");
            for (var m in thisOplModel.MONTH) {
                if (thisOplModel.monthly_balance["Student"][m] <= 0) {
                    writeln(m - 1);
                    break;
                }
            }
            write("Car: ");
            for (var m in thisOplModel.MONTH) {
                if (thisOplModel.monthly_balance["Car"][m] <= 0) {
                    writeln(m - 1);
                    break;
                }
            }
            write("Credit Card: ");
            for (var m in thisOplModel.MONTH) {
                if (thisOplModel.monthly_balance["Credit Card"][m] <= 0) {
                    writeln(m - 1);
                    break;
                }
            }
        } else {
            writeln("Either Unbounded or Infeasible");
        }
    } else {
        writeln("OPL could not read problem")      
    }
}
