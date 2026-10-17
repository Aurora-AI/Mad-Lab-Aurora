import { defineConfig } from "vitest/config";
import { resolve } from "node:path";

export default defineConfig({
  test: {
    environment: "node",
  },
  resolve: {
    alias: {
      "@aurora/arc-schema": resolve(__dirname, "../arc-schema/src/index.ts"),
    },
  },
});
