const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const entrypoint = path.join(__dirname, "..", "index.js");

test("Functions entrypoint exists and exports the documented triggers", () => {
  const source = fs.readFileSync(entrypoint, "utf8");
  assert.match(source, /exports\.health\s*=/);
  assert.match(source, /exports\.onCallingStatus\s*=/);
  assert.doesNotMatch(source, /TWILIO_AUTH_TOKEN\s*=\s*["'][^"']+["']/);
});

test("package main points to the tracked entrypoint", () => {
  const packageJson = JSON.parse(
    fs.readFileSync(path.join(__dirname, "..", "package.json"), "utf8"),
  );
  assert.equal(packageJson.main, "index.js");
  assert.equal(fs.existsSync(entrypoint), true);
});
