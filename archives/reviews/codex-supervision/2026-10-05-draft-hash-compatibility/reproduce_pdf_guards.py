from pathlib import Path
from unittest import mock
import json,sys,subprocess,contextlib,io
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];sys.path.insert(0,str(ROOT));from tools import render_review as m
fixture=OUT/'pdf-regression-fixture';fixture.mkdir(exist_ok=True);md=fixture/'unrendered.md';md.write_bytes(b'# Regression\n\n$\\frac{1}{3}$\n')
raw=m.build_html(md.read_text('utf-8'),'not-completed')
assert '<title>not-completed</title>' in raw and "document.title='MJDONE'" in raw and '<mjx-container' not in raw
# Isolated old artifact fixture. No real PDF is authored or delivered: this invalid sentinel only reproduces the exists/size gate.
pdf=fixture/'unrendered.pdf';sentinel=b'OLD-INVALID-SENTINEL';pdf.write_bytes(sentinel);dump=subprocess.CompletedProcess(['mock dump-dom'],0,raw.encode(),b'');fail=subprocess.CompletedProcess(['mock print'],1,b'',b'print failed; no output')
log=io.StringIO()
with mock.patch.object(m,'run_edge',side_effect=[dump,fail]),contextlib.redirect_stdout(log):rc=m.main([str(md),'--out-dir',str(fixture)])
assert rc==0 and pdf.read_bytes()==sentinel
result={'commit':'1e9f60b','unrendered_document_with_script_marker_accepted':True,'stale_invalid_pdf_with_failed_print_accepted':True,'actual_tool_returncode':rc,'printer_failure_returncode':1,'real_edge_launched':False,'real_pdf_authored_or_modified':False,'original_pdf_untouched':True,'stdout':log.getvalue(),'recommendation':'Require actual title and complete formula/error coverage; print to unique new target; validate a newly produced PDF; preserve prior artifacts.'}
(OUT/'pdf-guard-independent-reproduction.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps(result,ensure_ascii=False))
