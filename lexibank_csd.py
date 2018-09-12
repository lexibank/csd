# coding=utf-8
from __future__ import unicode_literals, print_function

from clldutils.path import Path
from csvw.dsv import reader
from pylexibank.providers import clld
from pylexibank.dataset import Metadata


class Dataset(clld.CLLD):
    __cldf_url__ = "http://cdstar.shh.mpg.de/bitstreams/EAEA0-4C22-790A-0FFC-0/csd_dataset.cldf.zip"
    dir = Path(__file__).parent
    id = "csd"

    def iteritems(self):
        for p in sorted(self.raw.glob('*.csv'), key=lambda p: int(p.stem.split('-')[-1])):
            for item in reader(p, dicts=True):
                yield item

    def cmd_install(self, **kw):
        concept_map = {cs.gloss: cs.id for cs in self.concepticon.conceptsets.values()}
        for concept in self.concepts:
            concept_map[concept['GLOSS']] = concept['CONCEPTICON_ID']

        with self.cldf as ds:
            ds.add_languages(id_factory=lambda l: l['ID'])
            for row in self.iteritems():
                #for ref in row.refs:
                #    ds.add_sources(ref.source)
                if row['Parameter_name'].upper() not in concept_map:
                    self.unmapped.add_concept(
                        ID=row['Parameter_ID'], Name=row['Parameter_name'])
                
                ds.add_concept(
                    ID=row['Parameter_ID'],
                    Name=row['Parameter_name'],
                    Concepticon_ID=concept_map.get(row['Parameter_name'].upper()))
                ds.add_lexemes(
                    Language_ID=row['Language_ID'],
                    Parameter_ID=row['Parameter_ID'],
                    Value=row['Value'],
                    Source=row['Source'],
                    Comment=row['Comment'])
