import os

def rename_01(src_path):
	"""
	Rename files manner 1

	Examples
	--------
    "190814_Ctr1_cell0-53bp1-raw-0-100.tif" --> "190814_Ctr1-1_cell0-53bp1-raw.tif"
	"190814_Ctr1_cell0-53bp1-raw-0-1100.tif" --> "190814_Ctr1-11_cell0-53bp1-raw.tif"
    """

	# find insert index
	filename = src_path.split('/')[-1]
	m = filename.find('_') + 1
	m = filename.find('_', m)
	n = len(filename) - m

	# find insert string
	stage_name = filename.split('-')[-1]
	stage_label = stage_name[:-6]

	# find end index
	end_ind = src_path.find('-raw') + 4

	# get src_path and rename
	dst_path = src_path[:-n] + '-' + stage_label + src_path[-n:end_ind] + '.tif'
	os.rename(src_path, dst_path)


def rename_02(src_path):
	"""
	Rename files manner 2

	Examples
	--------
    "190814_Ctr1-1_cell01-53bp1-0-3-0.2-2-0-1-True.tif" --> "190814_Ctr1-1_cell01-53bp1.tif"
    """

	# find insert index
	filename = src_path.split('/')[-1]
	m = filename.find('-') + 1
	m = filename.find('-', m) + 1
	m = filename.find('-', m)
	n = len(filename) - m

	# get src_path and rename
	dst_path = src_path[:-n] + '.tif'
	print(src_path)
	print(dst_path)
	os.rename(src_path, dst_path)
