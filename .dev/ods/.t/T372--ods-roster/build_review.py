"""review.src.html → review.html: the pictures of img/ go inside the page as data URIs, for viewing the page locally
as one file. The artifact itself is published from review.src.html together with img/.
Run from this folder: python3 build_review.py"""
import base64
import re
from pathlib import Path

HERE = Path(__file__).parent


def inline(m: re.Match) -> str:
    data = base64.b64encode((HERE / m[1]).read_bytes()).decode()
    return f'src="data:image/png;base64,{data}"'


page = re.sub(r'src="(img/[^"]+\.png)"', inline, (HERE / "review.src.html").read_text())
(HERE / "review.html").write_text(page)
print(f"review.html: {len(page) // 1024} KB")
