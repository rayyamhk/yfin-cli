# Industry

## `industry-overview`

Get overview information for an industry.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid industry key (use `yfin sector-industries <sector-key>` to find) |

**Examples:**

```bash
yfin industry-overview semiconductors
yfin industry-overview software-application
```

---

## `industry-research-reports`

Get research reports related to an industry.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid industry key |

**Examples:**

```bash
yfin industry-research-reports biotechnology
```

---

## `industry-top-companies`

Get the top companies within an industry.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid industry key |

**Examples:**

```bash
yfin industry-top-companies semiconductors
yfin industry-top-companies internet-retail
```

---

## `industry-top-growth-companies`

Get the top growth companies in an industry.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid industry key |

**Examples:**

```bash
yfin industry-top-growth-companies software-infrastructure
```

---

## `industry-top-performing-companies`

Get the top performing companies in an industry.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid industry key |

**Examples:**

```bash
yfin industry-top-performing-companies auto-manufacturers
```