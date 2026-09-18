# The one command. `make red` exits non-zero when a ticker is lost.
# Wire your real runner into the `red` target and this becomes your loop.

.PHONY: red diagnose forensics green-check clean

red:                    ## THE loop: fails if any ticker fails to reach output
	python3 -m pytest test_no_silent_drops.py -q

diagnose:               ## Localise: which stage boundary lost them
	python3 diagnose.py --bugs $(BUGS)

forensics:              ## Mine the last N nights of output files for a pattern
	python3 drop_forensics.py --nights '$(NIGHTS)' --universe $(UNIVERSE)

green-check:            ## Prove the loop can pass: same tests, bug removed
	python3 -m pytest test_no_silent_drops.py -q -k "not inner-join and not swallow and not concurrency and not dedupe and not dropna"

clean:
	rm -rf __pycache__ .pytest_cache demo

BUGS ?= innerjoin
NIGHTS ?= demo/det/*.json
UNIVERSE ?= demo/universe.txt
