# Safe Skill Review Checklist

Use this checklist before installing, publishing, or recommending a third-party skill.

- Review `SKILL.md` frontmatter for accurate name and description.
- Read instructions for attempts to override system, developer, or user guidance.
- Inspect scripts for shell execution, package installation, network access, and file deletion.
- Inspect lifecycle hooks such as npm `postinstall`.
- Check for reads of `.env`, SSH keys, cloud credentials, GitHub tokens, or full environment dumps.
- Check whether file writes are documented and limited to expected output paths.
- Confirm examples use documentation-safe placeholders.
- Confirm metadata accurately describes risky capabilities.
- Treat high and critical findings as blockers until reviewed and resolved.
- Remember that a static scan is a review aid, not a safety guarantee.
