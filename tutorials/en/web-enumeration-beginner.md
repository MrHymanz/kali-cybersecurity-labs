# Beginner tutorial: web enumeration

## Scope and learning objective

- Permitted lab target: `http://127.0.0.1:3000`
- Objective: explore an unknown web application systematically, starting with passive techniques.
- Out of scope: other local services, the LAN, and public hosts.

## Topics

- [ ] Difference between passive inspection and active enumeration
- [ ] Interpret the first HTTP response and headers
- [ ] Inspect the browser view, source, and network requests
- [ ] Describe technology indicators cautiously
- [ ] Record findings, uncertainty, and next steps

## Lesson

### Step 1 — First HTTP response

Use `curl` to request only the response headers of the main page:

```bash
curl -I http://127.0.0.1:3000/
```

Important option:

- `-I` requests only the HTTP headers, not the complete response body.

Look at the status line, `Content-Type`, server or framework indicators, and possible security headers. A missing header is an observation, not proof of a vulnerability.

## Topics covered

- Lesson started; scope, method, and the first passive task were introduced.
