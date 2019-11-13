from cellquantifier.segm import get_dist2boundary_mask

def add_dist_to_boundary(df, mask):

    """
    Label particles in a DataFrame based on dist2boundary_mask

    Parameters
    ----------
    mask : ndarray
        Binary mask of cell
    df : DataFrame
        DataFrame containing x,y columns

    Returns
    -------
    df: DataFrame
        DataFrame with added 'dist_to_boundary' column

    Examples
    --------
    import pandas as pd; import pims
    from cellquantifier.segm import get_thres_mask
    from cellquantifier.phys import add_dist_to_boundary

    frames = pims.open('cellquantifier/data/simulated_cell.tif')
    df = pd.read_csv('cellquantifier/data/test_fittData.csv')
    mask = get_thres_mask(frames[0], sig=3, thres_rel=0.1)
    df = add_dist_to_boundary(df, mask)
    print(df)
    """

    dist2boundary_mask = get_dist2boundary_mask(mask)

    for index in df.index:
        r = int(round(df.at[index, 'x']))
        c = int(round(df.at[index, 'y']))
        df.at[index, 'dist_to_boundary'] = dist2boundary_mask[r, c]

    return df
