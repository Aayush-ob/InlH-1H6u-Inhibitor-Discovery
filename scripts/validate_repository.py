"""Validate the current InlH research deposit with the Python standard library."""
from pathlib import Path
import json,hashlib,re,math
from urllib.parse import unquote,urlsplit
from inspect_data import inspect_repository
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def check(ok,message):
    if not ok:errors.append(message)
try:data=inspect_repository()
except Exception as exc:raise SystemExit('Numeric source validation failed: '+str(exc))
expected={'control':-10.88,'hederagenin':-17.09,'lupeol':-10.75,'maslinic_acid':-9.65}
check(len(data['mmgbsa'])==4,'Expected four endpoint files')
for row in data['mmgbsa']:
    check(math.isclose(row['mean_kcal_mol'],expected[row['system']],abs_tol=1e-6),row['system']+': endpoint mismatch')
    check(row['frames']==501,row['system']+': expected 501 complex frames')
check(len(data['series'])==36,'Expected 36 numeric trajectory series')
check(len(data['grids'])==8,'Expected eight saved XPM grids')
check(len(data['orbitals'])==4,'Expected four orbital summaries')
comparison=json.loads((ROOT/'data/PUBLISHED_SOURCE_COMPARISON.json').read_text(encoding='utf8'))
observed={r['system']:r['mean_kcal_mol'] for r in data['mmgbsa']}
for row in comparison['systems']:
    check(row['retained_output_kcal_mol']==observed[row['system']],row['system']+': discrepancy record does not match source')
known=[row for row in comparison['systems'] if row['published_narrative_kcal_mol']!=row['retained_output_kcal_mol']]
check(len(known)==1 and known[0]['system']=='lupeol','Expected the explicitly documented Lupeol discrepancy')
manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf8'))
for entry in manifest:
    p=ROOT/entry['path'];check(p.is_file(),entry['path']+': missing')
    if p.is_file():check(hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],entry['path']+': checksum mismatch')
for entry in json.loads((ROOT/'data/provenance.json').read_text(encoding='utf8')):
    p=ROOT/entry['retained_path'];check(hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],entry['retained_path']+': changed scientific source')
links=0
for p in ROOT.rglob('*.md'):
    if '.git' in p.parts:continue
    for target in re.findall(r'\]\(([^\n)]+)\)',p.read_text(encoding='utf8')):
        if target.startswith(('#','http:','https:','mailto:')):continue
        rel=unquote(urlsplit(target.strip('<>')).path)
        if rel:links+=1;check((p.parent/rel).exists(),str(p.relative_to(ROOT))+': broken link '+target)
for p in (ROOT/'notebooks').glob('*.ipynb'):
    nb=json.loads(p.read_text(encoding='utf8'))
    check(all(not c.get('outputs') and c.get('execution_count') is None for c in nb['cells'] if c['cell_type']=='code'),p.name+': notebook execution output retained')
for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts:continue
    check(p.suffix.lower() not in ['.xtc','.trr','.tpr','.edr','.gbw','.densities','.tmp'],str(p.relative_to(ROOT))+': excluded raw/cache file')
    check('reviewer' not in p.name.lower(),str(p.relative_to(ROOT))+': reviewer correspondence')
    check(not ('thesis' in p.name.lower() and p.suffix.lower() in ['.pdf','.doc','.docx']),str(p.relative_to(ROOT))+': thesis document')
print(json.dumps(dict(status='FAIL' if errors else 'PASS',scope='Integrity and data parsability; known published/source mismatch remains disclosed',endpoint_files=len(data['mmgbsa']),numeric_series=len(data['series']),xpm_grids=len(data['grids']),orbital_summaries=len(data['orbitals']),manifest_files=len(manifest),local_links=links,known_published_source_discrepancies=known,errors=errors),indent=2))
raise SystemExit(bool(errors))
