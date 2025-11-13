from pylamost import lamost
import io
import pandas as pd


def test_conesearch(lm, ismed=False):
    print(f"Testing {lm.dr_version} {lm.sub_version} ismed={ismed}")
    csv = lm.conesearch(ra=10.0004738,dec=40.9952444,radius=0.2, ismed=ismed, fmt='csv')
    print(csv[:100])
    try:
        df = pd.read_csv(io.StringIO(csv))
        print(df.head())
    except Exception as e:
        print(e)

is_dev = False

if False:
    lm = lamost(dr_version='dr1', sub_version='v2.0', is_dev=is_dev)
    drvs = lm.get_dr_versions()

    for dv in drvs['versions']:
        lm = lamost(dr_version=dv['dr_version'], sub_version=dv['sub_version'], is_dev=is_dev)
        print(f"Testing {lm.dr_version} {lm.sub_version}")
        test_conesearch(lm, ismed=False)
        if dv['has_mrs'] == 1:
            test_conesearch(lm, ismed=True)   
else:
    # lm_dr1 = lamost(dr_version='dr1', sub_version='', is_dev=is_dev)
    # test_conesearch(lm_dr1, ismed=False)

    lm_dr6 = lamost(dr_version='dr6', sub_version='v2', is_dev=is_dev)
    test_conesearch(lm_dr6, ismed=False)
    test_conesearch(lm_dr6, ismed=True)

    # lm_dr11 = lamost(dr_version='dr11', sub_version='v1.0', is_dev=is_dev)
    # test_conesearch(lm_dr11, ismed=False)
    # test_conesearch(lm_dr11, ismed=True)

    # lm_dr12 = lamost(dr_version='dr12', sub_version='v1.1', is_dev=is_dev)
    # test_conesearch(lm_dr12, ismed=False)
    # test_conesearch(lm_dr12, ismed=True)
