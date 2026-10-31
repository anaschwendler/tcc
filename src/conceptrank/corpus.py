"""Load the raw CSTNews corpus (data/raw/CSTNews/) into Cluster objects.

Choices that differ from the 2016 pipeline (archive/read_archives.py):

- Sentences come from "Textos-fonte segmentados", the corpus' own
  segmentation, instead of a tokenizer. Those files are a revised copy of the
  source texts: they add datelines ("RIO -") and fix a few quotes and
  full stops.
- Titles are kept apart from the sentences.
- The human extract is split into sentences and the source tag at the end of
  each line ("<D1_C1_Folha; p1-s1>") is removed from the text and kept as
  provenance.
- Files are read as UTF-8, falling back to Latin-1 (a few CSTSumm summaries
  and one human abstract). Windows curly quotes stored as the control
  characters U+0093/U+0094 become '"'.
- Folder names saved in a DOS code page are repaired ("Polбtica" ->
  "Política"). Categories are written without accents, as most folders do
  ("Politica", "Ciencia"), and the agency "Globo" becomes "OGlobo".
"""

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

RAW_DIR = Path(__file__).parents[2] / "data" / "raw" / "CSTNews"

_CLUSTER_NAME = re.compile(r"^(C\d+)_([^_]+)_(.+?)(?: - concordancia(RST|CST))?$")
# Tags vary: "<D1_C1_Folha; p1-s1>", "<D2_C41_Estadao: p3-s2>",
# "<D1_C5_Folha_p1-s1>", "P1-S1", "p1_s1", and one line without the "<".
_EXTRACT_LINE = re.compile(
    r"^(.*?)\s*<?(D\d+)_C\d+_[A-Za-z]+[;:_]\s*[pP](\d+)[-_][sS](\d+)\s*>$"
)
_WINDOWS_QUOTES = {0x93: '"', 0x94: '"'}
_AGENCY_ALIASES = {"Globo": "OGlobo"}


@dataclass(frozen=True)
class Source:
    id: str
    agency: str
    title: str | None
    sentences: tuple[str, ...]


@dataclass(frozen=True)
class ExtractSentence:
    text: str
    source_id: str
    position: str


@dataclass(frozen=True)
class Cluster:
    id: str
    category: str
    topic: str
    agreement: str | None
    sources: tuple[Source, ...]
    human_extract: tuple[ExtractSentence, ...]
    human_abstract: str
    cstsumm: str
    path: Path

    @property
    def sentences(self):
        return tuple(s for source in self.sources for s in source.sentences)


def read_text(path):
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")
    return text.replace("\r\n", "\n").translate(_WINDOWS_QUOTES).strip()


def repair_name(name):
    if any(ord(ch) > 0xFF for ch in name):
        return name.encode("cp866").decode("cp850")
    return name


def strip_accents(text):
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def _lines(text):
    return tuple(line.strip() for line in text.split("\n") if line.strip())


def _doc_prefix(filename):
    return "_".join(filename.split("_")[:2]).split(".")[0]


def load_sources(cluster_dir):
    segmented = list((cluster_dir / "Textos-fonte segmentados").glob("D*_C*"))
    sources = []
    for path in sorted((cluster_dir / "Textos-fonte").glob("D*.txt")):
        if path.stem.endswith("_titulo"):
            continue
        prefix = _doc_prefix(path.name)
        [seg] = [s for s in segmented if _doc_prefix(s.name) == prefix]
        title_path = path.with_name(path.stem + "_titulo.txt")
        agency = path.stem.split("_")[2]
        sources.append(Source(
            id=prefix.split("_")[0],
            agency=_AGENCY_ALIASES.get(agency, agency),
            title=read_text(title_path) if title_path.exists() else None,
            sentences=_lines(read_text(seg)),
        ))
    return tuple(sources)


def parse_extract(text):
    sentences = []
    for line in _lines(text):
        match = _EXTRACT_LINE.match(line)
        if match is None:
            raise ValueError(f"unexpected human extract line: {line!r}")
        sentence, source_id, paragraph, index = match.groups()
        sentences.append(ExtractSentence(sentence, source_id, f"p{paragraph}-s{index}"))
    return tuple(sentences)


def load_cluster(cluster_dir):
    match = _CLUSTER_NAME.match(repair_name(cluster_dir.name))
    if match is None:
        raise ValueError(f"unexpected cluster folder name: {cluster_dir.name!r}")
    cluster_id, category, topic, agreement = match.groups()
    summaries = cluster_dir / "Sumarios"
    return Cluster(
        id=cluster_id,
        category=strip_accents(category),
        topic=topic,
        agreement=agreement,
        sources=load_sources(cluster_dir),
        human_extract=parse_extract(read_text(summaries / f"{cluster_id}_extrato_humano.txt")),
        human_abstract=read_text(summaries / f"{cluster_id}_sumario_humano.txt"),
        cstsumm=read_text(summaries / f"{cluster_id}_sumario_automatico_CSTSumm.txt"),
        path=cluster_dir,
    )


def load_corpus(raw_dir=RAW_DIR):
    clusters = [load_cluster(d) for d in Path(raw_dir).iterdir() if re.match(r"C\d+_", d.name)]
    return sorted(clusters, key=lambda c: int(c.id[1:]))
