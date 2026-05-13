# df-lexvance-contracts-manager [CRUX-MK]

**Welle:** 48 Track-A Wave-1 DC-1
**Status:** SKELETON-CONDITIONAL (NICHT laden vor Martin-Phronesis-Approval Welle-49)
**Coverage:** LexVance Gap-Cluster C (Vertragsmanagement)

## Scope

Contracts-Manager ueber 6 Vertrags-Kategorien:
- **B2B_MSA** (SaaS-MSA + DPA + SLA)
- **AGB** (§§ 305-310 BGB Inhaltskontrolle)
- **NDA** (Bilateral + Multilateral)
- **LIZENZ** (Software + IP + Open-Source-Compliance)
- **HR** (Arbeitsvertraege + Bonusplan + Aufhebung)
- **MA** (LOI + SPA + Closing-Conditions, K_0-naehe)

Output: ContractsAuditResult mit Klausel-Findings + fehlende Pflicht-Klauseln + AGB-/IP-Status.

## LexVance-Coverage-Mapping

| LexVance-Funktion | Vor Welle-48 | Nach Welle-48 |
|-------------------|---------------|----------------|
| Klausel-Pipeline | df-101 + df-104 | df-lexvance-contracts-manager (orchestriert) |
| AGB-Inhaltskontrolle | UNGEDECKT | df-lexvance-contracts-manager |
| NDA-Manager | UNGEDECKT | df-lexvance-contracts-manager |
| Lizenz + OSS-Compliance | UNGEDECKT | df-lexvance-contracts-manager |
| HR-Vertraege | UNGEDECKT | df-lexvance-contracts-manager |
| M&A-Vertraege | UNGEDECKT | df-lexvance-contracts-manager (PHRONESIS Pflicht) |

## Compliance

- K11-K16 voll
- LC1-LC5 voll
- Trinity-Pattern via Kategorie-Status
- Audit-Trail
- ENV-Var-gated Default-Disabled
- **M&A-Kategorie erzwingt PHRONESIS_TICKET** (K_0-Schutz)
- Cross-Reference zu df-101-vertrags-pipeline + df-104-klausel-discovery

## Activation

1. Martin-Phronesis-Approval (Welle-49 Pflicht)
2. Cross-LLM-3OF3-Audit (Codex+Gemini+Copilot)
3. Tests passing: `python3 -m pytest tests/ -v`
4. Real-Mode: ENV `DF_LEXVANCE_CONTRACTS_REAL_ENABLED=true`
5. M&A-Mode: PHRONESIS_TICKET=PT-... Pflicht

## STOP

`touch /tmp/df-lexvance-contracts-manager.stop` oder LaunchAgent unloaden.

## Welle-49+ Roadmap

- [ ] df-101-Integration: Klausel-Discovery-Reader (Welle-49)
- [ ] AGB-Inhaltskontrolle-DB-Loader (BGB §§ 305-310 Rechtsprechung) (Welle-49)
- [ ] OSS-Compliance-Scanner (Lizenz-Kategorie) (Welle-50)
- [ ] HR-Vertrags-Template-Generator (Welle-50)
- [ ] M&A-Closing-Conditions-Checker (Welle-50, K_0-naehe)
- [ ] Cross-LLM-3OF3-Audit-Verdict (Welle-49)

## rho

~90k EUR/J (AGB-Inhaltskontrolle-Schaden-Vermeidung + IP-Compliance + M&A-Closing-Risk).

[CRUX-MK]
