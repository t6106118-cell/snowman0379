---
name: qsv
description: CSV and tabular-data command-line workflows with qsv. Use when Codex needs to install or verify qsv, inspect CSV metadata, validate CSV shape, count rows, select/reorder columns, slice/sample rows, search selected CSV fields, compute stats or frequency tables, generate schema, create indexes or stats caches, run Polars SQL over CSV/Parquet/JSONL, join/pivot tabular data, convert CSV to JSONL/Parquet/XLSX/SQLite/PostgreSQL, or decide whether qsv is better than awk/cut/rg/Python/DuckDB for a tabular-data task.
---

# qsv

## Decision Rule

Use `qsv` for CSV and tabular data. Do not hand-roll CSV parsing with `awk`, `cut`, or regex when `qsv` has a direct command.

| Task | Prefer |
|---|---|
| Inspect rows, columns, delimiter, headers, basic types | `qsv` |
| Validate CSV shape or schema | `qsv validate` |
| Select, slice, search, sort, sample CSV records | `qsv` |
| Compute stats, frequency tables, schema, data profile | `qsv` |
| SQL aggregation over CSV/Parquet/JSONL | `qsv sqlp` |
| Convert tabular formats | `qsv` |
| Plain text search in non-tabular files | `rg` |
| Long-lived complex analysis code | Python, R, or DuckDB |

## Workflow

1. Verify availability:

```bash
qsv --version
qsv --list
```

2. If missing or outdated, read `references/commands.md` for install options. Prefer official prebuilt/package-manager installs before source builds.

3. Inspect the file before transforming it:

```bash
qsv sniff data.csv
qsv validate data.csv
qsv headers data.csv
qsv count data.csv
```

4. Use qsv-native field selection and parsing. Avoid `cut -d,`, raw regex over CSV rows, or manual quote handling.

5. Create an index and stats cache when repeatedly slicing, sampling, running stats/frequency, or using smart commands on non-trivial CSV files.

6. For exact command syntax, install details, examples, sidecar files, and troubleshooting, read `references/commands.md`.

## Quick Commands

```bash
qsv count data.csv
qsv headers data.csv
qsv sniff data.csv
qsv validate data.csv
qsv select col1,col2 data.csv
qsv search -s status --exact completed data.csv
qsv sort -s amount -N -R data.csv
qsv stats --everything data.csv
qsv frequency -s category,status data.csv
qsv sample --seed 7 100 data.csv
qsv index data.csv
qsv schema data.csv
qsv tojsonl data.csv > data.jsonl
qsv sqlp data.csv 'select col1, count(*) as n from data group by col1 order by n desc' --quiet
```

## References

Read [references/commands.md](references/commands.md) when the task asks about installation, exact command usage, command categories, SQL, indexing/caching, conversion, sidecar cleanup, or practical examples.
