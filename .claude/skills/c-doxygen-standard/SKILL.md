---
name: c-doxygen-standard
description: Add or verify Doxygen comments on all C functions, types, and files being written or modified. Reference this skill whenever writing or editing .c or .h files.
origin: ECC
---

## When to Use

- Whenever writing or modifying `.c` or `.h` files
- When adding new public functions, structs, enums, or macros
- When performing a code review that covers documentation quality

---

## Step 1 — Ask for Author Name (REQUIRED before any code)

Before applying any Doxygen comments, ask the user:

```
What name should appear in @author?
(e.g. John Smith / J. Smith / NDR Dev Team)
```

**Wait for the answer.** Store it as `AUTHOR_NAME` and use it in every file header.

---

## Step 2 — Apply Doxygen Comment Rules

Apply the following rules to **all** C files being written or modified in this task.

---

### Rule 1 — File Header

Every `.c` and `.h` file must begin with:

```c
/**
 * @file    <filename>.<ext>
 * @brief   <one-line description of what this file contains>
 * @author  <AUTHOR_NAME>
 *
 * <Optional body: at most 2 lines of hardware context or design note>
 */
```

Rules:
- `@brief` line is one sentence only
- Optional body must not exceed **2 lines** (`@brief` + body ≤ **3 lines total**)
- `@note` and `@warning` are each one sentence maximum

---

### Rule 2 — Public Functions

```c
/**
 * @brief   <One-sentence description — start with a verb>
 *
 * <Optional: one short sentence on precondition or side effect — omit if obvious>
 *
 * @param[in]     name   Short description (no value ranges).
 * @param[out]    name   Short description.
 * @param[in,out] name   Short description.
 * @return              Short description.
 *
 * @note    One short sentence only.
 * @warning One short sentence only.
 */
```

Rules:
- `@brief` block (including the optional body line) must not exceed **3 lines total**
- `@param` and `@return` descriptions must be **short** — do not list value ranges or reproduce register details
- `@note` and `@warning` are each **one sentence** maximum
- Use simple common words — no long technical phrases
- `@return` is required for every non-`void` function

---

### Rule 3 — Structs and Typedefs

```c
/**
 * @brief   Configuration structure for the FOO peripheral.
 */
typedef struct {
    uint32_t baud_rate;   /**< Baud rate in bits per second. */
    uint8_t  word_length; /**< Word length in bits (7 or 8). */
    bool     parity_en;   /**< Set true to enable parity. */
} foo_config_t;
```

---

### Rule 4 — Enums

```c
/**
 * @brief   Status codes returned by FOO driver functions.
 */
typedef enum {
    FOO_OK    = 0, /**< Operation completed successfully. */
    FOO_ERROR = 1, /**< General error. */
    FOO_BUSY  = 2, /**< Peripheral busy with previous operation. */
} foo_status_t;
```

---

### Rule 5 — Macros and Constants

```c
/** Maximum RX ring buffer size in bytes. */
#define FOO_RX_BUF_SIZE  256U
```

Rules:
- Macro comment must be **single-line** `/** */` only
- Use simple plain words — no long technical phrases

---

### Rule 6 — Private (static) Functions

```c
/**
 * @brief   Check whether the RX ring buffer is empty.
 * @return  true if empty, false if not.
 */
static bool is_rx_empty(void)
```

Same length limits as Rule 2 — `@brief` at most 3 lines total, simple words only.

---

## What NOT to Do

- Do not start `@brief` with "This function..." — use a verb directly
- Do not use `//` style comments for Doxygen blocks
- Do not leave any public function without `@brief`
- Do not list value ranges, register addresses, or field names in `@param`/`@return`
- Do not write `@brief` blocks longer than 3 lines (applies to functions and file headers)
- Do not write file header body descriptions longer than 2 lines
- Do not write macro comments as multi-line blocks — single-line `/** */` only
- Do not use long technical phrases — keep words simple and sentences short

---

## Application Checklist

- [ ] Asked user for `@author` name (Step 1)
- [ ] File header: `@file`, `@brief`, `@author` on every new file
- [ ] Every public function: `@brief`, `@param[direction]`, `@return` (if non-void)
- [ ] Every struct: `@brief` + inline `/**<` member comments
- [ ] Every enum: `@brief` + inline `/**<` value comments
- [ ] Every `#define`: single-line `/** */` comment only — no multi-line blocks
- [ ] Private `static` functions: at minimum `@brief`
- [ ] All `@brief` lines start with a verb
- [ ] `@brief` block (including optional body) is at most 3 lines — applies to functions and file headers
- [ ] File header body description is at most 2 lines
- [ ] `@param` and `@return` are short — no value ranges or register details
- [ ] Simple words only — no long technical phrases
