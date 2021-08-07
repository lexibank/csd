import pathlib

from csvw.dsv import reader
from pylexibank import Dataset as Base


class Dataset(Base):
    #__cldf_url__ = "http://cdstar.shh.mpg.de/bitstreams/EAEA0-4C22-790A-0FFC-0/csd_dataset.cldf.zip"
    dir = pathlib.Path(__file__).parent
    id = "csd"

    def cmd_makecldf(self, args):
        raise NotImplementedError()
