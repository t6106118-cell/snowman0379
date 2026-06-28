# qsv Commands Reference

## Sources

- Official repo and README: https://github.com/dathere/qsv
- Official performance notes: https://github.com/dathere/qsv/blob/master/docs/PERFORMANCE.md
- Official wiki: https://github.com/dathere/qsv/wiki
- Local tested version: `qsv 21.1.0`
- Local tested data: `continuous-note-taking/data/qsv/penguins.csv`

## What qsv does

`qsv` is a Rust command-line toolkit for CSV and tabular data. It can inspect, validate, search, transform, analyze, join, query, sample, enrich, and convert CSV-like data. This install has Polars support, so `sqlp`, `joinp`, Parquet, JSONL, and other extended formats are available.

Use qsv when the input is structured tabular data. Use `rg` for plain text search and Python/R/DuckDB for longer analysis programs.

## Installation

Check first:

```bash
qsv --version
qsv --list
qsv --help
```

Preferred install methods are official prebuilt binaries or package-manager installs. The qsv README warns that `cargo install` can be unreliable for the full build because qsv uses patched dependencies.

Common install options:

```bash
# Homebrew
brew install qsv

# MacPorts
sudo port install qsv

# Arch Linux
pacman -S qsv

# Conda
conda install -c conda-forge qsv

# Scoop on Windows
scoop install qsv

# Nix
nix-env -iA nixpkgs.qsv

# mise/asdf style workflow if qsv plugin is available
mise use -g qsv
```

Install or upgrade from GitHub releases:

```bash
# Open releases and select the binary for the platform.
# https://github.com/dathere/qsv/releases
```

Self-update when qsv was installed in a compatible way:

```bash
qsv --update
qsv --updatenow
```

Source build fallback:

```bash
git clone https://github.com/dathere/qsv.git
cd qsv
cargo build --release
```

Use source builds only when package/prebuilt installs are unavailable or a specific branch/feature is needed.

## Global Options

```bash
qsv --help
qsv --list
qsv --envlist
qsv --generate-help-md
qsv --version
qsv COMMAND --help
```

Common command options:

```bash
-o, --output FILE       write output to a file
-d, --delimiter CHAR    read or write a non-comma delimiter
-n, --no-headers        treat first row as data, not headers
```

## Command Categories

| Area | Commands |
|---|---|
| Inspect/select | `headers`, `count`, `sniff`, `flatten`, `lens`, `select`, `slice`, `sample`, `table`, `color` |
| Clean/validate | `validate`, `fixlengths`, `input`, `safenames`, `rename`, `behead`, `fill` |
| Search/filter | `search`, `searchset`, `exclude`, `dedup`, `extdedup` |
| Transform | `apply`, `datefmt`, `edit`, `enum`, `explode`, `implode`, `replace`, `reverse`, `sort`, `extsort`, `sortcheck`, `split`, `partition`, `transpose`, `fmt`, `template`, `foreach`, `luau`, `pseudo` |
| Analyze | `stats`, `moarstats`, `frequency`, `pragmastat`, `pivotp`, `schema`, `scoresql` |
| Join/query | `join`, `joinp`, `sqlp` |
| Convert | `json`, `jsonl`, `tojsonl`, `to`, `excel`, `geoconvert`, `snappy` |
| Web/enrich | `fetch`, `fetchpost`, `geocode` |
| Other | `cat`, `diff`, `blake3`, `prompt`, `describegpt`, `pro` |

## Inspect CSV

Count rows:

```bash
qsv count data.csv
```

Show headers:

```bash
qsv headers data.csv
qsv headers --just-names data.csv
qsv headers --just-count data.csv
```

Sniff metadata:

```bash
qsv sniff data.csv
```

Validate shape and RFC4180 compliance:

```bash
qsv validate data.csv
```

Preview rows:

```bash
qsv slice --len 10 data.csv | qsv table
qsv slice --index 5 data.csv | qsv flatten
```

Interactive viewing:

```bash
qsv lens data.csv
```

## Select, Slice, Search, Sort

Select columns:

```bash
qsv select col1,col2 data.csv
qsv select 1,3-5 data.csv
qsv select 1,_ data.csv
qsv select '!secret,password' data.csv
qsv select '/^prefix_/' data.csv
```

Slice rows:

