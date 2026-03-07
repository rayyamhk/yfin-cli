# Sector

## `sector-keys`

Get all available sector keys. Use these keys as arguments for other sector commands.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| *(none)* | — | — | — | No parameters required |

**Examples:**

```bash
# List all sector keys
yfin sector-keys
```

---

## `sector-industries`

Get the industries within a sector.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid sector key (use `yfin sector-keys` to find) |

**Examples:**

```bash
# Get industries in Technology sector
yfin sector-industries technology

# Get industries in Healthcare sector
yfin sector-industries healthcare
```

---

## `sector-overview`

Get overview information for a sector.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid sector key |

**Examples:**

```bash
yfin sector-overview technology
yfin sector-overview energy
```

---

## `sector-research-reports`

Get research reports related to a sector.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid sector key |

**Examples:**

```bash
yfin sector-research-reports financial-services
```

---

## `sector-top-companies`

Get the top companies within a sector.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid sector key |

**Examples:**

```bash
yfin sector-top-companies technology
yfin sector-top-companies consumer-cyclical
```

---

## `sector-top-etfs`

Get the top ETFs for a sector.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid sector key |

**Examples:**

```bash
yfin sector-top-etfs technology
yfin sector-top-etfs energy
```

---

## `sector-top-mutual-funds`

Get the top mutual funds for a sector.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `KEY` | argument | ✅ | — | A valid sector key |

**Examples:**

```bash
yfin sector-top-mutual-funds healthcare
```