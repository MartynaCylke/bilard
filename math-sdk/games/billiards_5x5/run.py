import csv, json, os, random
from zstandard import ZstdCompressor
from games.billiards_5x5.gamestate import run_spin

PUBLISH_DIR = os.path.join(os.path.dirname(__file__), "library", "publish_files")
os.makedirs(PUBLISH_DIR, exist_ok=True)

def main(n=2000):
    books_path = os.path.join(PUBLISH_DIR, "books_base.jsonl.zst")
    csv_path = os.path.join(PUBLISH_DIR, "lookUpTable_base_0.csv")
    index_path = os.path.join(PUBLISH_DIR, "index.json")
    cctx = ZstdCompressor(level=10)
    with open(books_path, "wb") as fout:
        with cctx.stream_writer(fout) as compressor:
            for sim_id in range(1, n+1):
                compressor.write((json.dumps(run_spin(sim_id))+'\\n').encode())

    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        for sim_id in range(1, n+1):
            w.writerow([sim_id, 1, random.randint(0,200)])

    with open(index_path,"w") as f:
        json.dump({"modes":[{"name":"base","cost":1.0,"events":"books_base.jsonl.zst","weights":"lookUpTable_base_0.csv"}]}, f)

if __name__ == "__main__":
    main()
