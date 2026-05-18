/**
 * remark plugin: normalize relative post-citation links.
 *
 * Fellows write internal citations as `posts/<slug>/` (the natural form
 * recommended by the orchestrator brief). That string is a relative URL,
 * so when it appears inside a published post page at
 * /the-invisible-college/posts/<this>/, the browser resolves it to
 * /the-invisible-college/posts/<this>/posts/<other>/  — broken.
 *
 * This plugin rewrites those link targets to absolute paths anchored at
 * the configured base, so the same markdown works from anywhere on the
 * site:
 *   posts/<slug>          -> /the-invisible-college/posts/<slug>
 *   posts/<slug>/         -> /the-invisible-college/posts/<slug>
 *
 * Already-absolute links and external URLs are left alone.
 */

const POST_SLUG_RE = /^posts\/([A-Za-z0-9_-]+)\/?$/;

export function remarkNormalizePostLinks({
  base = '/the-invisible-college',
} = {}) {
  return (tree) => {
    visit(tree, 'link', (node) => {
      if (typeof node.url !== 'string') return;
      const m = node.url.match(POST_SLUG_RE);
      if (!m) return;
      const trimmedBase = base.replace(/\/+$/, '');
      node.url = `${trimmedBase}/posts/${m[1]}`;
    });
  };
}

function visit(tree, type, fn) {
  if (!tree || typeof tree !== 'object') return;
  if (tree.type === type) fn(tree);
  const children = tree.children;
  if (Array.isArray(children)) {
    for (const child of children) visit(child, type, fn);
  }
}

export default remarkNormalizePostLinks;
