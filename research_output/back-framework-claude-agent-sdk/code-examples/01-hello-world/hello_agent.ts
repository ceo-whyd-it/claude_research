/**
 * 01-hello-world/hello_agent.ts
 * ------------------------------
 * Your first Claude Agent SDK program (TypeScript version).
 *
 * Prerequisites:
 *   npm install @anthropic-ai/claude-agent-sdk
 *   export ANTHROPIC_API_KEY=sk-ant-api...
 *
 * Run:
 *   npx tsx hello_agent.ts
 */

import { query } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  console.log("Hello Agent SDK!");
  console.log("=".repeat(50));
  console.log("Prompt: What is the Claude Agent SDK and what can it do?\n");

  // query() returns an async generator of SDK messages
  for await (const message of query({
    prompt:
      "What is the Claude Agent SDK and what can it do? Give a 3-sentence summary.",
  })) {
    // Assistant messages contain Claude's text responses
    if (message.type === "assistant") {
      const content = message.message?.content ?? [];
      for (const block of content) {
        if (block.type === "text") {
          // Print streaming text as it arrives
          process.stdout.write(block.text);
        }
      }
    }

    // Result message is always last — contains cost and session info
    if (message.type === "result") {
      console.log(`\n\n${"=".repeat(50)}`);
      console.log("Session complete!");
      console.log(`  Cost:  $${message.total_cost_usd?.toFixed(4) ?? "N/A"}`);
      console.log(`  Turns: ${message.num_turns}`);
    }
  }
}

main().catch(console.error);

/**
 * Expected output:
 * ================
 * Hello Agent SDK!
 * ==================================================
 * Prompt: What is the Claude Agent SDK and what can it do?
 *
 * The Claude Agent SDK is Anthropic's framework for building autonomous AI agents...
 *
 * ==================================================
 * Session complete!
 *   Cost:  $0.0023
 *   Turns: 1
 */
