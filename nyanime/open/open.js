"use strict";

// The fragment stays in the browser. Only Nyanime resolves the opaque reference.
function sharedItem(fragment) {
  if (!fragment || fragment.length > 24000) return null;
  const [route, query, extra] = fragment.split("?");
  const match = /^v2\/(anime|manga|tv)\/([a-z0-9]+(?:-[a-z0-9]+)*)$/.exec(route);
  if (!match || match[2].length > 80 || !query || extra !== undefined) return null;
  const pairs = query.split("&");
  if (pairs.length > 20) return null;
  const fields = new Map();
  try {
    for (const pair of pairs) {
      const split = pair.indexOf("=");
      if (split < 0) return null;
      const key = decodeURIComponent(pair.slice(0, split).replace(/\+/g, " "));
      const value = decodeURIComponent(pair.slice(split + 1).replace(/\+/g, " "));
      if (fields.has(key) || /[\x00-\x1f\x7f]/.test(key + value)) return null;
      fields.set(key, value);
    }
    const source = fields.get("source") || "";
    if (!/^[+-]?\d+$/.test(source)) return null;
    const id = BigInt(source);
    if (id === 0n || id < -9223372036854775808n || id > 9223372036854775807n) return null;
    for (const [key, max] of [["ref", 4096], ["title", 512]]) {
      const value = fields.get(key);
      if (!value || !value.trim() || value.length > max) return null;
    }
    return { medium: match[1], title: fields.get("title"), fragment };
  } catch {
    return null;
  }
}

if (typeof document !== "undefined") {
  const item = sharedItem(location.hash.slice(1));
  if (item) {
    document.getElementById("shared-title").textContent = item.title;
    document.title = item.title + " · Nyanime";
    document.getElementById("shared-kind").textContent = {
      anime: "Shared video", manga: "Shared manga", tv: "Shared channel"
    }[item.medium];
    document.getElementById("shared-description").textContent =
      "Open the shared item in the app. If your browser asks, choose Nyanime.";
    const button = document.getElementById("open-app");
    button.href = "nyanime://open/v2#" + item.fragment;
    button.hidden = false;
    document.getElementById("source-note").hidden = false;
  }
}