```bash
qsv slice --len 10 data.csv
qsv slice --start 100 --len 20 data.csv
qsv slice --index 5 data.csv
qsv slice --start -10 data.csv
```

Search selected fields:

```bash
qsv search -s status --exact completed data.csv
qsv search -i -s message 'error|warning' data.csv
qsv search --literal -s name 'a.b*c' data.csv
qsv search --invert-match -s status failed data.csv
qsv search --quick -s message urgent data.csv
qsv search --count -s status completed data.csv
```

Sort:

```bash
qsv sort -s amount -N -R data.csv
qsv sort -s name --natural data.csv
qsv sort -s status --unique data.csv
```

Use `extsort` for files too large to sort in memory:

```bash
qsv index data.csv
qsv extsort --select amount data.csv
```

Pretty-print:

```bash
qsv table
qsv color data.csv
```

## Stats and Frequency

Basic stats:

```bash
qsv stats data.csv
```

All stats:

```bash
qsv stats --everything data.csv
```

Type inference only:

```bash
qsv stats --typesonly data.csv
```

Useful compact stats view:

```bash
qsv stats --everything data.csv \
  | qsv select field,type,min,max,mean,q2_median,mode,nullcount \
  | qsv table
```

Infer dates and booleans:

```bash
qsv stats --everything --infer-dates --infer-boolean data.csv
```

Frequency tables:

```bash
qsv frequency -s status,category data.csv
qsv frequency -s status --limit 20 data.csv
qsv frequency -s status --json data.csv
qsv frequency -s status --pretty-json data.csv
```

## Index and Cache

Create an index for repeated slicing, counting, sampling, stats, frequency, split, schema, or tojsonl work:

```bash
qsv index data.csv
```

Create stats cache:

```bash
qsv stats --everything --stats-jsonl data.csv
```

Stats/cache sidecars may include:

```text
*.idx
*.stats.csv
*.stats.csv.data.jsonl
*.stats.csv.json
*.freq.csv.data.jsonl
*.schema.json
*.pschema.json
```

Keep these files when repeated qsv work benefits from them. Remove them when packaging a clean dataset.

## Schema and Validation

Generate JSON Schema:

```bash
qsv schema data.csv
```

Validate with generated schema:

```bash
qsv validate data.csv data.csv.schema.json
```

Generate Polars schema for `sqlp`, `joinp`, and `pivotp` optimization:

```bash
qsv schema --polars data.csv
```

## Sampling

Uniform sample:

```bash
qsv sample 100 data.csv
qsv sample 0.1 data.csv
qsv sample --seed 7 100 data.csv
```

Stratified sample:

```bash
qsv sample --stratified species 2 --seed 7 data.csv
```

Weighted sample:

```bash
qsv sample --weighted weight_col 100 data.csv
qsv sample --varopt weight_col 100 data.csv
```

Cluster sample:

```bash
qsv sample --cluster group_col 10 data.csv
```

Remote CSV sample:

```bash
qsv sample --bernoulli 0.01 'https://example.com/data.csv'
```

## SQL With Polars

For one CSV, the table name is the file stem:

```bash
qsv sqlp data.csv \
  'select col1, count(*) as n from data group by col1 order by n desc' \
  --quiet
```

For several files, use file-stem table names or `_t_1`, `_t_2`:

```bash
qsv sqlp left.csv right.csv \
  'select * from _t_1 join _t_2 on _t_1.id = _t_2.id' \
  --quiet
```

Use SQL scripts for complex queries:

```bash
qsv sqlp data.csv query.sql --quiet
```

Export SQL results:

```bash
qsv sqlp data.csv 'select * from data' --format csv --output out.csv --quiet
qsv sqlp data.csv 'select * from data' --format json --output out.json --quiet
qsv sqlp data.csv 'select * from data' --format jsonl --output out.jsonl --quiet
qsv sqlp data.csv 'select * from data' --format parquet --output out.parquet --quiet
```

Query Parquet or JSONL directly via Polars table functions:

```bash
qsv sqlp SKIP_INPUT "select * from read_parquet('data.parquet') limit 10" --quiet
qsv sqlp SKIP_INPUT "select * from read_ndjson('data.jsonl') limit 10" --quiet
```

## Join and Pivot

Classic CSV join:

