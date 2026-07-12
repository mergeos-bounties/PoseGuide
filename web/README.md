# PoseGuide web demo

The `web/` directory is a static mobile-friendly demo for issue #15. It lets a user pick scene tags, attach a background image for preview, and rank the bundled standing pose catalog.

## Local dev

From the repository root:

```bash
python -m http.server 5173
```

Open `http://localhost:5173/web/`.

## Local API

The app can call a local API when one is available. Enable `Local API` in the UI and set the base URL, for example `http://localhost:8000`.

Expected request:

```http
POST /recommend
Content-Type: application/json
```

```json
{
  "tags": ["urban", "street", "daylight"],
  "top_k": 3,
  "background_name": "street-crossing.jpg"
}
```

Expected response:

```json
{
  "recommendations": [
    {
      "pose_id": "walk_toward_camera",
      "name": "Walk Toward Camera",
      "score": 0.62,
      "tag_overlap": ["daylight", "street", "urban"]
    }
  ]
}
```

If the API is unavailable or returns an unexpected shape, the demo falls back to the offline catalog in `web/data/catalog.json`.

## Catalog refresh

Regenerate the offline catalog after pose or scene data changes:

```bash
python scripts/build-web-catalog.py
```

## Screenshots

For PR screenshots, run the local server and capture:

- Mobile viewport around 390 x 844 with a scene selected and results visible.
- Desktop viewport with the preview canvas and top poses visible.
