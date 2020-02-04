import pims; import pandas as pd; import numpy as np
import trackpy as tp
import os.path as osp; import os; import ast
from datetime import date, datetime
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte
from skimage.measure import regionprops
import warnings
import glob

from ..deno import filter_batch
from ..io import *
from ..segm import *
from ..regi import get_regi_params, apply_regi_params

from ..smt.detect import detect_blobs, detect_blobs_batch
from ..smt.fit_psf import fit_psf, fit_psf_batch
from ..smt.track import track_blobs
from ..smt.msd import plot_msd_batch, get_sorter_list
from ..phys import *
from ..util.config2 import Config
from ..plot import plot_phys_1 as plot_merged
from ..phys.physutil import relabel_particles, merge_physdfs


def file1_exists_or_pimsopen_file2(head_str, tail_str1, tail_str2):
	if osp.exists(head_str + tail_str1):
		frames = pims.open(head_str + tail_str1)
	else:
		frames = pims.open(head_str + tail_str2)
	return frames


def nonempty_exists_then_copy(input_path, output_path, filename):
	not_empty = len(filename)!=0
	exists_in_input = osp.exists(input_path + filename)
	not_exists_in_output = not osp.exists(output_path + filename)

	if not_empty and exists_in_input and not_exists_in_output:
		frames = imread(input_path + filename)
		frames = frames / frames.max()
		frames = img_as_ubyte(frames)
		imsave(output_path + filename, frames)


def nonempty_openfile1_or_openfile2(path, filename1, filename2):
	if filename1: # if not empty
		frames = imread(path + filename1)
	else:
		frames = imread(path + filename2)
	return frames


