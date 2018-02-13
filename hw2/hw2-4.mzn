enum LOAN;
array[LOAN] of float: initial_balance;
array[LOAN] of float: interest_rate_per_month;
array[LOAN] of float: minimum_monthly_payment;
float: monthly_debt_retirement_budget;
int: max_month;
set of int: MONTH_0 = 0..max_month;
set of int: MONTH = 1..max_month;
float: over_minimum;

array[LOAN, MONTH_0] of var float: monthly_balance;
array[LOAN, MONTH_0] of var float: monthly_interest_charge;
array[LOAN, MONTH] of var float: monthly_payment;
array[LOAN, MONTH] of var 0..1: pay_over_minimum;

% Initial balances.
constraint
    forall (loan in LOAN) (
        monthly_balance[loan, 0] == initial_balance[loan]
    );

% Month-over-month interest.
constraint
    forall (loan in LOAN, m in MONTH_0) (
        monthly_interest_charge[loan, m]
        ==
        monthly_balance[loan, m] * interest_rate_per_month[loan]
    );

% Month-over-month balances.
constraint
    forall (loan in LOAN, m in MONTH) (
        monthly_balance[loan, m]
        ==
        monthly_balance[loan, m - 1]
        +
        monthly_interest_charge[loan, m - 1]
        -
        monthly_payment[loan, m]
    );

% Pay no more than your budget each month.
constraint
    forall (m in MONTH) (
        sum (loan in LOAN) (monthly_payment[loan, m])
        <=
        monthly_debt_retirement_budget
    );
    
% Pay at least the minimum plus any overage each month.
constraint
    forall (loan in LOAN, m in MONTH) (
        monthly_payment[loan, m]
        >=
        (
            minimum_monthly_payment[loan]
            +
            (pay_over_minimum[loan, m] * over_minimum)
        )
    );

% Pay over the minimum on at least two loans.
constraint
    forall (m in MONTH) (
        sum (loan in LOAN) (
            pay_over_minimum[loan, m]
        ) >= 2
    );

var float: obj =
    sum (loan in LOAN, m in MONTH_0) (
        monthly_interest_charge[loan, m]
    );
    
solve minimize obj;
