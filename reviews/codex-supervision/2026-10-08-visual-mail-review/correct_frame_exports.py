"""Create new, video-bound page PNGs without overwriting raw screenshot failures."""
from pathlib import Path
from fractions import Fraction
import hashlib,json
import av
ROOT=Path(__file__).resolve().parents[3]
OWNER=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    output=OWNER/"corrected-video-pages"
    output.mkdir(exist_ok=False)
    records=[]
    for i in range(1,4):
        batch=OWNER/("shard-"+str(i))
        receipt=json.loads((batch/"receipt.json").read_text("utf-8"))
        assert receipt["summary"]=={"total":55,"passed":55,"failed":0}
        for row in receipt["results"]:
            video=ROOT/row["mp4_path"]
            assert video.resolve().is_relative_to(OWNER.resolve()) and sha(video)==row["mp4_sha256"]
            work=video.parents[3].parent
            geometry=work/"page-geometry.json"
            assert sha(geometry)==row["geometry_sha256"]
            pages=json.loads(geometry.read_text("utf-8"))["pages"]
            folder=output/row["id"];folder.mkdir()
            frames=[];n=0
            with av.open(str(video)) as c:
                stream=c.streams.video[0];assert Fraction(stream.average_rate)==15
                for frame in c.decode(stream):
                    if n%45==0:
                        index=n//45
                        assert index<len(pages) and Fraction(frame.pts)*Fraction(frame.time_base)==index*3
                        p=folder/pages[index]["frame"]
                        frame.to_image().save(p)
                        frames.append({"path":p.relative_to(ROOT).as_posix(),"sha256":sha(p),
                                       "video_frame_index":n,"video_time_seconds_exact":str(index*3)})
                    n+=1
            assert n==45*len(pages) and len(frames)==len(pages)
            records.append({"id":row["id"],"source_mp4_path":row["mp4_path"],"source_mp4_sha256":row["mp4_sha256"],
                            "geometry_sha256":row["geometry_sha256"],"original_render_receipt_sha256":sha(work/"receipt.json"),
                            "frames":frames,"status":"REPAIRED_PNG_EXPORT_FROM_ACTUAL_VIDEO","raw_pages_retained":True})
            if len(records)%15==0:print("Corrected actual-video page exports",len(records),flush=True)
    assert len(records)==165 and len({r["id"] for r in records})==165
    with (OWNER/"corrected-frames.jsonl").open("xb") as f:
        for row in records:f.write((json.dumps(row,sort_keys=True)+"\n").encode("utf-8"))
    print("Corrected 165 bound page exports; raw failures preserved",flush=True)
if __name__=="__main__":main()