class Pipeline2():

	def __init__(self, config):
		self.config = config

	def clean_dir(self):
		self.config.clean_dir()

	def load(self):
		# load data file
		if osp.exists(self.config.INPUT_PATH + self.config.ROOT_NAME + '.tif'):
			frames = imread(self.config.INPUT_PATH + self.config.ROOT_NAME + '.tif')
		else:
			frames = imread(self.config.INPUT_PATH + self.config.ROOT_NAME + '-raw.tif')

		frames = frames / frames.max()
		frames = img_as_ubyte(frames)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-raw.tif', frames)

		if frames.ndim == 3 & self.config.DICT['End frame index'] <= len(frames):
			frames = frames[list(self.config.TRANGE),:,:]
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif', frames)

		print('\tRegi_ref_file: [%s]' % self.config.REF_FILE_NAME)
		print('\tMask_dist2boundary_file: [%s]' % self.config.DIST2BOUNDARY_MASK_NAME)
		print('\tMask_dist253bp1_file: [%s]' % self.config.DIST253BP1_MASK_NAME)
		# load reference files
		nonempty_exists_then_copy(self.config.INPUT_PATH, self.config.OUTPUT_PATH, self.config.REF_FILE_NAME)
		nonempty_exists_then_copy(self.config.INPUT_PATH, self.config.OUTPUT_PATH, self.config.DIST2BOUNDARY_MASK_NAME)
		nonempty_exists_then_copy(self.config.INPUT_PATH, self.config.OUTPUT_PATH, self.config.DIST253BP1_MASK_NAME)


	def split(self):
		split_tif(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-raw.tif', 100)


	def rename(self):
		rename_01(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '.tif')


	def check_regi(self):

		print("######################################")
		print("Check regi parameters")
		print("######################################")

		# If no regi ref file, use raw file automatically
		ref_im = nonempty_openfile1_or_openfile2(self.config.OUTPUT_PATH,
					self.config.REF_FILE_NAME,
					self.config.ROOT_NAME+'-raw.tif')[list(self.config.TRANGE),:,:]

		im = imread(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif')


		for j in range(len(self.config.REF_IND_NUM)):
			for k in range(len(self.config.SIG_MASK)):
				for l in range(len(self.config.THRES_REL)):
					for m in range(len(self.config.POLY_DEG)):
						for n in range(len(self.config.ROTATION_MULTIPLIER)):
							for o in range(len(self.config.TRANSLATION_MULTIPLIER)):

								# Get regi parameters from ref file, save the regi params in csv file
								regi_params_array_2d = get_regi_params(ref_im,
								              ref_ind_num=self.config.REF_IND_NUM[j],
								              sig_mask=self.config.SIG_MASK[k],
								              thres_rel=self.config.THRES_REL[l],
								              poly_deg=self.config.POLY_DEG[m],
								              rotation_multplier=self.config.ROTATION_MULTIPLIER[n],
								              translation_multiplier=self.config.TRANSLATION_MULTIPLIER[o],
								              diagnostic=False)

								# Apply the regi params, save the registered file
								registered = apply_regi_params(im, regi_params_array_2d)

								imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-'
									+ str(self.config.REF_IND_NUM[j]) + '-'
									+ str(self.config.SIG_MASK[k]) + '-'
									+ str(self.config.THRES_REL[l]) + '-'
									+ str(self.config.POLY_DEG[m]) + '-'
									+ str(self.config.ROTATION_MULTIPLIER[n]) + '-'
									+ str(self.config.TRANSLATION_MULTIPLIER[o])
									+ '.tif', registered)
		return


	def regi(self):

		print("######################################")
		print("Registering Image Stack")
		print("######################################")

		# If no regi ref file, use raw file automatically
		ref_im = nonempty_openfile1_or_openfile2(self.config.OUTPUT_PATH,
					self.config.REF_FILE_NAME,
					self.config.ROOT_NAME+'-raw.tif')[list(self.config.TRANGE),:,:]

		im = imread(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif')

		# Get regi parameters from ref file, save the regi params in csv file
		regi_params_array_2d = get_regi_params(ref_im,
		              ref_ind_num=self.config.REF_IND_NUM,
		              sig_mask=self.config.SIG_MASK,
		              thres_rel=self.config.THRES_REL,
		              poly_deg=self.config.POLY_DEG,
		              rotation_multplier=self.config.ROTATION_MULTIPLIER,
		              translation_multiplier=self.config.TRANSLATION_MULTIPLIER,
		              diagnostic=False,
					  use_ransac=self.config.USE_RANSAC)
		regi_data = pd.DataFrame(regi_params_array_2d,
				columns=['x_center', 'y_center', 'angle', 'delta_x', 'delta_y' ])
		regi_data.to_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME +
		 				'-regiData.csv', index=False)

		# Apply the regi params, save the registered file
		registered = apply_regi_params(im, regi_params_array_2d)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-regi.tif', registered)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif', registered)


	def get_boundary_mask(self):
		# If no mask ref file, use raw file automatically
		frames = nonempty_openfile1_or_openfile2(self.config.OUTPUT_PATH,
					self.config.DIST2BOUNDARY_MASK_NAME,
					self.config.ROOT_NAME+'-raw.tif')[list(self.config.TRANGE),:,:]

		# If regi params csv file exsits, load it and do the registration.
		if osp.exists(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-regiData.csv'):
			regi_params_array_2d = pd.read_csv(self.config.OUTPUT_PATH +
			 				self.config.ROOT_NAME + '-regiData.csv').to_numpy()
			frames = apply_regi_params(frames, regi_params_array_2d)

		boundary_masks = get_thres_mask_batch(frames,
					self.config.MASK_SIG_BOUNDARY, self.config.MASK_THRES_BOUNDARY)

		return boundary_masks


	def get_53bp1_mask(self):
		# If no mask ref file, use raw file automatically
		frames = nonempty_openfile1_or_openfile2(self.config.OUTPUT_PATH,
					self.config.DIST253BP1_MASK_NAME,
					self.config.ROOT_NAME+'-raw.tif')[list(self.config.TRANGE),:,:]

		# If regi params csv file exsits, load it and do the registration.
		if osp.exists(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-regiData.csv'):
			regi_params_array_2d = pd.read_csv(self.config.OUTPUT_PATH +
							self.config.ROOT_NAME + '-regiData.csv').to_numpy()
			frames = apply_regi_params(frames, regi_params_array_2d)

		# Get mask file and save it using 255 and 0
		masks_53bp1 = get_thres_mask_batch(frames,
							self.config.MASK_SIG_53BP1, self.config.MASK_THRES_53BP1)

		return masks_53bp1


	def get_53bp1_blob_mask(self):
		# If no mask ref file, use raw file automatically
		frames = nonempty_openfile1_or_openfile2(self.config.OUTPUT_PATH,
					self.config.MASK_53BP1_BLOB_NAME,
					self.config.ROOT_NAME+'-raw.tif')[list(self.config.TRANGE),:,:]

		# If regi params csv file exsits, load it and do the registration.
		if osp.exists(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-regiData.csv'):
			regi_params_array_2d = pd.read_csv(self.config.OUTPUT_PATH +
							self.config.ROOT_NAME + '-regiData.csv').to_numpy()
			frames = apply_regi_params(frames, regi_params_array_2d)

		# Get mask file and save it using 255 and 0
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-tempFile.tif',
				frames)
		pims_frames = pims.open(self.config.OUTPUT_PATH + self.config.ROOT_NAME +
								'-tempFile.tif')
		os.remove(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-tempFile.tif')

		blobs_df, det_plt_array = detect_blobs_batch(pims_frames,
									min_sig=self.config.MASK_53BP1_BLOB_MINSIG,
									max_sig=self.config.MASK_53BP1_BLOB_MAXSIG,
									num_sig=self.config.MASK_53BP1_BLOB_NUMSIG,
									blob_thres=self.config.MASK_53BP1_BLOB_THRES,
									peak_thres_rel=self.config.MASK_53BP1_BLOB_PKTHRES_REL,
									r_to_sigraw=1.4,
									pixel_size=self.config.PIXEL_SIZE,
									diagnostic=False,
									pltshow=False,
									plot_r=False,
									truth_df=None)

		masks_53bp1_blob = blobs_df_to_mask(frames, blobs_df)

		return masks_53bp1_blob


	def mask_boundary(self):
		print("######################################")
		print("Generate mask_boundary")
		print("######################################")
		boundary_masks = self.get_boundary_mask()

		# Save it using 255 and 0
		boundary_masks = np.rint(boundary_masks / \
							boundary_masks.max() * 255).astype(np.uint8)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-boundaryMask.tif',
				boundary_masks)


	def mask_53bp1(self):
		print("######################################")
		print("Generate mask_53bp1")
		print("######################################")
		masks_53bp1 = self.get_53bp1_mask()

		# Save it using 255 and 0
		masks_53bp1 = np.rint(masks_53bp1 / \
							masks_53bp1.max() * 255).astype(np.uint8)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-53bp1Mask.tif',
				masks_53bp1)


	def mask_53bp1_blob(self):
		print("######################################")
		print("Generate mask_53bp1_blob")
		print("######################################")

		masks_53bp1_blob = self.get_53bp1_blob_mask()

		# Save it using 255 and 0
		masks_53bp1_blob = np.rint(masks_53bp1_blob / \
							masks_53bp1_blob.max() * 255).astype(np.uint8)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-53bp1BlobMask.tif',
				masks_53bp1_blob)


	def segmentation(self, method):

		print("######################################")
		print("Segmenting Image Stack")
		print("######################################")

		frames = imread(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif')
		mask, centroid = get_mask_batch(frames, method, min_size=self.config.MIN_SIZE,show_mask=self.config.PLTSHOW)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-mask.tif', mask)

		return centroid


	def deno_gaus(self):

		print("######################################")
		print('Applying Gaussian Filter')
		print("######################################")

		frames = imread(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif')
		frames = frames / frames.max()
		frames = img_as_ubyte(frames)
		filtered = filter_batch(frames, method='gaussian', arg=self.config.GAUS_BLUR_SIG)

		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif', filtered)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-deno.tif', filtered)


	def deno_box(self):

		print("######################################")
		print('Applying Boxcar Filter')
		print("######################################")

		frames = imread(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif')
		frames = frames / frames.max()
		frames = img_as_ubyte(frames)
		filtered = filter_batch(frames, method='boxcar', arg=self.config.BOXCAR_RADIUS)

		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif', filtered)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-deno.tif', filtered)


	def check_detect_fit(self):

		print("######################################")
		print("Check detection and fitting")
		print("######################################")

		frames = file1_exists_or_pimsopen_file2(self.config.OUTPUT_PATH + self.config.ROOT_NAME,
									'-regi.tif', '-raw.tif')

		frames_deno = pims.open(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif')

		blobs_df, det_plt_array = detect_blobs(frames[0],
									min_sig=self.config.MIN_SIGMA,
									max_sig=self.config.MAX_SIGMA,
									num_sig=self.config.NUM_SIGMA,
									blob_thres=self.config.THRESHOLD,
									peak_thres_rel=self.config.PEAK_THRESH_REL,
									r_to_sigraw=1,
									pixel_size=self.config.PIXEL_SIZE,
									diagnostic=True,
									pltshow=True,
									plot_r=False,
									truth_df=None)

		psf_df, fit_plt_array = fit_psf(frames_deno[0],
		            blobs_df,
		            diagnostic=True,
		            pltshow=True,
		            diag_max_dist_err=self.config.FILTERS['MAX_DIST_ERROR'],
		            diag_max_sig_to_sigraw = self.config.FILTERS['SIG_TO_SIGRAW'],
		            truth_df=None,
		            segm_df=blobs_df)


	def detect_fit(self):

		print("######################################")
		print("Detect, Fit")
		print("######################################")

		frames = file1_exists_or_pimsopen_file2(self.config.OUTPUT_PATH + self.config.ROOT_NAME,
									'-regi.tif', '-raw.tif')

		frames_deno = pims.open(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-active.tif')

		blobs_df, det_plt_array = detect_blobs_batch(frames,
									min_sig=self.config.MIN_SIGMA,
									max_sig=self.config.MAX_SIGMA,
									num_sig=self.config.NUM_SIGMA,
									blob_thres=self.config.THRESHOLD,
									peak_thres_rel=self.config.PEAK_THRESH_REL,
									r_to_sigraw=1,
									pixel_size=self.config.PIXEL_SIZE,
									diagnostic=True,
									pltshow=False,
									plot_r=False,
									truth_df=None)
		imsave(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-detVideo.tif', det_plt_array)

		psf_df, fit_plt_array = fit_psf_batch(frames_deno,
		            blobs_df,
		            diagnostic=False,
		            pltshow=False,
		            diag_max_dist_err=self.config.FILTERS['MAX_DIST_ERROR'],
		            diag_max_sig_to_sigraw = self.config.FILTERS['SIG_TO_SIGRAW'],
		            truth_df=None,
		            segm_df=None)
		psf_df = psf_df.apply(pd.to_numeric)
		psf_df.round(6).to_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + \
						'-fittData.csv', index=False)


	def filt_track(self):

		print("######################################")
		print("Filter and Linking")
		print("######################################")

		frames = file1_exists_or_pimsopen_file2(self.config.OUTPUT_PATH + self.config.ROOT_NAME,
									'-regi.tif', '-raw.tif')

		psf_df = pd.read_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-fittData.csv')

		blobs_df, im = track_blobs(psf_df,
								    search_range=self.config.SEARCH_RANGE,
									memory=self.config.MEMORY,
									pixel_size=self.config.PIXEL_SIZE,
									frame_rate=self.config.FRAME_RATE,
									divide_num=self.config.DIVIDE_NUM,
									filters=None,
									do_filter=False)

		traj_num_before = blobs_df['particle'].nunique()

		if self.config.DO_FILTER:
			blobs_df, im = track_blobs(blobs_df,
									    search_range=self.config.SEARCH_RANGE,
										memory=self.config.MEMORY,
										pixel_size=self.config.PIXEL_SIZE,
										frame_rate=self.config.FRAME_RATE,
										divide_num=self.config.DIVIDE_NUM,
										filters=self.config.FILTERS,
										do_filter=True)

		# Add 'traj_length' column and save physData before traj_length_thres filter
		blobs_df = add_traj_length(blobs_df)
		blobs_df.round(6).to_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + \
									'-physData.csv', index=False)

		after_filter_df = blobs_df [blobs_df['traj_length'] > self.config.FILTERS['TRAJ_LEN_THRES']]
		print("######################################")
		print("Trajectory number before filters: \t%d" % traj_num_before)
		print("Trajectory number after filters: \t%d" % after_filter_df['particle'].nunique())
		print("######################################")


	def phys(self):

		print("######################################")
		print("Add Physics Parameters")
		print("######################################")
		blobs_df = pd.read_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-physData.csv')

		# add 'dist_to_boundary' column
		print("######################################")
		print("Add 'dist_to_boundary'")
		print("######################################")
		boundary_masks = self.get_boundary_mask()
		phys_df = add_dist_to_boundary_batch(blobs_df, boundary_masks)

		# add 'dist_to_53bp1' column
		print("######################################")
		print("Add 'dist_to_53bp1'")
		print("######################################")
		masks_53bp1 = self.get_53bp1_mask()
		phys_df = add_dist_to_53bp1_batch(blobs_df, masks_53bp1)

		# Save '-physData.csv'
		phys_df.round(6).to_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + \
						'-physData.csv', index=False)


	def phys_dist2boundary(self):
		print("######################################")
		print("Add Physics Param: dist_to_boundary")
		print("######################################")
		phys_df = pd.read_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-physData.csv')
		boundary_masks = self.get_boundary_mask()
		phys_df = add_dist_to_boundary_batch(phys_df, boundary_masks)
		phys_df.round(6).to_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + \
						'-physData.csv', index=False)


	def phys_dist253bp1(self):
		print("######################################")
		print("Add Physics Param: dist_to_53bp1")
		print("######################################")
		phys_df = pd.read_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-physData.csv')
		masks_53bp1 = self.get_53bp1_mask()
		phys_df = add_dist_to_53bp1_batch(phys_df, masks_53bp1)
		phys_df.round(6).to_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + \
						'-physData.csv', index=False)


	def phys_dist253bp1_blob(self):
		print("######################################")
		print("Add Physics Param: dist_to_53bp1_blob")
		print("######################################")
		phys_df = pd.read_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-physData.csv')
		masks_53bp1_blob = self.get_53bp1_blob_mask()
		phys_df = add_dist_to_53bp1_batch(phys_df, masks_53bp1_blob)
		phys_df.round(6).to_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + \
						'-physData.csv', index=False)


	def sort_plot(self):

		print("######################################")
		print("Sort and PlotMSD")
		print("######################################")

		frames = file1_exists_or_pimsopen_file2(self.config.OUTPUT_PATH + self.config.ROOT_NAME,
									'-regi.tif', '-raw.tif')

		phys_df = pd.read_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + '-physData.csv')

		if self.config.DO_SORT & \
			('dist_to_53bp1' in phys_df.columns) & \
			('dist_to_boundary' in phys_df):
			phys_df = sort_phys(phys_df, self.config.SORTERS)
			phys_df.round(6).to_csv(self.config.OUTPUT_PATH + self.config.ROOT_NAME + \
						'-physData.csv', index=False)
		else:
			sorter_list = get_sorter_list(phys_df)
			phys_df = phys_df.drop(columns=sorter_list[1:-1])

		# Apply traj_length_thres filter
		phys_df = phys_df[ phys_df['traj_length'] > self.config.FILTERS['TRAJ_LEN_THRES'] ]

		plot_msd_batch(phys_df,
					 image=frames[0],
					 output_path=self.config.OUTPUT_PATH,
					 root_name=self.config.ROOT_NAME,
					 pixel_size=self.config.PIXEL_SIZE,
					 frame_rate=self.config.FRAME_RATE,
					 divide_num=self.config.DIVIDE_NUM,
					 plot_without_sorter=False,
					 show_fig=False,
					 save_pdf=True,
					 open_pdf=False)

		self.config.DICT['Load existing analMeta'] = True
		self.config.save_config()

	def merge_plot(self):

		start_ind = self.config.ROOT_NAME.find('_')
		end_ind = self.config.ROOT_NAME.find('_', start_ind+1)
		today = str(date.today().strftime("%y%m%d"))
		merged_name = today + self.config.ROOT_NAME[start_ind:end_ind]

		print("######################################")
		print("Merge and PlotMSD")
		print("######################################")

		merged_files = np.array(sorted(glob.glob(self.config.OUTPUT_PATH + '/*physDataMerged.csv')))
		print(merged_files)

		if len(merged_files) > 1:
			print("######################################")
			print("Found multiple physDataMerged file!!!")
			print("######################################")
			return

		if len(merged_files) == 1:
			phys_df = pd.read_csv(merged_files[0])

		else:
			phys_files = np.array(sorted(glob.glob(self.config.OUTPUT_PATH + '/*physData.csv')))
			print(phys_files)

			if len(phys_files) > 1:
				phys_df = merge_physdfs(phys_files)
				phys_df = relabel_particles(phys_df)
			else:
				phys_df = pd.read_csv(phys_files[0])

			phys_df.round(6).to_csv(self.config.OUTPUT_PATH + merged_name + \
							'-physDataMerged.csv', index=False)

		# Apply traj_length_thres filter
		phys_df = phys_df[ phys_df['traj_length'] > self.config.FILTERS['TRAJ_LEN_THRES'] ]

		# phys_df = phys_df.loc[phys_df['exp_label'] == 'BLM']
		fig = plot_merged(phys_df, 'exp_label',
						pixel_size=self.config.PIXEL_SIZE,
						frame_rate=self.config.FRAME_RATE,
						divide_num=self.config.DIVIDE_NUM,
						RGBA_alpha=0.5,
						do_gmm=False)

		fig.savefig(self.config.OUTPUT_PATH + merged_name + '-mergedResults.pdf')


