import pathlib

from csvw.dsv import reader
from pylexibank.providers import clld


class Dataset(clld.CLLD):
    __cldf_url__ = "http://cdstar.shh.mpg.de/bitstreams/EAEA0-4C22-790A-0FFC-0/csd_dataset.cldf.zip"
    dir = pathlib.Path(__file__).parent
    id = "csd"

    def iteritems(self):
        for p in sorted(self.raw_dir.glob('*.csv'), key=lambda p: int(p.stem.split('-')[-1])):
            for item in reader(p, dicts=True):
                yield item

    def cmd_makecldf(self, args):
        concept_map = {cs.gloss: cs.id for cs in self.concepticon.conceptsets.values()}
        for concept in self.concepts:
            concept_map[concept['GLOSS']] = concept['CONCEPTICON_ID']

        for bib in sorted(self.raw_dir.glob('*.bib'), key=lambda p: int(p.stem.split('-')[-1])):
            args.writer.add_sources(*self.raw_dir.read_bib(bib.name))
        args.writer.add_languages(id_factory=lambda l: l['ID'])
        for row in self.iteritems():
            #for ref in row.refs:
            #    ds.add_sources(ref.source)
            if row['Parameter_name'].upper() not in concept_map:
                self.unmapped.add_concept(
                    ID=row['Parameter_ID'], Name=row['Parameter_name'])

            args.writer.add_concept(
                ID=row['Parameter_ID'],
                Name=row['Parameter_name'],
                Concepticon_ID=concept_map.get(row['Parameter_name'].upper()))
            args.writer.add_lexemes(
                Language_ID=row['Language_ID'],
                Parameter_ID=row['Parameter_ID'],
                Value=row['Value'],
                Source=row['Source'],
                Comment=row['Comment'])
