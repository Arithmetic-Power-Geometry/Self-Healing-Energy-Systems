# IEEE123 reproducibility: identified concrete Linux failure
Date 2026-10-22.

Directly inspected tshort/OpenDSS IEEE123Master.dss: it invokes 'Redirect IEEELinecodes.DSS'. The actual upstream file in the same directory is 'IEEELineCodes.DSS' (capital C). GitHub fetched the real file (blob SHA 7ff5b2ebdf6fc6384fc93554d9f677ea13a17e7a; 11851 characters). This is a **filename case mismatch** on case-sensitive Linux, not a missing electrical-parameter file.

Corrective GitHub Actions step now checks the original, refuses to overwrite an existing target, copies the original to the exact name referenced by the master, and records both SHA256 hashes. No linecode content or physical parameter is fabricated or changed.

Other redirects in IEEE123Master.dss: IEEE123Regulators.DSS, IEEE123Loads.DSS. The actual static convergence result is not yet verified. Gate 3 remains open. No new academic citation is appended because this was a source-code diagnostic, not a newly verified paper.
