# HITCON 2026 Wargame - Technical Methodology

> **Date**: August 21-23, 2026
> **Purpose**: Document the technical methodology used in the HITCON 2026 Wargame PHP Composer Security Challenge.

---

## 1. AI-to-AI Collaboration Framework

### Division of Labor

```
+------------------------------------------+
|         AI Security Analyzer             |
|  - Full-source taint analysis            |
|  - Root-cause diagnosis                  |
|  - Heuristic adaptation                  |
+----------------------------------|-------+
                                   |
                    Task Specification
                                   v
+------------------------------------------+
|     Freebuff Runner / Verifier           |
|  - Queue watching & state machine        |
|  - Sandbox (Docker) execution            |
|  - Feedback collector (HTTP/Error logs)  |
+------------------------------------------+
```

### Closed-Loop Workflow

1. **Analyze**: Analyzer produces TaskSpec from SAST data
2. **Verify**: Runner executes in Docker sandbox
3. **Diagnose**: Collect HTTP status, error logs, output
4. **Adapt**: Analyzer performs root-cause diagnosis and adjusts parameters
5. **Retry**: Loop until all targets achieved or time exhausted

### Communication Protocol

Communication via file-system JSON queues (fully decoupled async):

- **Task Queue**: `data/queue/<task_id>.json` - TaskSpec from Analyzer to Runner
- **Feedback Queue**: `data/dossiers/<package>.json` - Execution results from Runner to Analyzer

**TaskSpec format**:
```json
{
  "task_id": "pkg_owasp_phprbac_2.0.0_7.4.33",
  "package_name": "owasp/phprbac",
  "version": "2.0.0",
  "php_version": "7.4.33",
  "retry_count": 0,
  "max_retries": 5,
  "endpoint": "/vendor/owasp/phprbac/PhpRbac/install.php",
  "method": "GET",
  "strategy": "installer_file_injection"
}
```

### Key Lessons
- **Static analysis alone is insufficient** - 43,924 findings, only 1 confirmed exploitable
- **Dynamic verification is essential** - Docker exec testing revealed false positives
- **AI collaboration requires tight feedback loops** - Version mismatches (1.2.0 vs 3.2.0) wasted significant time

---

## 2. SAST False Positive Analysis Methodology

### Background
- 43,924 findings across 217 packages (4,701 total challenges)
- Pattern-based SAST (grep/regex) rules for 12 vulnerability categories
- After review: only 1 package (owasp/phprbac) confirmed exploitable from web

### False Positive Classification (5 Types)

#### Type 1: Framework Internal DI/Event Dispatch (~60%)
**Pattern**: Variable function call with variable (`$func($args)`)
**Root cause**: Framework dependency injection and event dispatch mechanisms
**Example**: `$listener->$eventName($eventArgs)` in Symfony EventManager
**Why FP**: Variables injected by framework container at startup, not controllable via HTTP

#### Type 2: Test Framework assert/eval (~15%)
**Pattern**: Direct eval() execution / Dangerous assert() call
**Root cause**: Test framework code that is not executed in production
**Example**: PHPUnit assert patterns, Rector rule definitions
**Why FP**: assert() disabled by default; create_function in string templates, not executable

#### Type 3: Class Definitions Without Web Entry (~10%)
**Pattern**: eval() / unserialize() / exec() inside Class methods
**Root cause**: Library code that is never directly accessed via HTTP
**Example**: Symfony Console Cursor.php, Doctrine EntityGenerator
**Why FP**: Requesting .php files only completes Class definitions (200 OK, 0 bytes)

#### Type 4: Functions Behind Unreachable Code Paths (~10%)
**Pattern**: Dangerous functions behind conditional checks
**Root cause**: Debug-only code, CLI-only handlers, authentication requirements
**Example**: eval() inside `if ($debug && DEV_MODE)`
**Why FP**: Conditions cannot be triggered from HTTP requests

