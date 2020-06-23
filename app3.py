"""Part I: CellQuantifier Sequence Control"""

control = [
# 'clean_dir',
# 'load',
# 'regi',
# 'mask_boundary',
# 'mask_53bp1',
# 'mask_53bp1_blob',
# 'deno_mean',
# 'deno_median',
# 'deno_box',
# 'deno_gaus',
# 'check_detect_fit',
# 'detect',
# 'fit',

# 'filt_track',
# 'phys_xy_global',
# 'phys_dist2halfcilia',
# 'phys_cilia_halfsign',
# 'phys_cilia_otherinfo',
'plot_traj',
# 'anim_traj',
# 'merge_plot',

# 'phys_dist253bp1',
# 'phys_dist253bp1_blob',


# 'filt_track',
# 'phys_dist2boundary',
# 'phys_antigen_data',
# 'plot_traj',
# 'anim_traj',

# 'sort_plot',
# 'merge_plot',
]

"""Part II: CellQuantifier Parameter Settings"""

settings = {

  #IO
  'IO input_path': '/home/linhua/Desktop/old_data/',
  'IO output_path': '/home/linhua/Desktop/old_data/',

  #HEADER INFO
  'Processed By:': 'Hua Lin',
  'Start frame index': 0,
  'End frame index': 28,
  'Load existing analMeta': False,

  #REGISTRATION SETTINGS
  'Regi reference file label': '',
  'Regi ref_ind_num': '',
  'Regi sig_mask': '',
  'Regi thres_rel': '',
  'Regi poly_deg': '',
  'Regi rotation_multiplier': '',
  'Regi translation_multiplier': '',
  'Regi use_ransac': '',

  #SEGMENTATION SETTINGS
  'Segm min_size': '',
  'Segm threshold': '',

  #MASK_BOUNDARY SETTINGS
  'Mask boundary_mask file label': '',
  'Mask boundary_mask sig': '',
  'Mask boundary_mask thres_rel': '',
  #MASK_53BP1 SETTINGS
  'Mask 53bp1_mask file label': '',
  'Mask 53bp1_mask sig': '',
  'Mask 53bp1_mask thres_rel': '',
  #MASK_53BP1_BLOB SETTINGS
  'Mask 53bp1_blob_mask file label': '',
  'Mask 53bp1_blob_threshold': '',
  'Mask 53bp1_blob_min_sigma': '',
  'Mask 53bp1_blob_max_sigma': '',
  'Mask 53bp1_blob_num_sigma': '',
  'Mask 53bp1_blob_pk_thresh_rel': '',
  'Mask 53bp1_blob_search_range': '',
  'Mask 53bp1_blob_memory': '',
  'Mask 53bp1_blob_traj_length_thres': '',

  #DENOISE SETTINGS
  'Deno mean_radius': '',
  'Deno median_radius': 2,
  'Deno boxcar_radius': 10,
  'Deno gaus_blur_sig': 0.5,

  #DETECTION SETTINGS
  'Det blob_threshold': 0.01,
  'Det blob_min_sigma': 2,
  'Det blob_max_sigma': 10,
  'Det blob_num_sigma': 9,
  'Det pk_thresh_rel': 0.1,

  #TRACKING SETTINGS
  'Trak frame_rate': 0.41,
  'Trak pixel_size': 0.04,
  'Trak divide_num': 3,

  ###############################################
  'Trak search_range': 8,  # NO. 1
  ###############################################

  'Trak memory': 3,

  #FILTERING SETTINGS
  'Filt max_dist_err': 5,
  'Filt max_sig_to_sigraw': 10,
  'Filt max_delta_area': 4,

  ###############################################
  'Filt traj_length_thres': 15, # NO. 2
  #SORTING SETTINGS
  'Sort dist_to_boundary': [-15, 10], # NO. 3
  'Sort travel_dist': None, # NO. 4
  ###############################################

  'Sort dist_to_53bp1': None,

}

"""Part III: Run CellQuantifier"""
# from cellquantifier.util.pipeline3_cilia2 import *
# pipeline_batch(settings, control)

import pandas as pd
from cellquantifier.publish._fig_quick_cilia_5 import *
from cellquantifier.phys.travel_dist import *
df = pd.read_csv('/home/linhua/Desktop/phys/200619-physDataMerged.csv',
                index_col=False)
df = add_travel_dist(df)
fig_quick_cilia_5(df)

# from cellquantifier.publish import *
# plot_fig_1()



# from cellquantifier.publish import *
# import pandas as pd
# df = pd.read_csv('/home/linhua/Desktop/temp/200303_50NcBLM-physDataMerged.csv',
#                 index_col=False)
#
# print(len(df))
# df= df[ ~df['raw_data'].isin(['200211_50NcLiving_D1-HT-physData.csv',
#                         '200211_50NcLiving_A2-HT-physData.csv',
#                         '200206_50NcLiving_L2-HT-physData.csv',
#                         '190925_50NcLiving_K1-HT-physData.csv']) ]
#
# # df= df[ df['raw_data'].isin(['190924_50NcLiving_B1-HT-physData.csv',
# #                         '190924_50NcLiving_D1-HT-physData.csv',
# #                         '190924_50NcLiving_E1-HT-physData.csv',
# #                         '190924_50NcLiving_I1-HT-physData.csv',
# #                         '190924_50NcLiving_J2-HT-physData.csv',
# #                         '191010_50NcLiving_B1-HT-physData.csv',
# #
# #                         '191004_50NcBLM_A1-HT-physData.csv',
# #                         '191004_50NcBLM_B1-HT-physData.csv',
# #                         '191004_50NcBLM_C1-HT-physData.csv',
# #                         '191004_50NcBLM_E1-HT-physData.csv',
# #                         '191004_50NcBLM_F1-HT-physData.csv',
# #                         '191004_50NcBLM_I1-HT-physData.csv',
# #                         '191004_50NcBLM_K1-HT-physData.csv',
# #                         '191004_50NcBLM_Q1-HT-physData.csv',
# #                         '191004_50NcBLM_T1-HT-physData.csv'
# #                         ]) ]
#
# df['date'] = df['raw_data'].astype(str).str[0:6]
# df = df[ df['date'].isin(['191004', '190924', '190925', '191010', '200206',]) ]
# print(len(df))
# fig_quick_nucleosome(df)


