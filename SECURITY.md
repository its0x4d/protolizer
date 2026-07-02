# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | -------------------- |
| 1.3.x   | :white_check_mark:   |
| < 1.3   | :x:                  |

## Reporting a Vulnerability

If you discover a security issue, please **do not** open a public GitHub issue.

Instead, report it privately by emailing [mostafa.uwsgi@gmail.com](mailto:mostafa.uwsgi@gmail.com).

Include:

- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

You should receive a response within 7 days. If the issue is confirmed, we will:

1. Acknowledge the report
2. Work on a fix
3. Release a patched version
4. Credit you in the changelog (unless you prefer to remain anonymous)

## Security Considerations

Protolizer is a serialization library. When using it in API handlers:

- Validate all untrusted input with `.is_valid()` before calling `.protobuf`
- Be aware that `ParseDict` behavior depends on your `protobuf` version
- Avoid reusing serializer instances across requests if hooks mutate shared state
- Do not pass untrusted data to `pre_serialize` hooks without review
