from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt

def format_ax(ax,
    xlabel='',
    ylabel='',
    xlabel_color=(0,0,0,1),
    ylabel_color=(0,0,0,1),
    label_fontname='Arial',
    label_fontweight='normal',
    label_fontsize='medium',
    xscale=[None,None,None,None],
    yscale=[None,None,None,None],
    tklabel_fontname='Arial',
    tklabel_fontweight='normal',
    tklabel_fontsize='medium',
    show_legend=True,
    legend_loc='upper left',
    legend_frameon=False,
    legend_fontname='Arial',
    legend_fontweight='normal',
    legend_fontsize='medium'):
    """
    Adjust ax format: axis label, ticker label, tickers.

    Parameters
    ----------
    ax : object
        matplotlib ax.

    xlabel : str
        x axis label name.

    ylabel : str
        x axis label name.

    xlabel_color : tuple
        RGB or RGBA tuple.

    ylabel_color : tuple
        RGB or RGBA tuple.

    xscale : list
        [x_min, x_max, x_major_ticker, x_minor_ticker]

    yscale : list
        [y_min, y_max, y_major_ticker, y_minor_ticker]

    label_fontname : str

    label_fontsize : str or int

    label_fontweight : str or int

    tklabel_fontname : str

    tklabel_fontsize : str or int

    tklabel_fontweight : str or int
    """

    # """
    # ~~~~~~~~~~~format x, y axis label~~~~~~~~~~~~~~
    # """
    ax.set_xlabel(xlabel,
                color=xlabel_color,
                fontname=label_fontname,
                fontweight=label_fontweight,
                fontsize=label_fontsize)
    ax.set_ylabel(ylabel,
                color=ylabel_color,
                fontname=label_fontname,
                fontweight=label_fontweight,
                fontsize=label_fontsize)
    ax.spines['bottom'].set_color(xlabel_color)
    ax.spines['left'].set_color(ylabel_color)

    # """
    # ~~~~~~~~~~~format xtick, ytick label~~~~~~~~~~~~~~
    # """
    plt.setp(ax.get_xticklabels(),
                color=xlabel_color,
                fontname=tklabel_fontname,
                fontweight=tklabel_fontweight,
                fontsize=tklabel_fontsize)
    plt.setp(ax.get_yticklabels(),
                color=ylabel_color,
                fontname=tklabel_fontname,
                fontweight=tklabel_fontweight,
                fontsize=tklabel_fontsize)

    ax.tick_params(axis='x', which='both', color=xlabel_color)
    ax.tick_params(axis='y', which='both', color=ylabel_color)

    # """
    # ~~~~~~~~~~~format xlim, ylim, major_tk, minor_tk~~~~~~~~~~~~~~
    # """
    while(len(xscale) < 4):
        xscale.append(None)
    while(len(yscale) < 4):
        yscale.append(None)

    x_min, x_max, x_major_tk, x_minor_tk = xscale
    ax.set_xlim(x_min, x_max)
    if x_major_tk:
        ax.xaxis.set_major_locator(MultipleLocator(x_major_tk))
    if x_minor_tk:
        if x_minor_tk < x_major_tk:
            ax.xaxis.set_minor_locator(MultipleLocator(x_minor_tk))

    y_min, y_max, y_major_tk, y_minor_tk = yscale
    ax.set_ylim(y_min, y_max)
    if y_major_tk:
        ax.yaxis.set_major_locator(MultipleLocator(y_major_tk))
    if y_minor_tk:
        if y_minor_tk < y_major_tk:
            ax.yaxis.set_minor_locator(MultipleLocator(y_minor_tk))

    # """
    # ~~~~~~~~~~~format legend~~~~~~~~~~~~~~
    # """
    if show_legend:
        ax.legend(loc=legend_loc,
                frameon=legend_frameon,
                fontsize=legend_fontsize,
                prop={'family' : legend_fontname,
                    'size' : legend_fontsize,
                    'weight' : legend_fontweight})

    # """
    # ~~~~~~~~~~~set anchor position~~~~~~~~~~~~~~
    # """
    ax.set_anchor('SW')
