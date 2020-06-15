import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from ..phys import *
from ..util import get_frac_df
from ..plot.plotutil import *

from matplotlib.lines import Line2D
from scipy.stats import sem

def fig_quick_rna_3(merged_blobs_df, merged_int_df, norm_row_props,
					norm_nest_col, typ_arr=['type1','type2','type3','type4']):

	"""

	Pseudo code
	----------
	1. Build the figure
	2. Group by 'label', 'cell_type' and 'prefix' columns

	Parameters
	----------
	input_dir : str,
		Directory containing the files of interest
	typ_arr: list
		List of unique types some of which may be in merged_xxx_df

	"""

	fig, ax = plt.subplots(1, 2)
	path = '/home/clayton/Desktop/data-analysis/'

	# """
	# ~~~~~~~~~~~Copy number pivot table~~~~~~~~~~~~~~
	# """

	cols = ['cell_type', 'sample_type', 'label']
	merged_blobs_df = merged_blobs_df[cols + ['region_type', 'prefix']]
	merged_blobs_df = merged_blobs_df.rename(columns={'prefix':'count_'})

	count_df_pivot = pd.pivot_table(merged_blobs_df,
									index=cols,
									columns=['region_type'],
									aggfunc='count',
									fill_value=0)

	count_df = count_df_pivot.reset_index()
	count_df.columns = [''.join(col) for col in count_df.columns]
	count_df['count_total'] = count_df['count_cyto'] + count_df['count_nuc']

	# """
	# ~~~~~~~~~~~Statistics~~~~~~~~~~~~~~
	# """kkkk

	data_col = 'count_total'; cat_cols = ['cell_type', 'sample_type']
	count_df_stat = count_df[[data_col] + cat_cols]
	count_df_stat = count_df_stat.groupby(cat_cols, sort=True)[data_col].agg([np.mean, sem])
	count_df_stat = count_df_stat.reset_index()

	count_df_stat = norm_df(count_df_stat,
					   col='mean',
					   col_arr=['mean', 'sem'],
					   row_props=norm_row_props,
					   nest_col=norm_nest_col)


	count_df_stat.to_csv(path + '200611_HLA-DMB-count-df-stat.csv')

	# """
	# ~~~~~~~~~~~Nucleus/Cytoplasm Fractions~~~~~~~~~~~~~~
	# """


	frac_df = count_df.copy();
	frac_df['frac_cyto'] = frac_df['count_cyto']/frac_df['count_total']
	frac_df['frac_nuc'] = frac_df['count_nuc']/frac_df['count_total']
	frac_df = frac_df.drop(columns=['count_cyto', 'count_nuc', 'count_total'])
	data_cols = ['frac_nuc', 'frac_cyto']
	frac_df_stat = frac_df.groupby(cat_cols, sort=True)[data_cols].agg([np.mean, sem])
	frac_df_stat = frac_df_stat.reset_index()


	frac_df_stat.to_csv(path + '200611_HLA-DMB-frac-df-stat.csv')
