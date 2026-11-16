# Renz

Renz is a static, English-language U.S. business setup website. The source is ready for a dedicated GitHub repository.

## Publish

1. Push the contents of this directory to the repo's main branch.
2. To use GitHub Pages, open **Settings → Pages**, choose **Deploy from a branch**, and select **main /docs**. GitHub Pages availability depends on the repository's visibility and plan.
3. If hosting with Cloudflare Pages, connect the GitHub repository, skip the build command, and set the output directory to `docs`.
4. Use the selected hosting provider's custom-domain setup after deciding the domain.

All internal paths are relative so the site works at the root or under a GitHub Pages project path.

## Edit and test locally

- Edit `homepage.html` for the landing page.
- Edit `content.json` for content pages.
- Edit `docs/styles.css` and `docs/app.js` for design and the checklist.
- Run `python3 scripts/build.py` to update the checked-in HTML in `docs`.
- Run `python3 -m http.server 8080 --directory docs` and open `http://localhost:8080/`.

The initial site does not accept messages or payment. The checklist runs locally in the visitor's browser. Connect an approved inbox or submission service before enabling customer requests.
