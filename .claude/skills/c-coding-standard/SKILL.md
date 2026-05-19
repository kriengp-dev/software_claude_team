---
name: c-coding-standard
description: Enforce C language coding standards on all C code being written or modified. Reference this skill whenever writing or editing .c or .h files.
origin: ECC
---

## When to Use

- Whenever writing or modifying `.c` or `.h` files
- After implementing a new driver, module, or ISR
- During code review to verify compliance before commit
- Use together with `/doxygen-pattern` for full coverage

---

Apply the following coding standards to **all** C code written or modified in this task.

---

## 1. Naming Conventions

| Entity | Convention | Example |
|--------|-----------|---------|
| Variables (local) | `snake_case` | `rx_count`, `byte_index` |
| Variables (global) | `g_snake_case` | `g_system_tick` |
| Variables (static file-scope) | `s_snake_case` | `s_rx_head` |
| Constants / Macros | `UPPER_SNAKE_CASE` | `MAX_BUFFER_SIZE` |
| Functions | `module_verb_noun` | `uart_read_byte` |
| Types (struct/enum/typedef) | `snake_case_t` | `uart_config_t` |
| Enum values | `MODULE_VALUE` | `UART_STATUS_OK` |
| Pointers | no extra prefix — type makes it clear | `uint8_t *p_buf` — use `p_` prefix for pointer variables |

---

## 2. File Structure

Every `.c` file must follow this order:

```c
/* 1. File header (Doxygen) */
/* 2. Includes — system headers first, then project headers */
#include <stdbool.h>
#include "module.h"

/* 3. Private macros and constants */
#define MODULE_TIMEOUT_MS   100U

/* 4. Private type definitions */
typedef struct { ... } module_priv_t;

/* 5. Private function prototypes */
static void helper_function(void);

/* 6. Private variables (static) */
static uint8_t s_buffer[BUFFER_SIZE];

/* 7. Public function implementations */

/* 8. Private function implementations */
```

Every `.h` file must follow this order:

```c
/* 1. File header (Doxygen) */
/* 2. Include guard */
#ifndef MODULE_H
#define MODULE_H

/* 3. Includes */
/* 4. Public macros and constants */
/* 5. Public type definitions */
/* 6. Public function declarations */

#endif /* MODULE_H */
```

---

## 3. Types

- Use **standard C types** as the default:
  `int`, `unsigned int`, `long`, `unsigned long`, `char`, `unsigned char`
- Use `bool` (from `<stdbool.h>`) for true/false flags — never `int` as boolean
- Use `size_t` for sizes and counts that cannot be negative
- Use `unsigned char` for binary/byte data; reserve `char` for null-terminated strings only
- Avoid fixed-width types (`uint8_t`, `uint16_t`, `uint32_t`, etc.) — use them only when the exact bit-width is a hard hardware or protocol requirement and must be documented with a comment explaining why

---

## 4. Functions

- Maximum **50 lines** per function body (excluding comments and blank lines)
- Maximum **4 levels** of nesting — use early returns or helper functions to reduce depth
- Maximum **5 parameters** per function — group related params into a struct if more are needed
- Every function must have **one clearly defined purpose**
- Functions that can fail must return a status code — never ignore error returns
- Use `const` on pointer parameters that are not modified:
  ```c
  void foo_write(const unsigned char *data, unsigned int len);
  ```
- **Write each function call as a single line** — do not split one call across multiple lines:
  ```c
  /* Wrong — one call split across lines */
  (void)reg_32b_write(
      (uint32_t)(BASE | OFFSET),
      (uint32_t)value);

  /* Right — one call, one line */
  (void)reg_32b_write((uint32_t)(BASE | OFFSET), (uint32_t)value);
  ```

---

## 5. Variables

- Declare variables at the **narrowest scope** possible
- Initialize variables at declaration — never leave them uninitialized
- Use `static` for all file-scope variables and functions not exposed in a header
- Mark variables shared between ISR and task context as `volatile`:
  ```c
  static volatile unsigned int s_rx_head = 0;
  ```
- Do not use global mutable variables unless unavoidable; pass state explicitly

---

## 6. Constants and Macros

- Replace all magic numbers with named constants:
  ```c
  /* Wrong */
  if (len > 256) { ... }

  /* Right */
  #define UART_RX_BUF_SIZE  256U
  if (len > UART_RX_BUF_SIZE) { ... }
  ```
- Append `U` suffix to unsigned integer literals **in `#define` constants only**: `#define FOO 256U`, `#define MASK 0xFFU`
- Append `UL` for 32-bit unsigned **in `#define` constants only**: `#define BASE 0xDEADBEEFUL`
- **Never use `U` or `UL` suffix in code statements, comparisons, return values, or expressions:**
  ```c
  /* Wrong — U suffix in code */
  if (x != 0U) { ... }
  for (unsigned int i = 0U; i < len; i++) { ... }
  buf[i] = 0U;
  return 0U;

  /* Right — plain integer in code */
  if (x != 0) { ... }
  for (unsigned int i = 0; i < len; i++) { ... }
  buf[i] = 0;
  return 0;
  ```
- Macro parameters must be parenthesized; the entire expression must be parenthesized:
  ```c
  #define MIN(a, b)  (((a) < (b)) ? (a) : (b))
  ```
- Prefer `enum` over `#define` for related integer constants

---

## 7. Control Flow

