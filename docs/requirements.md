# Personal History - Vital Requirements

**Version:** 1.0  
**Date:** 2026-04-05  
**Author:** William Acevedo & OpenClaw Assistant  
**Status:** Vital Requirements Analysis

## 🎯 Primary Purpose

**"Irrefutable Verification" of personal activities with cryptographic proof, while maintaining user privacy and data sovereignty.**

## 🔐 Most Vital Requirements

### **1. Cryptographic Integrity (Non-Negotiable)**
- **Requirement:** All data must be cryptographically verifiable
- **Why Vital:** Without this, there's no "irrefutable verification"
- **Implementation:** Ed25519 signatures, SHA-256 hashes, forward-secure hash chains
- **Constraint:** Must work without root access (user-level installation)

### **2. User Data Sovereignty**
- **Requirement:** Users completely own their data
- **Why Vital:** Core to the "Right to Share" philosophy
- **Implementation:** Local storage, no required cloud, open format
- **Constraint:** Must be usable by average users (not just developers)

### **3. Privacy by Design**
- **Requirement:** Exact timing hidden, duration visible
- **Why Vital:** Protects sensitive patterns while allowing useful analysis
- **Implementation:** Cryptographic commitments for exact times
- **Constraint:** Must still enable multi-device sync and conflict detection

### **4. Practical Usability**
- **Requirement:** 30-second activity logging, works offline
- **Why Vital:** If it's not easy to use, people won't use it
- **Implementation:** Smart duration parsing, time tracking commands
- **Constraint:** Must balance security with convenience

## 🚨 The Critical Tension

### **Vital Requirement #1 vs. Vital Constraint:**
- **Need:** Real cryptography (Ed25519, SHA-256)
- **Constraint:** User-level installation (no root, no system packages)
- **Problem:** `cryptography` library needs C dependencies (OpenSSL)

### **This is THE MOST CRITICAL architectural decision** because:
1. **Without cryptography:** No "irrefutable verification" (defeats primary purpose)
2. **Without user-level install:** Limits adoption (only users with root access)
3. **Current v0.01:** Has simulated mode (defeats the purpose)

## 💡 Solution Options (Ranked by Vitality)

### **Option A: Modular Crypto Backend (Most Vital)**
- **Pros:** Solves both requirements (crypto + user-level install)
- **Cons:** Most complex to implement
- **Approach:** Abstract interface with multiple implementations:
  - `cryptography` backend (best security, needs system deps)
  - `pynacl` backend (pure Python, user-level install)
  - `ecdsa` backend (alternative pure Python)

### **Option B: Require Cryptography + Clear Instructions**
- **Pros:** Best security guarantees
- **Cons:** Installation barrier for some users
- **Approach:** Fail fast with excellent documentation for:
  - Virtual environments with build tools
  - System package alternatives
  - Docker containers

### **Option C: Static/Bundled Distribution**
- **Pros:** Truly self-contained, no dependencies
- **Cons:** Platform-specific builds, complex distribution
- **Approach:** PyInstaller/staticx bundles with all dependencies

## 📊 Vitality Matrix

| Requirement | Vitality | Current Status | Gap |
|------------|----------|----------------|-----|
| Cryptographic Proof | 🔴 **CRITICAL** | ⚠️ Simulated mode | Needs real crypto |
| User-Level Install | 🔴 **CRITICAL** | ❌ Problematic | Crypto dependencies |
| Privacy (hidden times) | 🟡 **HIGH** | ✅ Implemented | Working well |
| Ease of Use | 🟡 **HIGH** | ✅ CLI implemented | Good foundation |
| Multi-Device Sync | 🟠 **MEDIUM** | ⏳ Planned | Needs conflict resolution |
| Data Portability | 🟢 **LOW** | ✅ JSON format | Good |

## 🎯 Immediate Vital Requirements (Next Steps)

### **1. Fix the Cryptography Dilemma**
- **Decision:** Choose Option A, B, or C above
- **Action:** Implement chosen approach
- **Success:** Real cryptography + user-level installation

### **2. Make Verification Actually Work**
- **Decision:** Remove simulated mode or clearly mark as INSECURE
- **Action:** Fix verification in v0.01 or implement v0.02
- **Success:** `ph verify` works with real cryptographic proof

### **3. Document the Installation Challenge**
- **Decision:** Be transparent about the cryptography dependency issue
- **Action:** Create clear installation guide with workarounds
- **Success:** Users can install successfully in their environment

## 🤔 The Core Question

**Which is more vital to the primary purpose?**
- A) **Cryptographic proof** (even if some users can't install)
- B) **Accessibility** (even if with reduced security)
- C) **Both** (through modular architecture)

**Analysis:** **Option C (Both)** is most vital because:
1. Without cryptographic proof → No "irrefutable verification"
2. Without user-level install → Limited to technical users with root
3. Personal History needs BOTH to fulfill its purpose for a wide audience

## 📝 Decision Framework

### **When evaluating design choices, ask:**
1. Does this support **cryptographic proof**?
2. Does this enable **user-level installation**?
3. Does this preserve **user privacy**?
4. Does this maintain **practical usability**?

### **Priority Order:**
1. **Cryptographic integrity** (non-negotiable for core purpose)
2. **User accessibility** (without which the tool has limited impact)
3. **Privacy protection** (essential for personal data)
4. **Ease of use** (necessary for adoption)

## 🔄 Living Document

This document captures the most vital requirements for Personal History. It should be:
- **Referenced** during design discussions
- **Updated** when requirements evolve
- **Used as a filter** for implementation decisions
- **Shared understanding** between collaborators

---

*This document focuses on VITAL requirements only. For comprehensive requirements, see the full requirements document in the workspace.*