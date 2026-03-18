---
name: auto-updater
description: "Automatically update Clawdbot and all installed skills once daily via cron. Checks for updates, applies them, and delivers a summary of changes. Use when setting up automated update schedules, daily maintenance, auto-update routines, background maintenance, keeping skills updated automatically, scheduling updates, or self-healing agent infrastructure."
metadata: {"version":"1.0.0","clawdbot":{"emoji":"🔄","os":["darwin","linux"]}}
---

# Auto-Updater Skill

Keep your Clawdbot and skills up to date automatically with daily update checks.

## Setup

### Quick Start

Ask Clawdbot to set up the auto-updater:

```
Set up daily auto-updates for yourself and all your skills.
```

Or manually add the cron job:

```bash
clawdbot cron add \
  --name "Daily Auto-Update" \
  --cron "0 4 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --wake now \
  --deliver \
  --message "Run daily auto-updates: check for Clawdbot updates and update all skills. Report what was updated."
```

Then verify the job was created:
```bash
clawdbot cron list
```
Confirm "Daily Auto-Update" appears in the output before proceeding.

## How Updates Work

### Clawdbot Updates

For **npm installs** (most common):
```bash
npm update -g clawdbot@latest
```

For other install methods (pnpm, bun, source/git), see the [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating).

After updating, run `clawdbot doctor` to apply any pending migrations:
```bash
clawdbot doctor
```

### Skill Updates

```bash
clawdhub update --all
```

This checks all installed skills against the registry and updates any with new versions available.

## Update Workflow (Full Sequence)

1. Update Clawdbot via your install method (see above)
2. Run `clawdbot doctor` to apply migrations
3. Run `clawdhub update --all` to update skills
4. Review the delivered summary for any errors

## Update Summary

After updates complete, you'll receive a message listing the Clawdbot version change (if any), which skills were updated with their old and new versions, and which skills were already current. Any errors encountered will be included in the summary.

## Manual Commands

Check for updates without applying:
```bash
clawdhub update --all --dry-run
```

View current skill versions:
```bash
clawdhub list
```

Check Clawdbot version:
```bash
clawdbot --version
```

## Troubleshooting

### Updates Not Running

1. Verify the cron job exists: `clawdbot cron list`
2. Confirm `cron.enabled` is `true` in config
3. Confirm the Gateway is running continuously

### Update Failures

The summary will include the error detail. Key fixes:

- **Permission errors**: Ensure the Gateway user can write to skill directories
- **Package conflicts**: Run `clawdbot doctor` to diagnose and repair

### Disabling Auto-Updates

Remove the cron job:
```bash
clawdbot cron remove "Daily Auto-Update"
```

Or disable temporarily in config:
```json
{
  "cron": {
    "enabled": false
  }
}
```

## Resources

- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating)
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub)
- [Cron Jobs](https://docs.clawd.bot/cron)