- Always use braces `{ }` for `if`, `else`, `for`, `while`, `do` — even single-line bodies
- Opening brace `{` **always goes on a new line** (Allman style) — applies to all block constructs including `if`, `else`, `for`, `while`, `do`, `switch`, and function bodies:
  ```c
  /* Wrong — brace on same line */
  if (error) return;
  if (error) {
      return;
  }

  /* Right — brace on new line */
  if (error)
  {
      return;
  }

  for (unsigned int i = 0; i < len; i++)
  {
      buf[i] = 0;
  }

  void foo_init(void)
  {
      /* ... */
  }
  ```
- Use `switch` with an explicit `default` case — always handle the unexpected:
  ```c
  switch (state)
  {
      case STATE_IDLE:    handle_idle();    break;
      case STATE_RUN:     handle_run();     break;
      default:            handle_error();   break;
  }
  ```
- Prefer early return over deeply nested `if` chains — but if the total `return` count would exceed 2, use a result variable with a single exit instead:
  ```c
  /* Wrong — three returns */
  int foo_read(uint32_t *p_val)
  {
      if (p_val == NULL) { return FOO_ERR; }
      if (reg_read(BASE, p_val) != 0) { return FOO_ERR; }
      return FOO_OK;
  }

  /* Right — result variable, single exit */
  int foo_read(uint32_t *p_val)
  {
      int ret = FOO_OK;

      if (p_val == NULL)
      {
          ret = FOO_ERR;
      }
      else if (reg_read(BASE, p_val) != 0)
      {
          ret = FOO_ERR;
      }

      return ret;
  }
  ```

---

## 8. Memory

- **No dynamic allocation** (`malloc`, `calloc`, `realloc`, `free`) in bare-metal firmware
- Use static or stack allocation only
- Keep stack allocations small — avoid large local arrays on targets with limited RAM
- Zero-initialize structs at declaration:
  ```c
  uart_config_t cfg = { 0 };
  ```

---

## 9. Pointers

- Always check pointer parameters for `NULL` before dereferencing:
  ```c
  if (p_cfg == NULL) {
      return MODULE_ERROR_NULL;
  }
  ```
- Never cast between unrelated pointer types without explicit justification in a comment
- Do not use pointer arithmetic beyond array indexing — use index variables instead

---

## 10. Integers and Arithmetic

- Avoid signed/unsigned mixing — cast explicitly when comparing or assigning
- Guard against integer overflow on arithmetic used for sizes or indices:
  ```c
  /* Wrong — may overflow */
  unsigned int next = (head + 1) % BUF_SIZE;

  /* Right — cast ensures no implicit promotion issue */
  unsigned int next = (unsigned int)((head + 1) % BUF_SIZE);
  ```
- Do not use bitwise operators on signed types

---

## 11. Interrupts and Concurrency

- Protect shared data between ISR and task with a critical section:
  ```c
  __disable_irq();
  /* access shared variable */
  __enable_irq();
  ```
- Keep ISR bodies minimal — set a flag or write to a ring buffer; do processing in task context
- Never call blocking functions inside an ISR (`HAL_Delay`, `printf`, mutex lock)
- Never call non-ISR-safe OS APIs from an ISR

---

## 12. Comments

- Write comments in **simple, plain English** — short words, short sentences, one idea per line
- Explain **why**, not what (the code already shows what it does)
- Use Doxygen `/** */` blocks for all public APIs (see `/doxygen-pattern`)
- Use `/* */` for inline explanatory comments — never `//` in production embedded code
- **Inline comments inside a function body must not exceed 2 lines**
- Keep comments as **short summaries** — do not list value ranges or reproduce register field details
- Use simple common words — avoid long technical phrases
- Mark workarounds and hardware quirks clearly:
  ```c
  /* WORKAROUND: SPI CS needs 500 ns gap before next transfer */
  ```
- Wrong vs right:
  ```c
  /* Wrong — verbose, lists values, complex sentence */
  /* Guard the 16-bit hardware LEN register — reject zero and over-length transfers
     that exceed the maximum value of 0xFFFF supported by the NUM register. */

  /* Right — short summary, simple words */
  /* reject zero or oversized length */
  ```

---

## 13. Includes and Dependencies

- Every `.h` file must be self-contained — include everything it needs to compile standalone
- Use include guards (`#ifndef`) — not `#pragma once` (portability)
- Do not include `.c` files
- Do not use relative paths with `..` in includes — configure include paths in the build system

---

## Checklist — apply before presenting any C code

- [ ] All variables use standard C types (`int`, `unsigned int`, `unsigned char`, etc.); fixed-width types only when bit-width is a hard hardware/protocol requirement
- [ ] All magic numbers replaced with named `#define` or `enum` constants
- [ ] `U`/`UL` suffix used only in `#define` constants — never in code statements, comparisons, or expressions
- [ ] Functions with more than 2 `return` statements use a result variable and single exit point
- [ ] All `if`/`else`/`for`/`while` bodies have braces
- [ ] Opening brace `{` is always on a new line (Allman style) for all block constructs
- [ ] All `switch` statements have a `default` case
- [ ] All pointer parameters checked for `NULL` where applicable
- [ ] No `malloc`/`free` in bare-metal code
- [ ] All file-scope non-public symbols are `static`
- [ ] All variables shared with ISR are `volatile`
- [ ] No blocking calls inside ISR
- [ ] Functions are ≤ 50 lines and ≤ 4 levels deep
- [ ] Every function that can fail returns a status code
- [ ] Include guard present on every `.h` file
- [ ] Each function call is written on a single line — not split across multiple lines
- [ ] All inline comments are in simple, plain English — short words and short sentences
- [ ] Inline comments inside a function body are at most 2 lines
- [ ] No value ranges or register field details in comments — summary only
