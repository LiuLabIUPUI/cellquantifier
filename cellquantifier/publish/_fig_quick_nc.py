import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from ..plot.plotutil import *
from ..plot.plotutil._add_mean_msd2 import add_mean_msd2
from ..phys import *

def fig_quick_nc():

    # """
	# ~~~~Initialize the colors~~~~
	# """
    # print("\n")
    # print("Preparing colors")
    # palette = sns.color_palette('Reds')
    # RGBA_alpha = 0.9
    # c1 = (0.2, 0.2, 0.2)
    # c2 = palette[0]
    # c3 = palette[1]
    # c4 = palette[2]
    # c5 = palette[3]
    # c6 = palette[4]
    # c7 = palette[5]
    # p = [c1, c2, c3, c4, c5, c6, c7, ]

    # c1 = (1, 0, 0)
    # c2 = (1, 0, 1)
    # c3 = (0, 0, 1)
    # c4 = (0, 1, 1)
    # c5 = (0, 1, 0)
    # c6 = (0.5, 0.5, 0.5)
    # c7 = (0, 0, 0)
    # RGBA_alpha = 0.8
    # c1_alp = (c1[0], c1[1], c1[2], RGBA_alpha)
    # c2_alp = (c2[0], c2[1], c2[2], RGBA_alpha)
    # c3_alp = (c3[0], c3[1], c3[2], RGBA_alpha)
    #
    # p = [c1, c2, c3, c4, c5, c6, c7]

    # c1 = (0, 0, 1)
    # c2 = (0, 0, 0)
    # c3 = (1, 0, 0)
    # RGBA_alpha = 0.8
    # p = [c1, c2, c3]

    c1 = (0, 0, 1)
    c2 = (0, 0, 0)
    RGBA_alpha = 0.8
    p = [c1, c2]


    # """
	# ~~~~Initialize the page layout~~~~
	# """
    # Layout settings
    col_num = 3
    row_num = 1
    divide_index = []
    hidden_index = []
    # Sub_axs_1 settings
    col_num_s1 = 1
    row_num_s1 = 2
    index_s1 = [
        0, 1,
        ]
    # Sub_axs_2 settings
    col_num_s2 = 1
    row_num_s2 = 2
    index_s2 = [
        ]

    # Layout implementation
    print("\n")
    print("Preparing layout")
    tot_width = col_num * 4
    tot_height = row_num * 3
    all_figures, page = plt.subplots(1, 1, figsize=(tot_width, tot_height))

    grids = []
    axs = []

    axs_s1_bg = []
    axs_s1 = []
    axs_s1_base = []
    axs_s1_slave = []

    axs_s2_bg = []
    axs_s2 = []
    axs_s2_base = []
    axs_s2_slave = []
    for i in range(col_num*row_num):
        r = i // col_num
        c = i % col_num
        w = 1 / col_num
        h = 1 / row_num
        x0 = c * w
        y0 = 1 - (r+1) * h

        # Generate Grids
        grids.append(page.inset_axes([x0, y0, w, h]))

        # Generate individual axs
        axs.append(grids[i].inset_axes([0.33, 0.33, 0.6, 0.6]))

        # Customize axs_s1
        if i in index_s1:
            axs_s1_bg.append(axs[i])
            for i_s1 in range(col_num_s1*row_num_s1):
                r_s1 = i_s1 // col_num_s1
                c_s1 = i_s1 % col_num_s1
                w_s1 = 1 / col_num_s1
                h_s1 = 1 / row_num_s1
                x0_s1 = c_s1 * w_s1
                y0_s1 = 1 - (r_s1+1) * h_s1
                # Generate axs_s1, axs_s1_base, axs_s1_slave
                temp = axs[i].inset_axes([x0_s1, y0_s1, w_s1, h_s1])
                axs_s1.append(temp)
                if y0_s1 == 0:
                    axs_s1_base.append(temp)
                else:
                    axs_s1_slave.append(temp)

        # Customize axs_s2
        if i in index_s2:
            axs_s2_bg.append(axs[i])
            for i_s2 in range(col_num_s2*row_num_s2):
                r_s2 = i_s2 // col_num_s2
                c_s2 = i_s2 % col_num_s2
                w_s2 = 1 / col_num_s2
                h_s2 = 1 / row_num_s2
                x0_s2 = c_s2 * w_s2
                y0_s2 = 1 - (r_s2+1) * h_s2
                # Generate axs_s2, axs_s2_base, axs_s2_slave
                temp = axs[i].inset_axes([x0_s2, y0_s2, w_s2, h_s2])
                axs_s2.append(temp)
                if y0_s2 == 0:
                    axs_s2_base.append(temp)
                else:
                    axs_s2_slave.append(temp)

    # """
	# ~~~~format figures~~~~
	# """
    print("\n")
    print("Formating figures")
    # Format page
    for ax in [page]:
        ax.set_xticks([]);
        ax.set_yticks([])
        format_spine(ax, spine_linewidth=2)

    # Format grids
    for ax in grids:
        ax.set_xticks([]);
        ax.set_yticks([])
        format_spine(ax, spine_linewidth=2)
        for spine in ['top', 'bottom', 'left', 'right']:
            ax.spines[spine].set_visible(False)

    for i in divide_index:
        for spine in ['bottom']:
            grids[i].spines[spine].set_visible(True)

    # Format axs
    for ax in axs:
        format_spine(ax, spine_linewidth=0.5)
        format_tick(ax, tk_width=0.5)
        format_tklabel(ax, tklabel_fontsize=10)
        format_label(ax, label_fontsize=10)

    for i in hidden_index:
        axs[i].set_xticks([]);
        axs[i].set_yticks([])
        for spine in ['top', 'bottom', 'left', 'right']:
            axs[i].spines[spine].set_visible(False)

    # Format sub_axs_background
    for ax in axs_s1_bg + axs_s2_bg:
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ['top', 'bottom', 'left', 'right']:
            ax.spines[spine].set_visible(False)

    # Format sub_axs
    for ax in axs_s1 + axs_s2:
        format_spine(ax, spine_linewidth=0.5)
        format_tick(ax, tk_width=0.5)
        format_tklabel(ax, tklabel_fontsize=10)
        format_label(ax, label_fontsize=10)
        ax.set_yticks([])

    # Format sub_axs_slave
    for ax in axs_s1_slave + axs_s2_slave:
        # labels = [item.get_text() for item in ax.get_xticklabels()]
        # empty_string_labels = ['']*len(labels)
        # ax.set_xticklabels(empty_string_labels)
        #
        # labels = [item.get_text() for item in ax.get_yticklabels()]
        # empty_string_labels = ['']*len(labels)
        # ax.set_yticklabels(empty_string_labels)
        ax.set_xticks([])




    # """
	# ~~~~Prepare df for the whole page~~~~
	# """
    print("\n")
    print("Preparing data")
    # """
    # ~~~~Filters applied to df~~~~
    # """
    # df1 = pd.read_csv('/home/linhua/Desktop/phys/200730_All-physDataMerged.csv',
    #                 index_col=False)
    #
    # df1 = add_stepsize(df1, pixel_size=0.163)
    # df1 = add_constrain_length(df1, pixel_size=0.163)
    #
    # df_blm = df1[ df1['exp_label']=='50NcBLM' ]
    # df_liv =  df1[ df1['exp_label']=='50NcLiving' ]
    # df_moc =  df1[ df1['exp_label']=='50NcMOCK' ]
    # df_atp =  df1[ df1['exp_label']=='50NcATP' ]
    # df_fix =  df1[ df1['exp_label']=='50NcFixed' ]
    # df_livm = df1[ df1['exp_label']=='50NcLivingM' ]
    # df_livb = df1[ df1['exp_label']=='50NcLivingB' ]
    #
    # df_blm = df_blm[ df_blm['traj_length']>=80 ]
    # df_liv = df_liv[ df_liv['traj_length']>=80 ]
    # df_moc = df_moc[ df_moc['traj_length']>=80 ]
    # df_atp = df_atp[ df_atp['traj_length']>=80 ]
    # df_fix = df_fix[ df_fix['traj_length']>=80 ]
    # df_livm = df_livm[ df_livm['traj_length']>=40 ]
    # df_livb = df_livb[ df_livb['traj_length']>=40 ]
    #
    # dfp_blm = df_blm.drop_duplicates('particle')
    # dfp_liv = df_liv.drop_duplicates('particle')
    # dfp_moc = df_moc.drop_duplicates('particle')
    # dfp_atp = df_atp.drop_duplicates('particle')
    # dfp_fix = df_fix.drop_duplicates('particle')
    # dfp_livm = df_livm.drop_duplicates('particle')
    # dfp_livb = df_livb.drop_duplicates('particle')
    #
    # df1 = pd.concat([df_blm, df_liv, df_moc, df_atp, df_fix, df_livm, df_livb], ignore_index=True)
    # df1p = pd.concat([dfp_blm, dfp_liv, dfp_moc, dfp_atp, dfp_fix, dfp_livm, dfp_livb], ignore_index=True)

    # df1 = pd.read_csv('/home/linhua/Desktop/phys/200925_NcUV-physDataMerged.csv',
    #                 index_col=False)
    #
    # df1 = add_stepsize(df1, pixel_size=0.163)
    # df1 = add_constrain_length(df1, pixel_size=0.163)
    #
    # df_ctr = df1[ df1['exp_label']=='NcUVCTL' ]
    # df_half_sec = df1[ df1['exp_label']=='NcUV0.5' ]
    # df_1s = df1[ df1['exp_label']=='NcUV1s' ]
    # df_2s = df1[ df1['exp_label']=='NcUV2s' ]
    # df_3s = df1[ df1['exp_label']=='NcUV3s' ]
    # df_5s = df1[ df1['exp_label']=='NcUV5s' ]
    # df_7s = df1[ df1['exp_label']=='NcUV7s' ]
    #
    # df_ctr = df_ctr[ df_ctr['traj_length']>=80 ]
    # df_half_sec = df_half_sec[ df_half_sec['traj_length']>=80 ]
    # df_1s = df_1s[ df_1s['traj_length']>=80 ]
    # df_2s = df_2s[ df_2s['traj_length']>=80 ]
    # df_3s = df_3s[ df_3s['traj_length']>=80 ]
    # df_5s = df_5s[ df_5s['traj_length']>=80 ]
    # df_7s = df_7s[ df_7s['traj_length']>=80 ]
    #
    # dfp_ctr = df_ctr.drop_duplicates('particle')
    # dfp_half_sec = df_half_sec.drop_duplicates('particle')
    # dfp_1s = df_1s.drop_duplicates('particle')
    # dfp_2s = df_2s.drop_duplicates('particle')
    # dfp_3s = df_3s.drop_duplicates('particle')
    # dfp_5s = df_5s.drop_duplicates('particle')
    # dfp_7s = df_7s.drop_duplicates('particle')
    #
    # df1 = pd.concat([df_ctr, df_half_sec, df_1s, df_2s, df_3s, df_5s, df_7s], ignore_index=True)
    # df1p = pd.concat([dfp_ctr, dfp_half_sec, dfp_1s, dfp_2s, dfp_3s, dfp_5s, dfp_7s], ignore_index=True)

    # df1 = pd.read_csv('/home/linhua/Desktop/phys/200813_NcUV-physDataMerged.csv',
    #                 index_col=False)
    #
    # df1 = add_stepsize(df1, pixel_size=0.163)
    # df1 = add_constrain_length(df1, pixel_size=0.163)
    #
    # df_ctr = df1[ df1['exp_label']=='50NcLiving' ]
    # df_10s = df1[ df1['exp_label']=='NcUV10s' ]
    # df_20s = df1[ df1['exp_label']=='NcUV20s' ]
    # df_30s = df1[ df1['exp_label']=='NcUV30s' ]
    # df_40s = df1[ df1['exp_label']=='NcUV40s' ]
    # df_1s = df1[ df1['exp_label']=='NcUV1s' ]
    #
    # df_ctr = df_ctr[ df_ctr['traj_length']>=80 ]
    # df_10s = df_10s[ df_10s['traj_length']>=80 ]
    # df_20s = df_20s[ df_20s['traj_length']>=80 ]
    # df_30s = df_30s[ df_30s['traj_length']>=80 ]
    # df_40s = df_40s[ df_40s['traj_length']>=80 ]
    # df_1s = df_1s[ df_1s['traj_length']>=80 ]
    #
    # dfp_ctr = df_ctr.drop_duplicates('particle')
    # dfp_10s = df_10s.drop_duplicates('particle')
    # dfp_20s = df_20s.drop_duplicates('particle')
    # dfp_30s = df_30s.drop_duplicates('particle')
    # dfp_40s = df_40s.drop_duplicates('particle')
    # dfp_1s = df_1s.drop_duplicates('particle')
    #
    # df1 = pd.concat([df_ctr, df_1s, df_10s, df_20s, df_30s, df_40s], ignore_index=True)
    # df1p = pd.concat([dfp_ctr, dfp_1s, dfp_10s, dfp_20s, dfp_30s, dfp_40s], ignore_index=True)

    # df1 = pd.read_csv('/home/linhua/Desktop/phys/200810_50NcLivingBMT-physDataMerged.csv',
    #                 index_col=False)
    #
    # df1 = add_stepsize(df1, pixel_size=0.163)
    # df1 = add_constrain_length(df1, pixel_size=0.163)
    #
    # df_b = df1[ df1['exp_label']=='50NcLivingB' ]
    # df_m = df1[ df1['exp_label']=='50NcLivingM' ]
    # df_t = df1[ df1['exp_label']=='50NcLivingT' ]
    #
    # df_b = df_b[ df_b['traj_length']>=40 ]
    # df_m = df_m[ df_m['traj_length']>=40 ]
    # df_t = df_t[ df_t['traj_length']>=40 ]
    #
    # dfp_b = df_b.drop_duplicates('particle')
    # dfp_m = df_m.drop_duplicates('particle')
    # dfp_t = df_t.drop_duplicates('particle')
    #
    # df1 = pd.concat([df_b, df_m, df_t], ignore_index=True)
    # df1p = pd.concat([dfp_b, dfp_m, dfp_t], ignore_index=True)

    df1 = pd.read_csv('/home/linhua/Desktop/phys/200708_50NcLiving-MvsBphysDataMerged.csv',
                    index_col=False)

    df1 = add_stepsize(df1, pixel_size=0.163)
    df1 = add_constrain_length(df1, pixel_size=0.163)

    df_b = df1[ df1['exp_label']=='B' ]
    df_m = df1[ df1['exp_label']=='M' ]

    df_b = df_b[ df_b['traj_length']>=40 ]
    df_m = df_m[ df_m['traj_length']>=40 ]

    dfp_b = df_b.drop_duplicates('particle')
    dfp_m = df_m.drop_duplicates('particle')

    df1 = pd.concat([df_b, df_m], ignore_index=True)
    df1p = pd.concat([dfp_b, dfp_m], ignore_index=True)



    # traj_length filter
    # if 'traj_length' in df:
    #     df = df[ df['traj_length']>=80 ]

    # # alpha filter
    # if 'alpha' in df:
    #     df = df[ df['alpha']>=0 ]

    # # travel_dist filter
    # if 'travel_dist' in df:
    #     travel_dist_min = 0
    #     travel_dist_max = 7
    #     df = df[ (df['travel_dist']>=travel_dist_min) & \
    #     					(df['travel_dist']<=travel_dist_max) ]


    # # """
    # # ~~~~Divide df into sub_dfs~~~~
    # # """
    # dfp = df.drop_duplicates('particle')
    # dfp_ctr = dfp[ dfp['exp_label']=='NcUVCTL' ]
    # dfp_half_sec = dfp[ dfp['exp_label']=='NcUV0.5' ]
    # dfp_1s = dfp[ dfp['exp_label']=='NcUV1s' ]
    # dfp_2s = dfp[ dfp['exp_label']=='NcUV2s' ]
    # dfp_3s = dfp[ dfp['exp_label']=='NcUV3s' ]
    # dfp_5s = dfp[ dfp['exp_label']=='NcUV5s' ]
    # dfp_7s = dfp[ dfp['exp_label']=='NcUV7s' ]
    #
    # dfv = df.dropna()


    # # """
	# # ~~~~Plot msd~~~~
	# # """
    # rename_msd_figs = []
    # msd_figs = [
    #     axs[0],
    #     ]
    # datas = [
    #     df,
    #     ]
    # palettes = [
    #     p,
    #     ]
    # cat_cols = [
    #     'exp_label',
    #     ]
    # orders = [
    #     ['NcUVCTL', 'NcUV0.5', 'NcUV1s', 'NcUV2s', 'NcUV3s', 'NcUV5s', 'NcUV7s', ],
    #     ]
    #
    # for i, (fig, data, palette, cat_col, order, ) \
    # in enumerate(zip(msd_figs, datas, palettes, cat_cols, orders, )):
    #     print("\n")
    #     print("Plotting (%d/%d)" % (i+1, len(msd_figs)))
    #
    #     add_mean_msd2(fig, data,
    #                 pixel_size=0.163,
    #                 frame_rate=20,
    #                 divide_num=5,
    #
    #                 cat_col=cat_col,
    #                 cat_order=order,
    #                 color_order=palette,
    #
    #                 fitting_linewidth=1,
    #                 elinewidth=1,
    #                 markersize=3,
    #                 capsize=1.5,
    #                 )
    #     set_xylabel(fig,
    #                 xlabel='Time (s)',
    #                 ylabel=r'MSD (nm$^2$)',
    #                 )


    # """
	# ~~~~Plot hist~~~~
	# """
    figs = axs_s1
    datas = [
            # df_blm, df_livm, df_liv, df_livb, df_moc, df_atp, df_fix,
            # dfp_blm, dfp_livm, dfp_liv, dfp_livb, dfp_moc, dfp_atp, dfp_fix,
            # df_ctr, df_half_sec, df_1s, df_2s, df_3s, df_5s, df_7s,
            # dfp_ctr, dfp_half_sec, dfp_1s, dfp_2s, dfp_3s, dfp_5s, dfp_7s,
            # df_ctr, df_1s, df_10s, df_20s, df_30s, df_40s,
            # dfp_ctr, dfp_1s, dfp_10s, dfp_20s, dfp_30s, dfp_40s,
            df_b, df_m,
            dfp_b, dfp_m,
            ]
    bins = [
            None, None,
            None, None,
            ]
    data_cols = [
            'stepsize', 'stepsize',
            'constrain_length', 'constrain_length',
            ]
    colors = [
            c1, c2,
            c1, c2,
            ]
    for i, (fig, data, bin, data_col, color, ) \
    in enumerate(zip(figs, datas, bins, data_cols, colors, )):
        print("\n")
        print("Plotting (%d/%d)" % (i+1, len(figs)))

        sns.distplot(data[data_col].dropna(),
                    bins=bin,
                    kde=True,
                    color=color,
                    ax=fig,
                    hist_kws={"alpha": RGBA_alpha,
                    'linewidth': 0.5, 'edgecolor': (0,0,0)},
                    kde_kws={"alpha": RGBA_alpha,
                    'linewidth': 1.5, 'color': color},
                    )


    # # """
	# # ~~~~Add t test~~~~
	# # """
    # figs = [
    #         axs_s1[0], axs_s1[2],
    #         ]
    # datas = [
    #         dfp, dfp,
    #         ]
    # data_cols = [
    #         'D', 'alpha',
    #         ]
    # cat_cols = [
    #         'exp_label', 'exp_label',
    #         ]
    # text_poss = [
    #         (0.98, 0.78), (0.98, 0.78),
    #         ]
    # for i, (fig, data, data_col, cat_col, text_pos, ) \
    # in enumerate(zip(figs, datas, data_cols, cat_cols, text_poss, )):
    #     print("\n")
    #     print("Plotting (%d/%d)" % (i+1, len(figs)))
    #
    #     add_t_test(fig,
    #                 blobs_df=data,
    #                 cat_col=cat_col,
    #                 hist_col=data_col,
    #                 drop_duplicates=False,
    #                 text_pos=text_pos,
    #                 color=(0,0,0,1),
    #                 fontname='Liberation Sans',
    #                 fontweight=9,
    #                 fontsize=9,
    #                 horizontalalignment='right',
    #                 format='general',
    #                 )
    # # """
	# # ~~~~Add figure text~~~~
	# # """
    # figs = grids
    # fig_texts = [
    #         'Fig.1a. Mean MSD curve comparion',
    #         'Fig.1b. D value comparison',
    #         'Fig.1c. Alpha value comparion',
    #         ]
    # for i, (fig, fig_text, ) \
    # in enumerate(zip(figs, fig_texts, )):
    #     print("\n")
    #     print("Plotting (%d/%d)" % (i+1, len(figs)))
    #
    #     fig.text(0.1,
    #             0.05,
    #             fig_text,
    #             horizontalalignment='left',
    #             color=(0,0,0,1),
    #             family='Liberation Sans',
    #             fontweight=10,
    #             fontsize=10,
    #             transform=fig.transAxes,
    #             )


    # """
	# ~~~~Additional figures format~~~~
	# """
    # # Format legend
    # for ax in msd_figs:
    #     format_legend(ax,
    #             show_legend=True,
    #             legend_loc='upper left',
    #             legend_fontweight=5,
    #             legend_fontsize=5,
    #             )
    # # Rename legend
    # for ax in rename_msd_figs:
    #     rename_legend(ax,
    #             new_labels=['Boundary', 'Inside'],
    #             replace_ind=1,
    #             replace_type='prefix',
    #             legend_loc='lower right',
    #             legend_fontweight=7,
    #             legend_fontsize=7,
    #             )
    # Format scale
    figs = [
            # axs_s1[0], axs_s1[1], axs_s1[2], axs_s1[3], axs_s1[4], axs_s1[5], axs_s1[6],
            # axs_s1[7], axs_s1[8], axs_s1[9], axs_s1[10], axs_s1[11], axs_s1[12], axs_s1[13],
            # axs_s1[0], axs_s1[1], axs_s1[2], axs_s1[3], axs_s1[4], axs_s1[5],
            # axs_s1[6], axs_s1[7], axs_s1[8], axs_s1[9], axs_s1[10], axs_s1[11],
            # axs_s1[0], axs_s1[1], axs_s1[2],
            # axs_s1[3], axs_s1[4], axs_s1[5],
            axs_s1[0], axs_s1[1],
            axs_s1[2], axs_s1[3],
            ]
    xscales = [
            # [0, 0.15], [0, 0.15], [0, 0.15], [0, 0.15], [0, 0.15], [0, 0.15], [0, 0.15],
            # [0, 0.2], [0, 0.2], [0, 0.2], [0, 0.2], [0, 0.2], [0, 0.2], [0, 0.2],
            # [0, 0.15], [0, 0.15], [0, 0.15], [0, 0.15], [0, 0.15], [0, 0.15],
            # [0, 0.2], [0, 0.2], [0, 0.2], [0, 0.2], [0, 0.2], [0, 0.2],
            [0, 0.15], [0, 0.15],
            [0, 0.2], [0, 0.2],
            ]
    yscales = [
            # [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None],
            # [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None],
            # [None, None], [None, None], [None, None], [None, None], [None, None], [None, None],
            # [None, None], [None, None], [None, None], [None, None], [None, None], [None, None],
            [None, None], [None, None],
            [None, None], [None, None],
            ]
    for i, (fig, xscale, yscale, ) \
    in enumerate(zip(figs, xscales, yscales,)):
        format_scale(fig,
                xscale=xscale,
                yscale=yscale,
                )


    # """
	# ~~~~Save the figure into pdf file, preview the figure in webbrowser~~~~
	# """
    all_figures.savefig('/home/linhua/Desktop/Figure_NC.pdf', dpi=600)
    plt.clf(); plt.close()
    # plt.show()
