# coding=utf-8
from __future__ import unicode_literals, print_function

from pylexibank.providers import clld
from pylexibank.dataset import Metadata


class Dataset(clld.CLLD):
    __cldf_url__ = "http://cdstar.shh.mpg.de/bitstreams/EAEA0-4C22-790A-0FFC-0/csd_dataset.cldf.zip"
    dir = Path(__file__).parent

    def cmd_install(self, **kw):
        concept_map = {cs.gloss: cs.id for cs in self.concepticon.conceptsets.values()}
        for concept in self.concepts:
            concept_map[concept['GLOSS']] = concept['CONCEPTICON_ID']
        language_map = {l['ID']: l['GLOTTOCODE'] or None for l in self.languages}

        with self.cldf as ds:
            for row in self.iteritems():
                if not row['Language_glottocode']:
                    if row['Language_ID'] in language_map:
                        row['Language_glottocode'] = language_map[row['Language_ID']]
                    else:
                        self.unmapped.add_language(
                            id=row['Language_ID'],
                            name=row['Language_name'],
                            iso=row['Language_iso'])
                #for ref in row.refs:
                #    ds.add_sources(ref.source)
                if row['Parameter_name'].upper() not in concept_map:
                    self.unmapped.add_concept(
                        id=row['Parameter_ID'], gloss=row['Parameter_name'])
                ds.add_language(
                    ID=row['Language_ID'],
                    name=row['Language_name'],
                    iso=row['Language_iso'],
                    glottocode=row['Language_glottocode'])
                ds.add_concept(
                    ID=row['Parameter_ID'],
                    gloss=row['Parameter_name'],
                    conceptset=concept_map.get(row['Parameter_name'].upper()))
                ds.add_lexemes(
                    Language_ID=row['Language_ID'],
                    Parameter_ID=row['Parameter_ID'],
                    Value=row['Value'],
                    Source=row['Source'],
                    Comment=row['Comment'])
