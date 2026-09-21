"""Phase 4 instrumentation: find the stage that loses tickers, in ONE nightly run.

Every log line carries the tag [DEBUG-7c31] so cleanup is a single grep:
    grep -rn 'DEBUG-7c31' . && git checkout -- <files>

Drop-in usage - wrap each stage boundary in the nightly pipeline:

    from stage_census import census

    with census("fetch", [t for t in universe]) as c:
        rows = fetch_all(universe)
        c.out([r.ticker for r in rows])

    with census("enrich", [r.ticker for r in rows]) as c:
        enriched = enrich(rows)
        c.out([r.ticker for r in enriched])

    with census("persist", [r.ticker for r in enriched]) as c:
        written = upsert(enriched)
        c.out(written_tickers)

One night of this prints a funnel. The stage whose `lost` is non-empty is the bug site;
every hypothesis about the other stages dies at once.
"""
import logging
from contextlib import contextmanager

TAG = "[DEBUG-7c31]"
log = logging.getLogger("stage_census")


class _Census:
    def __init__(self, stage, inputs):
        self.stage, self.inputs, self.outputs = stage, list(inputs), None

    def out(self, outputs):
        self.outputs = list(outputs)


@contextmanager
def census(stage, inputs):
    c = _Census(stage, inputs)
    try:
        yield c
    finally:
        outs = c.outputs if c.outputs is not None else []
        out_set = set(outs)
        lost = [t for t in c.inputs if t not in out_set]
        gained = sorted(out_set - set(c.inputs))
        dupes = len(outs) - len(out_set)
        log.warning(
            "%s stage=%-10s in=%-5d out=%-5d lost=%-3d dupes=%-3d gained=%-3d %s",
            TAG, stage, len(c.inputs), len(outs), len(lost), dupes, len(gained),
            ("LOST=" + ",".join(lost[:20])) if lost else "",
        )
        if gained:
            log.warning("%s stage=%s GAINED=%s", TAG, stage, gained[:20])