def get_root_name_list(settings_dict):
	# Make a copy of settings_dict
	# Use '*%#@)9_@*#@_@' to substitute if the labels are empty
	settings = settings_dict.copy()
	if settings['Regi reference file label'] == '':
		settings['Regi reference file label'] = '*%#@)9_@*#@_@'
	if settings['Mask boundary_mask file label'] == '':
		settings['Mask boundary_mask file label'] = '*%#@)9_@*#@_@'
	if settings['Mask 53bp1_mask file label'] == '':
		settings['Mask 53bp1_mask file label'] = '*%#@)9_@*#@_@'

	root_name_list = []

	path_list = glob.glob(settings['IO input_path'] + '/*-raw.tif')
	if len(path_list) != 0:
		for path in path_list:
			temp = path.split('/')[-1]
			temp = temp[:temp.index('.') - len('-raw')]
			root_name_list.append(temp)
	else:
		path_list = glob.glob(settings['IO input_path'] + '/*.tif')
		for path in path_list:
			temp = path.split('/')[-1]
			temp = temp[:temp.index('.')]
			if (settings['Mask boundary_mask file label'] not in temp+'.tif') & \
				(settings['Mask 53bp1_mask file label'] not in temp+'.tif') & \
				(settings['Regi reference file label'] not in temp+'.tif'):
				root_name_list.append(temp)

	return np.array(sorted(root_name_list))


