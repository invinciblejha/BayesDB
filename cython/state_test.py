import argparse
#
import tabular_predDB.cython.State as State
import tabular_predDB.cython.gen_data as gen_data


# parse input
parser = argparse.ArgumentParser()
parser.add_argument('--gen_seed', default=0, type=int)
parser.add_argument('--num_clusters', default=4, type=int)
parser.add_argument('--num_cols', default=8, type=int)
parser.add_argument('--num_rows', default=1000, type=int)
parser.add_argument('--num_splits', default=2, type=int)
parser.add_argument('--max_mean', default=10, type=float)
parser.add_argument('--max_std', default=0.3, type=float)
args = parser.parse_args()
#
gen_seed = args.gen_seed
num_clusters = args.num_clusters
num_cols = args.num_cols
num_rows = args.num_rows
num_splits = args.num_splits
max_mean = args.max_mean
max_std = args.max_std

# create the data
T, M_r, M_c = gen_data.gen_factorial_data_objects(
    gen_seed, num_clusters,
    num_cols, num_rows, num_splits,
    max_mean=max_mean, max_std=max_std,
    )

# with open('SynData2.csv') as fh:
#     import numpy
#     import csv
#     T = numpy.array([row for row in csv.reader(fh)], dtype=float).tolist()
#     M_r = gen_data.gen_M_r_from_T(T)
#     M_c = gen_data.gen_M_c_from_T(T)

# create the state
p_State = State.p_State(M_c, T)

# transition the sampler
print "p_State.get_marginal_logp():", p_State.get_marginal_logp()
for transition_idx in range(300):
    print "transition #: %s" % transition_idx
    p_State.transition()
    print "s.num_views:", p_State.get_num_views(), "; s.column_crp_score:", p_State.get_column_crp_score(), "; s.data_score:", p_State.get_data_score(), "; s.score:", p_State.get_marginal_logp()
    print p_State

# print the final state
X_D = p_State.get_X_D()
X_L = p_State.get_X_L()
print "X_D:", X_D
print "X_L:", X_L
for view_idx, view_state_i in enumerate(p_State.get_view_state()):
    print "view_state_i:", view_idx, view_state_i
print p_State

# test generation of state from X_L, X_D
p_State_2 = State.p_State(M_c, T, X_L, X_D)
X_D_prime = p_State_2.get_X_D()
X_L_prime = p_State_2.get_X_L()

print "X_D_prime:", X_D_prime
print "X_L_prime:", X_L_prime
