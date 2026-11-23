"""Monday Edition: the world news of Monday 23 November 2026, in one image.

This program writes the entry image to ``entry.png`` in the output
folder. The image itself ships in this repository as ``entry.png``: a
single-page newspaper front page, "THE WORLD IN ONE DAY", drawn by
``draw.py`` with Pillow at build time. This program only copies those
bytes, so both runs produce identical output. No network, no clock,
no randomness, standard library only.

The six stories on the page, all first reported Monday 23 Nov 2026:
1. KOSPI crashes 5% in Seoul (AI rout; 10-trillion-won rescue fund).
2. M6.5 deep earthquake, Vanuatu region (02:40 UTC, 601 km down).
3. New Zealand bat out a draw vs India, Wellington (day five).
4. Modi meets Nepal PM Balen Shah in Delhi (welcome + talks).
5. NHS launches EDITH, the world's largest AI breast-screening trial.
6. UN demands a probe into the Libya ship strikes off Benghazi.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    data = dest.read_bytes()
    print(f"wrote {dest}  {len(data)} bytes")
    print(f"sha256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
