
# Lines above this one are auto-generated by the wrapper to provide as params:
# i
import time
import osmosis.multi_bvals as sfm_mb
import osmosis.model.dti as dti
import osmosis.predict_n as pn
from osmosis.utils import separate_bvals
import nibabel as nib
import os
import numpy as np

if __name__=="__main__":
    t1 = time.time()
    data_path = "/biac4/wandell/data/klchan13/100307/Diffusion/data"
    
    data_file = nib.load(os.path.join(data_path, "data.nii.gz"))
    wm_data_file = nib.load(os.path.join(data_path,"wm_mask_registered.nii.gz"))
    
    data = data_file.get_data()
    wm_data = wm_data_file.get_data()
    wm_idx = np.where(wm_data==1)
    
    bvals = np.loadtxt(os.path.join(data_path, "bvals"))
    bvecs = np.loadtxt(os.path.join(data_path, "bvecs"))
    
    low = i*65
    # Make sure not to go over the edge of the mask:
    high = np.min([(i+1) * 65, int(np.sum(wm_data))])

    # Now set the mask:
    mask = np.zeros(wm_data_file.shape)
    mask[wm_idx[0][low:high], wm_idx[1][low:high], wm_idx[2][low:high]] = 1

    # Predict 10% (n = 10)
    ad = {1000:1.6386920952169737, 2000:1.2919249903637751, 3000:0.99962593218241236}
    rd = {1000:0.33450124887561905, 2000:0.28377379537043729, 3000:0.24611723207420028}
    
    actual_pn_all, predicted_pn_all = pn.predict_n(data, bvals, bvecs,
                                                   mask, ad, rd, 10, "all",
                                                   solver = "nnls")
    actual_pn_bvals, predicted_pn_bvals = pn.predict_n(data, bvals, bvecs,
                                                       mask, ad, rd, 10, "bvals",
                                                       mean = "mean_model", solver = "nnls")
    #actual_pn_grid, predicted_pn_grid = pn.predict_grid(data, bvals, bvecs,
    #                                                   mask, ad, rd, 10,
    #
    #                                                   solver = "nnls")
    aff = np.eye(4)
    nib.Nifti1Image(predicted_pn_all, aff).to_filename("/hsgs/nobackup/klchan13/all_predict%s.nii.gz"%(i))
    nib.Nifti1Image(predicted_pn_bvals, aff).to_filename("/hsgs/nobackup/klchan13/bvals_predict%s.nii.gz"%(i))
    #nib.Nifti1Image(predicted_pn_grid, aff).to_filename("/hsgs/nobackup/klchan13/grid_predict%s.nii.gz"%(i))
    #actual_all, predict_all = pn.predict_n(data, bvals, bvecs,
                                           #mask, ad, rd, 10,"all")
    #actual_bvals, predict_bvals = pn.predict_n(data, bvals, bvecs,
                                               #mask, ad, rd, 10, "bvals")
                                               
    ## Predict tensor
    #bval_list, b_inds, unique_b, rounded_bvals = separate_bvals(bvals)
    #inds = np.concatenate((b_inds[0], b_inds[1:][0]))
    #actual_tensor, predict_tensor = pn.kfold_xval(dti.TensorModel, data[:,:,:,inds],
                                                  #bvecs[:,inds], bvals[inds], 9,
                                                  #mask)
   
    #aff = np.eye(4)
    #nib.Nifti1Image(actual_all, aff).to_filename("/hsgs/nobackup/klchan13/actual%s.nii.gz"%(i))
    #nib.Nifti1Image(predict_all, aff).to_filename("/hsgs/nobackup/klchan13/all_predict%s.nii.gz"%(i)) 
    #nib.Nifti1Image(predict_bvals, aff).to_filename("/hsgs/nobackup/klchan13/bvals_predict%s.nii.gz"%(i))
    #nib.Nifti1Image(predict_tensor, aff).to_filename("/hsgs/nobackup/klchan13/tensor_predict%s.nii.gz"%(i))
    t2 = time.time()
    print "This program took %4.2f minutes to run."%((t2 - t1)/60.)
