import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import { fileURLToPath } from "url";
import path from "path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
 server: {
 host: "localhost",
 port: 5173,
 },
 plugins: [react()],
 resolve: {
 alias: {
 "@": path.resolve(__dirname, "src"),
 },
 },
});

