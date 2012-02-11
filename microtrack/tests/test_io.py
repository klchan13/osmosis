import os

import numpy as np
import numpy.testing as npt
import scipy.io as sio 

import microtrack.io as mio
import microtrack.fibers as mtf
import microtrack as mt


def test_fg_from_pdb():
    """
    Test initialization of the FiberGroup from pdb file

    Benchmark was generated using vistasoft in Matlab as follows:

    >> fg = mtrImportFibers('FG_w_stats.pdb')
    
    """
    data_path = os.path.split(mt.__file__)[0] + '/data/'
    file_name = data_path + "FG_w_stats.pdb"
    fg = mio.fg_from_pdb(file_name)
    # Get the same fiber group as saved in matlab:
    mat_fg = sio.loadmat(data_path + "fg_from_matlab.mat",
                         squeeze_me=True)["fg"]
    k = [d[0] for d in mat_fg.dtype.descr]
    v = mat_fg.item()
    mat_fg_dict = dict(zip(k,v))
    npt.assert_equal(fg.name, mat_fg_dict["name"])
    npt.assert_equal(fg.fibers[0].coords, mat_fg_dict["fibers"][0])
    npt.assert_equal(fg.fiber_stats["eccentricity"],
                     mat_fg_dict["params"][0].item()[-1])
    

def test_pdb_from_fg():
    """
    Test writing a fiber-group to file
    """

    coords1 = np.arange(900).reshape(3,300)
    coords2 = np.arange(900).reshape(3,300) + 100

    fiber_stats = dict(foo=1,bar=2)
    node_stats = dict(ecc=np.random.rand(coords1.shape[-1]))
    
    
    fg = mtf.FiberGroup([mtf.Fiber(coords1,
                                   fiber_stats=fiber_stats,
                                   node_stats=node_stats),
                         mtf.Fiber(coords2,
                                   fiber_stats=fiber_stats,
                                   node_stats=node_stats)])

    
    mio.pdb_from_fg(fg, '/tmp/fg.pdb')
