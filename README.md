# NightTalk public support site

This repository hosts NightTalk’s App Store-facing public website through GitHub Pages.

## Public URLs

- App overview: `https://minh.systems/Nighttalk/`
- Privacy Policy: `https://minh.systems/Nighttalk/privacy.html`
- Support: `https://minh.systems/Nighttalk/support.html`
- Terms: `https://minh.systems/Nighttalk/terms.html`
- User guide: `https://minh.systems/Nighttalk/documentation.html`
- First-night tutorial: `https://minh.systems/Nighttalk/tutorial.html`

## Publication

Run `python3 tests/validate_site.py` before publication. CI checks page structure, local links and anchors, the sitemap, email-only support, and selected light/dark text contrast pairs. These checks do not replace browser or assistive-technology testing.

The included GitHub Actions workflow deploys the repository root to GitHub Pages on each push to `main`. In the repository’s **Settings → Pages**, select **GitHub Actions** as the source if it is not selected automatically after the first push. Do not add a `CNAME`; these URLs intentionally use the repository’s project-site address.

The site intentionally uses no JavaScript, cookies, fonts/CDNs, contact form, advertising, or analytics. Support is provided only at `mip@gmx.biz`.

## App Store Connect fields

Use the public HTTPS URLs above for the NightTalk App Store Connect Support URL, Privacy Policy URL, and (optionally) Marketing URL. Confirm that the live Pages deployment succeeds before entering them in App Store Connect.
