"""Inspect retained numerical files without rerunning any scientific calculation."""
from pathlib import Path
import argparse,json,re,math

ROOT=Path(__file__).resolve().parents[1]
NUMBER=r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[Ee][-+]?\d+)?'

def inspect_repository(root=ROOT):
    result={'series':[],'grids':[],'mmgbsa':[],'orbitals':[]}
    for p in sorted((root/'data/md').rglob('*')):
        if p.suffix.lower() in ['.xvg','.agr']:
            rows=[]
            for line in p.read_text(encoding='utf8',errors='strict').splitlines():
                s=line.strip()
                if not s or s.startswith(('#','@','&')):continue
                values=[float(x) for x in s.split()]
                assert len(values)>=2 and all(math.isfinite(x) for x in values),str(p)
                rows.append(values)
            assert rows and len({len(row) for row in rows})==1,str(p)
            result['series'].append(dict(file=p.relative_to(root).as_posix(),rows=len(rows),columns=len(rows[0]),first_coordinate=rows[0][0],last_coordinate=rows[-1][0]))
        elif p.suffix=='.xpm':
            lines=p.read_text(encoding='utf8').splitlines()
            pos=next(i for i,s in enumerate(lines) if re.match(r'^"\d+\s+\d+\s+\d+\s+\d+"',s))
            width,height,colors,cpp=map(int,re.findall(r'\d+',lines[pos]))
            rows=[m[1] for s in lines[pos+1+colors:] if (m:=re.match(r'^"([^\"]*)"',s)) and len(m[1])==width*cpp]
            assert len(rows)==height,f'{p}: grid rows {len(rows)} != {height}'
            label=next((s for s in lines if '/* legend:' in s),'')
            result['grids'].append(dict(file=p.relative_to(root).as_posix(),width=width,height=height,legend=label))
    for p in sorted((root/'data/mmgbsa').glob('*/FINAL_RESULTS_MMPBSA.dat')):
        text=p.read_text(encoding='utf8');delta=text.split('Delta (Complex - Receptor - Ligand):')[-1]
        components={}
        for line in delta.splitlines():
            if line.startswith('Δ'):
                label,values=re.split(r'\s{2,}',line.strip(),maxsplit=1);components[label]=list(map(float,values.split()))
        assert 'ΔTOTAL' in components,str(p)
        frames=int(re.search(r'Calculations performed using (\d+) complex frames',text)[1])
        result['mmgbsa'].append(dict(system=p.parent.name,file=p.relative_to(root).as_posix(),frames=frames,mean_kcal_mol=components['ΔTOTAL'][0],propagated_sd=components['ΔTOTAL'][1],sample_sd=components['ΔTOTAL'][2],components=components))
    for p in sorted((root/'data/dft').glob('*/frontier_orbital_energies.txt')):
        text=p.read_text(encoding='utf8');values={}
        for line in text.splitlines():
            for name in ['HOMO','LUMO']:
                if name in line:values[name]=float(re.findall(NUMBER,line)[-1])
        assert set(values)=={'HOMO','LUMO'},str(p)
        result['orbitals'].append(dict(system=p.parent.name,homo_ev=values['HOMO'],lumo_ev=values['LUMO'],gap_ev=values['LUMO']-values['HOMO']))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);args=parser.parse_args()
    text=json.dumps(inspect_repository(),indent=2,ensure_ascii=False)
    if args.output:args.output.write_text(text+'\n',encoding='utf8')
    else:print(text)
