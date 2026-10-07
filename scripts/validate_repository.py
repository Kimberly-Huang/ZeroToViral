"""Validate the preserved evidence and the contracts used by the retrospective."""
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import zipfile
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]

def table(name):
    return list(csv.DictReader((ROOT/'results/tables'/f'{name}.csv').open()))

def main():
    import nbformat
    manifest=json.loads((ROOT/'results/run_manifest.json').read_text())
    assert hashlib.sha256((ROOT/'scripts/analyze.py').read_bytes()).hexdigest()==manifest['analysis_source_sha256']
    for name,digest in manifest['data_sha256'].items():
        assert hashlib.sha256((ROOT/'data'/name).read_bytes()).hexdigest()==digest,name
    sources=list(csv.DictReader((ROOT/'archive/source-manifest.csv').open()))
    assert len(sources)==19
    for row in sources:
        assert hashlib.sha256((ROOT/row['repository_path']).read_bytes()).hexdigest()==row['sha256_published'],row['source']
        if row['action']!='Credential redacted':assert row['sha256_source']==row['sha256_published']
    audit={r['dataset']:r for r in table('data_audit')}
    assert {k:int(v['rows']) for k,v in audit.items()}==dict(raw_collection=1108,micro_snapshot=1090,large_snapshot=1177,micro_analysis=1035,large_analysis=1174)
    assert [int(r['rows']) for r in table('cohort_flow')]==[1090,1061,1060,1035]
    assert sum(int(r['videos']) for r in table('cluster_profiles_corrected'))==2209
    sentiments={r['like_rate_group']:r for r in table('sentiment')}
    assert all(int(r['videos'])==545 for r in sentiments.values())
    assert abs(float(sentiments['High']['mean_compound'])-.419)<.001
    assert abs(float(sentiments['Low']['mean_compound'])-.327)<.001
    for g in ['High','Low']:
        assert math.isclose(sum(float(r['share']) for r in table('topic_distributions') if r['group']==g),1,abs_tol=1e-8)
    q={r['quadrant']:int(r['videos']) for r in table('tag_quadrants')}
    assert q=={'Golden':226,'Exposure Trap':292,'Niche':292,'Ineffective':225}
    for cohort,total in [('micro',1035),('large',1174)]:
        assert sum(int(r['videos']) for r in table('hashtag_quantity') if r['cohort']==cohort)==total
    pearson=next(r for r in table('hashtag_correlations') if r['count_definition']=='hashtag_count' and r['method']=='pearson')
    assert abs(float(pearson['r'])-(-.02339913835))<1e-8
    for row in table('golden_windows'):
        assert -1<=float(row['golden_score'])<=1
        assert int(row['micro_videos'])>=1
        assert math.isclose(float(row['golden_score']),float(row['micro_rank'])-float(row['large_density_rank']),abs_tol=1e-8)
    assert sum(int(r['micro_videos']) for r in table('golden_windows'))==1035
    for row in table('golden_windows_min5'):assert int(row['micro_videos'])>=5
    notebooks=list((ROOT/'notebooks').glob('*.ipynb'));assert len(notebooks)==6
    for path in notebooks:
        nb=nbformat.read(path,as_version=4);nbformat.validate(nb)
        for cell in nb.cells:
            if cell.cell_type=='code':compile(cell.source,str(path),'exec')
    # Content scan reports file locations only; never prints potential credentials.
    credential=re.compile(rb'AIza[0-9A-Za-z_-]{35}|ghp_[A-Za-z0-9]{30,}')
    for folder in ['archive','reports','notebooks','scripts','docs','data']:
        for path in (ROOT/folder).rglob('*'):
            if not path.is_file() or '__pycache__' in path.parts:continue
            if path.suffix in ['.docx','.pptx']:
                with zipfile.ZipFile(path) as z:
                    assert all(not credential.search(z.read(n)) for n in z.namelist() if n.endswith('.xml')),path
            else:assert not credential.search(path.read_bytes()),path
    for path in [ROOT/'README.md',*list((ROOT/'docs').glob('*.md')),ROOT/'archive/README.md',ROOT/'results/README.md']:
        text=path.read_text()
        for target in re.findall(r'\]\(([^)]+)\)',text):
            target=target.split('#')[0]
            if not target or '://' in target or target.startswith('mailto:'):continue
            assert (path.parent/unquote(target)).exists(),(str(path),target)
    print('PASS: 19 source artifacts, preserved input hashes, cohort flow, NLP checks, tag totals, timing arithmetic, six notebooks, credential scan and documentation links.')

if __name__=='__main__':main()
