# HITCON 2026 Wargame - PHP Composer Security Challenge Writeup

> **Team**: Buffy (Freebuff Runner) + Antigravity (Analyzer)
> **Competition**: HITCON 2026 Wargame - PHP Composer Security Challenge
> **Result**: 4 AC (Full Solve), 4/76 challenges solved
> **Date**: August 21-23, 2026

---

## 1. Competition Overview

### Challenge Structure
- **4,701 total challenges** across **3,544 unique package versions**
- Each challenge: one PHP Composer package installed in a Docker container
- Goal: exploit package vulnerabilities to read flags

### Scoring
| Level | Flag | Score |
|-------|------|-------|
| PA (Partial Attack) | /flag1 (readable, 0444) | 50% of stars |
| AC (Full Attack) | /readflag (SUID 4755, reads /flag2) | 100% of stars |

### Our Result
| # | Package | PHP | Attack | Status |
|---|---------|-----|--------|--------|
| 1 | owasp/phprbac 2.0.0 | 7.4.33 | install.php -> file_put_contents -> RCE | AC |
| 2 | owasp/phprbac 2.0.0 | 8.4 | Same as above | AC |
| 3 | internations/http-mock 0.14.0 | 7.4.33 | @unserialize($_COOKIE) -> SuperClosure eval() -> RCE | AC |
| 4 | internations/http-mock 0.12.0 | 8.4 | Same as above | AC |

**Leaderboard**: Top team solved 76 challenges (190,894 points). We solved 4.

---

## 2. Challenge Environment

### Container Specs
| Setting | Value |
|---------|-------|
| Base image | php:8.4-apache-bookworm / php:7.4.33-apache-bullseye |
| Web root | /var/www/html |
| AllowOverride | All (.htaccess works, but HTTP write blocked) |
| auto_prepend_file | Not set |
| disable_functions | Empty (all functions available) |
| open_basedir | Empty (no directory restriction) |
| phar.readonly | On |
| session.auto_start | Off |
| session.upload_progress.enabled | On |
| Composer install | --no-dev --prefer-dist (excludes tests/, examples/) |
| File ownership | www-data writable |

### Apache Configuration
- SetHandler application/x-httpd-php via FilesMatch .php$
- Options -Indexes (no directory listing)
- Network: internal Docker only (internal: true), no external access

### Exploit Constraints
- Executed in isolated container: /exploit challenge_host
- Writable directory: only /tmp
- Time limit: 60 seconds
- Memory limit: 128 MiB (exploit) / 256 MiB (challenge)
- Dependencies: only requests (py3-requests) + stdlib

---

## 3. Successful Exploits

### 3.1 owasp/phprbac - PHP Code Injection via install.php

**Vulnerability**: install.php accepts user-controlled database auth parameter and passes it to file_put_contents(), enabling arbitrary PHP code injection.

**Exploit Chain**:
1. GET /vendor/owasp/phprbac/PhpRbac/install.php to get CSRF token
2. POST with auth payload containing PHP code -> written to config file
3. Config file auto-loaded on subsequent requests -> RCE
4. Execute /readflag -> AC

**Score**: 445 stars x 2 (7.4.33 + 8.4) = 890 stars

### 3.2 internations/http-mock - Deserialization RCE via SuperClosure

**Vulnerability**: @unserialize($_COOKIE) in index.php triggers a gadget chain through SuperClosure SerializableClosure eval() method.

**Exploit Chain**:
1. Craft serialized PHP object with SuperClosure gadget chain
2. Send as cookie to /vendor/internations/http-mock/public/index.php
3. Deserialization triggers eval() -> RCE
4. Execute /readflag -> AC

**Gadget Chain**: SuperClosure SerializableClosure -> __destruct() -> eval() -> PHP code execution

**Score**: 395 stars x 2 (7.4.33 + 8.4) = 790 stars

---

## 4. False Positive Analysis - Why 95% of SAST Findings Were Useless

### The Problem
Our SAST scanner produced **43,924 findings** across 217 packages. After code review and Docker testing, **only 1 package (owasp/phprbac) was confirmed exploitable from the web**.

### False Positive Classification

