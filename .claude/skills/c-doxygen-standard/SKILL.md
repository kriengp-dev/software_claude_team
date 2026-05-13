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
@author に記載される名前を教えてください。
(例: Tanaka Kenji / K. Tanaka / NDR開発チーム)
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
 * <Optional: hardware context, design decisions, timing constraints>
 */
```

---

### Rule 2 — Public Functions

```c
/**
 * @brief   <One-sentence description — start with a verb>
 *
 * <Optional: preconditions, side effects, thread-safety, hardware state>
 *
 * @param[in]     name   Description
 * @param[out]    name   Description (written by this function)
 * @param[in,out] name   Description (read and written)
 * @return              Description; list enum values if applicable.
 *
 * @note    Optional note.
 * @warning Optional warning (e.g. "Not ISR-safe").
 */
```

`@return` is required for every non-`void` function.

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

---

### Rule 6 — Private (static) Functions

```c
/**
 * @brief   Check whether the RX ring buffer is empty.
 * @return  true if empty, false otherwise.
 */
static bool is_rx_empty(void)
```

---

## What NOT to Do

- Do not start `@brief` with "This function..." — use a verb directly
- Do not use `//` style comments for Doxygen blocks
- Do not leave any public function without `@brief`

---

## Application Checklist

- [ ] Asked user for `@author` name (Step 1)
- [ ] File header: `@file`, `@brief`, `@author` on every new file
- [ ] Every public function: `@brief`, `@param[direction]`, `@return` (if non-void)
- [ ] Every struct: `@brief` + inline `/**<` member comments
- [ ] Every enum: `@brief` + inline `/**<` value comments
- [ ] Every `#define`: single-line `/** */` comment
- [ ] Private `static` functions: at minimum `@brief`
- [ ] All `@brief` lines start with a verb