#### Type 5: Dead Code / Legacy (~5%)
**Pattern**: Removed language features, unused utilities
**Root cause**: Historical code that is no longer executed
**Example**: preg_replace /e modifier (removed in PHP 7.4)
**Why FP**: Language/runtime prevents execution

### Key Insight
**Pattern-based SAST lacks data flow analysis (taint analysis)**. It cannot determine whether user input actually reaches the sink (dangerous function). A proper SAST tool needs:
1. **Source identification**: Where does user input enter? ($_GET, $_POST, $_COOKIE, etc.)
2. **Sink identification**: What dangerous functions exist? (eval, system, exec, etc.)
3. **Taint propagation**: Can user input flow from Source to Sink through data transformations?
4. **Sanitization check**: Are there any input validation/sanitization steps in between?

Without this, pattern-based SAST produces overwhelming false positive rates that obscure real vulnerabilities.

---

## 3. Vulnerability Triage Methodology

### Background
- 73 "package version x security advisory" hits across 3 Composer environments
- Naive approach: create 73 separate patch tickets
- Efficient approach: merge into 3 patch tickets by deployment boundary

### Triage Principles
1. **Merge by deployment boundary** - Same deployment unit, same owner, same root fix
2. **Prioritize by real-world impact** - Not all CVEs are equally exploitable
3. **Distinguish test data from production** - eval fixtures are not product dependencies

### Triage Results

| Deployment Boundary | Advisories Hit | Why Merge | Fix Condition |
|---------------------|---------------|-----------|---------------|
| JMose + Symfony 3.4 + Twig 2.16 | 36 | All blocked by same old JMose constraint | Replace JMose, migrate Symfony/Twig |
| Schickling Backup + Laravel 4 stack | 32 | Backup package bundles Laravel, AWS SDK, Symfony, phpseclib | Retire old job/keys, use maintained backup |
| Zend Framework 2.5 skeleton | 5 | Zend aggregate abandoned, old PHPUnit dev chain | Migrate to Laminas |

### Key Lessons
- **73 CVEs -> 3 tickets** by understanding deployment boundaries
- **Don't treat every CVE as independent** - many are in the same dependency graph
- **Test fixtures need isolation governance, not patching**

---

## 4. Global Security Audit Approach

### Scan Scope
- 4,701 challenges (3,544 unique package versions)
- 12 vulnerability categories scanned
- 32 threads, 971.78 seconds total scan time

### Results Summary

| Severity | Count | Percentage |
|----------|-------|------------|
| CRITICAL | 6,102 | 12.9% |
| HIGH | 27,874 | 58.8% |
| MEDIUM | 9,099 | 19.2% |
| LOW/INFO | 4,324 | 9.1% |

### Top Attack-Potential Packages
1. openmage/magento-lts:1.9.3.1 (2,981 findings)
2. openmage/magento-lts:20.0.14 (2,729 findings)
3. pimcore/pimcore:3.1.1 (1,694 findings)

### Limitations
- High finding count does not equal high exploitability
- Most findings are in framework internals, not user-accessible code
- Need to combine SAST with dynamic testing for accurate risk assessment

---

## 5. Exploit Development Methodology

### Environment Constraints
- Exploit runs in isolated container with /exploit challenge_host
- Only /tmp writable
- 60 second time limit, 128 MiB memory
- Dependencies: requests + stdlib only
- Network: internal Docker only, no external access

### Exploit Development Process
1. **Identify web entry points**: Find PHP files with $_GET/$_POST/$_COOKIE
2. **Trace data flow**: Follow user input through code to dangerous functions
3. **Craft payload**: Develop exploit that achieves code execution
4. **Test in sandbox**: Use run.sh to verify in Docker container
5. **Handle constraints**: .php suffix, file_exists(), phar.readonly, etc.

### Exploit Scripts
Located in `bot/submit/`:
- `v_01_owasp_phprbac_7.4.33.py` - AC verified
- `v_02_owasp_phprbac_8.4.py` - AC verified
- `v_03_internations_http-mock_7.4.33.py` - AC verified
- `v_04_internations_http-mock_8.4.py` - AC verified
