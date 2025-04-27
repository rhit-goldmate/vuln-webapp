# 🛡️ Penetration Test Report: Vulnerable Web App

---

## 1. Executive Summary

**Test Date**: April 27, 2025  
**Tested System**: Vulnerable Web Application (localhost:5000)

**Objective**:  
To identify and assess security vulnerabilities in a prototype web application before production deployment.

**Summary of Findings**:  
The web application was found to be vulnerable to several critical security flaws including SQL Injection, Cross-Site Scripting (XSS), Unrestricted File Upload, and Missing Security Headers. These vulnerabilities could allow attackers to gain unauthorized access, execute arbitrary code, and compromise user data.

**Overall Risk Rating**: **Critical**

---

## 2. Methodology

The following methodology was used during the assessment:

- **Reconnaissance**: Identifying technologies, open ports, and application structure.
- **Threat Modeling**: Identifying attack surfaces and entry points.
- **Vulnerability Analysis**: Testing for known vulnerabilities through manual and automated techniques.
- **Exploitation**: Confirming the existence and impact of vulnerabilities through safe proof-of-concept (PoC) attacks.
- **Reporting**: Documenting findings, risk ratings, and actionable recommendations.

**Tools Used**:
- Browser-based manual testing
- Burp Suite Community Edition
- Curl
- Nmap
- Gobuster

---

## 3. Detailed Findings

### 3.1 SQL Injection in Login Form

**Severity**: Critical  
**Affected Endpoint**: `/login`

**Description**:  
The login mechanism directly incorporates user input into SQL queries without proper sanitization, making it vulnerable to SQL Injection.

**Proof of Concept (PoC)**:
- Input into the username and password fields:
```sql
'OR '1'='1
```
- Result: Login was bypassed successfully without valid credentials.

**Risk**:  
An attacker could log in as any user, access sensitive data, or perform unauthorized actions.

**Recommendations**:
- Use **parameterized queries** or **prepared statements**.
- Implement **input validation** and **output encoding**.

---

### 3.2 Cross-Site Scripting (XSS) in Comment Section

**Severity**: High  
**Affected Endpoint**: `/comment`

**Description**:  
User input in the comment section is not sanitized before being rendered back to the user, allowing for persistent XSS attacks.

**Proof of Concept (PoC)**:
- Submitted the following payload:
```html
<script>alert('XSS')</script>
```
- Visiting the comments page caused a popup alert.

**Risk**:
Attackers could execute malicious JavaScript in users' browsers, steal session cookies, or perform actions on behalf of the users.

**Recommendations**:
- **Sanitize and encode** all user input before rendering.
- Implement a **Content Security Policy (CSP)** header.

---

### 3.3 Unrestricted File Upload

**Severity**: High  
**Affected Endpoint**: `/upload`

**Description**:  
The application allows uploading files without validating file types or restricting file content.

**Proof of Concept (PoC)**:
- Uploaded a file named evil.html containing:
```html
<h1>Hacked!</h1><script>alert('Owned')</script>
```
- Accessed http://localhost:5000/uploads/evil.html and the script executed in the browser.

**Risk**:
Attackers can upload malicious scripts, shells, or executables to the server, potentially leading to full server compromise.

**Recommendations**:
- Restrict file uploads to a whitelist of specific file types (e.g., .jpg, .png).
- Store uploaded files **outside the web root**.
- Generate **randomized file names** for uploads.
- Scan uploaded files for malicious content.

---

## 4. Conclusion

The vulnerable web application presents several critical issues that must be addresed before any production deployment.
By remediating these vulnerabilities and adopting secure coding practices, the security posture of the application can be significantly strengthened.

**Recommendations Summary**:
- Sanitize and validate all user inputs.
- Implement parameterized database queries.
- Restrict and validate file uploads.
- Configure appropriate security headers.
- Regularly perform penetration testing and code reviews.

---

## 5. Appendix

**Tools Used**: 
- Burp Suite Community Edition
- Nmap
- Gobuster
- Curl
- Manual Browser Testing

**Testers**:
- Taylor Goldman

**References**:
- OWASP Top 10 (https://owasp.org/www-project-top-ten/)
- CWE Common Weakness Enumeration (https://cwe.mitre.org/)