def analMeta_to_dict(analMeta_path):
	df = pd.read_csv(analMeta_path, header=None, index_col=0, na_filter=False)
	df = df.rename(columns={1:'value'})
	srs = df['value']

	dict = {}
	for key in srs.index:
		try: dict[key] = ast.literal_eval(srs[key])
		except: dict[key] = srs[key]
	return dict


def pipeline_batch(settings_dict, control_list):

	# """
	# ~~~~~~~~~~~~~~~~~1. Get root_name_list~~~~~~~~~~~~~~~~~
	# """
	root_name_list = get_root_name_list(settings_dict)

	print("######################################")
	print("Data to be processed")
	print("######################################")
	print(root_name_list)

	for root_name in root_name_list:

		print("Processing: %s" % root_name)

		# """
		# ~~~~~~~~~~~~~~~~~2. Update config~~~~~~~~~~~~~~~~~
		# """

		config = Config(settings_dict)

		# 2.0. If LOAD_ANALMETA==True, then load existing analMeta file, if there is one
		if config.DICT['Load existing analMeta'] & \
		osp.exists(settings_dict['IO input_path'] + root_name + '-analMeta.csv'):
			existing_settings = analMeta_to_dict(settings_dict['IO input_path'] + root_name + '-analMeta.csv')
			existing_settings['IO input_path']= settings_dict['IO input_path']
			existing_settings['IO output_path'] = settings_dict['IO output_path']
			existing_settings['Processed By:'] = settings_dict['Processed By:']
			existing_settings.pop('Processed by:', None)
			settings_dict = existing_settings
			config = Config(settings_dict)

		# 2.1. Update config.ROOT_NAME and config.DICT
		config.ROOT_NAME = root_name
		config.DICT['Raw data file'] = root_name + '.tif'
		config.DICT['Processed date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		config.DICT['Processed by:'] = settings_dict['Processed By:']

		# 2.2. Update config.REF_FILE_NAME
		if '-' in root_name and root_name.find('-')>0:
			key = root_name[0:root_name.find('-')]

		if settings_dict['Regi reference file label']:# if label is not empty, find file_list
			file_list = np.array(sorted(glob.glob(settings_dict['IO input_path'] + '*' + key +
					'*' + settings_dict['Regi reference file label'] + '*')))
			if len(file_list) == 1: # there should be only 1 file targeted
				config.REF_FILE_NAME = file_list[0].split('/')[-1]
			else:
				config.DICT['Regi reference file label'] = ''

		# 2.3. Update config.DIST2BOUNDARY_MASK_NAME
		if settings_dict['Mask boundary_mask file label']:# if label is not empty, find file_list
			file_list = np.array(sorted(glob.glob(settings_dict['IO input_path'] + '*' + key +
					'*' + settings_dict['Mask boundary_mask file label'] + '*')))
			if len(file_list) == 1: # there should be only 1 file targeted
				config.DIST2BOUNDARY_MASK_NAME = file_list[0].split('/')[-1]
			else:
				config.DICT['Mask boundary_mask file label'] = ''

		# 2.4. Update config.DIST253BP1_MASK_NAME
		if settings_dict['Mask 53bp1_mask file label']:# if label is not empty, find file_list
			file_list = np.array(sorted(glob.glob(settings_dict['IO input_path'] + '*' + key +
					'*' + settings_dict['Mask 53bp1_mask file label'] + '*')))
			if len(file_list) == 1: # there should be only 1 file targeted
				config.DIST253BP1_MASK_NAME = file_list[0].split('/')[-1]
			else:
				config.DICT['Mask 53bp1_mask file label'] = ''

		# 2.5. Update config.MASK_53BP1_BLOB_NAME
		if settings_dict['Mask 53bp1_blob_mask file label']:# if label is not empty, find file_list
			file_list = np.array(sorted(glob.glob(settings_dict['IO input_path'] + '*' + key +
					'*' + settings_dict['Mask 53bp1_blob_mask file label'] + '*')))
			if len(file_list) == 1: # there should be only 1 file targeted
				config.MASK_53BP1_BLOB_NAME = file_list[0].split('/')[-1]
			else:
				config.DICT['Mask 53bp1_blob_mask file label'] = ''

		# """
		# ~~~~~~~~~~~~~~~~~3. Setup pipe and run~~~~~~~~~~~~~~~~~
		# """
		pipe = Pipeline2(config)
		for func in control_list:
			getattr(pipe, func)()