```bash
qsv join id left.csv id right.csv
```

Polars join:

```bash
qsv joinp id left.csv id right.csv
```

SQL join is often clearer:

```bash
qsv sqlp left.csv right.csv \
  'select * from left join right on left.id = right.id' \
  --quiet
```

Pivot with Polars:

```bash
qsv pivotp status data.csv --index category --values amount
```

Check per-command help before non-trivial joins or pivots:

```bash
qsv join --help
qsv joinp --help
qsv pivotp --help
```

## Convert

CSV to JSONL:

```bash
qsv tojsonl data.csv > data.jsonl
```

JSON array to CSV:

```bash
qsv json data.json > data.csv
```

JSONL to CSV:

```bash
qsv jsonl data.jsonl > data.csv
```

CSV to Parquet:

```bash
qsv sqlp data.csv 'select * from data' --format parquet --output data.parquet --quiet
```

CSV to Excel/XLSX, SQLite, PostgreSQL, or other supported targets:

```bash
qsv to xlsx out.xlsx data.csv
qsv to sqlite out.sqlite data.csv
qsv to postgres 'postgres://USER:PASSWORD@HOST/DB' data.csv
```

Excel to CSV:

```bash
qsv excel workbook.xlsx --sheet Sheet1 --output sheet1.csv
```

Delimiter conversion:

```bash
qsv fmt --out-delimiter '\t' data.csv > data.tsv
qsv fmt --delimiter '\t' data.tsv > data.csv
```

## Clean and Normalize

Safe database-ready names:

```bash
qsv safenames data.csv > safe.csv
```

Rename headers:

```bash
qsv rename new1,new2,new3 data.csv
```

Fix ragged records:

```bash
qsv fixlengths data.csv > fixed.csv
```

Normalize odd input:

```bash
qsv input --trim-headers --trim-fields data.csv > normalized.csv
```

Fill empty values:

```bash
qsv fill status --default unknown data.csv
```

## Tested Example

Dataset:

```text
continuous-note-taking/data/qsv/penguins.csv
344 rows, 7 columns
```

Useful commands:

```bash
qsv sniff continuous-note-taking/data/qsv/penguins.csv
qsv validate continuous-note-taking/data/qsv/penguins.csv
qsv stats --everything continuous-note-taking/data/qsv/penguins.csv \
  | qsv select field,type,min,max,mean,q2_median,mode,nullcount \
  | qsv table
qsv frequency -s species,island,sex --limit 5 continuous-note-taking/data/qsv/penguins.csv | qsv table
qsv search --exact Adelie -s species continuous-note-taking/data/qsv/penguins.csv | qsv count
qsv sqlp continuous-note-taking/data/qsv/penguins.csv \
  "select species, island, count(*) as n, round(avg(body_mass_g), 1) as avg_mass
   from penguins group by species, island order by species, island" \
  --quiet | qsv table
```

Observed facts:

```text
rows: 344
species counts: Adelie 152, Gentoo 124, Chinstrap 68
sex nulls: 11
body_mass_g mean: 4201.7544
```

## qsv vs Other Tools

| Use case | Better tool |
|---|---|
| CSV row/column inspection | `qsv` |
| CSV field-aware search/filter | `qsv search` |
| CSV stats/frequencies/schema | `qsv` |
| One-off SQL aggregation over CSV/Parquet | `qsv sqlp` |
| Plain text search in arbitrary files | `rg` |
| JSON document transformation | `jq` |
| Long reusable analysis code | Python/R/DuckDB |

## Troubleshooting

Unexpected columns or row counts:

```bash
qsv sniff data.csv
qsv validate data.csv
qsv headers data.csv
```

Wrong delimiter:

```bash
qsv headers -d ';' data.csv
qsv stats -d '\t' data.tsv
```

No headers:

```bash
qsv rename _all_generic --no-headers data.csv > with_headers.csv
qsv headers with_headers.csv
```

Large-file performance:

```bash
qsv index data.csv
qsv stats --everything --stats-jsonl data.csv
```

Memory pressure:

```bash
qsv stats --memcheck data.csv
qsv sqlp data.csv 'select * from data' --streaming --quiet
qsv index data.csv
qsv extsort --select col data.csv
```

Need exact syntax:

```bash
qsv COMMAND --help
```
