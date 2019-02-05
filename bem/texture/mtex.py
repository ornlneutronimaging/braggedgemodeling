import os, shutil, numpy as np
here = os.path.dirname(__file__)
import matlab.engine, matlab

startup_m = 'startup.m'
odf2vpsc_m = 'odf2VPSC.m'
polfig2vpsc_m = 'polfig2VPSC.m'
startup_modules = [startup_m, odf2vpsc_m, polfig2vpsc_m]
def setup(mtex_path="/HFIR/CG1D/shared/mtex/mtex-4.5.2"):
    # assume the current directory is the working dir
    if not os.path.exists(startup_m):
        _createStartupM(startup_m, mtex_path)
    #
    if not os.path.exists(odf2vpsc_m):
        shutil.copyfile(os.path.join(here, odf2vpsc_m), odf2vpsc_m)
    #
    if not os.path.exists(polfig2vpsc_m):
        shutil.copyfile(os.path.join(here, polfig2vpsc_m), polfig2vpsc_m)
    return

def check_setup():
    for m in startup_modules:
        if not os.path.exists(m):
            raise RuntimeError("Missing %s. Run `setup` first" % m)


def _createStartupM(path, mtex_path):
    content = "addpath('%s')\nstartup_mtex\n" % mtex_path
    open(path, 'wt').write(content)
    return


_ml_engine = None
def mlEngine():
    global _ml_engine
    if _ml_engine is None:
        _ml_engine = matlab.engine.start_matlab()
    return _ml_engine


def polfig2VPSC(rpfpath, outpath, hkls, Npoints=5000):
    """calling mtex to convert pol figure data to texture data.

    rpfpath: pol figure data path
    outpath: output path
    hkls: miller indexes of the pole figures
    Npoints: number of sampling points

    !!! This implemenation is limited. Should autodetect the hkl (miller indexes) stored in the file (rpfpath) !!!
    """
    check_setup()
    engine = mlEngine()
    import StringIO
    out = StringIO.StringIO()
    err = StringIO.StringIO()

    ml_hkls = matlab.double(hkls)
    engine.polfig2VPSC(rpfpath, ml_hkls, outpath, Npoints, nargout=0, stdout=out, stderr=err)
    if not os.path.exists(outpath):
        raise RuntimeError("polfig2VPSC failed. \nOutput: %s\nError: %s" % (out.getvalue(), err.getvalue()))
    return
