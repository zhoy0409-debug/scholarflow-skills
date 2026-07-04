#!/usr/bin/env python3
"""Resolve an OPEN-ACCESS PDF link for a paper, by DOI or PMID, using free
public services that need NO login cookies:
  1. Unpaywall   (by DOI)         -> best_oa_location.url_for_pdf
  2. NCBI id conv (PMID -> DOI/PMCID) and PMC (free full text)
  3. arXiv       (arXiv id)       -> direct PDF

Use this to fill the open-access gap: for items the browser session could not
get a gated PDF for, try to find a legitimately free PDF. The returned URL is
publicly downloadable, so it can be handed straight to Zotero as an attachment
(see references/zotero-connector.md) or downloaded to disk.

Note: closed Chinese databases (CNKI/Wanfang) are NOT in these indexes; OA
lookup will not help there -- those PDFs only come from the logged-in session.

Usage:
    python oa_pdf.py --doi 10.1038/s41586-020-2649-2 --email you@example.com
    python oa_pdf.py --pmid 32015507 --email you@example.com
    python oa_pdf.py --arxiv 2103.00020
    python oa_pdf.py --doi 10.xxx/yyy --email you@x.com --json

Unpaywall requires an email in the query string (any real address). Pass --email
or set the UNPAYWALL_EMAIL environment variable.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

UA = "zotero-lit-fetch/1.0 (mailto:%s)"


def _get_json(url, email, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA % email})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def from_unpaywall(doi, email):
    doi = doi.strip().lower().replace("https://doi.org/", "")
    url = ("https://api.unpaywall.org/v2/" + urllib.parse.quote(doi)
           + "?email=" + urllib.parse.quote(email))
    try:
        data = _get_json(url, email)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"source": "unpaywall", "is_oa": False, "note": "DOI not found"}
        raise
    best = data.get("best_oa_location") or {}
    return {
        "source": "unpaywall",
        "is_oa": bool(data.get("is_oa")),
        "url_for_pdf": best.get("url_for_pdf"),
        "landing_url": best.get("url"),
        "version": best.get("version"),
        "host_type": best.get("host_type"),
        "title": data.get("title"),
    }


def pmid_to_ids(pmid, email):
    """Use NCBI ID Converter to map PMID -> DOI / PMCID."""
    url = ("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
           "?tool=zotero-lit-fetch&email=" + urllib.parse.quote(email)
           + "&ids=" + urllib.parse.quote(pmid) + "&format=json")
    data = _get_json(url, email)
    recs = data.get("records", [])
    if not recs:
        return {}
    r = recs[0]
    return {"doi": r.get("doi"), "pmcid": r.get("pmcid")}


def pmc_pdf(pmcid):
    """PMC exposes a free PDF for open-access articles."""
    if not pmcid:
        return None
    pid = pmcid.replace("PMC", "")
    return "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC" + pid + "/pdf/"


def from_arxiv(arxiv_id):
    aid = arxiv_id.strip().replace("arXiv:", "")
    return {
        "source": "arxiv",
        "is_oa": True,
        "url_for_pdf": "https://arxiv.org/pdf/" + aid + ".pdf",
        "landing_url": "https://arxiv.org/abs/" + aid,
        "version": "submittedVersion",
    }


def resolve(args):
    email = args.email or os.environ.get("UNPAYWALL_EMAIL", "")
    if args.arxiv:
        return from_arxiv(args.arxiv)

    if args.pmid and not args.doi:
        if not email:
            return {"error": "PMID lookup needs --email (for NCBI/Unpaywall)."}
        ids = pmid_to_ids(args.pmid, email)
        if ids.get("pmcid"):
            return {"source": "pmc", "is_oa": True,
                    "url_for_pdf": pmc_pdf(ids["pmcid"]),
                    "pmcid": ids["pmcid"], "doi": ids.get("doi")}
        args.doi = ids.get("doi")
        if not args.doi:
            return {"source": "pmc", "is_oa": False,
                    "note": "No PMCID and no DOI for this PMID."}

    if args.doi:
        if not email:
            return {"error": "DOI lookup needs --email for Unpaywall."}
        return from_unpaywall(args.doi, email)

    return {"error": "Provide one of --doi, --pmid, or --arxiv."}


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--doi")
    p.add_argument("--pmid")
    p.add_argument("--arxiv")
    p.add_argument("--email", help="contact email (required by Unpaywall/NCBI)")
    p.add_argument("--json", action="store_true", help="print raw JSON only")
    args = p.parse_args()

    try:
        result = resolve(args)
    except urllib.error.URLError as e:
        result = {"error": "network error reaching OA service: " + str(e)
                           + ". Check connection; if it persists, tag needs-PDF."}
    except (OSError, ValueError, json.JSONDecodeError) as e:
        result = {"error": "OA lookup failed: " + str(e)}

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return 2 if result.get("error") else 0

    if result.get("error"):
        print("Error:", result["error"], file=sys.stderr)
        return 2
    pdf = result.get("url_for_pdf")
    if pdf:
        print("OA PDF found (" + str(result.get("source")) + ", "
              + str(result.get("version", "n/a")) + "):\n" + pdf)
    else:
        print("No OA PDF. is_oa=" + str(result.get("is_oa"))
              + " note=" + str(result.get("note", ""))
              + " -> tag item as needs-PDF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