#### Type 1: Framework Internal DI/Event Dispatch (~60%)
Framework dependency injection and event dispatch mechanisms. Variables injected by container at startup - **not controllable via HTTP requests**.

#### Type 2: Test Framework assert/eval (~15%)
PHPUnit assert() disabled by default. Rector create_function in string template, not executable code.

#### Type 3: Class Definitions Without Web Entry (~10%)
95%+ of dangerous functions encapsulated inside Class methods. Requesting .php files only completes Class definitions, returning 200 OK (0 bytes).

#### Type 4: Functions Behind Unreachable Code Paths (~10%)
Dangerous functions behind conditions untriggerable from HTTP (debug flags, CLI-only handlers).

#### Type 5: Dead Code / Legacy (~5%)
preg_replace /e (removed in PHP 7.4), unused utilities, commented-out code.

### Key Insight
**Pattern-based SAST lacks data flow analysis** - cannot determine whether user input reaches the sink. Proper SAST needs taint analysis (Source -> Sink).

---

## 5. Failed Attempts and Lessons Learned

### 5.1 Adminer (vrana/adminer 5.5.1) - 21 solves
- Rogue MySQL Server: FAIL - no mysqli/pdo_mysql extensions in PHP 8.4
- SQLite login-password-less: PARTIAL - SQLite plugin auth works, SQL limited
- SQLite ATTACH DATABASE: FAIL - ATTACH rejects arbitrary file paths
- **Password Paradox**: login() requires non-empty, SQLite connect() requires empty

### 5.2 potsky/pimp-my-log 1.7.10
configure.php writes from template, no arbitrary PHP injection possible.

### 5.3 pingplusplus/pingpp-php - 8-9 Solves
LFI blocked by .php suffix auto-appended + file_exists() blocking PHP wrappers.

### 5.4 Infrastructure Attacks (All Failed)
WebDAV, .htaccess write, .user.ini write, Phar deserialization, Session upload + LFI.

### 5.5 Unsolved High-Solve Packages

| Package | PHP | Solves | Problem |
|---------|-----|--------|---------|
| oddvalue/laravel-drafts | 8.4 | 27 | vendor/ all class definitions, no HTTP input |
| creolab/laravel-modules | 8.4 | 20 | boris REPL + SuperClosure, no HTTP trigger |
| schickling/backup | 7.4.33 | 18 | Same as above |
| lexpress/symfony1 | 7.4.33 | 15 | No web entry points |
| friendsofsymfony1/symfony1 | 7.4.33 | 14 | No web entry points |

---

## 6. Key Technical Discoveries

### 6.1 /readflag Has No Anti-Bot
No math question, no stdin interaction. Any RCE can execute system('/readflag 2>&1') directly.

### 6.2 Apache AllowOverride All
.htaccess auto_prepend_file works, but cannot write .htaccess via HTTP.

### 6.3 /var/www/html Is www-data Writable
Any file write vulnerability can create webshell or .htaccess.

### 6.4 Session Upload Progress
session.upload_progress.enabled = On writes user-controlled serialized data to /tmp/sess_*. Need LFI to trigger.

### 6.5 Composer --no-dev Excludes Entry Points
tests/, examples/, and export-ignore directories removed.

---

## 7. Global Security Audit Statistics

| Severity | Count | Percentage | Core Risk |
|----------|-------|------------|-----------|
| CRITICAL | 6,102 | 12.9% | eval(), assert(), create_function(), preg_replace /e |
| HIGH | 27,874 | 58.8% | system/exec, file_put_contents, unserialize, include |
| MEDIUM | 9,099 | 19.2% | readfile, MD5/SHA1, loose comparison (==), SSRF |
| LOW/INFO | 4,324 | 9.1% | mt_rand, uniqid, phpinfo, var_dump |

---

## 8. Unresolved Questions

1. oddvalue/laravel-drafts: tested v1.2.0, challenge was v3.2.0
2. MultiViews: /vendor/bin/boris (PHP REPL) could trigger RCE if enabled
3. Composer autoload side-effects: autoload_files.php file writes?
4. Symfony1 autoloader: exploitable include paths?