# from cellquantifier.publish import *
# import pandas as pd
# df = pd.read_csv('/home/linhua/Desktop/temp/200407-physDataMerged.csv',
#                 index_col=False)
# fig_quick_cilia(df)

# from cellquantifier.phys import *
# import pandas as pd
# df = pd.read_csv('/home/linhua/Desktop/temp/200407_globalPhysDataMerged.csv',
#                 index_col=False)
# df = add_cilia_liftime(df)
# df.round(6).to_csv('/home/linhua/Desktop/temp/200407_globalPhysDataMerged-lifetime.csv',
#                 index=False)


# from cellquantifier.publish import *
# import pandas as pd
# df_glb = pd.read_csv('/home/linhua/Desktop/temp/200407_globalPhysDataMerged-lifetime.csv',
#                 index_col=False)
# df_loc = pd.read_csv('/home/linhua/Desktop/temp/200505_localPhysDataMerged-lifetime.csv',
#                 index_col=False)
# fig_quick_cilia_2(df_glb, df_loc)


# from cellquantifier.phys import add_d_alpha
# import pandas as pd
# df = pd.read_csv('/home/linhua/Desktop/temp/df.csv',
#                 index_col=False)
# df = add_d_alpha(df, divide_num=3, unified_pixel_size=0.1)
# df.round(6).to_csv('/home/linhua/Desktop/temp/df_newD.csv',
#                 index=False)



# from cellquantifier.plot import plot_msd_fitting
# import pandas as pd
# df = pd.read_csv('/home/linhua/Desktop/temp/df_newD.csv',
#                 index_col=False)
# df = df[ df['particle'].isin([0,1,2,3,5,9,10,12,14,15,17,20,25,29,30,31,32,
#         38,39,43,46,50,51,53,55,58,62,65,66])]
# plot_msd_fitting(df, output_path='/home/linhua/Desktop/temp/')


# from cellquantifier.plot import plot_1dfft
# import pandas as pd
# df = pd.read_csv('/home/linhua/Desktop/temp/df_newD.csv',
#                 index_col=False)
# # df = df[ df['particle'].isin([0,1,2,3,4])]
# # df = df[ df['exp_label'].isin(['cohort a'])]
# # df = df[ ~df['particle'].isin([14, 25, 26, 35, 36, 37])]
# df = df[ df['exp_label'].isin(['cohort b'])]
# df = df[ ~df['particle'].isin([41,42,45,54,55,60,63,69,70])]
# plot_1dfft(df, output_path='/home/linhua/Desktop/temp/')


# from cellquantifier.publish import *
# import pandas as pd
# df_glb = pd.read_csv('/home/linhua/Desktop/temp/200407_globalPhysDataMerged-lifetime.csv',
#                 index_col=False)
# df_loc = pd.read_csv('/home/linhua/Desktop/temp/df_newD.csv',
#                 index_col=False)
# df_loc = df_loc[ df_loc['particle'].isin([0,1,3,5,9,10,12,14,15,17,20,25,29,30,31,32,
#         38,39,43,46,50,51,53,55,58,62,65,66])]
# fig_quick_cilia_4(df_glb, df_loc)


# from cellquantifier.publish import *
# import pandas as pd
# df = pd.read_csv('/home/linhua/Desktop/output/cilia-physData.csv',
#                 index_col=False)
# fig_quick_msd(df)


# from skimage.io import imread, imsave
# from cellquantifier.publish import *
# from cellquantifier.video import *
# import pandas as pd
#
# df = pd.read_csv('/home/linhua/Desktop/temp/200205_MalKN-E-physData.csv',
#                 index_col=False)
# df = df[ df['traj_length']>20 ]
# fig_quick_antigen(df)



# df = pd.read_csv('/home/linhua/Desktop/temp-E/200205_MalKN-E-physData.csv',
#                 index_col=False)
# tif = imread('/home/linhua/Desktop/temp-E/200205_MalKN-E-raw.tif')[0:50]
# df = df[ (df['traj_length']>100) & (df['frame']<50) ]
# anim_tif = anim_traj(df, tif,
#                 pixel_size=0.163,
#                 cb_min=2000, cb_max=10000,
#                 cb_major_ticker=2000, cb_minor_ticker=2000,
#                 show_image=True)
# anim_tif = anim_blob(df, tif, pixel_size=0.163,
#                 show_image=False)
# imsave('/home/linhua/Desktop/temp-E/anim-traj-result.tif', anim_tif)
# fig_quick_antigen(df)



# from cellquantifier.publish import *
# import pandas as pd
#
# df = pd.read_csv('/home/linhua/Desktop/temp/200426_physDataMerged.csv',
#                 index_col=False)
# fig_quick_antigen_3(df)
