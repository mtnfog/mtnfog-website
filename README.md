# mtnfog-website

Source for the [www.mtnfog.com](https://www.mtnfog.com) website — the public site for Mountain Fog, Inc.

The site is a static [Hugo](https://gohugo.io) project. Pushes to `main` are built and deployed to GitHub Pages by `.github/workflows/hugo.yml`. The custom domain is configured via the `CNAME` file in `static/`.

## Local development

```sh
hugo server
```

Then open http://localhost:1313.

## Build

```sh
hugo --minify
```

Output is written to `public/`.
